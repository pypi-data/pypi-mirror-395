from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any
from typing import Dict

from blissdata.beacon.data import BeaconData
from blissdata.redis_engine.store import DataStore

from blissoda.import_utils import unavailable_class
from blissoda.import_utils import unavailable_function

from ..persistent.parameters import ParameterInfo

try:
    from bliss.scanning.scan import ScanState as BlissScanState
    from tomo.globals import get_active_tomo_config
except ImportError as ex:
    BlissScanState = unavailable_class(ex)
    get_active_tomo_config = unavailable_function(ex)

from esrf_pathlib import ESRFPath
from ewoksjob.client import submit

from blissoda.resources import resource_filename
from blissoda.tomo.online_tomo_plotter import OnlineTomoAccumulatedPlotter
from blissoda.tomo.tomo_processor import TomoProcessor

from .tomo_model import TomoProcessorModel
from .utils import ImageKey
from .utils import get_reconstruction_metadata

logger = logging.getLogger(__name__)

FUTURE_TIMEOUT = None
SUPPORTED_TOMO_SCANS = ["tomo:basic", "tomo:zseries", "tomo:fullturn", "tomo:halfturn"]
# The following scan types are not yet supported:
# tomo:helical, tomo:zhelical, tomo:ptychotomo, tomo:multitomo , tomo:holotomo


class OnlineTomoSliceProcessor(
    TomoProcessor,
    parameters=[
        ParameterInfo(
            "batch_size",
            category="slice_reconstruction_parameters",
            doc="Number of projections to process in each batch",
        ),
        ParameterInfo(
            "flat_reduction_method",
            category="flat_dark_reduction_parameters",
            doc="Method for flat field reduction ('mean', 'median')",
        ),
        ParameterInfo(
            "padding_mode",
            category="slice_reconstruction_parameters",
            doc="Padding mode for reconstruction ('edges', 'zeros', etc.)",
        ),
        ParameterInfo(
            "extra_options",
            category="slice_reconstruction_parameters",
            doc="Additional options for reconstruction as a dictionary",
        ),
    ],
):
    def __init__(
        self,
        config: Dict[str, Any] | None = None,
        defaults: Dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize the OnlineTomoSliceProcessor for online tomographic slice reconstruction.

        This processor can be integrated into a BLISS beamline configuration. Typical
        usage involves adding the following to a configuration yaml file:

        - name: tomo_blissoda
          plugin: generic
          class: OnlineTomoSliceProcessor
          package: blissoda.tomo.online_tomo_slice_processor
        """

        if defaults is None:
            defaults = {}
        defaults.setdefault("trigger_at", "PREPARED")
        defaults.setdefault("workflow", "tomo_reconstruction_online.json")
        defaults.setdefault("nabu_config_file", None)
        defaults.setdefault("slice_index", "middle")
        defaults.setdefault("cor_algorithm", "sliding-window")
        defaults.setdefault("phase_retrieval_method", "None")
        defaults.setdefault("delta_beta", "100")
        defaults.setdefault("_flip_left_right", False)
        defaults.setdefault("offset_mm", 0.0)
        defaults.setdefault("_orientation_factor", 1.0)
        defaults.setdefault("estimated_cor", 0.0)
        defaults.setdefault("show_last_slice", False)
        defaults.setdefault("flat_reduction_method", "mean")
        defaults.setdefault("batch_size", 100)
        defaults.setdefault("padding_mode", "edges")
        defaults.setdefault("extra_options", None)

        super(TomoProcessor, self).__setattr__(
            "_tomo_model", TomoProcessorModel(**defaults)
        )

        # Initialize internal state
        self._sequence_scan = None
        self._dark_n = 0
        self._flat_n = 0
        self._sample_name = None

        # Initialize workflow output paths
        self.reduced_dark_path = None
        self.reduced_flat_path = None

        # Initialize workflow futures
        self.reduced_dark_future = None
        self.reduced_flat_future = None

        # Workflow paths
        self._reduced_dark_flat_workflow = "tomo_reduction_online.json"
        self._reconstruction_workflow = "tomo_reconstruction_online.json"

        # Initialize the plotter for accumulated slices
        self.accumulated_plotter = OnlineTomoAccumulatedPlotter(
            history=1,
        )

        super(TomoProcessor, self).__init__(config=config, defaults=defaults)

    def execute_workflow(self, scan) -> None:
        """Execute workflow based on scan type and state."""

        # Check if this is a tomography configuration scan
        technique = scan.scan_info.get("technique", "")
        if (
            "tomoconfig" in technique
            and scan.scan_info["title"] in SUPPORTED_TOMO_SCANS
        ):
            logger.info(
                f"Starting tomography sequence for scan: {scan.scan_info.get('title', 'Unknown')}"
            )
            self._reset_state()
            self._sequence_scan = scan
            self._output_path = self.get_processed_path(scan.scan_saving.data_path)
            # Set sample name from output path, format will be {sample}_{dataset}
            self._sample_name = self._output_path.name
            return

        # Handle individual scans within the sequence
        if self._sequence_scan is not None:
            scan_type = self._get_scan_type(scan)

            logger.info(f"Processing scan: {scan_type}")

            if scan_type is ImageKey.DARK_FIELD:
                self._dark_n = self._extract_frame_count(scan, "dark")
                self.on_new_darkflat_scan("dark", index=self._flat_n)
            elif scan_type is ImageKey.FLAT_FIELD:
                self._flat_n = self._extract_frame_count(scan, "flat")
                self.on_new_darkflat_scan("flat", index=self._dark_n)
            elif scan_type is ImageKey.PROJECTION:
                self.wait_for_futures()
                # Only run reconstruction if we have both dark and flat processed
                if self.reduced_dark_path and self.reduced_flat_path:
                    self.result = self.on_new_projection_scan()
                else:
                    logger.warning(
                        "Cannot run reconstruction: missing reduced dark or flat files"
                    )

    def _reset_state(self) -> None:
        """Reset internal state for new tomography sequence."""
        self._sequence_scan = None
        self._dark_n = 0
        self._flat_n = 0
        self._output_path = None
        self._sample_name = None
        self.reduced_dark_path = None
        self.reduced_flat_path = None
        self.reduced_dark_future = None
        self.reduced_flat_future = None

    def _extract_frame_count(self, scan, frame_type: str) -> int:
        technique = scan.scan_info.get("technique", {})
        frame_info = technique.get(frame_type, {})
        return int(frame_info.get(f"{frame_type}_n", 0))

    def _get_scan_type(self, scan) -> ImageKey:
        """Determine the type of scan based on the key in scan_info."""
        image_key = int(scan.scan_info.get("technique", {}).get("image_key", 3))
        return ImageKey(image_key)

    def wait_for_futures(self):
        """Wait for any ongoing reduction workflows to complete."""
        for attr in ["reduced_dark_future", "reduced_flat_future"]:
            future = getattr(self, attr, None)
            if future is not None:
                try:
                    future.result(timeout=FUTURE_TIMEOUT)  # Wait for completion
                    logger.info(f"{attr} completed successfully")
                except Exception as e:
                    logger.error(f"Error in {attr}: {e}")

    def get_processed_path(self, data_path: str) -> Path:
        """
        Get the processed path for the reconstructed slices.
        """
        output_path = ESRFPath(data_path)
        return (
            output_path.processed_data_path / output_path.collection / output_path.stem
        )

    def _get_workflow(self, workflow: str) -> Dict[str, Any]:
        """Load workflow definition from JSON file."""
        try:
            with open(resource_filename("tomo", workflow), "r") as wf:
                return json.load(wf)
        except Exception as e:
            logger.error(f"Failed to load workflow {workflow}: {e}")
            raise

    def _connect_data_store(self) -> None:
        """Initialize connection to the data store."""
        try:
            beacon_client = BeaconData()
            redis_url = beacon_client.get_redis_data_db()
            data_store = DataStore(redis_url)
            logger.info("Connected to beacon")
            return data_store
        except Exception as e:
            logger.error(f"Failed to connect to beacon: {e}")
            raise

    def on_new_darkflat_scan(self, scan_type: str, index: int = 0):
        """Run reduction workflow for dark or flat frames."""
        try:
            data_store = self._connect_data_store()
            _, key = data_store.get_last_scan()

            # Create output path
            output_path = self._output_path / f"references/{scan_type}_field.h5"
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Determine reduction method based on scan type
            if "dark" in scan_type.lower():
                reduction_method = "mean"
                convert_destination = str(
                    output_path.parent
                    / f"workflows/{self._sample_name}_dark_online.json"
                )
            elif "flat" in scan_type.lower():
                reduction_method = self.flat_reduction_method
                convert_destination = str(
                    output_path.parent
                    / f"workflows/{self._sample_name}_flat_online.json"
                )
            else:
                logger.warning(f"Unknown scan type for reduction: {scan_type}")
                return

            logger.info(
                f"Submitting reduction workflow for {scan_type} with method {reduction_method}"
            )

            # Submit the reduction workflow
            future = self._submit_reduction_workflow(
                scan_key=key,
                output_path=output_path,
                reduction_method=reduction_method,
                index=index,
                convert_destination=convert_destination,
            )

            # Use dynamic attribute names to store futures and paths
            # e.g., reduced_dark_future, reduced_flat_future
            attr_name = f"reduced_{scan_type}_future"
            setattr(self, attr_name, future)
            # e.g., reduced_dark_path, reduced_flat_path
            attr_name = f"reduced_{scan_type}_path"
            setattr(self, attr_name, str(output_path))

        except Exception as e:
            logger.error(f"Failed to run reduction workflow for {scan_type}: {e}")

    def on_new_projection_scan(self):
        """Run reconstruction workflow for projection data."""
        try:
            data_store = self._connect_data_store()
            _, key = data_store.get_last_scan()
            scan = data_store.load_scan(key)

            # Create output path
            output_path = self._output_path / "slices/online"
            output_path.mkdir(parents=True, exist_ok=True)

            # Get rotation motor name from tomo configuration
            tomo_config = get_active_tomo_config()
            rotation_motor = tomo_config.rotation_axis.name

            # Extract reconstruction parameters from scan metadata
            technique_info = scan.info.get("technique", {})
            tomo_n = int(technique_info.get("proj", {}).get("proj_n"))
            scan_info = self._sequence_scan.scan_info.get("technique", {}).get(
                "scan", {}
            )
            halftomo = scan_info.get("half_acquisition", False)

            # Get metadata for CoR estimation
            center_of_rotation = self.estimate_CoR()

            # Get reconstruction metadata
            distance_m, energy_keV, pixel_size_m = get_reconstruction_metadata(
                self._sequence_scan
            )

            logger.info(
                f"Submitting reconstruction workflow - tomo_n: {tomo_n}, rotation_motor: {rotation_motor}"
            )

            # Submit the reconstruction workflow
            job = self._submit_reconstruction_workflow(
                scan_key=key,
                output_path=output_path,
                rotation_motor=rotation_motor,
                total_nb_projection=tomo_n,
                center_of_rotation=center_of_rotation,
                batch_size=self.batch_size,
                reduced_dark_path=self.reduced_dark_path,
                reduced_flat_path=self.reduced_flat_path,
                pixel_size_m=pixel_size_m,
                distance_m=distance_m,
                energy_keV=energy_keV,
                slice_index=self.slice_index,
                delta_beta=self.delta_beta,
                halftomo=halftomo,
                padding_mode=self.padding_mode,
                extra_options=self.extra_options,
            )

            logger.info("Reconstruction workflow submitted successfully")

            # Trigger the plotter if show_last_slice is enabled
            if self.show_last_slice:
                self.accumulated_plotter.handle_workflow_result(
                    future=job,
                    output_path=str(output_path),
                    slice_index=self.slice_index,
                    batch_size=self.batch_size,
                )

            return job

        except Exception as e:
            logger.error(f"Failed to run reconstruction workflow: {e}")

    def _submit_reduction_workflow(
        self,
        scan_key: str,
        output_path: Path,
        reduction_method: str,
        index: int,
        convert_destination: str,
    ):
        """Submit a reduction workflow for dark or flat frames."""

        # Load workflow definition
        workflow = self._get_workflow(self._reduced_dark_flat_workflow)

        # Prepare inputs for the workflow
        inputs = [
            {
                "task_identifier": "ewokstomo.tasks.online.reducedarkflat.OnlineReduceDarkFlat",
                "name": "scan_key",
                "value": scan_key,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reducedarkflat.OnlineReduceDarkFlat",
                "name": "output_file_path",
                "value": str(output_path),
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reducedarkflat.OnlineReduceDarkFlat",
                "name": "reduction_method",
                "value": reduction_method,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reducedarkflat.OnlineReduceDarkFlat",
                "name": "index",
                "value": index,
            },
        ]

        # Submit the workflow
        kwargs = {
            "inputs": inputs,
            "convert_destination": convert_destination,
        }

        try:
            job = submit(args=(workflow,), kwargs=kwargs, queue=self.queue)
            logger.info(f"Submitted reduction workflow job: {job}")
            return job
        except Exception as e:
            logger.error(f"Failed to submit reduction workflow: {e}")
            raise

    def _submit_reconstruction_workflow(
        self,
        scan_key: str,
        output_path: Path,
        rotation_motor: str,
        batch_size: int,
        total_nb_projection: int,
        center_of_rotation: float,
        reduced_dark_path: str,
        reduced_flat_path: str,
        pixel_size_m: float,
        distance_m: float,
        energy_keV: float,
        slice_index: str = "middle",
        delta_beta: float = 100.0,
        halftomo: bool = False,
        padding_mode: str = "edges",
        extra_options: dict | None = None,
    ):
        """Submit a reconstruction workflow for projection data."""

        if extra_options is None:
            extra_options = {"centered_axis": True}

        # Load workflow definition
        workflow = self._get_workflow(self._reconstruction_workflow)

        convert_destination = str(
            output_path.parent
            / f"workflows/{self._sample_name}_slice_reconstruction.json"
        )

        # Prepare inputs for the workflow
        inputs = [
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "scan_key",
                "value": scan_key,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "output_path",
                "value": str(output_path),
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "rotation_motor",
                "value": rotation_motor,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "total_nb_projection",
                "value": total_nb_projection,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "center_of_rotation",
                "value": center_of_rotation,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "batch_size",
                "value": batch_size,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "reduced_dark_path",
                "value": str(reduced_dark_path),
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "reduced_flat_path",
                "value": str(reduced_flat_path),
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "pixel_size_m",
                "value": pixel_size_m,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "distance_m",
                "value": distance_m,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "energy_keV",
                "value": energy_keV,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "slice_index",
                "value": slice_index,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "delta_beta",
                "value": delta_beta,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "halftomo",
                "value": halftomo,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "padding_mode",
                "value": padding_mode,
            },
            {
                "task_identifier": "ewokstomo.tasks.online.reconstruct_slice.OnlineReconstructSlice",
                "name": "extra_options",
                "value": extra_options,
            },
        ]

        # Submit the workflow
        kwargs = {
            "inputs": inputs,
            "convert_destination": convert_destination,
        }

        try:
            job = submit(args=(workflow,), kwargs=kwargs, queue=self.queue)
            logger.info(f"Submitted reconstruction workflow job: {job}")
            return job
        except Exception as e:
            logger.error(f"Failed to submit reconstruction workflow: {e}")
            raise

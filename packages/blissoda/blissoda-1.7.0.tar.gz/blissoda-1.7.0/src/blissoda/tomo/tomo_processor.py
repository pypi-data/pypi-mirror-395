from __future__ import annotations

import json
import time
from configparser import ConfigParser
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from ewoksjob.client import submit

from ..persistent.parameters import ParameterInfo
from ..persistent.parameters import ParameterValue
from ..persistent.parameters import _format_info_category
from ..processor import BaseProcessor
from ..processor import BlissScanType
from ..resources import resource_filename
from .flint_tomo_imshow import SingleSliceImshow
from .tomo_model import TomoProcessorModel
from .utils import calculate_relative_CoR_estimate
from .utils import get_estimate_cor_metadata

SUPPORTED_TOMO_SCANS = ["tomo:basic", "tomo:zseries", "tomo:fullturn", "tomo:halfturn"]
# The following scan types are not yet supported:
# tomo:helical, tomo:zhelical, tomo:ptychotomo, tomo:multitomo , tomo:holotomo


class TomoProcessor(
    BaseProcessor,
    parameters=[
        ParameterInfo("workflow", category="workflows"),
        ParameterInfo("queue", category="workflows"),
        ParameterInfo(
            "_bliss_hdf5_path",
            category="files",
            doc="HDF5 Dataset path (filled automatically)",
        ),
        ParameterInfo(
            "_output_path",
            category="files",
            doc="Nx output path (filled automatically)",
        ),
        ParameterInfo(
            "nabu_config_file",
            category="slice_reconstruction_parameters",
            doc="Nabu configuration file",
        ),
        ParameterInfo(
            "_darks_flats_dir",
            category="files",
            doc="Directory containing previously reduced darks and flats",
        ),
        ParameterInfo(
            "_flip_left_right",
            category="estimate_center_of_rotation",
            doc="If True, the center of rotation estimate is flipped",
        ),
        ParameterInfo(
            "offset_mm",
            category="estimate_center_of_rotation",
            doc="Offset (mm) subtracted from the translation_y motor position",
        ),
        ParameterInfo(
            "_orientation_factor",
            category="estimate_center_of_rotation",
            doc="Orientation factor to be multiplied to the translation_y motor value",
        ),
        ParameterInfo(
            "_mechanical_ud_flip",
            category="slice_reconstruction_parameters",
            doc="If True, adds a NXtransformation in the NX file to describe a flip up-down",
        ),
        ParameterInfo(
            "_mechanical_lr_flip",
            category="slice_reconstruction_parameters",
            doc="If True, adds a NXtransformation in the NX file to describe a flip left-right",
        ),
        ParameterInfo(
            "cor_algorithm",
            category="estimate_center_of_rotation",
            doc="Method to estimate the centre of rotation in the frame",
        ),
        ParameterInfo(
            "estimated_cor",
            category="estimate_center_of_rotation",
            doc="Pixel value of the CoR in the frame (relative, filled automatically)",
        ),
        ParameterInfo(
            "slice_index",
            category="slice_reconstruction_parameters",
            doc="Index of the slice that will be reconstructed online",
        ),
        ParameterInfo(
            "phase_retrieval_method",
            category="slice_reconstruction_parameters",
            doc="Phase retrieval method or 'None'",
        ),
        ParameterInfo(
            "delta_beta",
            category="slice_reconstruction_parameters",
            doc="For Paganin or CTF phase retrieval, default is 100",
        ),
        ParameterInfo(
            "show_last_slice",
            category="flint_display_parameters",
            doc="If True, displays the last reconstructed slice in Flint",
        ),
    ],
):
    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        defaults: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the TomoProcessor for converting BLISS HDF5 data to Nexus (NX) format.

        This processor can be integrated into a BLISS beamline configuration. Typical
        usage involves adding the following to a configuration yaml file:

        - name: tomo_blissoda
          plugin: generic
          class: TomoProcessor
          package: blissoda.tomo.tomo_processor
        """

        if defaults is None:
            defaults = {}
        defaults.setdefault("trigger_at", "END")
        defaults.setdefault("workflow", "tomo_processor.json")
        defaults.setdefault("nabu_config_file", None)
        defaults.setdefault("_darks_flats_dir", None)
        defaults.setdefault("slice_index", "middle")
        defaults.setdefault("cor_algorithm", "sliding-window")
        defaults.setdefault("phase_retrieval_method", "None")
        defaults.setdefault("delta_beta", "100")
        defaults.setdefault("_flip_left_right", False)
        defaults.setdefault("offset_mm", 0.0)
        defaults.setdefault("_orientation_factor", 1.0)
        defaults.setdefault("_mechanical_ud_flip", False)
        defaults.setdefault("_mechanical_lr_flip", False)
        defaults.setdefault("estimated_cor", 0.0)
        defaults.setdefault("show_last_slice", False)
        super().__setattr__("_tomo_model", TomoProcessorModel(**defaults))

        self.imshow = SingleSliceImshow(history=1)

        super().__init__(config=config, defaults=defaults)

    def __setattr__(self, name, value):
        if hasattr(self._tomo_model, name):
            setattr(self._tomo_model, name, value)
            value = getattr(self._tomo_model, name)

        super().__setattr__(name, value)

    def __info__(self) -> str:
        self.estimated_cor = self.estimate_CoR()
        categories = self._info_categories()
        for category in categories.values():
            for key, info in list(category.items()):
                if key in dir(self) and isinstance(info, ParameterValue):
                    category[key] = ParameterValue(getattr(self, key), info.doc)

        # Does not display delta_beta if phase_retrieval_method is None
        parameters = categories.get("slice_reconstruction_parameters")
        if parameters is not None:
            method = parameters.get("phase_retrieval_method")
            if method == "None":
                parameters.pop("delta_beta", None)

        return "\n" + "\n\n".join(
            [
                f"{name.replace('_', ' ').title()}:\n {_format_info_category(category)}"
                for name, category in categories.items()
                if category
            ]
        )

    def load_nabu_config_file(self, nabu_file, allow_no_value=False) -> Dict[str, Any]:
        """
        Parse a configuration file and returns a dictionary.
        """
        if nabu_file and Path(nabu_file).exists():
            parser = ConfigParser(
                inline_comment_prefixes=("#",),
                allow_no_value=allow_no_value,
            )
            with open(nabu_file) as fid:
                file_content = fid.read()
            parser.read_string(file_content)
            nabu_dict = parser._sections
        else:
            nabu_dict = dict()

        # Ensure nested dictionaries exist
        nabu_dict.setdefault("dataset", {})
        nabu_dict.setdefault("reconstruction", {})
        nabu_dict["dataset"]["darks_flats_dir"] = self._darks_flats_dir
        nabu_dict["reconstruction"]["rotation_axis_position"] = self.cor_algorithm
        current_cor_options = nabu_dict["reconstruction"].get("cor_options")
        nabu_dict["reconstruction"]["cor_options"] = self._update_cor_options(
            current_cor_options, self.estimated_cor
        )
        nabu_dict.setdefault("phase", {})
        nabu_dict["phase"]["method"] = self.phase_retrieval_method
        nabu_dict["phase"]["delta_beta"] = self.delta_beta
        nabu_dict.setdefault("output", {})

        return nabu_dict

    def _update_cor_options(
        self, existing_options: Optional[str], side_value: Any
    ) -> str:
        """Replace the 'side' option and keep any others as-is."""
        if not existing_options:
            return f"side={side_value}"

        options = [opt.strip() for opt in existing_options.split(";") if opt.strip()]
        options = [opt for opt in options if not opt.startswith("side")]
        return "; ".join([f"side={side_value}", *options])

    def estimate_CoR(self) -> float:
        """
        Estimate the relative center of rotation based on scan metadata and processor parameters.
        """

        pixel_size_mm, _, translation_y_mm = get_estimate_cor_metadata()

        center_of_rotation = calculate_relative_CoR_estimate(
            pixel_size_mm=pixel_size_mm,
            translation_y_mm=translation_y_mm,
            offset_mm=self.offset_mm,
            flip=self._flip_left_right,
            orientation_factor=self._orientation_factor,
        )
        return center_of_rotation

    def _get_scan_parameters(self, scan: BlissScanType) -> Dict[str, Any]:
        scan_parameters = dict()
        for key in list(scan.scan_info.keys()):
            scan_parameters[key] = scan.scan_info[key]
        return scan_parameters

    def _build_output_path(self, bliss_path: str) -> str:
        """
        Build the Nx output path under PROCESSED_DATA/sample/sample_dataset/projections.
        """
        processed_path = bliss_path.replace("RAW_DATA", "PROCESSED_DATA")
        nx_path = Path(processed_path).with_suffix(".nx")
        projections_dir = nx_path.parent / "projections"
        return str(projections_dir / nx_path.name)

    def _build_darks_flats_dir_path(self, _output_path: str, scan) -> str:
        """
        Build the references output path under PROCESSED_DATA/sample/sample_dataset/references if
        the scan contains darks and flats at the start.
        """
        if self._has_darks_and_flats(scan):
            darks_flats_dir = Path(_output_path).parent.parent / "references"
            self._darks_flats_dir = str(darks_flats_dir)
        elif self._darks_flats_dir is None:
            raise ValueError("Darks and flats directory cannot be determined")

    def _has_darks_and_flats(self, scan: BlissScanType) -> bool:
        """
        Check if the scan contains darks and flats at the start.
        """
        scan_parameters = self._get_scan_parameters(scan)
        scan_flags = scan_parameters.get("technique", {}).get("scan_flags", {})
        has_darks_flats = scan_flags.get(
            "dark_images_at_start", False
        ) and scan_flags.get("ref_images_at_start", False)
        return has_darks_flats

    def _get_inputs(self, scan: BlissScanType) -> List[Dict[str, Any]]:
        scan_parameters = self._get_scan_parameters(scan)
        self.estimated_cor = self.estimate_CoR()
        self._bliss_hdf5_path = scan_parameters["filename"]
        self._output_path = self._build_output_path(self._bliss_hdf5_path)
        self._build_darks_flats_dir_path(self._output_path, scan)

        inputs = list()
        inputs.append(
            {
                "task_identifier": "ewokstomo.tasks.nxtomomill.H5ToNx",
                "name": "bliss_hdf5_path",
                "value": self._bliss_hdf5_path,
            }
        )
        inputs.append(
            {
                "task_identifier": "ewokstomo.tasks.nxtomomill.H5ToNx",
                "name": "nx_path",
                "value": self._output_path,
            }
        )
        inputs.append(
            {
                "task_identifier": "ewokstomo.tasks.nxtomomill.H5ToNx",
                "name": "mechanical_ud_flip",
                "value": self._mechanical_ud_flip,
            }
        )
        inputs.append(
            {
                "task_identifier": "ewokstomo.tasks.nxtomomill.H5ToNx",
                "name": "mechanical_lr_flip",
                "value": self._mechanical_lr_flip,
            }
        )

        if not self._has_darks_and_flats(scan):
            inputs.append(
                {
                    "task_identifier": "ewokstomo.tasks.reducedarkflat.ReduceDarkFlat",
                    "name": "dark_flats_dir",
                    "value": self._darks_flats_dir,
                }
            )

        inputs.append(
            {
                "task_identifier": "ewokstomo.tasks.reconstruct_slice.ReconstructSlice",
                "name": "nx_path",
                "value": self._output_path,
            }
        )
        nabu_dict = self.load_nabu_config_file(self.nabu_config_file)
        inputs.append(
            {
                "task_identifier": "ewokstomo.tasks.reconstruct_slice.ReconstructSlice",
                "name": "config_dict",
                "value": nabu_dict,
            }
        )
        inputs.append(
            {
                "task_identifier": "ewokstomo.tasks.reconstruct_slice.ReconstructSlice",
                "name": "slice_index",
                "value": self.slice_index,
            }
        )
        inputs.append(
            {
                "id": "dataportal_task_projections",
                "task_identifier": "ewokstomo.tasks.dataportalupload.DataPortalUpload",
                "name": "dataset",
                "value": "projections",
            }
        )
        inputs.append(
            {
                "id": "dataportal_task_slices",
                "task_identifier": "ewokstomo.tasks.dataportalupload.DataPortalUpload",
                "name": "dataset",
                "value": "slices",
            }
        )

        return inputs

    def _get_workflow(self):
        with open(resource_filename("tomo", self.workflow), "r") as wf:
            return json.load(wf)

    def _get_submit_arguments(self, scan) -> Dict[str, Any]:
        return {"inputs": self._get_inputs(scan), "outputs": [{"all": True}]}

    def workflow_destination(self) -> str:
        """
        Returns the destination path for the workflow output.
        """
        return self._output_path.replace(".nx", ".json")

    def execute_workflow(self, scan: BlissScanType) -> None:
        if (
            "tomoconfig" not in scan.scan_info.get("technique", "")
            or not scan.scan_info["title"] in SUPPORTED_TOMO_SCANS
        ):
            return
        workflow = self._get_workflow()
        kwargs = self._get_submit_arguments(scan)
        kwargs["convert_destination"] = self.workflow_destination()
        time.sleep(2)
        future = submit(args=(workflow,), kwargs=kwargs, queue=self.queue)
        if self.show_last_slice:
            self.imshow._spawn(self.imshow.handle_workflow_result, future)

    def _trigger_workflow_on_new_scan(self, scan: BlissScanType) -> None:
        self.execute_workflow(scan)

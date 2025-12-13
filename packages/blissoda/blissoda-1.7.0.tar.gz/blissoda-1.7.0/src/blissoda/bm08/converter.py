"""User API for HDF5 conversion on the Bliss repl"""

import logging
import os
import shutil
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from esrf_pathlib import ESRFPath
from ewoksjob.client import submit
from ewoksjob.client.futures import FutureInterface

from ..bliss_globals import current_session
from ..import_utils import unavailable_module
from ..persistent.parameters import ParameterInfo
from ..processor import BaseProcessor
from ..processor import BlissScanType
from ..resources import resource_filename

try:
    import gevent
except ImportError as ex:
    gevent = unavailable_module(ex)


logger = logging.getLogger(__name__)


def _optional_float(value):
    if value is None:
        return None
    return float(value)


def _optional_list_of_strings(value):
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    return list(map(str, value))


class Bm08Hdf5ToXdiConverter(
    BaseProcessor,
    parameters=[
        ParameterInfo(
            "workflow",
            category="workflows",
            validator=str,
            doc="Workflows to submit for every Kscan.",
        ),
        ParameterInfo(
            "queue",
            category="workflows",
            validator=str,
            doc="Ewoks queue to submit the jobs to.",
        ),
        ParameterInfo(
            "mono_counter",
            category="parameters",
            validator=str,
            doc="Monochromator energy or theta counter name.",
        ),
        ParameterInfo(
            "crystal_motor",
            category="parameters",
            validator=str,
            doc="Motor that selects the monochromator crystal.",
        ),
        ParameterInfo(
            "optional_counters",
            category="parameters",
            validator=_optional_list_of_strings,
            doc="Other counter name to be saved in XDI.",
        ),
        ParameterInfo(
            "optional_mca_counters",
            category="parameters",
            validator=_optional_list_of_strings,
            doc="MCA counter names like ROI names to be saved in XDI.",
        ),
        ParameterInfo(
            "livetime_normalization",
            category="parameters",
            validator=_optional_float,
            doc="Live-time normalization in seconds for the MCA counters.\n"
            " None: no normalization\n"
            " `<=0` the median of the elapsed per point",
        ),
        ParameterInfo(
            "retry_timeout",
            category="data access",
            validator=_optional_float,
            doc="Timeout for HDF5 reading.\n None: wait forever",
        ),
        ParameterInfo(
            "mono_edge_theoretical",
            category="calibration",
            validator=_optional_float,
            doc="The theoretical edge position in 'mono_counter' units.",
        ),
        ParameterInfo(
            "mono_edge_experimental",
            category="calibration",
            validator=_optional_float,
            doc="The experimental edge position in 'mono_counter' units.",
        ),
    ],
):
    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        defaults: Optional[Dict[str, Any]] = None,
    ) -> None:
        if defaults is None:
            defaults = dict()
        defaults.setdefault("trigger_at", "END")
        defaults.setdefault("queue", "online")
        defaults.setdefault("mono_counter", "mono_enc")
        defaults.setdefault("crystal_motor", "c_sel")
        defaults.setdefault(
            "optional_counters",
            [
                "I0_eh1",
                "I1_eh1",
                "IX_eh1",
                "I0_eh2",
                "I1_eh2",
                "IX_eh2",
                "IR_eh2",
                "volt1",
                "volt2",
            ],
        )
        defaults.setdefault("optional_mca_counters", [])
        defaults.setdefault("workflow", resource_filename("bm08", "convert.json"))
        defaults.setdefault("retry_timeout", 60)
        defaults.setdefault("livetime_normalization", -1)
        super().__init__(config=config, defaults=defaults)

        # For integration tests
        self._future = None

    def on_new_scan_metadata(self, scan: BlissScanType) -> None:
        if not self.scan_requires_processing(scan):
            return
        workflow = self._get_workflow(scan)
        if not workflow:
            return
        kwargs = self.get_submit_arguments(scan)
        future = submit(args=(workflow,), kwargs=kwargs, queue=self.queue)
        self._future = future

        retry_timeout = self.retry_timeout
        if retry_timeout is not None:
            retry_timeout += 3
        _ = gevent.spawn(_print_result, future, self.retry_timeout)

    def _trigger_workflow_on_new_scan(self, scan: BlissScanType) -> None:
        self.on_new_scan_metadata(scan)

    def scan_requires_processing(self, scan: BlissScanType) -> bool:
        if not scan.scan_info["save"]:
            return False
        scan_parameters = scan.scan_info.get("scan_parameters", {})
        scan_type = scan_parameters.get("scan_type")
        if scan_type != "Kscan":
            return False
        counter_names = self._get_counter_names(scan)
        if self.mono_counter not in counter_names:
            logger.warning(
                "Do not trigger XDI conversion: %r is not used in the scan",
                self.mono_counter,
            )
            return False
        # TODO: check the motor self.crystal_motor is available
        return True

    def get_submit_arguments(self, scan: BlissScanType) -> dict:
        return {
            "inputs": self.get_inputs(scan),
            "outputs": [{"all": False}],
            "convert_destination": self._get_convert_destination(scan),
            "upload_parameters": self._get_workflow_upload_parameters(scan),
        }

    def get_inputs(self, scan: BlissScanType) -> List[dict]:
        load_identifier = "ReadXasHdf5"
        save_identifier = "SaveXasXdi"
        return [
            {
                "task_identifier": load_identifier,
                "name": "filename",
                "value": scan.scan_info["filename"],
            },
            {
                "task_identifier": load_identifier,
                "name": "entry_name",
                "value": f'{scan.scan_info["scan_nb"]}.1',
            },
            {
                "task_identifier": load_identifier,
                "name": "mono_counter",
                "value": self.mono_counter,
            },
            {
                "task_identifier": load_identifier,
                "name": "crystal_motor",
                "value": self.crystal_motor,
            },
            {
                "task_identifier": load_identifier,
                "name": "optional_counters",
                "value": self._get_optional_counters(scan),
            },
            {
                "task_identifier": load_identifier,
                "name": "optional_mca_counters",
                "value": self.optional_mca_counters,
            },
            {
                "task_identifier": load_identifier,
                "name": "livetime_normalization",
                "value": self.livetime_normalization,
            },
            {
                "task_identifier": load_identifier,
                "name": "mono_edge_theoretical",
                "value": self.mono_edge_theoretical,
            },
            {
                "task_identifier": load_identifier,
                "name": "mono_edge_experimental",
                "value": self.mono_edge_experimental,
            },
            {
                "task_identifier": load_identifier,
                "name": "retry_timeout",
                "value": self.retry_timeout,
            },
            {
                "task_identifier": save_identifier,
                "name": "filename",
                "value": self._get_output_filename(scan),
            },
        ]

    def _get_workflow(self, scan: BlissScanType) -> Optional[str]:
        """Get the workflow to execute for the scan and ensure it is located
        in the proposal directory for user reference and worker accessibility.
        """
        src_file = self.workflow
        if src_file is None:
            return
        if not os.path.isfile(src_file):
            src_file = resource_filename("bm08", "xdi_convert.json")

        filename = ESRFPath(scan.scan_info["filename"])
        dst_file = filename.scripts_path / "workflows" / "xdi_convert.json"
        str_dst_file = str(dst_file)

        if src_file != str_dst_file:
            self.workflow = str_dst_file

        if not dst_file.exists():
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src_file, str_dst_file)

        return str_dst_file

    def _get_counter_names(self, scan: BlissScanType) -> List[str]:
        """Names in the measurement group."""
        counter_names = []
        for full_name in scan.scan_info.get("channels", dict()):
            _, _, name = full_name.rpartition(":")
            counter_names.append(name)
        return counter_names

    def _get_optional_counters(self, scan: BlissScanType) -> List[str]:
        """Names in the measurement group."""
        if not self.optional_counters:
            return []
        counter_names = self._get_counter_names(scan)
        return [s for s in counter_names if s in self.optional_counters]

    def _get_convert_destination(self, scan: BlissScanType) -> str:
        filename = ESRFPath(scan.scan_info["filename"])
        output_directory = filename.processed_dataset_path
        output_stem = f"{filename.stem}_scan{scan.scan_info['scan_nb']}"
        return str(output_directory / "workflows" / f"{output_stem}.json")

    def _get_output_filename(self, scan: BlissScanType) -> str:
        filename = ESRFPath(scan.scan_info["filename"])
        output_directory = filename.processed_dataset_path
        output_stem = scan.scan_info["title"].replace(" ", "_")
        return str(output_directory / f"{output_stem}.xdi")

    def _get_workflow_upload_parameters(self, scan: BlissScanType) -> dict:
        raw_directory = ESRFPath(scan.scan_info["filename"]).raw_dataset_path
        processed_directory = raw_directory.processed_dataset_path
        scan_saving = current_session.scan_saving
        metadata = {"Sample_name": scan_saving.dataset["Sample_name"]}
        return {
            "beamline": scan_saving.beamline,
            "proposal": scan_saving.proposal_name,
            "dataset": "integrate",
            "path": str(processed_directory),
            "raw": [str(raw_directory)],
            "metadata": metadata,
        }


def _print_result(future: FutureInterface, timeout: Optional[float]) -> None:
    try:
        output_filename = future.result(timeout)["output_filename"]
        print(f"XDI file saved: {output_filename}")
    except Exception as ex:
        logger.warning("XDI conversion failed: %s", ex)

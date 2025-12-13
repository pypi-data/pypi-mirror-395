"""Automatic pyfai integration for every scan with saving and plotting"""

import os
import tempfile
from glob import glob
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from ..persistent.parameters import ParameterInfo
from ..processor import BlissScanType
from ..utils.pyfai import read_config
from ..xrpd.processor import XrpdProcessor


class Bm20XrpdProcessor(
    XrpdProcessor,
    parameters=[
        ParameterInfo("pyfai_config_directory", category="PyFai"),
        ParameterInfo("integration_options", category="PyFai"),
    ],
):
    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        defaults: Optional[Dict[str, Any]] = None,
        **deprecated_defaults: Dict[str, Any],
    ) -> None:
        defaults = self._merge_defaults(deprecated_defaults, defaults)

        defaults.setdefault("pyfai_config_directory", tempfile.gettempdir())

        super().__init__(config=config, defaults=defaults)

    def _info_categories(self) -> Dict[str, dict]:
        categories = super()._info_categories()
        if not self.lima_names:
            return categories
        categories["PyFai"]["integration_options"] = "... (see below)"
        lima_name = self.lima_names[0]
        categories["PyFai integration"] = {
            "1. JSON file": self._detector_config_filename(lima_name, ".json"),
            "2. PONI file": self._detector_config_filename(lima_name, ".poni"),
            "3. User": self.integration_options,
            "Merged": self.get_integration_options(scan=None, lima_name=lima_name),
        }
        return categories

    def get_config_filename(self, lima_name: str) -> Optional[str]:
        return None

    def get_integration_options(
        self, scan: BlissScanType, lima_name: str
    ) -> Optional[dict]:
        options = self._default_azint_options(lima_name)
        options.update(self._default_calib_options(lima_name))
        integration_options = self.integration_options
        if integration_options:
            options.update(integration_options.to_dict())
        return options

    def _default_azint_options(self, lima_name: str) -> dict:
        filename = self._detector_config_filename(lima_name, ".json")
        return read_config(filename)

    def _default_calib_options(self, lima_name: str) -> dict:
        filename = self._detector_config_filename(lima_name, ".poni")
        return read_config(filename)

    def _detector_config_filename(self, lima_name: str, ext: str) -> Optional[str]:
        pyfai_config_directory = self.pyfai_config_directory
        if not pyfai_config_directory:
            pyfai_config_directory = tempfile.gettempdir()
        pattern = os.path.join(pyfai_config_directory, lima_name, f"*{ext}")
        files = sorted(glob(pattern))
        if not files:
            return
        return files[-1]

    def get_inputs(self, scan, lima_name: str) -> List[dict]:
        inputs = super().get_inputs(scan, lima_name)
        return inputs

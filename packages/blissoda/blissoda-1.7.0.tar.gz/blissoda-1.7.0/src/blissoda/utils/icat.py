from importlib.metadata import version
from typing import Any
from typing import Dict

from packaging.version import Version

DEFINITIONS_VERSION = Version(version("icat-esrf-definitions"))
SUPPORTS_TECHNIQUE_PID = DEFINITIONS_VERSION >= Version("2.0.0")


def adapt_legacy_metadata(metadata: Dict[str, Any]) -> None:
    """Modifies ``metadata`` in case the installed ``icat-esrf-definitions``
    library does not support the latest ICAT metadata schema.
    """
    if not SUPPORTS_TECHNIQUE_PID:
        _ = metadata.pop("technique_pid")

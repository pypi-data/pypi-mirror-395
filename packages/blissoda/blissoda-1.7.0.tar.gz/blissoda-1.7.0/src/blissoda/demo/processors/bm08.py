from typing import Any
from typing import Dict
from typing import Optional

from ...bm08.converter import Bm08Hdf5ToXdiConverter


class DemoBm08Hdf5ToXdiConverter(Bm08Hdf5ToXdiConverter):
    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        defaults: Optional[Dict[str, Any]] = None,
    ) -> None:
        if defaults is None:
            defaults = dict()
        defaults.setdefault("mono_counter", "roby")  # Must have no units
        defaults.setdefault("crystal_motor", "sy")
        defaults.setdefault("optional_counters", ["diode1", "diode2"])
        defaults.setdefault("optional_mca_counters", ["OdaRoi"])
        defaults.setdefault("retry_timeout", 15)
        defaults.setdefault("queue", "celery")
        super().__init__(config=config, defaults=defaults)

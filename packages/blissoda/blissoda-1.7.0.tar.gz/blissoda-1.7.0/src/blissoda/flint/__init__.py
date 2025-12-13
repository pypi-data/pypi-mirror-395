import logging
from functools import wraps
from importlib.metadata import version
from typing import Callable

from packaging.version import Version

from ..import_utils import unavailable_class

try:
    if Version(version("bliss")) >= Version("2.2"):
        from flint.client.plots import BasePlot
        from flint.client.proxy import FlintClient
    else:
        from bliss.flint.client.plots import BasePlot
        from bliss.flint.client.proxy import FlintClient
except ImportError as ex:
    FlintClient = unavailable_class(ex)
    BasePlot = unavailable_class(ex)

logger = logging.getLogger(__name__)


def capture_errors(method) -> Callable:
    @wraps(method)
    def wrapper(*args, **kw):
        try:
            return method(*args, **kw)
        except Exception as e:
            msg = f"Flint plot error: {e}"
            logger.error(msg, exc_info=True)

    return wrapper

import logging
from contextlib import contextmanager
from typing import Dict
from typing import Generator
from typing import Optional
from typing import Type

from ..bliss_globals import current_session
from ..import_utils import is_available
from ..import_utils import unavailable_class
from ..import_utils import unavailable_function
from . import BasePlot
from . import FlintClient

try:
    from gevent.lock import RLock
except ImportError as ex:
    RLock = unavailable_class(ex)

try:
    from bliss.common.plot import get_flint as _native_get_flint
except ImportError as ex:
    _native_get_flint = unavailable_function(ex)


logger = logging.getLogger(__name__)


class WithFlintAccess:
    _HAS_BLISS = is_available(current_session)

    def __init__(self) -> None:
        self.__plots: Dict[str, BasePlot] = dict()
        self.__flint_client_id = None
        self.__plots_lock = None
        self.__get_plot_stack = 0

    @property
    def _plots_lock(self) -> RLock:
        if self.__plots_lock is None:
            self.__plots_lock = RLock()
        return self.__plots_lock

    def _get_plot(self, plot_id: str, plot_cls: Type[BasePlot]) -> BasePlot:
        """Launches Flint and creates the plot when either is missing."""
        with self._plots_lock:
            with self._access_flint_context() as flint_client:
                plot = self.__plots.get(plot_id)
                if plot is None:
                    plot = flint_client.get_plot(plot_cls, unique_name=plot_id)
                    logger.info("Created Flint plot %r", plot_id)
                    self.__plots[plot_id] = plot
                return plot

    @contextmanager
    def _access_flint_context(
        self, reset: bool = False
    ) -> Generator[FlintClient, None, None]:
        with self._plots_lock:
            self.__get_plot_stack += 1
            try:
                flint_client = _get_flint(reset=reset)
                flint_client_id = id(flint_client), flint_client.pid
                if flint_client_id != self.__flint_client_id:
                    self.__flint_client_id = flint_client_id
                    if self.__get_plot_stack > 1:
                        if self.__plots:
                            logger.warning(
                                "Cannot resetting Flint plots after restart (recursive call)"
                            )
                    else:
                        self._on_flint_restart(flint_client)
                yield flint_client
            finally:
                self.__get_plot_stack -= 1

    def reset_flint(self) -> None:
        with self._access_flint_context(reset=True) as _:
            pass

    def _on_flint_restart(self, flint_client: FlintClient) -> None:
        """Called whenever a new Flint client is instantiated."""
        with self._plots_lock:
            plots = {}
            for plot_id in self.__plots:
                plot_instance = self.__plots[plot_id]
                plot_cls = type(plot_instance)
                plots[plot_id] = flint_client.get_plot(plot_cls, unique_name=plot_id)
            self.__plots = plots


_flint_lock: Optional[RLock] = None
_flint_client: Optional[FlintClient] = None
_flint_pid: Optional[int] = None


def _get_flint(reset: bool = False) -> FlintClient:
    """Create the Flint client when needed:

    - not created yet
    - different process id
    - not available
    """
    global _flint_client, _flint_pid, _flint_lock
    if _flint_lock is None:
        _flint_lock = RLock()

    with _flint_lock:
        if reset:
            _flint_client = None
            _flint_pid = None

        try:
            new_client = (
                _flint_client is None
                or _flint_pid != _flint_client.pid
                or not _flint_client.is_available()
            )
        except FileNotFoundError:
            new_client = True

        if new_client:
            _flint_client = _native_get_flint()
            _flint_pid = _flint_client.pid
        return _flint_client

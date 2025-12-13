from __future__ import annotations

import logging
from collections import OrderedDict
from typing import Any
from typing import Optional

import h5py
import numpy

from blissoda.tomo.utils import apply_labels
from blissoda.tomo.utils import compute_axes

from ..bliss_globals import current_session
from ..flint import capture_errors
from ..flint.plotter import BasePlotter
from ..import_utils import unavailable_class

try:
    from flint.viewers.custom_image.client import ImageView
except ImportError as ex:
    ImageView = unavailable_class(ex)

_logger = logging.getLogger(__name__)


class SingleSliceImshow(BasePlotter):
    """
    Manage a Flint window showing the most recent reconstructed slice with enhanced controls,
    using the flint DataPlot–based ImageView.
    """

    TITLE = "Last Reconstructed Slice"

    def __init__(self, history: int = 1) -> None:
        super().__init__(max_plots=history)
        self._cache: OrderedDict[str, numpy.ndarray] = OrderedDict()

    def handle_workflow_result(self, future: Any) -> None:
        """
        Called by BasePlotter._spawn when the workflow future completes.
        Handles both success and failure with logging.
        """
        result = self._extract_result(future)
        if not result:
            return

        img_path = result.get("reconstructed_slice_path")

        if img_path is None:
            _logger.warning(
                "No 'reconstructed_slice_path' in workflow result: %r", result
            )
            return

        with h5py.File(img_path, "r") as h5In:
            img = h5In["entry0000/reconstruction/results/data"][:]

        self.set_image(numpy.squeeze(img))

    def _extract_result(self, future: Any) -> Optional[dict]:
        """
        Safely retrieve result from a future via result() or get().
        Logs warnings or errors and returns None on failure.
        """
        try:
            res_fn = getattr(future, "result", None) or getattr(future, "get", None)
            if not callable(res_fn):
                _logger.warning("Future has no callable result()/get(): %r", future)
                return None
            result = res_fn()
            if isinstance(result, dict) or result is None:
                return result
            _logger.warning("Future result is not a dict or None: %r", result)
            return None
        except Exception as e:
            _logger.error("Workflow execution failed: %s", e, exc_info=True)
            return None

    @capture_errors
    def set_image(self, image: numpy.ndarray) -> None:
        """
        Display a new image with physical axis limits based on pixel size and image center.
        """
        widget = self._get_plot(self.TITLE, ImageView)
        self._set_title(widget)

        x_axis, y_axis = compute_axes(image)
        origin = (float(x_axis[0]), float(y_axis[0]))

        dx = float(x_axis[1] - x_axis[0]) if len(x_axis) > 1 else 1.0
        dy = float(y_axis[1] - y_axis[0]) if len(y_axis) > 1 else 1.0
        scale = (dx, dy)

        widget.set_data(image, origin=origin, scale=scale)
        apply_labels(widget)

        self._cache[self.TITLE] = image
        self.purge_tasks()
        self._purge()

    def _set_title(self, widget: ImageView) -> None:
        """
        Set the plot window title using the current data filename from scan saving.
        """
        widget.title = current_session.scan_saving.data_filename

    def _purge(self) -> None:
        """
        Remove oldest images beyond history.
        """
        while len(self._cache) > self._max_plots:
            self._cache.popitem(last=False)

from __future__ import annotations

import functools
import logging
import time
from collections import OrderedDict
from pathlib import Path

import h5py
import numpy as np

from blissoda.tomo.utils import apply_labels
from blissoda.tomo.utils import compute_axes

from ..bliss_globals import current_session
from ..flint.plotter import BasePlotter

try:
    from flint.viewers.custom_image.client import ImageView
except ImportError as ex:
    from ..import_utils import unavailable_class

    ImageView = unavailable_class(ex)

logger = logging.getLogger(__name__)


def _background_task(method):
    """Decorator to handle exceptions in background tasks."""

    @functools.wraps(method)
    def wrapper(*args, **kw):
        try:
            return method(*args, **kw)
        except Exception as e:
            logger.error("Online tomo plotter task failed (%s)", e, exc_info=True)
            raise

    return wrapper


class OnlineTomoAccumulatedPlotter(BasePlotter):
    """
    Plotter for online tomography reconstruction that accumulates partial slices.

    Monitors the output directory for new reconstructed slice files and
    progressively accumulates them to show the evolving reconstruction.
    """

    TITLE = "Accumulated Reconstructed Slice"

    def __init__(self, history: int = 1, retry_period: int = 3) -> None:
        """
        Initialize the plotter.

        :param history: Number of plots to keep (should be 1 for current scan only).
        :param retry_period: Polling interval in seconds to check for new batch files.

        """
        super().__init__(max_plots=history)
        self.retry_period = retry_period
        self._cache: OrderedDict[str, np.ndarray] = OrderedDict()
        self._current_plot_widget = None
        self._accumulated_slice = None
        self._batch_count = 0
        self._batch_size = None

    def handle_workflow_result(
        self,
        future,
        output_path: str,
        slice_index: int | str = "middle",
        batch_size: int = 100,
    ) -> None:
        """
        Monitor workflow execution and update plot as new batches are saved.

        :param future: The workflow job future
        :param output_path: Directory where batch files are being saved
        :param slice_index: The slice index being reconstructed (for display only)
        :param batch_size: Number of projections per batch

        """

        self._spawn(
            self._monitor_reconstruction,
            future,
            output_path,
            slice_index,
            batch_size,
        )

    @_background_task
    def _monitor_reconstruction(
        self,
        future,
        output_path: str,
        slice_index: int | str,
        batch_size: int,
    ) -> None:
        """
        Background task to monitor reconstruction progress.

        Polls the output directory for new batch files and updates the plot.
        :param future: The workflow job future
        :param output_path: Directory where batch files are being saved
        :param slice_index: The slice index being reconstructed (for display only)
        :param batch_size: Number of projections per batch
        """
        output_dir = Path(output_path)

        # Reset state for new reconstruction
        self._accumulated_slice = None
        self._batch_count = 0
        self._batch_size = batch_size

        logger.info(f"Starting monitoring of reconstruction in {output_dir}")

        last_processed_count = 0

        # Monitor while workflow is running
        while not future.done():
            last_processed_count = self._poll_for_batches(
                output_dir, last_processed_count
            )
            if last_processed_count != self._batch_count:
                self._update_plot(slice_index)
            time.sleep(self.retry_period)

        # Final update after workflow completes
        try:
            self._finalize_monitoring(output_dir, last_processed_count, slice_index)
        except Exception as e:
            logger.error(f"Error in final batch processing: {e}")

    def _poll_for_batches(self, output_dir: Path, start_count: int) -> int:
        """
        Poll the output directory for new batch files and process them.
        :param output_dir: Directory containing the batch slice files
        :param start_count: Number of batches already processed
        :return: Updated number of batches processed
        """
        try:
            new_batches = self._process_new_batches(output_dir, start_count)
            if new_batches > 0:
                return self._batch_count
        except Exception as e:
            logger.debug(f"Error processing batches: {e}")
        return start_count

    def _finalize_monitoring(
        self, output_dir: Path, last_processed_count: int, slice_index
    ):
        """
        Final processing after workflow completion.
        :param output_dir: Directory containing the batch slice files
        :param last_processed_count: Number of batches already processed
        :param slice_index: The slice index being reconstructed
        """
        self._process_new_batches(output_dir, last_processed_count)
        self._update_plot(slice_index)

        projections_done = self._batch_count * self._batch_size
        logger.info(
            f"Reconstruction monitoring completed: "
            f"{projections_done} projections processed."
        )

    def _process_new_batches(self, output_dir: Path, start_count: int) -> int:
        """
        Process any new batch slice files that have appeared.

        :param output_dir: Directory containing the batch slice files
        :param start_count: Number of batches already processed

        :return: Number of new batches processed

        """
        if not output_dir.exists():
            return 0

        # Find all batch files
        batch_files = sorted(output_dir.glob("*.h5"))
        if not batch_files:
            return 0

        new_batches = 0

        # Process only new files
        for batch_file in batch_files[start_count:]:
            try:
                with h5py.File(batch_file, "r") as f:
                    if "reconstructed_slice" not in f:
                        logger.debug(f"Missing dataset in {batch_file}")
                        continue

                    slice_data = f["reconstructed_slice"][()]

                    # Accumulate by addition
                    if self._accumulated_slice is None:
                        self._accumulated_slice = slice_data.astype(np.float32)
                    else:
                        self._accumulated_slice += slice_data

                    self._batch_count += 1
                    new_batches += 1
                    logger.debug(f"Processed batch file: {batch_file.name}")

            except (OSError, KeyError) as e:
                logger.debug(f"Could not read {batch_file}: {e}")
                continue

        return new_batches

    def _update_plot(self, slice_index: int | str) -> None:
        """
        Update the Flint plot with the accumulated slice.

        :param slice_index: The slice index being reconstructed
        """

        if self._accumulated_slice is None:
            return

        widget = self._get_plot(self.TITLE, ImageView)

        # Set title with progress information
        self._set_title_with_progress(widget, slice_index)

        # Compute physical axes from tomo config
        x_axis, y_axis = compute_axes(self._accumulated_slice)
        origin = (float(x_axis[0]), float(y_axis[0]))

        dx = float(x_axis[1] - x_axis[0]) if len(x_axis) > 1 else 1.0
        dy = float(y_axis[1] - y_axis[0]) if len(y_axis) > 1 else 1.0
        scale = (dx, dy)

        # Update the image data
        widget.set_data(self._accumulated_slice, origin=origin, scale=scale)

        # Apply axis labels
        apply_labels(widget)

        # Cache the current image
        self._cache[self.TITLE] = self._accumulated_slice

        self.purge_tasks()
        self._purge()

    def _set_title_with_progress(
        self, widget: ImageView, slice_index: int | str
    ) -> None:
        """
        Set the plot window title with progress information.

        :param widget: The plot widget
        :param slice_index: The slice index being reconstructed
        """
        base_title = current_session.scan_saving.data_filename

        # Add progress and slice info to title
        nb_projections = self._batch_count * self._batch_size
        title = f"{base_title} - Slice {slice_index} ({nb_projections} projections processed)"
        widget.title = title

    def clear(self) -> None:
        """Clear the current plot and reset state."""
        self._accumulated_slice = None
        self._batch_count = 0
        logger.debug("Plotter state cleared")

    def _purge(self) -> None:
        """
        Remove oldest images beyond history.
        """
        while len(self._cache) > self._max_plots:
            self._cache.popitem(last=False)

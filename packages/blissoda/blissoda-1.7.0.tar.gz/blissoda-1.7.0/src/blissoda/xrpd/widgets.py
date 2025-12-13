"""Flint-side for Flint XRPD plots"""

import logging
from typing import List

from silx.gui.plot import Plot1D
from silx.gui.plot import Plot2D

from ..flint import capture_errors
from .models import XrpdPlotInfo
from .plot_data import append_image_data
from .plot_data import get_2d_integration_data
from .plot_data import get_curve_data

logger = logging.getLogger(__name__)


class XrpdCurveWidget(Plot1D):
    @capture_errors
    def remove_plot(self, plot_key: str) -> None:
        try:
            plot_info = XrpdPlotInfo.get(plot_key)
        except KeyError as ex:
            logger.debug("%r already removed: %s", plot_key, ex)
            return

        legend = plot_info.legend
        logger.debug("remove %r", legend)
        self.remove(legend=plot_info.legend)

    @capture_errors
    def update_plot(self, plot_key: str, retry_options: dict) -> None:
        x, y, plot_info = get_curve_data(plot_key, **retry_options)
        if y is None:
            return
        legend = plot_info.legend
        if len(x) != len(y):
            logger.error("XRPD curve plot %r: Nx=%d, Ny=%d", legend, len(x), len(y))
        else:
            logger.debug("XRPD curve plot %r: Nx=%d, Ny=%d", legend, len(x), len(y))
            self.addCurve(
                x,
                y,
                legend=legend,
                xlabel=plot_info.radial_label,
                color=plot_info.color,
                linestyle="-",
                ylabel="Intensity",
            )

    @capture_errors
    def get_labels(self) -> List[str]:
        return [legend.getName() for legend in self.getItems()]


class XrpdImageWidget(Plot2D):
    @capture_errors
    def remove_plot(self, plot_key: str) -> None:
        self.clear()

    @capture_errors
    def update_plot(self, plot_key: str, retry_options: dict) -> None:
        img = self.getImage(legend=plot_key)
        if img is None:
            current_data = None
        else:
            current_data = img.getData(copy=False)
        x, y, plot_info = append_image_data(plot_key, current_data, **retry_options)
        if y is None:
            return
        origin = x[0], 0
        scale = x[1] - x[0], 1
        self.clear()
        title = plot_info.legend
        self.setGraphTitle(title)
        logger.debug("XRPD image plot %s: %s points", title, len(y))
        self.addImage(
            y,
            legend=title,
            xlabel=plot_info.radial_label,
            ylabel="Scan points",
            origin=origin,
            scale=scale,
        )

    @capture_errors
    def get_labels(self) -> List[str]:
        return [self.getGraphTitle()]


class Xrpd2dIntegrationWidget(Plot2D):
    @capture_errors
    def remove_plot(self, plot_key: str) -> None:
        self.clear()

    @capture_errors
    def update_plot(self, plot_key: str, retry_options: dict) -> None:
        x, y, intensity, plot_info = get_2d_integration_data(plot_key, **retry_options)
        if x is None or y is None or intensity is None:
            return
        origin = x[0], y[0]
        scale = x[1] - x[0], y[1] - y[0]
        self.clear()
        title = plot_info.legend
        self.setGraphTitle(title)
        logger.debug(
            "XRPD 2D integration plot %r: Nx=%d, Ny=%d, Shape=%s",
            title,
            len(x),
            len(y),
            intensity.shape,
        )
        self.addImage(
            intensity,
            legend=title,
            xlabel=plot_info.radial_label,
            ylabel=plot_info.azim_label,
            origin=origin,
            scale=scale,
        )

    @capture_errors
    def get_labels(self) -> List[str]:
        return [self.getGraphTitle()]

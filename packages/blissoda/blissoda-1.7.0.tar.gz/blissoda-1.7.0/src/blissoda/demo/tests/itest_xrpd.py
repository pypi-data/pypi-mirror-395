"""Integration tests for the generic XRPD processor."""

import os
import time

from ...bliss_globals import current_session
from ...bliss_globals import setup_globals
from ...xrpd.plots import Xrpd2dIntegrationPlot
from ...xrpd.plots import XrpdCurvePlot
from ...xrpd.plots import XrpdImagePlot
from .. import testing
from ..processors.xrpd import DemoXrpdProcessor

XRPD_PROCESSED = DemoXrpdProcessor()


def xrpd_demo_1d(nrepeats: int = None, expo=0.2, npoints=10):
    test_xrpd_ct_with_1d_integration(nrepeats=nrepeats, expo=expo)
    test_xrpd_scan_with_1d_integration(nrepeats=nrepeats, expo=expo, npoints=npoints)


def xrpd_demo_2d(nrepeats: int = None, expo=0.2, npoints=10):
    test_xrpd_ct_with_2d_integration(nrepeats=nrepeats, expo=expo)
    test_xrpd_scan_with_2d_integration(nrepeats=nrepeats, expo=expo, npoints=npoints)


def pct(*args, **kw):
    """``ct`` with workflow triggering"""
    s = setup_globals.ct(*args, **kw)
    XRPD_PROCESSED.on_new_scan(s)
    return s


@testing.integration_fixture
def xrpd_processor_1d():
    XRPD_PROCESSED.enable(setup_globals.difflab6)
    XRPD_PROCESSED._plotter.clear_lima_plots("difflab6")
    yield XRPD_PROCESSED
    XRPD_PROCESSED.disable()


@testing.integration_fixture
def xrpd_processor_2d():
    XRPD_PROCESSED.enable(setup_globals.difflab6)
    XRPD_PROCESSED.integration_options["nbpt_azim"] = 360
    XRPD_PROCESSED._plotter.clear_lima_plots("difflab6")
    yield XRPD_PROCESSED
    XRPD_PROCESSED.integration_options.pop("nbpt_azim", None)
    XRPD_PROCESSED.disable()


@testing.integration_test
def test_xrpd_ct_with_1d_integration(xrpd_processor_1d, nrepeats: int = None, expo=0.2):
    if nrepeats is None:
        nrepeats = xrpd_processor_1d.number_of_scans + 1

    scans = []
    for _ in range(nrepeats):
        scan = pct(
            expo,
            setup_globals.difflab6,
            setup_globals.diode1,
            setup_globals.diode2,
        )
        scans.append(scan)
        # Workflow is getting data from Lima directly so we cannot start
        # the next scan until the workflow is done.
        testing.wait_workflows()

    scan_legends = [_get_scan_legend(scan) for scan in scans]
    nremoved = max(len(scans) - xrpd_processor_1d.number_of_scans, 0)

    _assert_1d_plot_accum(xrpd_processor_1d._plotter, [scan_legends[-1]])
    _assert_1d_plot_last(xrpd_processor_1d._plotter, scan_legends[nremoved:])


@testing.integration_test
def test_xrpd_scan_with_1d_integration(
    xrpd_processor_1d, nrepeats: int = None, expo=0.2, npoints=10
):
    if nrepeats is None:
        nrepeats = xrpd_processor_1d.number_of_scans + 1

    scans = []
    for _ in range(nrepeats):
        scan = setup_globals.loopscan(
            npoints,
            expo,
            setup_globals.difflab6,
            setup_globals.diode1,
            setup_globals.diode2,
        )
        scans.append(scan)

    testing.wait_workflows()
    scan_legends = [_get_scan_legend(scan) for scan in scans]
    nremoved = max(len(scans) - xrpd_processor_1d.number_of_scans, 0)

    _assert_1d_plot_accum(xrpd_processor_1d._plotter, [scan_legends[-1]])
    _assert_1d_plot_last(xrpd_processor_1d._plotter, scan_legends[nremoved:])
    for scan in scans:
        _assert_1d_data(xrpd_processor_1d, scan, npoints)


@testing.integration_test
def test_xrpd_ct_with_2d_integration(xrpd_processor_2d, nrepeats: int = None, expo=0.2):
    if nrepeats is None:
        nrepeats = xrpd_processor_2d.number_of_scans + 1

    scans = []
    for _ in range(nrepeats):
        scan = pct(
            expo,
            setup_globals.difflab6,
            setup_globals.diode1,
            setup_globals.diode2,
        )
        scans.append(scan)
        # Workflow is getting data from Lima directly so we cannot start
        # the next scan until the workflow is done.
        testing.wait_workflows()

    scan_legends = [_get_scan_legend(scan) for scan in scans]

    _assert_2d_plot_last(xrpd_processor_2d._plotter, [scan_legends[-1]])


@testing.integration_test
def test_xrpd_scan_with_2d_integration(
    xrpd_processor_2d, nrepeats: int = None, expo=0.2, npoints=10
):
    if nrepeats is None:
        nrepeats = xrpd_processor_2d.number_of_scans + 1

    scans = []
    for _ in range(nrepeats):
        scan = setup_globals.loopscan(
            npoints,
            expo,
            setup_globals.difflab6,
            setup_globals.diode1,
            setup_globals.diode2,
        )
        scans.append(scan)

    testing.wait_workflows()
    scan_legends = [_get_scan_legend(scan) for scan in scans]

    _assert_2d_plot_last(xrpd_processor_2d._plotter, [scan_legends[-1]])
    for scan in scans:
        _assert_2d_data(xrpd_processor_2d, scan, npoints)


def _assert_1d_plot_last(plotter, scan_legends):
    """The last 1D diffractogram of each scan is plotted as a curve."""
    _assert_plot(plotter, scan_legends, "Integrated (Last)", XrpdCurvePlot)


def _assert_1d_plot_accum(plotter, scan_legends):
    """The 1D diffractograms of the last scan are plotted as an image."""
    _assert_plot(plotter, scan_legends, "Integrated difflab6", XrpdImagePlot)


def _assert_2d_plot_last(plotter, scan_legends):
    """The last 2D cake of the last scan is plotted as an image."""
    _assert_plot(
        plotter, scan_legends, "2D Integrated difflab6 (last)", Xrpd2dIntegrationPlot
    )


@testing.demo_assert("Check {plot_id} plot for {scan_legends}")
def _assert_plot(
    plotter, scan_legends, plot_id, plot_cls, retry_timeout=10, retry_period=0.2
):
    image_plot = plotter._get_plot(plot_id, plot_cls)
    t0 = time.time()
    while True:
        labels = image_plot.get_labels()
        if labels == scan_legends:
            return
        dt = time.time() - t0
        if dt > retry_timeout:
            break
        time.sleep(retry_period)
    assert labels == scan_legends, labels


def _get_scan_legend(scan):
    filename = scan.scan_info["filename"]
    if not filename:
        filename = current_session.scan_saving.filename
    scan_nb = scan.scan_info["scan_nb"]
    scan_name = os.path.splitext(os.path.basename(filename))[0]
    return f"{scan_name}: {scan_nb}.1 {scan.name} (difflab6)"


@testing.demo_assert("Check 1D integration data")
def _assert_1d_data(processor, scan, npoints):
    data_keys = processor.get_data_keys(
        scan, "difflab6", retry_timeout=10, retry_period=0.2
    )

    shapes = {
        name: processor.get_data(scan, name, retry_timeout=10, retry_period=0.2).shape
        for name in data_keys
    }
    expected = {
        "difflab6:q": (4096,),
        "difflab6:intensity": (npoints, 4096),
        "difflab6:points": (npoints,),
    }
    assert shapes == expected, shapes


@testing.demo_assert("Check 2D integration data")
def _assert_2d_data(processor, scan, npoints):
    data_keys = processor.get_data_keys(
        scan, "difflab6", retry_timeout=10, retry_period=0.2
    )

    shapes = {
        name: processor.get_data(scan, name, retry_timeout=10, retry_period=0.2).shape
        for name in data_keys
    }
    expected = {
        "difflab6:chi": (360,),
        "difflab6:q": (4096,),
        "difflab6:intensity": (npoints, 360, 4096),
        "difflab6:points": (npoints,),
    }
    assert shapes == expected, shapes

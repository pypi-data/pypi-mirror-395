"""Integration tests for the BM08 HDF5 to XDI converter."""

import numpy

from ...bliss_globals import setup_globals
from .. import testing
from ..processors.bm08 import DemoBm08Hdf5ToXdiConverter

BM08_CONVERTER = DemoBm08Hdf5ToXdiConverter()


@testing.integration_fixture
def bm08_converter():
    BM08_CONVERTER.enable()

    setup_globals.mca1.rois.set("OdaRoi", 500, 530)
    yield BM08_CONVERTER
    setup_globals.mca1.rois.remove("OdaRoi")

    BM08_CONVERTER.disable()


def bm08_demo(expo=0.2, npoints=10):
    for _ in range(2):
        test_bm08_kscan(expo=expo, npoints=npoints)


@testing.integration_test
def test_bm08_kscan(bm08_converter: DemoBm08Hdf5ToXdiConverter, expo=0.2, npoints=10):
    positions = numpy.linspace(1, 2, npoints)
    scan_info = {
        "scan_parameters": {"scan_type": "Kscan"},
        "scan_metadata_categories": ["scan_parameters"],
    }
    scan = setup_globals.pointscan(
        setup_globals.roby,
        positions,
        expo,
        setup_globals.diode1,
        setup_globals.diode2,
        setup_globals.mca1,
        setup_globals.mca2,
        scan_info=scan_info,
    )
    scan_number = scan.scan_info["scan_nb"]
    _assert_xdi_file(bm08_converter, scan_number)


@testing.demo_assert("Check bm08 XDI file for scan #{scan_number}")
def _assert_xdi_file(bm08_converter: DemoBm08Hdf5ToXdiConverter, scan_number=int):
    result = bm08_converter._future.result(timeout=bm08_converter.retry_timeout + 5)
    output_filename = result["output_filename"]
    print(output_filename)
    with open(output_filename, "r") as fh:
        lines = fh.readlines()
    expected_counters = "# energy diode1 diode2 OdaRoi_0 OdaRoi_1 OdaRoi_2 OdaRoi_3\n"
    assert expected_counters in lines, "\n".join(expected_counters)

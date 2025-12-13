from ...bm02.xrpd_processor import Bm02XrpdProcessor
from ...bm08.converter import Bm08Hdf5ToXdiConverter
from ...bm23.exafs_processor import Bm23ExafsProcessor
from ...exafs.processor import ExafsProcessor
from ...id11.xrpd_processor import Id11XrpdProcessor
from ...id12.converter import Id12Hdf5ToAsciiConverter
from ...id14.converter import Id14Hdf5ToSpecConverter
from ...id22.xrpd_processor import Id22XrpdProcessor
from ...id31.streamline_scanner import Id31StreamlineScanner
from ...id31.xrpd_processor import Id31XrpdProcessor
from ...id32.processor import Id32SpecGenProcessor
from ...streamline.scanner import StreamlineScanner
from ...wrappers.ewoks_macros import EwoksMacroHandler
from ...xrpd.processor import XrpdProcessor
from ..user_scripts.bm02 import bm02_xrpd_processor
from ..user_scripts.id11 import id11_xrpd_processor
from ..user_scripts.id22 import id22_xrpd_processor
from ..user_scripts.id22 import stscan_processor
from ..user_scripts.id31 import id31_xrpd_processor
from ..user_scripts.streamline import streamline_scanner
from .itest_bm08 import BM08_CONVERTER
from .itest_ewoks_macros import EWOKS_MACROS
from .itest_exafs import EXAFS_PROCESSOR
from .itest_id12 import ID12_CONVERTER
from .itest_id14 import ID14_CONVERTER
from .itest_xrpd import XRPD_PROCESSED


def all_print():
    _print_objects(EXAFS_PROCESSOR)
    _print_objects(XRPD_PROCESSED)
    _print_objects(id11_xrpd_processor)
    _print_objects(id22_xrpd_processor)
    _print_objects(ID14_CONVERTER)
    _print_objects(ID12_CONVERTER)
    _print_objects(stscan_processor)
    _print_objects(streamline_scanner)
    _print_objects(bm02_xrpd_processor)
    _print_objects(id31_xrpd_processor)
    _print_objects(EWOKS_MACROS)
    _print_objects(BM08_CONVERTER)

    _print_objects(XrpdProcessor())
    _print_objects(ExafsProcessor())
    _print_objects(StreamlineScanner())
    _print_objects(Bm23ExafsProcessor())
    _print_objects(Bm02XrpdProcessor())
    _print_objects(Id11XrpdProcessor())
    _print_objects(Id22XrpdProcessor())
    _print_objects(Id31XrpdProcessor())
    _print_objects(Id14Hdf5ToSpecConverter())
    _print_objects(Id12Hdf5ToAsciiConverter())
    _print_objects(Id31StreamlineScanner())
    _print_objects(Id32SpecGenProcessor())
    _print_objects(EwoksMacroHandler())
    _print_objects(Bm08Hdf5ToXdiConverter())


def _print_objects(obj):
    print()
    print("===================")
    print(obj._parameters.name)
    print(obj.__info__())

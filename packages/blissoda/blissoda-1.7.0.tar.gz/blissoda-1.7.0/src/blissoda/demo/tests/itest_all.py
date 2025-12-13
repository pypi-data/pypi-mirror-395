from blissoda.bliss_globals import setup_globals

from .itest_bm08 import bm08_demo
from .itest_ewoks_macros import ewoks_macro_demo
from .itest_exafs import exafs_demo
from .itest_id12 import id12_demo
from .itest_id14 import id14_demo
from .itest_template import template_demo
from .itest_xrpd import xrpd_demo_1d
from .itest_xrpd import xrpd_demo_2d

# from ..user_scripts.bm02 import bm02_demo_1d
# from ..user_scripts.bm02 import bm02_demo_2d
# from ..user_scripts.id11 import id11_pdf_demo
# from ..user_scripts.id22 import id22_stscan_demo
# from ..user_scripts.id22 import id22_xrpd_demo
# from ..user_scripts.streamline import streamline_demo


def all_demo():
    print()
    print("===================")
    template_demo()

    # print()
    # print("===================")
    # setup_globals.newcollection("id22_stscan_collection")
    # id22_stscan_demo()

    # print()
    # print("===================")
    # setup_globals.newcollection("id22_xrpd_collection")
    # id22_xrpd_demo()

    # print()
    # print("===================")
    # setup_globals.newcollection("streamline_collection")
    # streamline_demo()

    # print()
    # print("===================")
    # setup_globals.newcollection("id11_collection")
    # print("TODO: get license for diffpy")
    # # id11_pdf_demo()

    print()
    print("===================")
    setup_globals.newcollection("xrpd_1d_collection")
    xrpd_demo_1d()

    print()
    print("===================")
    setup_globals.newcollection("xrpd_2d_collection")
    xrpd_demo_2d()

    # TODO: ewoksxrpd needs to be imported before xraylarch?
    #       Cannot load backend 'Qt5Agg' which requires the 'qt' interactive framework
    print()
    print("===================")
    setup_globals.newcollection("exafs_collection")
    exafs_demo()

    print()
    print("===================")
    setup_globals.newcollection("id14_collection")
    id14_demo()

    print()
    print("===================")
    setup_globals.newcollection("id12_collection")
    id12_demo()

    # print()
    # print("===================")
    # setup_globals.newcollection("bm02_collection")
    # bm02_demo_1d()
    # bm02_demo_2d()

    print()
    print("===================")
    setup_globals.newcollection("macro_collection")
    ewoks_macro_demo()

    print()
    print("===================")
    setup_globals.newcollection("bm08_collection")
    bm08_demo()

    print()
    print("===================")
    setup_globals.newcollection("done_collection")

    print()
    print("SUCCESS: all demos can be executed")

# coding: UTF-8
import sys
bstack11ll11l_opy_ = sys.version_info [0] == 2
bstack1llll_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1l1l11l_opy_ (bstack111l_opy_):
    global bstack11ll111_opy_
    bstack11l1l1_opy_ = ord (bstack111l_opy_ [-1])
    bstack11l1ll1_opy_ = bstack111l_opy_ [:-1]
    bstack1ll1l11_opy_ = bstack11l1l1_opy_ % len (bstack11l1ll1_opy_)
    bstack1lllll_opy_ = bstack11l1ll1_opy_ [:bstack1ll1l11_opy_] + bstack11l1ll1_opy_ [bstack1ll1l11_opy_:]
    if bstack11ll11l_opy_:
        bstack1lllllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll_opy_ - (bstack1l11111_opy_ + bstack11l1l1_opy_) % bstack1lllll1l_opy_) for bstack1l11111_opy_, char in enumerate (bstack1lllll_opy_)])
    else:
        bstack1lllllll_opy_ = str () .join ([chr (ord (char) - bstack1llll_opy_ - (bstack1l11111_opy_ + bstack11l1l1_opy_) % bstack1lllll1l_opy_) for bstack1l11111_opy_, char in enumerate (bstack1lllll_opy_)])
    return eval (bstack1lllllll_opy_)
from bstack_utils.constants import bstack11l1l1lllll_opy_
def bstack1l1ll1l11l_opy_(bstack11l1ll11111_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack111l11l11_opy_
    host = bstack111l11l11_opy_(cli.config, [bstack1l1l11l_opy_ (u"ࠧࡧࡰࡪࡵࠥᠿ"), bstack1l1l11l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣᡀ"), bstack1l1l11l_opy_ (u"ࠢࡢࡲ࡬ࠦᡁ")], bstack11l1l1lllll_opy_)
    return bstack1l1l11l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᡂ").format(host, bstack11l1ll11111_opy_)
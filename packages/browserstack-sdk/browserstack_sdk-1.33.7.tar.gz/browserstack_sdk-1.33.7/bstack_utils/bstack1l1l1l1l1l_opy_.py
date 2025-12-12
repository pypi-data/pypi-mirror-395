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
import threading
import logging
import bstack_utils.accessibility as bstack11ll1lllll_opy_
from bstack_utils.helper import bstack111111l11_opy_
logger = logging.getLogger(__name__)
def bstack1111ll1l_opy_(bstack11l111lll_opy_):
  return True if bstack11l111lll_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1ll1l1lll_opy_(context, *args):
    tags = getattr(args[0], bstack1l1l11l_opy_ (u"ࠬࡺࡡࡨࡵࠪᡍ"), [])
    bstack1ll111ll11_opy_ = bstack11ll1lllll_opy_.bstack1111ll11l_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll111ll11_opy_
    try:
      bstack1l1llll1_opy_ = threading.current_thread().bstackSessionDriver if bstack1111ll1l_opy_(bstack1l1l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬᡎ")) else context.browser
      if bstack1l1llll1_opy_ and bstack1l1llll1_opy_.session_id and bstack1ll111ll11_opy_ and bstack111111l11_opy_(
              threading.current_thread(), bstack1l1l11l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᡏ"), None):
          threading.current_thread().isA11yTest = bstack11ll1lllll_opy_.bstack1ll111lll1_opy_(bstack1l1llll1_opy_, bstack1ll111ll11_opy_)
    except Exception as e:
       logger.debug(bstack1l1l11l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡥ࠶࠷ࡹࠡ࡫ࡱࠤࡧ࡫ࡨࡢࡸࡨ࠾ࠥࢁࡽࠨᡐ").format(str(e)))
def bstack1ll1l1llll_opy_(bstack1l1llll1_opy_):
    if bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᡑ"), None) and bstack111111l11_opy_(
      threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᡒ"), None) and not bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡡࡶࡸࡴࡶࠧᡓ"), False):
      threading.current_thread().a11y_stop = True
      bstack11ll1lllll_opy_.bstack1lll11l111_opy_(bstack1l1llll1_opy_, name=bstack1l1l11l_opy_ (u"ࠧࠨᡔ"), path=bstack1l1l11l_opy_ (u"ࠨࠢᡕ"))
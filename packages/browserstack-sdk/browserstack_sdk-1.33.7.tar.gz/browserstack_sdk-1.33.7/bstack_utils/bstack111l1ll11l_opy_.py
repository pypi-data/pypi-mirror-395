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
import os
import threading
from bstack_utils.helper import bstack1llll111_opy_
from bstack_utils.constants import bstack11l11llllll_opy_, EVENTS, STAGE
from bstack_utils.bstack11l1l11111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l11l1l1l_opy_:
    bstack1llll1ll11ll_opy_ = None
    @classmethod
    def bstack11l11l1lll_opy_(cls):
        if cls.on() and os.getenv(bstack1l1l11l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ⊈")):
            logger.info(
                bstack1l1l11l_opy_ (u"ࠧࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧ⊉").format(os.getenv(bstack1l1l11l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ⊊"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⊋"), None) is None or os.environ[bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⊌")] == bstack1l1l11l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⊍"):
            return False
        return True
    @classmethod
    def bstack1lll1ll1ll1l_opy_(cls, bs_config, framework=bstack1l1l11l_opy_ (u"ࠧࠨ⊎")):
        bstack11l1l11llll_opy_ = False
        for fw in bstack11l11llllll_opy_:
            if fw in framework:
                bstack11l1l11llll_opy_ = True
        return bstack1llll111_opy_(bs_config.get(bstack1l1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⊏"), bstack11l1l11llll_opy_))
    @classmethod
    def bstack1lll1ll1l11l_opy_(cls, framework):
        return framework in bstack11l11llllll_opy_
    @classmethod
    def bstack1llll111l1ll_opy_(cls, bs_config, framework):
        return cls.bstack1lll1ll1ll1l_opy_(bs_config, framework) is True and cls.bstack1lll1ll1l11l_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⊐"), None)
    @staticmethod
    def bstack111l1lllll_opy_():
        if getattr(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ⊑"), None):
            return {
                bstack1l1l11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⊒"): bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࠨ⊓"),
                bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⊔"): getattr(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⊕"), None)
            }
        if getattr(threading.current_thread(), bstack1l1l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⊖"), None):
            return {
                bstack1l1l11l_opy_ (u"ࠧࡵࡻࡳࡩࠬ⊗"): bstack1l1l11l_opy_ (u"ࠨࡪࡲࡳࡰ࠭⊘"),
                bstack1l1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⊙"): getattr(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ⊚"), None)
            }
        return None
    @staticmethod
    def bstack1lll1ll11ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l11l1l1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1111l1l11l_opy_(test, hook_name=None):
        bstack1lll1ll1l1l1_opy_ = test.parent
        if hook_name in [bstack1l1l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⊛"), bstack1l1l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⊜"), bstack1l1l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ⊝"), bstack1l1l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ⊞")]:
            bstack1lll1ll1l1l1_opy_ = test
        scope = []
        while bstack1lll1ll1l1l1_opy_ is not None:
            scope.append(bstack1lll1ll1l1l1_opy_.name)
            bstack1lll1ll1l1l1_opy_ = bstack1lll1ll1l1l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1ll1l111_opy_(hook_type):
        if hook_type == bstack1l1l11l_opy_ (u"ࠣࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍࠨ⊟"):
            return bstack1l1l11l_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡪࡲࡳࡰࠨ⊠")
        elif hook_type == bstack1l1l11l_opy_ (u"ࠥࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠢ⊡"):
            return bstack1l1l11l_opy_ (u"࡙ࠦ࡫ࡡࡳࡦࡲࡻࡳࠦࡨࡰࡱ࡮ࠦ⊢")
    @staticmethod
    def bstack1lll1ll11lll_opy_(bstack1l1lllll1l_opy_):
        try:
            if not bstack11l11l1l1l_opy_.on():
                return bstack1l1lllll1l_opy_
            if os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠥ⊣"), None) == bstack1l1l11l_opy_ (u"ࠨࡴࡳࡷࡨࠦ⊤"):
                tests = os.environ.get(bstack1l1l11l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠦ⊥"), None)
                if tests is None or tests == bstack1l1l11l_opy_ (u"ࠣࡰࡸࡰࡱࠨ⊦"):
                    return bstack1l1lllll1l_opy_
                bstack1l1lllll1l_opy_ = tests.split(bstack1l1l11l_opy_ (u"ࠩ࠯ࠫ⊧"))
                return bstack1l1lllll1l_opy_
        except Exception as exc:
            logger.debug(bstack1l1l11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡵࡩࡷࡻ࡮ࠡࡪࡤࡲࡩࡲࡥࡳ࠼ࠣࠦ⊨") + str(str(exc)) + bstack1l1l11l_opy_ (u"ࠦࠧ⊩"))
        return bstack1l1lllll1l_opy_
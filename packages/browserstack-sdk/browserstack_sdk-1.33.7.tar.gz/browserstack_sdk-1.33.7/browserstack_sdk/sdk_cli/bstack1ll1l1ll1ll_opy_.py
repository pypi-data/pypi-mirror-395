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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1lllll1llll_opy_ import bstack1llllll11ll_opy_
class bstack1lll1llll1l_opy_(abc.ABC):
    bin_session_id: str
    bstack1lllll1llll_opy_: bstack1llllll11ll_opy_
    def __init__(self):
        self.bstack1ll1lllll11_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1lllll1llll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lll1ll1111_opy_(self):
        return (self.bstack1ll1lllll11_opy_ != None and self.bin_session_id != None and self.bstack1lllll1llll_opy_ != None)
    def configure(self, bstack1ll1lllll11_opy_, config, bin_session_id: str, bstack1lllll1llll_opy_: bstack1llllll11ll_opy_):
        self.bstack1ll1lllll11_opy_ = bstack1ll1lllll11_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1lllll1llll_opy_ = bstack1lllll1llll_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥࠢࡰࡳࡩࡻ࡬ࡦࠢࡾࡷࡪࡲࡦ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢ࠲ࡤࡥ࡮ࡢ࡯ࡨࡣࡤࢃ࠺ࠡࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥእ") + str(self.bin_session_id) + bstack1l1l11l_opy_ (u"ࠢࠣኦ"))
    def bstack1ll111l111l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1l11l_opy_ (u"ࠣࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥࡔ࡯࡯ࡧࠥኧ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False
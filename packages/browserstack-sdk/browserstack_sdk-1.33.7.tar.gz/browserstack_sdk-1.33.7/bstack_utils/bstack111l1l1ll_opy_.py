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
import tempfile
import math
from bstack_utils import bstack11l1l11111_opy_
from bstack_utils.constants import bstack1l111l1ll_opy_, bstack11l11ll1lll_opy_
from bstack_utils.helper import bstack111llll1lll_opy_, get_host_info
from bstack_utils.bstack11l1l1ll1ll_opy_ import bstack11l1l1lll1l_opy_
import json
import re
import sys
bstack1111l11111l_opy_ = bstack1l1l11l_opy_ (u"ࠤࡵࡩࡹࡸࡹࡕࡧࡶࡸࡸࡕ࡮ࡇࡣ࡬ࡰࡺࡸࡥࠣἵ")
bstack11111lll111_opy_ = bstack1l1l11l_opy_ (u"ࠥࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠤἶ")
bstack1111ll111l1_opy_ = bstack1l1l11l_opy_ (u"ࠦࡷࡻ࡮ࡑࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡊࡦ࡯࡬ࡦࡦࡉ࡭ࡷࡹࡴࠣἷ")
bstack1111l1lllll_opy_ = bstack1l1l11l_opy_ (u"ࠧࡸࡥࡳࡷࡱࡔࡷ࡫ࡶࡪࡱࡸࡷࡱࡿࡆࡢ࡫࡯ࡩࡩࠨἸ")
bstack1111l1ll111_opy_ = bstack1l1l11l_opy_ (u"ࠨࡳ࡬࡫ࡳࡊࡱࡧ࡫ࡺࡣࡱࡨࡋࡧࡩ࡭ࡧࡧࠦἹ")
bstack1111ll1111l_opy_ = bstack1l1l11l_opy_ (u"ࠢࡳࡷࡱࡗࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࠦἺ")
bstack1111l1l1l1l_opy_ = {
    bstack1111l11111l_opy_,
    bstack11111lll111_opy_,
    bstack1111ll111l1_opy_,
    bstack1111l1lllll_opy_,
    bstack1111l1ll111_opy_,
    bstack1111ll1111l_opy_
}
bstack11111ll111l_opy_ = {bstack1l1l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨἻ")}
logger = bstack11l1l11111_opy_.get_logger(__name__, bstack1l111l1ll_opy_)
class bstack1111l111111_opy_:
    def __init__(self):
        self.enabled = False
        self.name = None
    def enable(self, name):
        self.enabled = True
        self.name = name
    def disable(self):
        self.enabled = False
        self.name = None
    def bstack11111llllll_opy_(self):
        return self.enabled
    def get_name(self):
        return self.name
class bstack1llllll111_opy_:
    _1lll11l11ll_opy_ = None
    def __init__(self, config):
        self.bstack11111lllll1_opy_ = False
        self.bstack1111l1ll1ll_opy_ = False
        self.bstack11111l1l1ll_opy_ = False
        self.bstack11111lll1ll_opy_ = False
        self.bstack1111l11llll_opy_ = None
        self.bstack1111l111l1l_opy_ = bstack1111l111111_opy_()
        self.bstack1111l11lll1_opy_ = None
        opts = config.get(bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭Ἴ"), {})
        self.bstack1111l1l1111_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠪࡷࡲࡧࡲࡵࡕࡨࡰࡪࡩࡴࡪࡱࡱࡊࡪࡧࡴࡶࡴࡨࡆࡷࡧ࡮ࡤࡪࡨࡷࡊࡔࡖࠨἽ"), bstack1l1l11l_opy_ (u"ࠦࠧἾ"))
        self.bstack1111l1l1l11_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠬࡹ࡭ࡢࡴࡷࡗࡪࡲࡥࡤࡶ࡬ࡳࡳࡌࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࡪࡹࡃࡍࡋࠪἿ"), bstack1l1l11l_opy_ (u"ࠨࠢὀ"))
        bstack11111ll1ll1_opy_ = opts.get(bstack1111ll1111l_opy_, {})
        bstack11111ll11ll_opy_ = None
        if bstack1l1l11l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧὁ") in bstack11111ll1ll1_opy_:
            bstack1111l11l111_opy_ = bstack11111ll1ll1_opy_[bstack1l1l11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨὂ")]
            if bstack1111l11l111_opy_ is None or (isinstance(bstack1111l11l111_opy_, str) and bstack1111l11l111_opy_.strip() == bstack1l1l11l_opy_ (u"ࠩࠪὃ")) or (isinstance(bstack1111l11l111_opy_, list) and len(bstack1111l11l111_opy_) == 0):
                bstack11111ll11ll_opy_ = []
            elif isinstance(bstack1111l11l111_opy_, list):
                bstack11111ll11ll_opy_ = bstack1111l11l111_opy_
            elif isinstance(bstack1111l11l111_opy_, str) and bstack1111l11l111_opy_.strip():
                bstack11111ll11ll_opy_ = bstack1111l11l111_opy_
            else:
                logger.warning(bstack1l1l11l_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡵࡵࡳࡥࡨࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡳࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡼࡿ࠱ࠤࡉ࡫ࡦࡢࡷ࡯ࡸ࡮ࡴࡧࠡࡶࡲࠤࡪࡳࡰࡵࡻࠣࡰ࡮ࡹࡴ࠯ࠤὄ").format(bstack1111l11l111_opy_))
                bstack11111ll11ll_opy_ = []
        self.__1111l1l111l_opy_(
            bstack11111ll1ll1_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬὅ"), False),
            bstack11111ll1ll1_opy_.get(bstack1l1l11l_opy_ (u"ࠬࡳ࡯ࡥࡧࠪ὆"), bstack1l1l11l_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭὇")),
            bstack11111ll11ll_opy_
        )
        self.__1111l1ll1l1_opy_(opts.get(bstack1111ll111l1_opy_, False))
        self.__11111l1l1l1_opy_(opts.get(bstack1111l1lllll_opy_, False))
        self.__11111ll11l1_opy_(opts.get(bstack1111l1ll111_opy_, False))
    @classmethod
    def bstack11l111l11l_opy_(cls, config=None):
        if cls._1lll11l11ll_opy_ is None and config is not None:
            cls._1lll11l11ll_opy_ = bstack1llllll111_opy_(config)
        return cls._1lll11l11ll_opy_
    @staticmethod
    def bstack11l111llll_opy_(config: dict) -> bool:
        bstack11111llll11_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡵࡺࡩࡰࡰࡶࠫὈ"), {}).get(bstack1111l11111l_opy_, {})
        return bstack11111llll11_opy_.get(bstack1l1l11l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩὉ"), False)
    @staticmethod
    def bstack1llll1llll_opy_(config: dict) -> int:
        bstack11111llll11_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭Ὂ"), {}).get(bstack1111l11111l_opy_, {})
        retries = 0
        if bstack1llllll111_opy_.bstack11l111llll_opy_(config):
            retries = bstack11111llll11_opy_.get(bstack1l1l11l_opy_ (u"ࠪࡱࡦࡾࡒࡦࡶࡵ࡭ࡪࡹࠧὋ"), 1)
        return retries
    @staticmethod
    def bstack11llllll1l_opy_(config: dict) -> dict:
        bstack1111l1l1lll_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡲࡷ࡭ࡴࡴࡳࠨὌ"), {})
        return {
            key: value for key, value in bstack1111l1l1lll_opy_.items() if key in bstack1111l1l1l1l_opy_
        }
    @staticmethod
    def bstack1111l1111ll_opy_():
        bstack1l1l11l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡣࡥࡳࡷࡺࠠࡣࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡪࡾࡩࡴࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤὍ")
        return os.path.exists(os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃࠢ὎").format(os.getenv(bstack1l1l11l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ὏")))))
    @staticmethod
    def bstack11111ll1111_opy_(test_name: str):
        bstack1l1l11l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡵࡪࡨࠤࡦࡨ࡯ࡳࡶࠣࡦࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧὐ")
        bstack11111lll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣὑ").format(os.getenv(bstack1l1l11l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣὒ"))))
        with open(bstack11111lll11l_opy_, bstack1l1l11l_opy_ (u"ࠫࡦ࠭ὓ")) as file:
            file.write(bstack1l1l11l_opy_ (u"ࠧࢁࡽ࡝ࡰࠥὔ").format(test_name))
    @staticmethod
    def bstack1111l11l11l_opy_(framework: str) -> bool:
       return framework.lower() in bstack11111ll111l_opy_
    @staticmethod
    def bstack11l111l1ll1_opy_(config: dict) -> bool:
        bstack11111ll1lll_opy_ = config.get(bstack1l1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡴࡹ࡯࡯࡯ࡵࠪὕ"), {}).get(bstack11111lll111_opy_, {})
        return bstack11111ll1lll_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡤࠨὖ"), False)
    @staticmethod
    def bstack11l111ll1l1_opy_(config: dict, bstack11l111l1lll_opy_: int = 0) -> int:
        bstack1l1l11l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡵࡪࡵࡩࡸ࡮࡯࡭ࡦ࠯ࠤࡼ࡮ࡩࡤࡪࠣࡧࡦࡴࠠࡣࡧࠣࡥࡳࠦࡡࡣࡵࡲࡰࡺࡺࡥࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡵࠤࡦࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳ࡬ࡩࡨࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡴࡺࡡ࡭ࡡࡷࡩࡸࡺࡳࠡࠪ࡬ࡲࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࠨࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡩࡳࡷࠦࡰࡦࡴࡦࡩࡳࡺࡡࡨࡧ࠰ࡦࡦࡹࡥࡥࠢࡷ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࡸ࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡀࠠࡕࡪࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡺࡨࡳࡧࡶ࡬ࡴࡲࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨὗ")
        bstack11111ll1lll_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡰࡵ࡫ࡲࡲࡸ࠭὘"), {}).get(bstack1l1l11l_opy_ (u"ࠪࡥࡧࡵࡲࡵࡄࡸ࡭ࡱࡪࡏ࡯ࡈࡤ࡭ࡱࡻࡲࡦࠩὙ"), {})
        bstack1111l1lll1l_opy_ = 0
        bstack11111lll1l1_opy_ = 0
        if bstack1llllll111_opy_.bstack11l111l1ll1_opy_(config):
            bstack11111lll1l1_opy_ = bstack11111ll1lll_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡲࡧࡸࡇࡣ࡬ࡰࡺࡸࡥࡴࠩ὚"), 5)
            if isinstance(bstack11111lll1l1_opy_, str) and bstack11111lll1l1_opy_.endswith(bstack1l1l11l_opy_ (u"ࠬࠫࠧὛ")):
                try:
                    percentage = int(bstack11111lll1l1_opy_.strip(bstack1l1l11l_opy_ (u"࠭ࠥࠨ὜")))
                    if bstack11l111l1lll_opy_ > 0:
                        bstack1111l1lll1l_opy_ = math.ceil((percentage * bstack11l111l1lll_opy_) / 100)
                    else:
                        raise ValueError(bstack1l1l11l_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡳࡵࡴࡶࠣࡦࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡨࡲࡶࠥࡶࡥࡳࡥࡨࡲࡹࡧࡧࡦ࠯ࡥࡥࡸ࡫ࡤࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࡷ࠳ࠨὝ"))
                except ValueError as e:
                    raise ValueError(bstack1l1l11l_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡳࡩࡷࡩࡥ࡯ࡶࡤ࡫ࡪࠦࡶࡢ࡮ࡸࡩࠥ࡬࡯ࡳࠢࡰࡥࡽࡌࡡࡪ࡮ࡸࡶࡪࡹ࠺ࠡࡽࢀࠦ὞").format(bstack11111lll1l1_opy_)) from e
            else:
                bstack1111l1lll1l_opy_ = int(bstack11111lll1l1_opy_)
        logger.info(bstack1l1l11l_opy_ (u"ࠤࡐࡥࡽࠦࡦࡢ࡫࡯ࡹࡷ࡫ࡳࠡࡶ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡸ࡫ࡴࠡࡶࡲ࠾ࠥࢁࡽࠡࠪࡩࡶࡴࡳࠠࡤࡱࡱࡪ࡮࡭࠺ࠡࡽࢀ࠭ࠧὟ").format(bstack1111l1lll1l_opy_, bstack11111lll1l1_opy_))
        return bstack1111l1lll1l_opy_
    def bstack1111l111lll_opy_(self):
        return self.bstack11111lll1ll_opy_
    def bstack1111l1l11l1_opy_(self):
        return self.bstack1111l11llll_opy_
    def bstack1111l1llll1_opy_(self):
        return self.bstack1111l11lll1_opy_
    def __1111l1l111l_opy_(self, enabled, mode, source=None):
        try:
            self.bstack11111lll1ll_opy_ = bool(enabled)
            if mode not in [bstack1l1l11l_opy_ (u"ࠪࡶࡪࡲࡥࡷࡣࡱࡸࡋ࡯ࡲࡴࡶࠪὠ"), bstack1l1l11l_opy_ (u"ࠫࡷ࡫࡬ࡦࡸࡤࡲࡹࡕ࡮࡭ࡻࠪὡ")]:
                logger.warning(bstack1l1l11l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡳ࡮ࡣࡵࡸࠥࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠡ࡯ࡲࡨࡪࠦࠧࡼࡿࠪࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡅࡧࡩࡥࡺࡲࡴࡪࡰࡪࠤࡹࡵࠠࠨࡴࡨࡰࡪࡼࡡ࡯ࡶࡉ࡭ࡷࡹࡴࠨ࠰ࠥὢ").format(mode))
                mode = bstack1l1l11l_opy_ (u"࠭ࡲࡦ࡮ࡨࡺࡦࡴࡴࡇ࡫ࡵࡷࡹ࠭ὣ")
            self.bstack1111l11llll_opy_ = mode
            self.bstack1111l11lll1_opy_ = []
            if source is None:
                self.bstack1111l11lll1_opy_ = None
            elif isinstance(source, list):
                self.bstack1111l11lll1_opy_ = source
            elif isinstance(source, str) and source.endswith(bstack1l1l11l_opy_ (u"ࠧ࠯࡬ࡶࡳࡳ࠭ὤ")):
                self.bstack1111l11lll1_opy_ = self._11111ll1l11_opy_(source)
            self.__11111l1ll1l_opy_()
        except Exception as e:
            logger.error(bstack1l1l11l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡰࡥࡷࡺࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣ࠱ࠥ࡫࡮ࡢࡤ࡯ࡩࡩࡀࠠࡼࡿ࠯ࠤࡲࡵࡤࡦ࠼ࠣࡿࢂ࠲ࠠࡴࡱࡸࡶࡨ࡫࠺ࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣὥ").format(enabled, mode, source, e))
    def bstack11111ll1l1l_opy_(self):
        return self.bstack11111lllll1_opy_
    def __1111l1ll1l1_opy_(self, value):
        self.bstack11111lllll1_opy_ = bool(value)
        self.__11111l1ll1l_opy_()
    def bstack1111l111ll1_opy_(self):
        return self.bstack1111l1ll1ll_opy_
    def __11111l1l1l1_opy_(self, value):
        self.bstack1111l1ll1ll_opy_ = bool(value)
        self.__11111l1ll1l_opy_()
    def bstack11111llll1l_opy_(self):
        return self.bstack11111l1l1ll_opy_
    def __11111ll11l1_opy_(self, value):
        self.bstack11111l1l1ll_opy_ = bool(value)
        self.__11111l1ll1l_opy_()
    def __11111l1ll1l_opy_(self):
        if self.bstack11111lll1ll_opy_:
            self.bstack11111lllll1_opy_ = False
            self.bstack1111l1ll1ll_opy_ = False
            self.bstack11111l1l1ll_opy_ = False
            self.bstack1111l111l1l_opy_.enable(bstack1111ll1111l_opy_)
        elif self.bstack11111lllll1_opy_:
            self.bstack1111l1ll1ll_opy_ = False
            self.bstack11111l1l1ll_opy_ = False
            self.bstack11111lll1ll_opy_ = False
            self.bstack1111l111l1l_opy_.enable(bstack1111ll111l1_opy_)
        elif self.bstack1111l1ll1ll_opy_:
            self.bstack11111lllll1_opy_ = False
            self.bstack11111l1l1ll_opy_ = False
            self.bstack11111lll1ll_opy_ = False
            self.bstack1111l111l1l_opy_.enable(bstack1111l1lllll_opy_)
        elif self.bstack11111l1l1ll_opy_:
            self.bstack11111lllll1_opy_ = False
            self.bstack1111l1ll1ll_opy_ = False
            self.bstack11111lll1ll_opy_ = False
            self.bstack1111l111l1l_opy_.enable(bstack1111l1ll111_opy_)
        else:
            self.bstack1111l111l1l_opy_.disable()
    def bstack1l11lll1ll_opy_(self):
        return self.bstack1111l111l1l_opy_.bstack11111llllll_opy_()
    def bstack11l1lll11_opy_(self):
        if self.bstack1111l111l1l_opy_.bstack11111llllll_opy_():
            return self.bstack1111l111l1l_opy_.get_name()
        return None
    def _11111ll1l11_opy_(self, bstack1111l1111l1_opy_):
        bstack1l1l11l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡷࡴࡻࡲࡤࡧࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪ࡮ࡲࡥࠡࡣࡱࡨࠥ࡬࡯ࡳ࡯ࡤࡸࠥ࡯ࡴࠡࡨࡲࡶࠥࡹ࡭ࡢࡴࡷࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡳࡰࡷࡵࡧࡪࡥࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠢࠫࡷࡹࡸࠩ࠻ࠢࡓࡥࡹ࡮ࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡕࡒࡒࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡱ࡯ࡳࡵ࠼ࠣࡊࡴࡸ࡭ࡢࡶࡷࡩࡩࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡳࡧࡳࡳࡸ࡯ࡴࡰࡴࡼࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤὦ")
        if not os.path.isfile(bstack1111l1111l1_opy_):
            logger.error(bstack1l1l11l_opy_ (u"ࠥࡗࡴࡻࡲࡤࡧࠣࡪ࡮ࡲࡥࠡࠩࡾࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠮ࠣὧ").format(bstack1111l1111l1_opy_))
            return []
        data = None
        try:
            with open(bstack1111l1111l1_opy_, bstack1l1l11l_opy_ (u"ࠦࡷࠨὨ")) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(bstack1l1l11l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡐࡓࡐࡐࠣࡪࡷࡵ࡭ࠡࡵࡲࡹࡷࡩࡥࠡࡨ࡬ࡰࡪࠦࠧࡼࡿࠪ࠾ࠥࢁࡽࠣὩ").format(bstack1111l1111l1_opy_, e))
            return []
        _1111l1l11ll_opy_ = None
        _1111l11l1ll_opy_ = None
        def _1111l1lll11_opy_():
            bstack11111l1ll11_opy_ = {}
            bstack11111l1lll1_opy_ = {}
            try:
                if self.bstack1111l1l1111_opy_.startswith(bstack1l1l11l_opy_ (u"࠭ࡻࠨὪ")) and self.bstack1111l1l1111_opy_.endswith(bstack1l1l11l_opy_ (u"ࠧࡾࠩὫ")):
                    bstack11111l1ll11_opy_ = json.loads(self.bstack1111l1l1111_opy_)
                else:
                    bstack11111l1ll11_opy_ = dict(item.split(bstack1l1l11l_opy_ (u"ࠨ࠼ࠪὬ")) for item in self.bstack1111l1l1111_opy_.split(bstack1l1l11l_opy_ (u"ࠩ࠯ࠫὭ")) if bstack1l1l11l_opy_ (u"ࠪ࠾ࠬὮ") in item) if self.bstack1111l1l1111_opy_ else {}
                if self.bstack1111l1l1l11_opy_.startswith(bstack1l1l11l_opy_ (u"ࠫࢀ࠭Ὧ")) and self.bstack1111l1l1l11_opy_.endswith(bstack1l1l11l_opy_ (u"ࠬࢃࠧὰ")):
                    bstack11111l1lll1_opy_ = json.loads(self.bstack1111l1l1l11_opy_)
                else:
                    bstack11111l1lll1_opy_ = dict(item.split(bstack1l1l11l_opy_ (u"࠭࠺ࠨά")) for item in self.bstack1111l1l1l11_opy_.split(bstack1l1l11l_opy_ (u"ࠧ࠭ࠩὲ")) if bstack1l1l11l_opy_ (u"ࠨ࠼ࠪέ") in item) if self.bstack1111l1l1l11_opy_ else {}
            except json.JSONDecodeError as e:
                logger.error(bstack1l1l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡲࡤࡶࡸ࡯࡮ࡨࠢࡩࡩࡦࡺࡵࡳࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡱࡦࡶࡰࡪࡰࡪࡷ࠿ࠦࡻࡾࠤὴ").format(e))
            logger.debug(bstack1l1l11l_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡲࡧࡰࡱ࡫ࡱ࡫ࡸࠦࡦࡳࡱࡰࠤࡪࡴࡶ࠻ࠢࡾࢁ࠱ࠦࡃࡍࡋ࠽ࠤࢀࢃࠢή").format(bstack11111l1ll11_opy_, bstack11111l1lll1_opy_))
            return bstack11111l1ll11_opy_, bstack11111l1lll1_opy_
        if _1111l1l11ll_opy_ is None or _1111l11l1ll_opy_ is None:
            _1111l1l11ll_opy_, _1111l11l1ll_opy_ = _1111l1lll11_opy_()
        def bstack1111ll11111_opy_(name, bstack11111l1llll_opy_):
            if name in _1111l11l1ll_opy_:
                return _1111l11l1ll_opy_[name]
            if name in _1111l1l11ll_opy_:
                return _1111l1l11ll_opy_[name]
            if bstack11111l1llll_opy_.get(bstack1l1l11l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࡇࡸࡡ࡯ࡥ࡫ࠫὶ")):
                return bstack11111l1llll_opy_[bstack1l1l11l_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪࡈࡲࡢࡰࡦ࡬ࠬί")]
            return None
        if isinstance(data, dict):
            bstack1111l11l1l1_opy_ = []
            bstack1111l1l1ll1_opy_ = re.compile(bstack1l1l11l_opy_ (u"ࡸࠧ࡟࡝ࡄ࠱࡟࠶࠭࠺ࡡࡠ࠯ࠩ࠭ὸ"))
            for name, bstack11111l1llll_opy_ in data.items():
                if not isinstance(bstack11111l1llll_opy_, dict):
                    continue
                url = bstack11111l1llll_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡶࡴ࡯ࠫό"))
                if url is None or (isinstance(url, str) and url.strip() == bstack1l1l11l_opy_ (u"ࠨࠩὺ")):
                    logger.warning(bstack1l1l11l_opy_ (u"ࠤࡕࡩࡵࡵࡳࡪࡶࡲࡶࡾࠦࡕࡓࡎࠣ࡭ࡸࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡸࡵࡵࡳࡥࡨࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨύ").format(name, bstack11111l1llll_opy_))
                    continue
                if not bstack1111l1l1ll1_opy_.match(name):
                    logger.warning(bstack1l1l11l_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡸࡵࡵࡳࡥࡨࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࡨࡲࡶࡲࡧࡴࠡࡨࡲࡶࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢὼ").format(name, bstack11111l1llll_opy_))
                    continue
                if len(name) > 30 or len(name) < 1:
                    logger.warning(bstack1l1l11l_opy_ (u"ࠦࡘࡵࡵࡳࡥࡨࠤ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠡࠩࡾࢁࠬࠦ࡭ࡶࡵࡷࠤ࡭ࡧࡶࡦࠢࡤࠤࡱ࡫࡮ࡨࡶ࡫ࠤࡧ࡫ࡴࡸࡧࡨࡲࠥ࠷ࠠࡢࡰࡧࠤ࠸࠶ࠠࡤࡪࡤࡶࡦࡩࡴࡦࡴࡶ࠲ࠧώ").format(name))
                    continue
                bstack11111l1llll_opy_ = bstack11111l1llll_opy_.copy()
                bstack11111l1llll_opy_[bstack1l1l11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ὾")] = name
                bstack11111l1llll_opy_[bstack1l1l11l_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭὿")] = bstack1111ll11111_opy_(name, bstack11111l1llll_opy_)
                if not bstack11111l1llll_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࡃࡴࡤࡲࡨ࡮ࠧᾀ")) or bstack11111l1llll_opy_.get(bstack1l1l11l_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠨᾁ")) == bstack1l1l11l_opy_ (u"ࠩࠪᾂ"):
                    logger.warning(bstack1l1l11l_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡳࡵࡴࠡࡵࡳࡩࡨ࡯ࡦࡪࡧࡧࠤ࡫ࡵࡲࠡࡵࡲࡹࡷࡩࡥࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥᾃ").format(name, bstack11111l1llll_opy_))
                    continue
                if bstack11111l1llll_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡧࡧࡳࡦࡄࡵࡥࡳࡩࡨࠨᾄ")) and bstack11111l1llll_opy_[bstack1l1l11l_opy_ (u"ࠬࡨࡡࡴࡧࡅࡶࡦࡴࡣࡩࠩᾅ")] == bstack11111l1llll_opy_[bstack1l1l11l_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࡂࡳࡣࡱࡧ࡭࠭ᾆ")]:
                    logger.warning(bstack1l1l11l_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥࠡࡤࡵࡥࡳࡩࡨࠡࡣࡱࡨࠥࡨࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡧࡦࡴ࡮ࡰࡶࠣࡦࡪࠦࡴࡩࡧࠣࡷࡦࡳࡥࠡࡨࡲࡶࠥࡹ࡯ࡶࡴࡦࡩࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢᾇ").format(name, bstack11111l1llll_opy_))
                    continue
                bstack1111l11l1l1_opy_.append(bstack11111l1llll_opy_)
            return bstack1111l11l1l1_opy_
        return data
    def bstack1111ll1l11l_opy_(self):
        data = {
            bstack1l1l11l_opy_ (u"ࠨࡴࡸࡲࡤࡹ࡭ࡢࡴࡷࡣࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠧᾈ"): {
                bstack1l1l11l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪᾉ"): self.bstack1111l111lll_opy_(),
                bstack1l1l11l_opy_ (u"ࠪࡱࡴࡪࡥࠨᾊ"): self.bstack1111l1l11l1_opy_(),
                bstack1l1l11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᾋ"): self.bstack1111l1llll1_opy_()
            }
        }
        return data
    def bstack1111l11ll11_opy_(self, config):
        bstack1111l11ll1l_opy_ = {}
        bstack1111l11ll1l_opy_[bstack1l1l11l_opy_ (u"ࠬࡸࡵ࡯ࡡࡶࡱࡦࡸࡴࡠࡵࡨࡰࡪࡩࡴࡪࡱࡱࠫᾌ")] = {
            bstack1l1l11l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧᾍ"): self.bstack1111l111lll_opy_(),
            bstack1l1l11l_opy_ (u"ࠧ࡮ࡱࡧࡩࠬᾎ"): self.bstack1111l1l11l1_opy_()
        }
        bstack1111l11ll1l_opy_[bstack1l1l11l_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟ࡱࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡣ࡫ࡧࡩ࡭ࡧࡧࠫᾏ")] = {
            bstack1l1l11l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡦࠪᾐ"): self.bstack1111l111ll1_opy_()
        }
        bstack1111l11ll1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡶࡺࡴ࡟ࡱࡴࡨࡺ࡮ࡵࡵࡴ࡮ࡼࡣ࡫ࡧࡩ࡭ࡧࡧࡣ࡫࡯ࡲࡴࡶࠪᾑ")] = {
            bstack1l1l11l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬᾒ"): self.bstack11111ll1l1l_opy_()
        }
        bstack1111l11ll1l_opy_[bstack1l1l11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡪࡦ࡯࡬ࡪࡰࡪࡣࡦࡴࡤࡠࡨ࡯ࡥࡰࡿࠧᾓ")] = {
            bstack1l1l11l_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡪࠧᾔ"): self.bstack11111llll1l_opy_()
        }
        if self.bstack11l111llll_opy_(config):
            bstack1111l11ll1l_opy_[bstack1l1l11l_opy_ (u"ࠧࡳࡧࡷࡶࡾࡥࡴࡦࡵࡷࡷࡤࡵ࡮ࡠࡨࡤ࡭ࡱࡻࡲࡦࠩᾕ")] = {
                bstack1l1l11l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡥࠩᾖ"): True,
                bstack1l1l11l_opy_ (u"ࠩࡰࡥࡽࡥࡲࡦࡶࡵ࡭ࡪࡹࠧᾗ"): self.bstack1llll1llll_opy_(config)
            }
        if self.bstack11l111l1ll1_opy_(config):
            bstack1111l11ll1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡱࡱࡣ࡫ࡧࡩ࡭ࡷࡵࡩࠬᾘ")] = {
                bstack1l1l11l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡨࠬᾙ"): True,
                bstack1l1l11l_opy_ (u"ࠬࡳࡡࡹࡡࡩࡥ࡮ࡲࡵࡳࡧࡶࠫᾚ"): self.bstack11l111ll1l1_opy_(config)
            }
        return bstack1111l11ll1l_opy_
    def bstack1lll1111_opy_(self, config):
        bstack1l1l11l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡴࡲ࡬ࡦࡥࡷࡷࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢࠢࡥࡽࠥࡳࡡ࡬࡫ࡱ࡫ࠥࡧࠠࡤࡣ࡯ࡰࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩ࡛ࠥࡕࡊࡆࠣࡳ࡫ࠦࡴࡩࡧࠣࡦࡺ࡯࡬ࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᾛ")
        if not (config.get(bstack1l1l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᾜ"), None) in bstack11l11ll1lll_opy_ and self.bstack1111l111lll_opy_()):
            return None
        bstack1111l111l11_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᾝ"), None)
        logger.debug(bstack1l1l11l_opy_ (u"ࠤ࡞ࡧࡴࡲ࡬ࡦࡥࡷࡆࡺ࡯࡬ࡥࡆࡤࡸࡦࡣࠠࡄࡱ࡯ࡰࡪࡩࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤ࡚࡛ࡉࡅ࠼ࠣࡿࢂࠨᾞ").format(bstack1111l111l11_opy_))
        try:
            bstack11l1ll11111_opy_ = bstack1l1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠣᾟ").format(bstack1111l111l11_opy_)
            payload = {
                bstack1l1l11l_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤᾠ"): config.get(bstack1l1l11l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᾡ"), bstack1l1l11l_opy_ (u"࠭ࠧᾢ")),
                bstack1l1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥᾣ"): config.get(bstack1l1l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᾤ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢᾥ"): os.environ.get(bstack1l1l11l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠤᾦ"), bstack1l1l11l_opy_ (u"ࠦࠧᾧ")),
                bstack1l1l11l_opy_ (u"ࠧࡴ࡯ࡥࡧࡌࡲࡩ࡫ࡸࠣᾨ"): int(os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤᾩ")) or bstack1l1l11l_opy_ (u"ࠢ࠱ࠤᾪ")),
                bstack1l1l11l_opy_ (u"ࠣࡶࡲࡸࡦࡲࡎࡰࡦࡨࡷࠧᾫ"): int(os.environ.get(bstack1l1l11l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦᾬ")) or bstack1l1l11l_opy_ (u"ࠥ࠵ࠧᾭ")),
                bstack1l1l11l_opy_ (u"ࠦ࡭ࡵࡳࡵࡋࡱࡪࡴࠨᾮ"): get_host_info(),
            }
            logger.debug(bstack1l1l11l_opy_ (u"ࠧࡡࡣࡰ࡮࡯ࡩࡨࡺࡂࡶ࡫࡯ࡨࡉࡧࡴࡢ࡟ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡲࡤࡽࡱࡵࡡࡥ࠼ࠣࡿࢂࠨᾯ").format(payload))
            response = bstack11l1l1lll1l_opy_.bstack1111l1ll11l_opy_(bstack11l1ll11111_opy_, payload)
            if response:
                logger.debug(bstack1l1l11l_opy_ (u"ࠨ࡛ࡤࡱ࡯ࡰࡪࡩࡴࡃࡷ࡬ࡰࡩࡊࡡࡵࡣࡠࠤࡇࡻࡩ࡭ࡦࠣࡨࡦࡺࡡࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦᾰ").format(response))
                return response
            else:
                logger.error(bstack1l1l11l_opy_ (u"ࠢ࡜ࡥࡲࡰࡱ࡫ࡣࡵࡄࡸ࡭ࡱࡪࡄࡢࡶࡤࡡࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊ࠺ࠡࡽࢀࠦᾱ").format(bstack1111l111l11_opy_))
                return None
        except Exception as e:
            logger.error(bstack1l1l11l_opy_ (u"ࠣ࡝ࡦࡳࡱࡲࡥࡤࡶࡅࡹ࡮ࡲࡤࡅࡣࡷࡥࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡘ࡙ࡎࡊࠠࡼࡿ࠽ࠤࢀࢃࠢᾲ").format(bstack1111l111l11_opy_, e))
            return None
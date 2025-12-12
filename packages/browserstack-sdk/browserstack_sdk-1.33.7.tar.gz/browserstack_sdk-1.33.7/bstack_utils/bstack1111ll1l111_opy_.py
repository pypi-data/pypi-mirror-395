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
import time
from bstack_utils.bstack11l1l1ll1ll_opy_ import bstack11l1l1lll1l_opy_
from bstack_utils.constants import bstack11l11ll1ll1_opy_
from bstack_utils.helper import get_host_info, bstack111llll1lll_opy_
class bstack1111ll1ll1l_opy_:
    bstack1l1l11l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡷࡩࡸࡺࠠࡰࡴࡧࡩࡷ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡷࡪࡸࡶࡦࡴ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ⃻")
    def __init__(self, config, logger):
        bstack1l1l11l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡣࡰࡰࡩ࡭࡬ࡀࠠࡥ࡫ࡦࡸ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡤࡹࡴࡳࡣࡷࡩ࡬ࡿ࠺ࠡࡵࡷࡶ࠱ࠦࡴࡦࡵࡷࠤࡴࡸࡤࡦࡴ࡬ࡲ࡬ࠦࡳࡵࡴࡤࡸࡪ࡭ࡹࠡࡰࡤࡱࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⃼")
        self.config = config
        self.logger = logger
        self.bstack1llll11l1ll1_opy_ = bstack1l1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡲ࡯࡭ࡹ࠳ࡴࡦࡵࡷࡷࠧ⃽")
        self.bstack1llll11llll1_opy_ = None
        self.bstack1llll11ll11l_opy_ = 60
        self.bstack1llll11l1l1l_opy_ = 5
        self.bstack1llll1l11111_opy_ = 0
    def bstack1111lll1111_opy_(self, test_files, orchestration_strategy, orchestration_metadata={}):
        bstack1l1l11l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡱ࡭ࡹ࡯ࡡࡵࡧࡶࠤࡹ࡮ࡥࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡸࡺ࡯ࡳࡧࡶࠤࡹ࡮ࡥࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡶ࡯࡭࡮࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⃾")
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡎࡴࡩࡵ࡫ࡤࡸ࡮ࡴࡧࠡࡵࡳࡰ࡮ࡺࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࠤࡸࡺࡲࡢࡶࡨ࡫ࡾࡀࠠࡼࡿࠥ⃿").format(orchestration_strategy))
        try:
            bstack1llll1l111ll_opy_ = []
            bstack1l1l11l_opy_ (u"ࠨ࡙ࠢࠣࡨࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡦࡦࡶࡦ࡬ࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤ࡮ࡹࠠࡴࡱࡸࡶࡨ࡫ࠠࡪࡵࠣࡸࡾࡶࡥࠡࡱࡩࠤࡦࡸࡲࡢࡻࠣࡥࡳࡪࠠࡪࡶࠪࡷࠥ࡫࡬ࡦ࡯ࡨࡲࡹࡹࠠࡢࡴࡨࠤࡴ࡬ࠠࡵࡻࡳࡩࠥࡪࡩࡤࡶࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡨࡧࡦࡻࡳࡦࠢ࡬ࡲࠥࡺࡨࡢࡶࠣࡧࡦࡹࡥ࠭ࠢࡸࡷࡪࡸࠠࡩࡣࡶࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦ࡭ࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡷࡴࡻࡲࡤࡧࠣࡻ࡮ࡺࡨࠡࡨࡨࡥࡹࡻࡲࡦࡄࡵࡥࡳࡩࡨࠡ࡫ࡱࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠥࠦࠧ℀")
            source = orchestration_metadata[bstack1l1l11l_opy_ (u"ࠧࡳࡷࡱࡣࡸࡳࡡࡳࡶࡢࡷࡪࡲࡥࡤࡶ࡬ࡳࡳ࠭℁")].get(bstack1l1l11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨℂ"), [])
            bstack1llll11l11ll_opy_ = isinstance(source, list) and all(isinstance(src, dict) and src is not None for src in source) and len(source) > 0
            if orchestration_metadata[bstack1l1l11l_opy_ (u"ࠩࡵࡹࡳࡥࡳ࡮ࡣࡵࡸࡤࡹࡥ࡭ࡧࡦࡸ࡮ࡵ࡮ࠨ℃")].get(bstack1l1l11l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡧࠫ℄"), False) and not bstack1llll11l11ll_opy_:
                bstack1llll1l111ll_opy_ = bstack111llll1lll_opy_(source) # bstack1llll1l111l1_opy_-repo is handled bstack1llll1l1111l_opy_
            payload = {
                bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥ℅"): [{bstack1l1l11l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢ℆"): f} for f in test_files],
                bstack1l1l11l_opy_ (u"ࠨ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࡙ࡴࡳࡣࡷࡩ࡬ࡿࠢℇ"): orchestration_strategy,
                bstack1l1l11l_opy_ (u"ࠢࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡍࡦࡶࡤࡨࡦࡺࡡࠣ℈"): orchestration_metadata,
                bstack1l1l11l_opy_ (u"ࠣࡰࡲࡨࡪࡏ࡮ࡥࡧࡻࠦ℉"): int(os.environ.get(bstack1l1l11l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧℊ")) or bstack1l1l11l_opy_ (u"ࠥ࠴ࠧℋ")),
                bstack1l1l11l_opy_ (u"ࠦࡹࡵࡴࡢ࡮ࡑࡳࡩ࡫ࡳࠣℌ"): int(os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢℍ")) or bstack1l1l11l_opy_ (u"ࠨ࠱ࠣℎ")),
                bstack1l1l11l_opy_ (u"ࠢࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠧℏ"): self.config.get(bstack1l1l11l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ℐ"), bstack1l1l11l_opy_ (u"ࠩࠪℑ")),
                bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠨℒ"): self.config.get(bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧℓ"), os.path.basename(os.path.abspath(os.getcwd()))),
                bstack1l1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥ℔"): os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠧℕ"), bstack1l1l11l_opy_ (u"ࠢࠣ№")),
                bstack1l1l11l_opy_ (u"ࠣࡪࡲࡷࡹࡏ࡮ࡧࡱࠥ℗"): get_host_info(),
                bstack1l1l11l_opy_ (u"ࠤࡳࡶࡉ࡫ࡴࡢ࡫࡯ࡷࠧ℘"): bstack1llll1l111ll_opy_
            }
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥ࡟ࡸࡶ࡬ࡪࡶࡗࡩࡸࡺࡳ࡞ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹ࠺ࠡࡽࢀࠦℙ").format(payload))
            response = bstack11l1l1lll1l_opy_.bstack1llll1l1lll1_opy_(self.bstack1llll11l1ll1_opy_, payload)
            if response:
                self.bstack1llll11llll1_opy_ = self._1llll11ll111_opy_(response)
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡠࡹࡰ࡭࡫ࡷࡘࡪࡹࡴࡴ࡟ࠣࡗࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢℚ").format(self.bstack1llll11llll1_opy_))
            else:
                self.logger.error(bstack1l1l11l_opy_ (u"ࠧࡡࡳࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࡠࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡨࡧࡷࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠲ࠧℛ"))
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨ࡛ࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴ࠼࠽ࠤࢀࢃࠢℜ").format(e))
    def _1llll11ll111_opy_(self, response):
        bstack1l1l11l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡸࡶ࡬ࡪࡶࠣࡸࡪࡹࡴࡴࠢࡄࡔࡎࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡣࡱࡨࠥ࡫ࡸࡵࡴࡤࡧࡹࡹࠠࡳࡧ࡯ࡩࡻࡧ࡮ࡵࠢࡩ࡭ࡪࡲࡤࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢℝ")
        bstack111lll1l_opy_ = {}
        bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ℞")] = response.get(bstack1l1l11l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ℟"), self.bstack1llll11ll11l_opy_)
        bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࡍࡳࡺࡥࡳࡸࡤࡰࠧ℠")] = response.get(bstack1l1l11l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࡎࡴࡴࡦࡴࡹࡥࡱࠨ℡"), self.bstack1llll11l1l1l_opy_)
        bstack1llll11lllll_opy_ = response.get(bstack1l1l11l_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸ࡚ࡸ࡬ࠣ™"))
        bstack1llll11l1l11_opy_ = response.get(bstack1l1l11l_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࡕࡳ࡮ࠥ℣"))
        if bstack1llll11lllll_opy_:
            bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡕࡳ࡮ࠥℤ")] = bstack1llll11lllll_opy_.split(bstack11l11ll1ll1_opy_ + bstack1l1l11l_opy_ (u"ࠣ࠱ࠥ℥"))[1] if bstack11l11ll1ll1_opy_ + bstack1l1l11l_opy_ (u"ࠤ࠲ࠦΩ") in bstack1llll11lllll_opy_ else bstack1llll11lllll_opy_
        else:
            bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨ℧")] = None
        if bstack1llll11l1l11_opy_:
            bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸ࡚ࡸ࡬ࠣℨ")] = bstack1llll11l1l11_opy_.split(bstack11l11ll1ll1_opy_ + bstack1l1l11l_opy_ (u"ࠧ࠵ࠢ℩"))[1] if bstack11l11ll1ll1_opy_ + bstack1l1l11l_opy_ (u"ࠨ࠯ࠣK") in bstack1llll11l1l11_opy_ else bstack1llll11l1l11_opy_
        else:
            bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡖࡴ࡯ࠦÅ")] = None
        if (
            response.get(bstack1l1l11l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤℬ")) is None or
            response.get(bstack1l1l11l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡌࡲࡹ࡫ࡲࡷࡣ࡯ࠦℭ")) is None or
            response.get(bstack1l1l11l_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷ࡙ࡷࡲࠢ℮")) is None or
            response.get(bstack1l1l11l_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷ࡙ࡷࡲࠢℯ")) is None
        ):
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡡࡰࡳࡱࡦࡩࡸࡹ࡟ࡴࡲ࡯࡭ࡹࡥࡴࡦࡵࡷࡷࡤࡸࡥࡴࡲࡲࡲࡸ࡫࡝ࠡࡔࡨࡧࡪ࡯ࡶࡦࡦࠣࡲࡺࡲ࡬ࠡࡸࡤࡰࡺ࡫ࠨࡴࠫࠣࡪࡴࡸࠠࡴࡱࡰࡩࠥࡧࡴࡵࡴ࡬ࡦࡺࡺࡥࡴࠢ࡬ࡲࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏࠠࡳࡧࡶࡴࡴࡴࡳࡦࠤℰ"))
        return bstack111lll1l_opy_
    def bstack1111ll1ll11_opy_(self):
        if not self.bstack1llll11llll1_opy_:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡏࡱࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠳ࠨℱ"))
            return None
        bstack1llll11ll1ll_opy_ = None
        test_files = []
        bstack1llll11l1lll_opy_ = int(time.time() * 1000) # bstack1llll11lll11_opy_ sec
        bstack1llll11lll1l_opy_ = int(self.bstack1llll11llll1_opy_.get(bstack1l1l11l_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࡊࡰࡷࡩࡷࡼࡡ࡭ࠤℲ"), self.bstack1llll11l1l1l_opy_))
        bstack1llll11ll1l1_opy_ = int(self.bstack1llll11llll1_opy_.get(bstack1l1l11l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤℳ"), self.bstack1llll11ll11l_opy_)) * 1000
        bstack1llll11l1l11_opy_ = self.bstack1llll11llll1_opy_.get(bstack1l1l11l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࡘࡶࡱࠨℴ"), None)
        bstack1llll11lllll_opy_ = self.bstack1llll11llll1_opy_.get(bstack1l1l11l_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡘࡶࡱࠨℵ"), None)
        if bstack1llll11lllll_opy_ is None and bstack1llll11l1l11_opy_ is None:
            return None
        try:
            while bstack1llll11lllll_opy_ and (time.time() * 1000 - bstack1llll11l1lll_opy_) < bstack1llll11ll1l1_opy_:
                response = bstack11l1l1lll1l_opy_.bstack1llll1l1l1l1_opy_(bstack1llll11lllll_opy_, {})
                if response and response.get(bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࠥℶ")):
                    bstack1llll11ll1ll_opy_ = response.get(bstack1l1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡶࠦℷ"))
                self.bstack1llll1l11111_opy_ += 1
                if bstack1llll11ll1ll_opy_:
                    break
                time.sleep(bstack1llll11lll1l_opy_)
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠨ࡛ࡨࡧࡷࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡇ࡫࡯ࡩࡸࡣࠠࡇࡧࡷࡧ࡭࡯࡮ࡨࠢࡲࡶࡩ࡫ࡲࡦࡦࠣࡸࡪࡹࡴࡴࠢࡩࡶࡴࡳࠠࡳࡧࡶࡹࡱࡺࠠࡖࡔࡏࠤࡦ࡬ࡴࡦࡴࠣࡻࡦ࡯ࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡽࢀࠤࡸ࡫ࡣࡰࡰࡧࡷ࠳ࠨℸ").format(bstack1llll11lll1l_opy_))
            if bstack1llll11l1l11_opy_ and not bstack1llll11ll1ll_opy_:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠢ࡜ࡩࡨࡸࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡈ࡬ࡰࡪࡹ࡝ࠡࡈࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡳࡷࡪࡥࡳࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡬ࡱࡪࡵࡵࡵࠢࡘࡖࡑࠨℹ"))
                response = bstack11l1l1lll1l_opy_.bstack1llll1l1l1l1_opy_(bstack1llll11l1l11_opy_, {})
                if response and response.get(bstack1l1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡹࠢ℺")):
                    bstack1llll11ll1ll_opy_ = response.get(bstack1l1l11l_opy_ (u"ࠤࡷࡩࡸࡺࡳࠣ℻"))
            if bstack1llll11ll1ll_opy_ and len(bstack1llll11ll1ll_opy_) > 0:
                for bstack111l1llll1_opy_ in bstack1llll11ll1ll_opy_:
                    file_path = bstack111l1llll1_opy_.get(bstack1l1l11l_opy_ (u"ࠥࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠧℼ"))
                    if file_path:
                        test_files.append(file_path)
            if not bstack1llll11ll1ll_opy_:
                return None
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡠ࡭ࡥࡵࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡌࡩ࡭ࡧࡶࡡࠥࡕࡲࡥࡧࡵࡩࡩࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡶࡪࡩࡥࡪࡸࡨࡨ࠿ࠦࡻࡾࠤℽ").format(test_files))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠧࡡࡧࡦࡶࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡰࡴࡧࡩࡷ࡫ࡤࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷ࠿ࠦࡻࡾࠤℾ").format(e))
            return None
    def bstack1111ll11l11_opy_(self):
        bstack1l1l11l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡷࡵࡲࡩࡵࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍࠥࡩࡡ࡭࡮ࡶࠤࡲࡧࡤࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢℿ")
        return self.bstack1llll1l11111_opy_
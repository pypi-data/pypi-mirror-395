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
from bstack_utils.constants import *
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.bstack1111ll1l111_opy_ import bstack1111ll1ll1l_opy_
from bstack_utils.bstack111l1l1ll_opy_ import bstack1llllll111_opy_
from bstack_utils.helper import bstack1llll111_opy_
import json
class bstack1ll11ll11_opy_:
    _1lll11l11ll_opy_ = None
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.bstack1111ll111ll_opy_ = bstack1111ll1ll1l_opy_(self.config, logger)
        self.bstack111l1l1ll_opy_ = bstack1llllll111_opy_.bstack11l111l11l_opy_(config=self.config)
        self.bstack1111lll11l1_opy_ = {}
        self.bstack111111l11l_opy_ = False
        self.bstack1111ll1lll1_opy_ = (
            self.__1111ll1llll_opy_()
            and self.bstack111l1l1ll_opy_ is not None
            and self.bstack111l1l1ll_opy_.bstack1l11lll1ll_opy_()
            and config.get(bstack1l1l11l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧἙ"), None) is not None
            and config.get(bstack1l1l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭Ἒ"), os.path.basename(os.getcwd())) is not None
        )
    @classmethod
    def bstack11l111l11l_opy_(cls, config, logger):
        if cls._1lll11l11ll_opy_ is None and config is not None:
            cls._1lll11l11ll_opy_ = bstack1ll11ll11_opy_(config, logger)
        return cls._1lll11l11ll_opy_
    def bstack1l11lll1ll_opy_(self):
        bstack1l1l11l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡆࡲࠤࡳࡵࡴࠡࡣࡳࡴࡱࡿࠠࡵࡧࡶࡸࠥࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡸࡪࡨࡲ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡔ࠷࠱ࡺࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡑࡵࡨࡪࡸࡩ࡯ࡩࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠢ࡬ࡷࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢἛ")
        return self.bstack1111ll1lll1_opy_ and self.bstack1111ll11lll_opy_()
    def bstack1111ll11lll_opy_(self):
        bstack1111lll111l_opy_ = os.getenv(bstack1l1l11l_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭Ἔ"), self.config.get(bstack1l1l11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩἝ"), None))
        return bstack1111lll111l_opy_ in bstack11l11ll1lll_opy_
    def __1111ll1llll_opy_(self):
        bstack11l1l11llll_opy_ = False
        for fw in bstack11l11llllll_opy_:
            if fw in self.config.get(bstack1l1l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ἞"), bstack1l1l11l_opy_ (u"ࠨࠩ἟")):
                bstack11l1l11llll_opy_ = True
        return bstack1llll111_opy_(self.config.get(bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ἠ"), bstack11l1l11llll_opy_))
    def bstack1111ll1l1ll_opy_(self):
        return (not self.bstack1l11lll1ll_opy_() and
                self.bstack111l1l1ll_opy_ is not None and self.bstack111l1l1ll_opy_.bstack1l11lll1ll_opy_())
    def bstack1111ll1l1l1_opy_(self):
        if not self.bstack1111ll1l1ll_opy_():
            return
        if self.config.get(bstack1l1l11l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨἡ"), None) is None or self.config.get(bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧἢ"), os.path.basename(os.getcwd())) is None:
            self.logger.info(bstack1l1l11l_opy_ (u"࡚ࠧࡥࡴࡶࠣࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡤࡣࡱࠫࡹࠦࡷࡰࡴ࡮ࠤࡦࡹࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠣࡳࡷࠦࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠤ࡮ࡹࠠ࡯ࡷ࡯ࡰ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡳࡦࡶࠣࡥࠥࡴ࡯࡯࠯ࡱࡹࡱࡲࠠࡷࡣ࡯ࡹࡪ࠴ࠢἣ"))
        if not self.__1111ll1llll_opy_():
            self.logger.info(bstack1l1l11l_opy_ (u"ࠨࡔࡦࡵࡷࠤࡗ࡫࡯ࡳࡦࡨࡶ࡮ࡴࡧࠡࡥࡤࡲࠬࡺࠠࡸࡱࡵ࡯ࠥࡧࡳࠡࡶࡨࡷࡹࡘࡥࡱࡱࡵࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡦࡰࡤࡦࡱ࡫ࠠࡪࡶࠣࡪࡷࡵ࡭ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠤ࡫࡯࡬ࡦ࠰ࠥἤ"))
    def bstack1111ll11l1l_opy_(self):
        return self.bstack111111l11l_opy_
    def bstack1111111ll1_opy_(self, bstack1111ll11ll1_opy_):
        self.bstack111111l11l_opy_ = bstack1111ll11ll1_opy_
        self.bstack1lllllll1ll_opy_(bstack1l1l11l_opy_ (u"ࠢࡢࡲࡳࡰ࡮࡫ࡤࠣἥ"), bstack1111ll11ll1_opy_)
    def bstack11111l111l_opy_(self, test_files):
        try:
            if test_files is None:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡪࡴࡸࠠࡰࡴࡧࡩࡷ࡯࡮ࡨ࠰ࠥἦ"))
                return None
            orchestration_strategy = None
            orchestration_metadata = self.bstack111l1l1ll_opy_.bstack1111ll1l11l_opy_()
            if self.bstack111l1l1ll_opy_ is not None:
                orchestration_strategy = self.bstack111l1l1ll_opy_.bstack11l1lll11_opy_()
            if orchestration_strategy is None:
                self.logger.error(bstack1l1l11l_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼࠤ࡮ࡹࠠࡏࡱࡱࡩ࠳ࠦࡃࡢࡰࡱࡳࡹࠦࡰࡳࡱࡦࡩࡪࡪࠠࡸ࡫ࡷ࡬ࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠲ࠧἧ"))
                return None
            self.logger.info(bstack1l1l11l_opy_ (u"ࠥࡖࡪࡵࡲࡥࡧࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡯ࡴࡩࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡸࡷࡧࡴࡦࡩࡼ࠾ࠥࢁࡽࠣἨ").format(orchestration_strategy))
            if cli.is_running():
                self.logger.debug(bstack1l1l11l_opy_ (u"࡚ࠦࡹࡩ࡯ࡩࠣࡇࡑࡏࠠࡧ࡮ࡲࡻࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢἩ"))
                ordered_test_files = cli.test_orchestration_session(test_files, orchestration_strategy, json.dumps(orchestration_metadata))
            else:
                self.logger.debug(bstack1l1l11l_opy_ (u"࡛ࠧࡳࡪࡰࡪࠤࡸࡪ࡫ࠡࡨ࡯ࡳࡼࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣἪ"))
                self.bstack1111ll111ll_opy_.bstack1111lll1111_opy_(test_files, orchestration_strategy, orchestration_metadata)
                ordered_test_files = self.bstack1111ll111ll_opy_.bstack1111ll1ll11_opy_()
            if not ordered_test_files:
                return None
            self.bstack1lllllll1ll_opy_(bstack1l1l11l_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩ࡫ࡤࡕࡧࡶࡸࡋ࡯࡬ࡦࡵࡆࡳࡺࡴࡴࠣἫ"), len(test_files))
            self.bstack1lllllll1ll_opy_(bstack1l1l11l_opy_ (u"ࠢ࡯ࡱࡧࡩࡎࡴࡤࡦࡺࠥἬ"), int(os.environ.get(bstack1l1l11l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦἭ")) or bstack1l1l11l_opy_ (u"ࠤ࠳ࠦἮ")))
            self.bstack1lllllll1ll_opy_(bstack1l1l11l_opy_ (u"ࠥࡸࡴࡺࡡ࡭ࡐࡲࡨࡪࡹࠢἯ"), int(os.environ.get(bstack1l1l11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢἰ")) or bstack1l1l11l_opy_ (u"ࠧ࠷ࠢἱ")))
            self.bstack1lllllll1ll_opy_(bstack1l1l11l_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡗࡩࡸࡺࡆࡪ࡮ࡨࡷࡈࡵࡵ࡯ࡶࠥἲ"), len(ordered_test_files))
            self.bstack1lllllll1ll_opy_(bstack1l1l11l_opy_ (u"ࠢࡴࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࡅࡕࡏࡃࡢ࡮࡯ࡇࡴࡻ࡮ࡵࠤἳ"), self.bstack1111ll111ll_opy_.bstack1111ll11l11_opy_())
            return ordered_test_files
        except Exception as e:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣ࡝ࡵࡩࡴࡸࡤࡦࡴࡢࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹ࡝ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡳࡷࡪࡥࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡱࡧࡳࡴࡧࡶ࠾ࠥࢁࡽࠣἴ").format(e))
        return None
    def bstack1lllllll1ll_opy_(self, key, value):
        self.bstack1111lll11l1_opy_[key] = value
    def bstack11ll1lll1_opy_(self):
        return self.bstack1111lll11l1_opy_
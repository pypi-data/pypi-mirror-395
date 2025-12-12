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
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack11ll1lllll_opy_
from browserstack_sdk.bstack1l1lll1lll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l11ll1ll_opy_
from bstack_utils.bstack111l1l1ll_opy_ import bstack1llllll111_opy_
from bstack_utils.constants import bstack11111111ll_opy_
from bstack_utils.bstack11l1l1l11l_opy_ import bstack1ll11ll11_opy_
class bstack11ll111111_opy_:
    def __init__(self, args, logger, bstack11111l1ll1_opy_, bstack11111ll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111l1ll1_opy_ = bstack11111l1ll1_opy_
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1lllll1l_opy_ = []
        self.bstack11111l1111_opy_ = []
        self.bstack11l11l11l_opy_ = []
        self.bstack11111l1l1l_opy_ = self.bstack11l11llll1_opy_()
        self.bstack1l111l1lll_opy_ = -1
    def bstack1ll11ll1l1_opy_(self, bstack11111ll11l_opy_):
        self.parse_args()
        self.bstack111111lll1_opy_()
        self.bstack1llllllllll_opy_(bstack11111ll11l_opy_)
        self.bstack1111111l1l_opy_()
    def bstack11llllll11_opy_(self):
        bstack11l1l1l11l_opy_ = bstack1ll11ll11_opy_.bstack11l111l11l_opy_(self.bstack11111l1ll1_opy_, self.logger)
        if bstack11l1l1l11l_opy_ is None:
            self.logger.warn(bstack1l1l11l_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡩࡣࡱࡨࡱ࡫ࡲࠡ࡫ࡶࠤࡳࡵࡴࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩ࠴ࠠࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥ႒"))
            return
        bstack111111l11l_opy_ = False
        bstack11l1l1l11l_opy_.bstack1lllllll1ll_opy_(bstack1l1l11l_opy_ (u"ࠣࡧࡱࡥࡧࡲࡥࡥࠤ႓"), bstack11l1l1l11l_opy_.bstack1l11lll1ll_opy_())
        start_time = time.time()
        if bstack11l1l1l11l_opy_.bstack1l11lll1ll_opy_():
            test_files = self.bstack111111ll1l_opy_()
            bstack111111l11l_opy_ = True
            bstack111111llll_opy_ = bstack11l1l1l11l_opy_.bstack11111l111l_opy_(test_files)
            if bstack111111llll_opy_:
                self.bstack1l1lllll1l_opy_ = [os.path.normpath(item) for item in bstack111111llll_opy_]
                self.__111111ll11_opy_()
                bstack11l1l1l11l_opy_.bstack1111111ll1_opy_(bstack111111l11l_opy_)
                self.logger.info(bstack1l1l11l_opy_ (u"ࠤࡗࡩࡸࡺࡳࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡺࡹࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ႔").format(self.bstack1l1lllll1l_opy_))
            else:
                self.logger.info(bstack1l1l11l_opy_ (u"ࠥࡒࡴࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡻࡪࡸࡥࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤࡧࡿࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣ႕"))
        bstack11l1l1l11l_opy_.bstack1lllllll1ll_opy_(bstack1l1l11l_opy_ (u"ࠦࡹ࡯࡭ࡦࡖࡤ࡯ࡪࡴࡔࡰࡃࡳࡴࡱࡿࠢ႖"), int((time.time() - start_time) * 1000)) # bstack1lllllllll1_opy_ to bstack11111l1lll_opy_
    def __111111ll11_opy_(self):
        bstack1l1l11l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡵࡲࡡࡤࡧࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࡷࠥ࡯࡮ࠡࡅࡏࡍࠥ࡬࡬ࡢࡩࡶࠤࡼ࡯ࡴࡩࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡴࡧࡵࡺࡪࡸࠠࡳࡧࡷࡹࡷࡴࡳࠡࡴࡨࡳࡷࡪࡥࡳࡧࡧࠤ࡫࡯࡬ࡦࠢࡱࡥࡲ࡫ࡳ࠭ࠢࡤࡲࡩࠦࡷࡦࠢࡶ࡭ࡲࡶ࡬ࡺࠢࡸࡴࡩࡧࡴࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸ࡭࡫ࠠࡄࡎࡌࠤࡦࡸࡧࡴࠢࡷࡳࠥࡻࡳࡦࠢࡷ࡬ࡴࡹࡥࠡࡨ࡬ࡰࡪࡹ࠮ࠡࡗࡶࡩࡷ࠭ࡳࠡࡨ࡬ࡰࡹ࡫ࡲࡪࡰࡪࠤ࡫ࡲࡡࡨࡵࠣࠬ࠲ࡳࠬࠡ࠯࡮࠭ࠥࡸࡥ࡮ࡣ࡬ࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶࡤࡧࡹࠦࡡ࡯ࡦࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡦࡶࡰ࡭࡫ࡨࡨࠥࡴࡡࡵࡷࡵࡥࡱࡲࡹࠡࡦࡸࡶ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ႗")
        try:
            if not self.bstack1l1lllll1l_opy_:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡎࡰࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡱࡣࡷ࡬ࠥࡺ࡯ࠡࡵࡨࡸࠧ႘"))
                return
            bstack11111lll11_opy_ = []
            for flag in self.bstack11111l1111_opy_:
                if flag.startswith(bstack1l1l11l_opy_ (u"ࠧ࠮ࠩ႙")):
                    bstack11111lll11_opy_.append(flag)
                    continue
                bstack1111111111_opy_ = False
                if bstack1l1l11l_opy_ (u"ࠨ࠼࠽ࠫႚ") in flag:
                    bstack1111111lll_opy_ = flag.split(bstack1l1l11l_opy_ (u"ࠩ࠽࠾ࠬႛ"), 1)[0]
                    if os.path.exists(bstack1111111lll_opy_):
                        bstack1111111111_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1l1l11l_opy_ (u"ࠪ࠲ࡵࡿࠧႜ"))):
                        bstack1111111111_opy_ = True
                if not bstack1111111111_opy_:
                    bstack11111lll11_opy_.append(flag)
            bstack11111lll11_opy_.extend(self.bstack1l1lllll1l_opy_)
            self.bstack11111l1111_opy_ = bstack11111lll11_opy_
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷࡩࡩࠦࡳࡦ࡮ࡨࡧࡹࡵࡲࡴ࠼ࠣࡿࢂࠨႝ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack111111111l_opy_():
        import importlib
        if getattr(importlib, bstack1l1l11l_opy_ (u"ࠬ࡬ࡩ࡯ࡦࡢࡰࡴࡧࡤࡦࡴࠪ႞"), False):
            bstack11111111l1_opy_ = importlib.find_loader(bstack1l1l11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ႟"))
        else:
            bstack11111111l1_opy_ = importlib.util.find_spec(bstack1l1l11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩႠ"))
    def bstack111111l1ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l111l1lll_opy_ = -1
        if self.bstack11111ll1ll_opy_ and bstack1l1l11l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨႡ") in self.bstack11111l1ll1_opy_:
            self.bstack1l111l1lll_opy_ = int(self.bstack11111l1ll1_opy_[bstack1l1l11l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩႢ")])
        try:
            bstack1111111l11_opy_ = [bstack1l1l11l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬႣ"), bstack1l1l11l_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧႤ"), bstack1l1l11l_opy_ (u"ࠬ࠳ࡰࠨႥ")]
            if self.bstack1l111l1lll_opy_ >= 0:
                bstack1111111l11_opy_.extend([bstack1l1l11l_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧႦ"), bstack1l1l11l_opy_ (u"ࠧ࠮ࡰࠪႧ")])
            for arg in bstack1111111l11_opy_:
                self.bstack111111l1ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111111lll1_opy_(self):
        bstack11111l1111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11111l1111_opy_ = bstack11111l1111_opy_
        return self.bstack11111l1111_opy_
    def bstack1l1l11ll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack111111111l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l11ll1ll_opy_)
    def bstack1llllllllll_opy_(self, bstack11111ll11l_opy_):
        bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
        if bstack11111ll11l_opy_:
            self.bstack11111l1111_opy_.append(bstack1l1l11l_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬႨ"))
            self.bstack11111l1111_opy_.append(bstack1l1l11l_opy_ (u"ࠩࡗࡶࡺ࡫ࠧႩ"))
        if bstack1ll1l111l1_opy_.bstack111111l1l1_opy_():
            self.bstack11111l1111_opy_.append(bstack1l1l11l_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩႪ"))
            self.bstack11111l1111_opy_.append(bstack1l1l11l_opy_ (u"࡙ࠫࡸࡵࡦࠩႫ"))
        self.bstack11111l1111_opy_.append(bstack1l1l11l_opy_ (u"ࠬ࠳ࡰࠨႬ"))
        self.bstack11111l1111_opy_.append(bstack1l1l11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫႭ"))
        self.bstack11111l1111_opy_.append(bstack1l1l11l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩႮ"))
        self.bstack11111l1111_opy_.append(bstack1l1l11l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨႯ"))
        if self.bstack1l111l1lll_opy_ > 1:
            self.bstack11111l1111_opy_.append(bstack1l1l11l_opy_ (u"ࠩ࠰ࡲࠬႰ"))
            self.bstack11111l1111_opy_.append(str(self.bstack1l111l1lll_opy_))
    def bstack1111111l1l_opy_(self):
        if bstack1llllll111_opy_.bstack11l111llll_opy_(self.bstack11111l1ll1_opy_):
             self.bstack11111l1111_opy_ += [
                bstack11111111ll_opy_.get(bstack1l1l11l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࠩႱ")), str(bstack1llllll111_opy_.bstack1llll1llll_opy_(self.bstack11111l1ll1_opy_)),
                bstack11111111ll_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪႲ")), str(bstack11111111ll_opy_.get(bstack1l1l11l_opy_ (u"ࠬࡸࡥࡳࡷࡱ࠱ࡩ࡫࡬ࡢࡻࠪႳ")))
            ]
    def bstack1llllllll11_opy_(self):
        bstack11l11l11l_opy_ = []
        for spec in self.bstack1l1lllll1l_opy_:
            bstack1lllll11ll_opy_ = [spec]
            bstack1lllll11ll_opy_ += self.bstack11111l1111_opy_
            bstack11l11l11l_opy_.append(bstack1lllll11ll_opy_)
        self.bstack11l11l11l_opy_ = bstack11l11l11l_opy_
        return bstack11l11l11l_opy_
    def bstack11l11llll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11111l1l1l_opy_ = True
            return True
        except Exception as e:
            self.bstack11111l1l1l_opy_ = False
        return self.bstack11111l1l1l_opy_
    def bstack11l1ll1l1_opy_(self):
        bstack1l1l11l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥࡽࡩࡵࡪࡲࡹࡹࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࡱࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡭ࡳࡺ࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢႴ")
        try:
            from browserstack_sdk.bstack1111l111l1_opy_ import bstack11111llll1_opy_
            bstack11111l11ll_opy_ = bstack11111llll1_opy_(bstack1111l1111l_opy_=self.bstack11111l1111_opy_)
            if not bstack11111l11ll_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨႵ"), False):
                self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡖࡨࡷࡹࠦࡣࡰࡷࡱࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨႶ").format(bstack11111l11ll_opy_.get(bstack1l1l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨႷ"), bstack1l1l11l_opy_ (u"࡙ࠪࡳࡱ࡮ࡰࡹࡱࠤࡪࡸࡲࡰࡴࠪႸ"))))
                return 0
            count = bstack11111l11ll_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡨࡵࡵ࡯ࡶࠪႹ"), 0)
            self.logger.info(bstack1l1l11l_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࡀࠠࡼࡿࠥႺ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿࠥႻ").format(e))
            return 0
    def bstack1l11l11l11_opy_(self, bstack11111ll1l1_opy_, bstack1ll11ll1l1_opy_):
        bstack1ll11ll1l1_opy_[bstack1l1l11l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧႼ")] = self.bstack11111l1ll1_opy_
        multiprocessing.set_start_method(bstack1l1l11l_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧႽ"))
        bstack1lll11lll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llllllll1l_opy_ = manager.list()
        if bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬႾ") in self.bstack11111l1ll1_opy_:
            for index, platform in enumerate(self.bstack11111l1ll1_opy_[bstack1l1l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭Ⴟ")]):
                bstack1lll11lll_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11111ll1l1_opy_,
                                                            args=(self.bstack11111l1111_opy_, bstack1ll11ll1l1_opy_, bstack1llllllll1l_opy_)))
            bstack111111l111_opy_ = len(self.bstack11111l1ll1_opy_[bstack1l1l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧჀ")])
        else:
            bstack1lll11lll_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11111ll1l1_opy_,
                                                        args=(self.bstack11111l1111_opy_, bstack1ll11ll1l1_opy_, bstack1llllllll1l_opy_)))
            bstack111111l111_opy_ = 1
        i = 0
        for t in bstack1lll11lll_opy_:
            os.environ[bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬჁ")] = str(i)
            if bstack1l1l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩჂ") in self.bstack11111l1ll1_opy_:
                os.environ[bstack1l1l11l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨჃ")] = json.dumps(self.bstack11111l1ll1_opy_[bstack1l1l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫჄ")][i % bstack111111l111_opy_])
            i += 1
            t.start()
        for t in bstack1lll11lll_opy_:
            t.join()
        return list(bstack1llllllll1l_opy_)
    @staticmethod
    def bstack111l11111_opy_(driver, bstack11111l1l11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭Ⴥ"), None)
        if item and getattr(item, bstack1l1l11l_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬ჆"), None) and not getattr(item, bstack1l1l11l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭Ⴧ"), False):
            logger.info(
                bstack1l1l11l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦ჈"))
            bstack11111l11l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11ll1lllll_opy_.bstack1lll11l111_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack111111ll1l_opy_(self):
        bstack1l1l11l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡴࡰࠢࡥࡩࠥ࡫ࡸࡦࡥࡸࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ჉")
        try:
            from browserstack_sdk.bstack1111l111l1_opy_ import bstack11111llll1_opy_
            bstack11111ll111_opy_ = bstack11111llll1_opy_(bstack1111l1111l_opy_=self.bstack11111l1111_opy_)
            if not bstack11111ll111_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ჊"), False):
                self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡖࡨࡷࡹࠦࡦࡪ࡮ࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧ჋").format(bstack11111ll111_opy_.get(bstack1l1l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ჌"), bstack1l1l11l_opy_ (u"࡙ࠪࡳࡱ࡮ࡰࡹࡱࠤࡪࡸࡲࡰࡴࠪჍ"))))
                return []
            test_files = bstack11111ll111_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠨ჎"), [])
            count = bstack11111ll111_opy_.get(bstack1l1l11l_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫ჏"), 0)
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡃࡰ࡮࡯ࡩࡨࡺࡥࡥࠢࡾࢁࠥࡺࡥࡴࡶࡶࠤ࡮ࡴࠠࡼࡿࠣࡪ࡮ࡲࡥࡴࠤა").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱ࠾ࠥࢁࡽࠣბ").format(e))
            return []
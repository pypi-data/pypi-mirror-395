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
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1111l1_opy_,
    bstack1lllll1ll11_opy_,
)
from bstack_utils.helper import  bstack111111l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1lll1ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lll1ll_opy_, bstack1lll1l11111_opy_, bstack1ll1lll111l_opy_, bstack1ll1l111l1l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1ll1l1l1l_opy_ import bstack111l11l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111lll_opy_ import bstack1ll1llll111_opy_
from bstack_utils.percy import bstack11l1111ll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll11l1111_opy_(bstack1lll1llll1l_opy_):
    def __init__(self, bstack1l1l1111l11_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1111l11_opy_ = bstack1l1l1111l11_opy_
        self.percy = bstack11l1111ll_opy_()
        self.bstack11111ll1l_opy_ = bstack111l11l1l_opy_()
        self.bstack1l1l111l1ll_opy_()
        bstack1lll1ll11ll_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll111l1_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1l1l111ll1l_opy_)
        TestFramework.bstack1ll1111ll1l_opy_((bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.POST), self.bstack1ll1111ll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1111_opy_(self, instance: bstack1lllll1ll11_opy_, driver: object):
        bstack1l1l1ll1l1l_opy_ = TestFramework.bstack1llll111lll_opy_(instance.context)
        for t in bstack1l1l1ll1l1l_opy_:
            bstack1l1ll11ll1l_opy_ = TestFramework.bstack1llll11ll11_opy_(t, bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll11ll1l_opy_) or instance == driver:
                return t
    def bstack1l1l111ll1l_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll1ll11ll_opy_.bstack1ll11111l1l_opy_(method_name):
                return
            platform_index = f.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1llll1lll_opy_, 0)
            bstack1l1l1l1lll1_opy_ = self.bstack1l1l1ll1111_opy_(instance, driver)
            bstack1l1l111ll11_opy_ = TestFramework.bstack1llll11ll11_opy_(bstack1l1l1l1lll1_opy_, TestFramework.bstack1l1l111l111_opy_, None)
            if not bstack1l1l111ll11_opy_:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡦࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡫ࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡹࡴࡢࡴࡷࡩࡩࠨጸ"))
                return
            driver_command = f.bstack1ll1111l1ll_opy_(*args)
            for command in bstack1l11l1l111_opy_:
                if command == driver_command:
                    self.bstack11ll11ll1l_opy_(driver, platform_index)
            bstack1l1l1lll_opy_ = self.percy.bstack111l1111_opy_()
            if driver_command in bstack11ll111l1l_opy_[bstack1l1l1lll_opy_]:
                self.bstack11111ll1l_opy_.bstack111lllll_opy_(bstack1l1l111ll11_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡨࡶࡷࡵࡲࠣጹ"), e)
    def bstack1ll1111ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
        bstack1l1ll11ll1l_opy_ = f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_, [])
        if not bstack1l1ll11ll1l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥጺ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠤࠥጻ"))
            return
        if len(bstack1l1ll11ll1l_opy_) > 1:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጼ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠦࠧጽ"))
        bstack1l1l111l1l1_opy_, bstack1l1l111l11l_opy_ = bstack1l1ll11ll1l_opy_[0]
        driver = bstack1l1l111l1l1_opy_()
        if not driver:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨጾ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠨࠢጿ"))
            return
        bstack1l1l1111ll1_opy_ = {
            TestFramework.bstack1ll11l1l1ll_opy_: bstack1l1l11l_opy_ (u"ࠢࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥፀ"),
            TestFramework.bstack1ll111111l1_opy_: bstack1l1l11l_opy_ (u"ࠣࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦፁ"),
            TestFramework.bstack1l1l111l111_opy_: bstack1l1l11l_opy_ (u"ࠤࡷࡩࡸࡺࠠࡳࡧࡵࡹࡳࠦ࡮ࡢ࡯ࡨࠦፂ")
        }
        bstack1l1l111lll1_opy_ = { key: f.bstack1llll11ll11_opy_(instance, key) for key in bstack1l1l1111ll1_opy_ }
        bstack1l1l11l1111_opy_ = [key for key, value in bstack1l1l111lll1_opy_.items() if not value]
        if bstack1l1l11l1111_opy_:
            for key in bstack1l1l11l1111_opy_:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࠨፃ") + str(key) + bstack1l1l11l_opy_ (u"ࠦࠧፄ"))
            return
        platform_index = f.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1llll1lll_opy_, 0)
        if self.bstack1l1l1111l11_opy_.percy_capture_mode == bstack1l1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢፅ"):
            bstack1lll1lll1l_opy_ = bstack1l1l111lll1_opy_.get(TestFramework.bstack1l1l111l111_opy_) + bstack1l1l11l_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤፆ")
            bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_.bstack1l1llll111l_opy_(EVENTS.bstack1l1l1111lll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1lll1lll1l_opy_,
                bstack1llllll1l1_opy_=bstack1l1l111lll1_opy_[TestFramework.bstack1ll11l1l1ll_opy_],
                bstack1l111ll1l_opy_=bstack1l1l111lll1_opy_[TestFramework.bstack1ll111111l1_opy_],
                bstack1lll111ll_opy_=platform_index
            )
            bstack1lll1ll111l_opy_.end(EVENTS.bstack1l1l1111lll_opy_.value, bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢፇ"), bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨፈ"), True, None, None, None, None, test_name=bstack1lll1lll1l_opy_)
    def bstack11ll11ll1l_opy_(self, driver, platform_index):
        if self.bstack11111ll1l_opy_.bstack1ll1l1ll11_opy_() is True or self.bstack11111ll1l_opy_.capturing() is True:
            return
        self.bstack11111ll1l_opy_.bstack111lllllll_opy_()
        while not self.bstack11111ll1l_opy_.bstack1ll1l1ll11_opy_():
            bstack1l1l111ll11_opy_ = self.bstack11111ll1l_opy_.bstack1ll1l111_opy_()
            self.bstack11l1ll1l1l_opy_(driver, bstack1l1l111ll11_opy_, platform_index)
        self.bstack11111ll1l_opy_.bstack1lll1ll11l_opy_()
    def bstack11l1ll1l1l_opy_(self, driver, bstack1l111llll1_opy_, platform_index, test=None):
        from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
        bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_.bstack1l1llll111l_opy_(EVENTS.bstack1l1lll1ll1_opy_.value)
        if test != None:
            bstack1llllll1l1_opy_ = getattr(test, bstack1l1l11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧፉ"), None)
            bstack1l111ll1l_opy_ = getattr(test, bstack1l1l11l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨፊ"), None)
            PercySDK.screenshot(driver, bstack1l111llll1_opy_, bstack1llllll1l1_opy_=bstack1llllll1l1_opy_, bstack1l111ll1l_opy_=bstack1l111ll1l_opy_, bstack1lll111ll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l111llll1_opy_)
        bstack1lll1ll111l_opy_.end(EVENTS.bstack1l1lll1ll1_opy_.value, bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦፋ"), bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥፌ"), True, None, None, None, None, test_name=bstack1l111llll1_opy_)
    def bstack1l1l111l1ll_opy_(self):
        os.environ[bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫፍ")] = str(self.bstack1l1l1111l11_opy_.success)
        os.environ[bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫፎ")] = str(self.bstack1l1l1111l11_opy_.percy_capture_mode)
        self.percy.bstack1l1l1111l1l_opy_(self.bstack1l1l1111l11_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l111llll_opy_(self.bstack1l1l1111l11_opy_.percy_build_id)
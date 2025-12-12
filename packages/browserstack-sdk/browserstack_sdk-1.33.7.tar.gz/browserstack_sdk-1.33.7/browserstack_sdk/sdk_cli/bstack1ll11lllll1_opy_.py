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
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import bstack1lllll1ll11_opy_, bstack1lllll1l111_opy_, bstack1llll1111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111lll_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1lll1ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lll1ll_opy_, bstack1lll1l11111_opy_, bstack1ll1lll111l_opy_, bstack1ll1l111l1l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1l11lll11_opy_, bstack1l1l1l111ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1l1l111l1_opy_ = [bstack1l1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ኶"), bstack1l1l11l_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥ኷"), bstack1l1l11l_opy_ (u"ࠦࡨࡵ࡮ࡧ࡫ࡪࠦኸ"), bstack1l1l11l_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࠨኹ"), bstack1l1l11l_opy_ (u"ࠨࡰࡢࡶ࡫ࠦኺ")]
bstack1l1l11l1l11_opy_ = bstack1l1l1l111ll_opy_()
bstack1l1l1llllll_opy_ = bstack1l1l11l_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢኻ")
bstack1l1l11llll1_opy_ = {
    bstack1l1l11l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡋࡷࡩࡲࠨኼ"): bstack1l1l1l111l1_opy_,
    bstack1l1l11l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡓࡥࡨࡱࡡࡨࡧࠥኽ"): bstack1l1l1l111l1_opy_,
    bstack1l1l11l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡑࡴࡪࡵ࡭ࡧࠥኾ"): bstack1l1l1l111l1_opy_,
    bstack1l1l11l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡈࡲࡡࡴࡵࠥ኿"): bstack1l1l1l111l1_opy_,
    bstack1l1l11l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡌࡵ࡯ࡥࡷ࡭ࡴࡴࠢዀ"): bstack1l1l1l111l1_opy_
    + [
        bstack1l1l11l_opy_ (u"ࠨ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬࡯ࡣࡰࡩࠧ዁"),
        bstack1l1l11l_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤዂ"),
        bstack1l1l11l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦ࡫ࡱࡪࡴࠨዃ"),
        bstack1l1l11l_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦዄ"),
        bstack1l1l11l_opy_ (u"ࠥࡧࡦࡲ࡬ࡴࡲࡨࡧࠧዅ"),
        bstack1l1l11l_opy_ (u"ࠦࡨࡧ࡬࡭ࡱࡥ࡮ࠧ዆"),
        bstack1l1l11l_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦ዇"),
        bstack1l1l11l_opy_ (u"ࠨࡳࡵࡱࡳࠦወ"),
        bstack1l1l11l_opy_ (u"ࠢࡥࡷࡵࡥࡹ࡯࡯࡯ࠤዉ"),
        bstack1l1l11l_opy_ (u"ࠣࡹ࡫ࡩࡳࠨዊ"),
    ],
    bstack1l1l11l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥ࡮ࡴ࠮ࡔࡧࡶࡷ࡮ࡵ࡮ࠣዋ"): [bstack1l1l11l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡲࡤࡸ࡭ࠨዌ"), bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡩࡥ࡮ࡲࡥࡥࠤው"), bstack1l1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡶࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠨዎ"), bstack1l1l11l_opy_ (u"ࠨࡩࡵࡧࡰࡷࠧዏ")],
    bstack1l1l11l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡤࡱࡱࡪ࡮࡭࠮ࡄࡱࡱࡪ࡮࡭ࠢዐ"): [bstack1l1l11l_opy_ (u"ࠣ࡫ࡱࡺࡴࡩࡡࡵ࡫ࡲࡲࡤࡶࡡࡳࡣࡰࡷࠧዑ"), bstack1l1l11l_opy_ (u"ࠤࡤࡶ࡬ࡹࠢዒ")],
    bstack1l1l11l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳ࡌࡩࡹࡶࡸࡶࡪࡊࡥࡧࠤዓ"): [bstack1l1l11l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥዔ"), bstack1l1l11l_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨዕ"), bstack1l1l11l_opy_ (u"ࠨࡦࡶࡰࡦࠦዖ"), bstack1l1l11l_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢ዗"), bstack1l1l11l_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥዘ"), bstack1l1l11l_opy_ (u"ࠤ࡬ࡨࡸࠨዙ")],
    bstack1l1l11l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳࡙ࡵࡣࡔࡨࡵࡺ࡫ࡳࡵࠤዚ"): [bstack1l1l11l_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤዛ"), bstack1l1l11l_opy_ (u"ࠧࡶࡡࡳࡣࡰࠦዜ"), bstack1l1l11l_opy_ (u"ࠨࡰࡢࡴࡤࡱࡤ࡯࡮ࡥࡧࡻࠦዝ")],
    bstack1l1l11l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡳࡷࡱࡲࡪࡸ࠮ࡄࡣ࡯ࡰࡎࡴࡦࡰࠤዞ"): [bstack1l1l11l_opy_ (u"ࠣࡹ࡫ࡩࡳࠨዟ"), bstack1l1l11l_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࠤዠ")],
    bstack1l1l11l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡔ࡯ࡥࡧࡎࡩࡾࡽ࡯ࡳࡦࡶࠦዡ"): [bstack1l1l11l_opy_ (u"ࠦࡳࡵࡤࡦࠤዢ"), bstack1l1l11l_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧዣ")],
    bstack1l1l11l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡏࡤࡶࡰࠨዤ"): [bstack1l1l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧዥ"), bstack1l1l11l_opy_ (u"ࠣࡣࡵ࡫ࡸࠨዦ"), bstack1l1l11l_opy_ (u"ࠤ࡮ࡻࡦࡸࡧࡴࠤዧ")],
}
_1l1ll1l1l11_opy_ = set()
class bstack1lll111l1ll_opy_(bstack1lll1llll1l_opy_):
    bstack1l1l1l1l11l_opy_ = bstack1l1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡨࡪࡪࡸࡲࡦࡦࠥየ")
    bstack1l1l1l1llll_opy_ = bstack1l1l11l_opy_ (u"ࠦࡎࡔࡆࡐࠤዩ")
    bstack1l1l1lll1l1_opy_ = bstack1l1l11l_opy_ (u"ࠧࡋࡒࡓࡑࡕࠦዪ")
    bstack1l1ll1l111l_opy_: Callable
    bstack1l1ll1l11ll_opy_: Callable
    def __init__(self, bstack1ll1ll111ll_opy_, bstack1lll11lll1l_opy_):
        super().__init__()
        self.bstack1ll11l11l11_opy_ = bstack1lll11lll1l_opy_
        if os.getenv(bstack1l1l11l_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡕ࠱࠲࡛ࠥያ"), bstack1l1l11l_opy_ (u"ࠢ࠲ࠤዬ")) != bstack1l1l11l_opy_ (u"ࠣ࠳ࠥይ") or not self.is_enabled():
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠤࠥዮ") + str(self.__class__.__name__) + bstack1l1l11l_opy_ (u"ࠥࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠨዯ"))
            return
        TestFramework.bstack1ll1111ll1l_opy_((bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.PRE), self.bstack1ll11l111l1_opy_)
        TestFramework.bstack1ll1111ll1l_opy_((bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.POST), self.bstack1ll1111ll11_opy_)
        for event in bstack1lll1lll1ll_opy_:
            for state in bstack1ll1lll111l_opy_:
                TestFramework.bstack1ll1111ll1l_opy_((event, state), self.bstack1l1l11l1ll1_opy_)
        bstack1ll1ll111ll_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll111l1_opy_, bstack1llll1111l1_opy_.POST), self.bstack1l1l11ll111_opy_)
        self.bstack1l1ll1l111l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1ll1l1lll_opy_(bstack1lll111l1ll_opy_.bstack1l1l1l1llll_opy_, self.bstack1l1ll1l111l_opy_)
        self.bstack1l1ll1l11ll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1ll1l1lll_opy_(bstack1lll111l1ll_opy_.bstack1l1l1lll1l1_opy_, self.bstack1l1ll1l11ll_opy_)
        self.bstack1l1l1ll11ll_opy_ = builtins.print
        builtins.print = self.bstack1l1ll1l1111_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1l1lll111_opy_() and instance:
            bstack1l1l1ll11l1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1llll1l1ll1_opy_
            if test_framework_state == bstack1lll1lll1ll_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll1lll1ll_opy_.LOG:
                bstack1l11lll11_opy_ = datetime.now()
                entries = f.bstack1l1l1l11lll_opy_(instance, bstack1llll1l1ll1_opy_)
                if entries:
                    self.bstack1l1ll111ll1_opy_(instance, entries)
                    instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࠦደ"), datetime.now() - bstack1l11lll11_opy_)
                    f.bstack1l1l1l1l1ll_opy_(instance, bstack1llll1l1ll1_opy_)
                instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣዱ"), datetime.now() - bstack1l1l1ll11l1_opy_)
                return # bstack1l1ll1l1l1l_opy_ not send this event with the bstack1l1ll11l111_opy_ bstack1l1l11l1l1l_opy_
            elif (
                test_framework_state == bstack1lll1lll1ll_opy_.TEST
                and test_hook_state == bstack1ll1lll111l_opy_.POST
                and not f.bstack1llll1ll1l1_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_)
            ):
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠨࡤࡳࡱࡳࡴ࡮ࡴࡧࠡࡦࡸࡩࠥࡺ࡯ࠡ࡮ࡤࡧࡰࠦ࡯ࡧࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࠦዲ") + str(TestFramework.bstack1llll1ll1l1_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_)) + bstack1l1l11l_opy_ (u"ࠢࠣዳ"))
                f.bstack1llll11lll1_opy_(instance, bstack1lll111l1ll_opy_.bstack1l1l1l1l11l_opy_, True)
                return # bstack1l1ll1l1l1l_opy_ not send this event bstack1l1l11l111l_opy_ bstack1l1l1lllll1_opy_
            elif (
                f.bstack1llll11ll11_opy_(instance, bstack1lll111l1ll_opy_.bstack1l1l1l1l11l_opy_, False)
                and test_framework_state == bstack1lll1lll1ll_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1lll111l_opy_.POST
                and f.bstack1llll1ll1l1_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_)
            ):
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠣ࡫ࡱ࡮ࡪࡩࡴࡪࡰࡪࠤ࡙࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡗࡉࡘ࡚ࠬࠡࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡒࡒࡗ࡙ࠦࠢዴ") + str(TestFramework.bstack1llll1ll1l1_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_)) + bstack1l1l11l_opy_ (u"ࠤࠥድ"))
                self.bstack1l1l11l1ll1_opy_(f, instance, (bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.POST), *args, **kwargs)
            bstack1l11lll11_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1l1l11ll1_opy_ = sorted(
                filter(lambda x: x.get(bstack1l1l11l_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨዶ"), None), data.pop(bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦዷ"), {}).values()),
                key=lambda x: x[bstack1l1l11l_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣዸ")],
            )
            if bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_ in data:
                data.pop(bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_)
            data.update({bstack1l1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨዹ"): bstack1l1l1l11ll1_opy_})
            instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧዺ"), datetime.now() - bstack1l11lll11_opy_)
            bstack1l11lll11_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1l1l1l1l1_opy_)
            instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠣ࡬ࡶࡳࡳࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦዻ"), datetime.now() - bstack1l11lll11_opy_)
            self.bstack1l1l11l1l1l_opy_(instance, bstack1llll1l1ll1_opy_, event_json=event_json)
            instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧዼ"), datetime.now() - bstack1l1l1ll11l1_opy_)
    def bstack1ll11l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
        bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_.bstack1l1llll111l_opy_(EVENTS.bstack1l1l111lll_opy_.value)
        self.bstack1ll11l11l11_opy_.bstack1l1ll111l11_opy_(instance, f, bstack1llll1l1ll1_opy_, *args, **kwargs)
        req = self.bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_(instance, f, bstack1llll1l1ll1_opy_, *args, **kwargs)
        self.bstack1l1ll11lll1_opy_(f, instance, req)
        bstack1lll1ll111l_opy_.end(EVENTS.bstack1l1l111lll_opy_.value, bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥዽ"), bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤዾ"), status=True, failure=None, test_name=None)
    def bstack1ll1111ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        if not f.bstack1llll11ll11_opy_(instance, self.bstack1ll11l11l11_opy_.bstack1l1l1lll11l_opy_, False):
            req = self.bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_(instance, f, bstack1llll1l1ll1_opy_, *args, **kwargs)
            self.bstack1l1ll11lll1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1l1llll1l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l1ll11lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1l11l_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡊࡼࡥ࡯ࡶࠣ࡫ࡗࡖࡃࠡࡥࡤࡰࡱࡀࠠࡏࡱࠣࡺࡦࡲࡩࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠣዿ"))
            return
        bstack1l11lll11_opy_ = datetime.now()
        try:
            r = self.bstack1ll1lllll11_opy_.TestSessionEvent(req)
            instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡧࡹࡩࡳࡺࠢጀ"), datetime.now() - bstack1l11lll11_opy_)
            f.bstack1llll11lll1_opy_(instance, self.bstack1ll11l11l11_opy_.bstack1l1l1lll11l_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1l11l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤጁ") + str(r) + bstack1l1l11l_opy_ (u"ࠣࠤጂ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢጃ") + str(e) + bstack1l1l11l_opy_ (u"ࠥࠦጄ"))
            traceback.print_exc()
            raise e
    def bstack1l1l11ll111_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        _driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        _1l1ll11l11l_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll1ll11ll_opy_.bstack1ll11111l1l_opy_(method_name):
            return
        if f.bstack1ll1111l1ll_opy_(*args) == bstack1lll1ll11ll_opy_.bstack1l1l1ll1ll1_opy_:
            bstack1l1l1ll11l1_opy_ = datetime.now()
            screenshot = result.get(bstack1l1l11l_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥጅ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣ࡭ࡲࡧࡧࡦࠢࡥࡥࡸ࡫࠶࠵ࠢࡶࡸࡷࠨጆ"))
                return
            bstack1l1l1l1lll1_opy_ = self.bstack1l1l1ll1111_opy_(instance)
            if bstack1l1l1l1lll1_opy_:
                entry = bstack1ll1l111l1l_opy_(TestFramework.bstack1l1l11ll11l_opy_, screenshot)
                self.bstack1l1ll111ll1_opy_(bstack1l1l1l1lll1_opy_, [entry])
                instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡥࡹࡧࡦࡹࡹ࡫ࠢጇ"), datetime.now() - bstack1l1l1ll11l1_opy_)
            else:
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠢࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡴࡦࡵࡷࠤ࡫ࡵࡲࠡࡹ࡫࡭ࡨ࡮ࠠࡵࡪ࡬ࡷࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡺࡥࡸࠦࡴࡢ࡭ࡨࡲࠥࡨࡹࠡࡦࡵ࡭ࡻ࡫ࡲ࠾ࠢࡾࢁࠧገ").format(instance.ref()))
        event = {}
        bstack1l1l1l1lll1_opy_ = self.bstack1l1l1ll1111_opy_(instance)
        if bstack1l1l1l1lll1_opy_:
            self.bstack1l1l1l11l1l_opy_(event, bstack1l1l1l1lll1_opy_)
            if event.get(bstack1l1l11l_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨጉ")):
                self.bstack1l1ll111ll1_opy_(bstack1l1l1l1lll1_opy_, event[bstack1l1l11l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢጊ")])
            else:
                self.logger.debug(bstack1l1l11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡯ࡳ࡬ࡹࠠࡧࡱࡵࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡧࡹࡩࡳࡺࠢጋ"))
    @measure(event_name=EVENTS.bstack1l1ll111l1l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l1ll111ll1_opy_(
        self,
        bstack1l1l1l1lll1_opy_: bstack1lll1l11111_opy_,
        entries: List[bstack1ll1l111l1l_opy_],
    ):
        self.bstack1ll111l111l_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll11ll11_opy_(bstack1l1l1l1lll1_opy_, TestFramework.bstack1l1llll1lll_opy_)
        req.execution_context.hash = str(bstack1l1l1l1lll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l1lll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l1lll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llll11ll11_opy_(bstack1l1l1l1lll1_opy_, TestFramework.bstack1ll11l11111_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llll11ll11_opy_(bstack1l1l1l1lll1_opy_, TestFramework.bstack1l1l11l11l1_opy_)
            log_entry.uuid = TestFramework.bstack1llll11ll11_opy_(bstack1l1l1l1lll1_opy_, TestFramework.bstack1ll111111l1_opy_)
            log_entry.test_framework_state = bstack1l1l1l1lll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1l11l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥጌ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1l11l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢግ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l11ll1l1_opy_
                log_entry.file_path = entry.bstack11l111l_opy_
        def bstack1l1l1l1111l_opy_():
            bstack1l11lll11_opy_ = datetime.now()
            try:
                self.bstack1ll1lllll11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1l11ll11l_opy_:
                    bstack1l1l1l1lll1_opy_.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥጎ"), datetime.now() - bstack1l11lll11_opy_)
                elif entry.kind == TestFramework.bstack1l1ll11ll11_opy_:
                    bstack1l1l1l1lll1_opy_.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦጏ"), datetime.now() - bstack1l11lll11_opy_)
                else:
                    bstack1l1l1l1lll1_opy_.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠ࡮ࡲ࡫ࠧጐ"), datetime.now() - bstack1l11lll11_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1l11l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢ጑") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lllll1llll_opy_.enqueue(bstack1l1l1l1111l_opy_)
    @measure(event_name=EVENTS.bstack1l1ll11llll_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l1l11l1l1l_opy_(
        self,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        event_json=None,
    ):
        self.bstack1ll111l111l_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l1llll1lll_opy_)
        req.test_framework_name = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1ll11l11111_opy_)
        req.test_framework_version = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_)
        req.test_framework_state = bstack1llll1l1ll1_opy_[0].name
        req.test_hook_state = bstack1llll1l1ll1_opy_[1].name
        started_at = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l1l1l11111_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l1ll11l1ll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1l1l1l1l1_opy_)).encode(bstack1l1l11l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤጒ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1l1l1111l_opy_():
            bstack1l11lll11_opy_ = datetime.now()
            try:
                self.bstack1ll1lllll11_opy_.TestFrameworkEvent(req)
                instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡧࡹࡩࡳࡺࠢጓ"), datetime.now() - bstack1l11lll11_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1l11l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥጔ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lllll1llll_opy_.enqueue(bstack1l1l1l1111l_opy_)
    def bstack1l1l1ll1111_opy_(self, instance: bstack1lllll1ll11_opy_):
        bstack1l1l1ll1l1l_opy_ = TestFramework.bstack1llll111lll_opy_(instance.context)
        for t in bstack1l1l1ll1l1l_opy_:
            bstack1l1ll11ll1l_opy_ = TestFramework.bstack1llll11ll11_opy_(t, bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll11ll1l_opy_):
                return t
    def bstack1l1ll11111l_opy_(self, message):
        self.bstack1l1ll1l111l_opy_(message + bstack1l1l11l_opy_ (u"ࠨ࡜࡯ࠤጕ"))
    def log_error(self, message):
        self.bstack1l1ll1l11ll_opy_(message + bstack1l1l11l_opy_ (u"ࠢ࡝ࡰࠥ጖"))
    def bstack1l1ll1l1lll_opy_(self, level, original_func):
        def bstack1l1ll1111ll_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1l1l11l_opy_ (u"ࠣࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦࠤ጗") in message or bstack1l1l11l_opy_ (u"ࠤ࡞ࡗࡉࡑࡃࡍࡋࡠࠦጘ") in message or bstack1l1l11l_opy_ (u"ࠥ࡟࡜࡫ࡢࡅࡴ࡬ࡺࡪࡸࡍࡰࡦࡸࡰࡪࡣࠢጙ") in message:
                        return return_value
                    bstack1l1l1ll1l1l_opy_ = TestFramework.bstack1l1l11l1lll_opy_()
                    if not bstack1l1l1ll1l1l_opy_:
                        return return_value
                    bstack1l1l1l1lll1_opy_ = next(
                        (
                            instance
                            for instance in bstack1l1l1ll1l1l_opy_
                            if TestFramework.bstack1llll1ll1l1_opy_(instance, TestFramework.bstack1ll111111l1_opy_)
                        ),
                        None,
                    )
                    if not bstack1l1l1l1lll1_opy_:
                        return return_value
                    entry = bstack1ll1l111l1l_opy_(TestFramework.bstack1l1l11ll1ll_opy_, message, level)
                    self.bstack1l1ll111ll1_opy_(bstack1l1l1l1lll1_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l1ll1111ll_opy_
    def bstack1l1ll1l1111_opy_(self):
        def bstack1l1l1llll11_opy_(*args, **kwargs):
            try:
                self.bstack1l1l1ll11ll_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1l1l11l_opy_ (u"ࠫࠥ࠭ጚ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1l1l11l_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨጛ") in message:
                    return
                bstack1l1l1ll1l1l_opy_ = TestFramework.bstack1l1l11l1lll_opy_()
                if not bstack1l1l1ll1l1l_opy_:
                    return
                bstack1l1l1l1lll1_opy_ = next(
                    (
                        instance
                        for instance in bstack1l1l1ll1l1l_opy_
                        if TestFramework.bstack1llll1ll1l1_opy_(instance, TestFramework.bstack1ll111111l1_opy_)
                    ),
                    None,
                )
                if not bstack1l1l1l1lll1_opy_:
                    return
                entry = bstack1ll1l111l1l_opy_(TestFramework.bstack1l1l11ll1ll_opy_, message, bstack1lll111l1ll_opy_.bstack1l1l1l1llll_opy_)
                self.bstack1l1ll111ll1_opy_(bstack1l1l1l1lll1_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l1l1ll11ll_opy_(bstack1lll1l111l1_opy_ (u"ࠨ࡛ࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥ࡞ࠢࡏࡳ࡬ࠦࡣࡢࡲࡷࡹࡷ࡫ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡧࢀࠦጜ"))
                except:
                    pass
        return bstack1l1l1llll11_opy_
    def bstack1l1l1l11l1l_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll1l1l11_opy_
        levels = [bstack1l1l11l_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥጝ"), bstack1l1l11l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧጞ")]
        bstack1l1l11l11ll_opy_ = bstack1l1l11l_opy_ (u"ࠤࠥጟ")
        if instance is not None:
            try:
                bstack1l1l11l11ll_opy_ = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1ll111111l1_opy_)
            except Exception as e:
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡺ࡯ࡤࠡࡨࡵࡳࡲࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣጠ").format(e))
        bstack1l1l1l11l11_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫጡ")]
                bstack1l1ll1111l1_opy_ = os.path.join(bstack1l1l11l1l11_opy_, (bstack1l1l1llllll_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1ll1111l1_opy_):
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡰࡲࡸࠥࡶࡲࡦࡵࡨࡲࡹࠦࡦࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡕࡧࡶࡸࠥࡧ࡮ࡥࠢࡅࡹ࡮ࡲࡤࠡ࡮ࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣጢ").format(bstack1l1ll1111l1_opy_))
                    continue
                file_names = os.listdir(bstack1l1ll1111l1_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1ll1111l1_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll1l1l11_opy_:
                        self.logger.info(bstack1l1l11l_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦጣ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1ll111lll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1ll111lll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l1l11l_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥጤ"):
                                entry = bstack1ll1l111l1l_opy_(
                                    kind=bstack1l1l11l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥጥ"),
                                    message=bstack1l1l11l_opy_ (u"ࠤࠥጦ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l11ll1l1_opy_=file_size,
                                    bstack1l1l1ll1lll_opy_=bstack1l1l11l_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥጧ"),
                                    bstack11l111l_opy_=os.path.abspath(file_path),
                                    bstack1lll1l1ll_opy_=bstack1l1l11l11ll_opy_
                                )
                            elif level == bstack1l1l11l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣጨ"):
                                entry = bstack1ll1l111l1l_opy_(
                                    kind=bstack1l1l11l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢጩ"),
                                    message=bstack1l1l11l_opy_ (u"ࠨࠢጪ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l11ll1l1_opy_=file_size,
                                    bstack1l1l1ll1lll_opy_=bstack1l1l11l_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢጫ"),
                                    bstack11l111l_opy_=os.path.abspath(file_path),
                                    bstack1l1l11lll1l_opy_=bstack1l1l11l11ll_opy_
                                )
                            bstack1l1l1l11l11_opy_.append(entry)
                            _1l1ll1l1l11_opy_.add(abs_path)
                        except Exception as bstack1l1l1l1l111_opy_:
                            self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢጬ").format(bstack1l1l1l1l111_opy_))
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣጭ").format(e))
        event[bstack1l1l11l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣጮ")] = bstack1l1l1l11l11_opy_
class bstack1l1l1l1l1l1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1ll1l11l1_opy_ = set()
        kwargs[bstack1l1l11l_opy_ (u"ࠦࡸࡱࡩࡱ࡭ࡨࡽࡸࠨጯ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll1l1ll1_opy_(obj, self.bstack1l1ll1l11l1_opy_)
def bstack1l1l1ll1l11_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll1l1ll1_opy_(obj, bstack1l1ll1l11l1_opy_=None, max_depth=3):
    if bstack1l1ll1l11l1_opy_ is None:
        bstack1l1ll1l11l1_opy_ = set()
    if id(obj) in bstack1l1ll1l11l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1ll1l11l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1l1l1ll1l_opy_ = TestFramework.bstack1l1ll11l1l1_opy_(obj)
    bstack1l1l1l1ll11_opy_ = next((k.lower() in bstack1l1l1l1ll1l_opy_.lower() for k in bstack1l1l11llll1_opy_.keys()), None)
    if bstack1l1l1l1ll11_opy_:
        obj = TestFramework.bstack1l1ll111111_opy_(obj, bstack1l1l11llll1_opy_[bstack1l1l1l1ll11_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1l11l_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣጰ")):
            keys = getattr(obj, bstack1l1l11l_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤጱ"), [])
        elif hasattr(obj, bstack1l1l11l_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤጲ")):
            keys = getattr(obj, bstack1l1l11l_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥጳ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1l11l_opy_ (u"ࠤࡢࠦጴ"))}
        if not obj and bstack1l1l1l1ll1l_opy_ == bstack1l1l11l_opy_ (u"ࠥࡴࡦࡺࡨ࡭࡫ࡥ࠲ࡕࡵࡳࡪࡺࡓࡥࡹ࡮ࠢጵ"):
            obj = {bstack1l1l11l_opy_ (u"ࠦࡵࡧࡴࡩࠤጶ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1l1ll1l11_opy_(key) or str(key).startswith(bstack1l1l11l_opy_ (u"ࠧࡥࠢጷ")):
            continue
        if value is not None and bstack1l1l1ll1l11_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll1l1ll1_opy_(value, bstack1l1ll1l11l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll1l1ll1_opy_(o, bstack1l1ll1l11l1_opy_, max_depth) for o in value]))
    return result or None
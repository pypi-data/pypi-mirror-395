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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll111111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l11_opy_ import bstack11llll11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1lll1ll_opy_,
    bstack1lll1l11111_opy_,
    bstack1ll1lll111l_opy_,
    bstack11llll111l1_opy_,
    bstack1ll1l111l1l_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1l1l111ll_opy_
from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1lllll1llll_opy_ import bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.utils.bstack1ll1l11l1l1_opy_ import bstack1lll1111l1l_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11l11l1l1l_opy_
bstack1l1l11l1l11_opy_ = bstack1l1l1l111ll_opy_()
bstack1l1111l1111_opy_ = 1.0
bstack1l1l1llllll_opy_ = bstack1l1l11l_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᔾ")
bstack11lll1l1lll_opy_ = bstack1l1l11l_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᔿ")
bstack11lll1l1l1l_opy_ = bstack1l1l11l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᕀ")
bstack11lll1ll11l_opy_ = bstack1l1l11l_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᕁ")
bstack11lll1l1ll1_opy_ = bstack1l1l11l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᕂ")
_1l1ll1l1l11_opy_ = set()
class bstack1ll1l1111l1_opy_(TestFramework):
    bstack1l111l1l1l1_opy_ = bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᕃ")
    bstack11llll11lll_opy_ = bstack1l1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠥᕄ")
    bstack11llll1ll11_opy_ = bstack1l1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠧᕅ")
    bstack1l1111lll1l_opy_ = bstack1l1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠤᕆ")
    bstack1l1111l111l_opy_ = bstack1l1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠦᕇ")
    bstack1l1111lllll_opy_: bool
    bstack1lllll1llll_opy_: bstack1llllll11ll_opy_  = None
    bstack1ll1lllll11_opy_ = None
    bstack11llllllll1_opy_ = [
        bstack1lll1lll1ll_opy_.BEFORE_ALL,
        bstack1lll1lll1ll_opy_.AFTER_ALL,
        bstack1lll1lll1ll_opy_.BEFORE_EACH,
        bstack1lll1lll1ll_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack11lll1ll1l1_opy_: Dict[str, str],
        bstack1l1llll1l1l_opy_: List[str]=[bstack1l1l11l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᕈ")],
        bstack1lllll1llll_opy_: bstack1llllll11ll_opy_=None,
        bstack1ll1lllll11_opy_=None
    ):
        super().__init__(bstack1l1llll1l1l_opy_, bstack11lll1ll1l1_opy_, bstack1lllll1llll_opy_)
        self.bstack1l1111lllll_opy_ = any(bstack1l1l11l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥᕉ") in item.lower() for item in bstack1l1llll1l1l_opy_)
        self.bstack1ll1lllll11_opy_ = bstack1ll1lllll11_opy_
    def track_event(
        self,
        context: bstack11llll111l1_opy_,
        test_framework_state: bstack1lll1lll1ll_opy_,
        test_hook_state: bstack1ll1lll111l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1lll1ll_opy_.TEST or test_framework_state in bstack1ll1l1111l1_opy_.bstack11llllllll1_opy_:
            bstack11llll11l11_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1lll1ll_opy_.NONE:
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࠧᕊ") + str(test_hook_state) + bstack1l1l11l_opy_ (u"ࠧࠨᕋ"))
            return
        if not self.bstack1l1111lllll_opy_:
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡃࠢᕌ") + str(str(self.bstack1l1llll1l1l_opy_)) + bstack1l1l11l_opy_ (u"ࠢࠣᕍ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᕎ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠤࠥᕏ"))
            return
        instance = self.__11llll11ll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡥࡷ࡭ࡳ࠾ࠤᕐ") + str(args) + bstack1l1l11l_opy_ (u"ࠦࠧᕑ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1ll1l1111l1_opy_.bstack11llllllll1_opy_ and test_hook_state == bstack1ll1lll111l_opy_.PRE:
                bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_.bstack1l1llll111l_opy_(EVENTS.bstack11ll1111l1_opy_.value)
                name = str(EVENTS.bstack11ll1111l1_opy_.name)+bstack1l1l11l_opy_ (u"ࠧࡀࠢᕒ")+str(test_framework_state.name)
                TestFramework.bstack1l1111ll1l1_opy_(instance, name, bstack1ll11l1lll1_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࠣࡩࡷࡸ࡯ࡳࠢࡳࡶࡪࡀࠠࡼࡿࠥᕓ").format(e))
        try:
            if not TestFramework.bstack1llll1ll1l1_opy_(instance, TestFramework.bstack11lllll11l1_opy_) and test_hook_state == bstack1ll1lll111l_opy_.PRE:
                test = bstack1ll1l1111l1_opy_.__1l111l1111l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠢ࡭ࡱࡤࡨࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᕔ") + str(test_hook_state) + bstack1l1l11l_opy_ (u"ࠣࠤᕕ"))
            if test_framework_state == bstack1lll1lll1ll_opy_.TEST:
                if test_hook_state == bstack1ll1lll111l_opy_.PRE and not TestFramework.bstack1llll1ll1l1_opy_(instance, TestFramework.bstack1l1l1l11111_opy_):
                    TestFramework.bstack1llll11lll1_opy_(instance, TestFramework.bstack1l1l1l11111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡸࡺࡡࡳࡶࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᕖ") + str(test_hook_state) + bstack1l1l11l_opy_ (u"ࠥࠦᕗ"))
                elif test_hook_state == bstack1ll1lll111l_opy_.POST and not TestFramework.bstack1llll1ll1l1_opy_(instance, TestFramework.bstack1l1ll11l1ll_opy_):
                    TestFramework.bstack1llll11lll1_opy_(instance, TestFramework.bstack1l1ll11l1ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡸ࡫ࡴࠡࡶࡨࡷࡹ࠳ࡥ࡯ࡦࠣࡪࡴࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᕘ") + str(test_hook_state) + bstack1l1l11l_opy_ (u"ࠧࠨᕙ"))
            elif test_framework_state == bstack1lll1lll1ll_opy_.LOG and test_hook_state == bstack1ll1lll111l_opy_.POST:
                bstack1ll1l1111l1_opy_.__11llllll111_opy_(instance, *args)
            elif test_framework_state == bstack1lll1lll1ll_opy_.LOG_REPORT and test_hook_state == bstack1ll1lll111l_opy_.POST:
                self.__1l11111ll11_opy_(instance, *args)
                self.__11llll1l1l1_opy_(instance)
            elif test_framework_state in bstack1ll1l1111l1_opy_.bstack11llllllll1_opy_:
                self.__11lll1lll1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡥࡷࡧࡱࡸࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢᕚ") + str(instance.ref()) + bstack1l1l11l_opy_ (u"ࠢࠣᕛ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack11lll1ll1ll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1ll1l1111l1_opy_.bstack11llllllll1_opy_ and test_hook_state == bstack1ll1lll111l_opy_.POST:
                name = str(EVENTS.bstack11ll1111l1_opy_.name)+bstack1l1l11l_opy_ (u"ࠣ࠼ࠥᕜ")+str(test_framework_state.name)
                bstack1ll11l1lll1_opy_ = TestFramework.bstack11lll1llll1_opy_(instance, name)
                bstack1lll1ll111l_opy_.end(EVENTS.bstack11ll1111l1_opy_.value, bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᕝ"), bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᕞ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᕟ").format(e))
    def bstack1l1l1lll111_opy_(self):
        return self.bstack1l1111lllll_opy_
    def __1l111l11l1l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1l11l_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᕠ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1ll111111_opy_(rep, [bstack1l1l11l_opy_ (u"ࠨࡷࡩࡧࡱࠦᕡ"), bstack1l1l11l_opy_ (u"ࠢࡰࡷࡷࡧࡴࡳࡥࠣᕢ"), bstack1l1l11l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᕣ"), bstack1l1l11l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᕤ"), bstack1l1l11l_opy_ (u"ࠥࡷࡰ࡯ࡰࡱࡧࡧࠦᕥ"), bstack1l1l11l_opy_ (u"ࠦࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠥᕦ")])
        return None
    def __1l11111ll11_opy_(self, instance: bstack1lll1l11111_opy_, *args):
        result = self.__1l111l11l1l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1llllll1ll1_opy_ = None
        if result.get(bstack1l1l11l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᕧ"), None) == bstack1l1l11l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᕨ") and len(args) > 1 and getattr(args[1], bstack1l1l11l_opy_ (u"ࠢࡦࡺࡦ࡭ࡳ࡬࡯ࠣᕩ"), None) is not None:
            failure = [{bstack1l1l11l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᕪ"): [args[1].excinfo.exconly(), result.get(bstack1l1l11l_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᕫ"), None)]}]
            bstack1llllll1ll1_opy_ = bstack1l1l11l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᕬ") if bstack1l1l11l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᕭ") in getattr(args[1].excinfo, bstack1l1l11l_opy_ (u"ࠧࡺࡹࡱࡧࡱࡥࡲ࡫ࠢᕮ"), bstack1l1l11l_opy_ (u"ࠨࠢᕯ")) else bstack1l1l11l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᕰ")
        bstack1l111111lll_opy_ = result.get(bstack1l1l11l_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᕱ"), TestFramework.bstack1l111l1l1ll_opy_)
        if bstack1l111111lll_opy_ != TestFramework.bstack1l111l1l1ll_opy_:
            TestFramework.bstack1llll11lll1_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11111llll_opy_(instance, {
            TestFramework.bstack1l11ll11lll_opy_: failure,
            TestFramework.bstack11llll1l11l_opy_: bstack1llllll1ll1_opy_,
            TestFramework.bstack1l11ll1111l_opy_: bstack1l111111lll_opy_,
        })
    def __11llll11ll1_opy_(
        self,
        context: bstack11llll111l1_opy_,
        test_framework_state: bstack1lll1lll1ll_opy_,
        test_hook_state: bstack1ll1lll111l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1lll1ll_opy_.SETUP_FIXTURE:
            instance = self.__11llll1lll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack11llll1ll1l_opy_ bstack1l11111111l_opy_ this to be bstack1l1l11l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᕲ")
            if test_framework_state == bstack1lll1lll1ll_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l1111l1l1l_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1lll1ll_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1l11l_opy_ (u"ࠥࡲࡴࡪࡥࠣᕳ"), None), bstack1l1l11l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᕴ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1l11l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᕵ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1llll111l1l_opy_(target) if target else None
        return instance
    def __11lll1lll1l_opy_(
        self,
        instance: bstack1lll1l11111_opy_,
        test_framework_state: bstack1lll1lll1ll_opy_,
        test_hook_state: bstack1ll1lll111l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack11llll11l1l_opy_ = TestFramework.bstack1llll11ll11_opy_(instance, bstack1ll1l1111l1_opy_.bstack11llll11lll_opy_, {})
        if not key in bstack11llll11l1l_opy_:
            bstack11llll11l1l_opy_[key] = []
        bstack11llllll1ll_opy_ = TestFramework.bstack1llll11ll11_opy_(instance, bstack1ll1l1111l1_opy_.bstack11llll1ll11_opy_, {})
        if not key in bstack11llllll1ll_opy_:
            bstack11llllll1ll_opy_[key] = []
        bstack1l1111ll111_opy_ = {
            bstack1ll1l1111l1_opy_.bstack11llll11lll_opy_: bstack11llll11l1l_opy_,
            bstack1ll1l1111l1_opy_.bstack11llll1ll11_opy_: bstack11llllll1ll_opy_,
        }
        if test_hook_state == bstack1ll1lll111l_opy_.PRE:
            hook = {
                bstack1l1l11l_opy_ (u"ࠨ࡫ࡦࡻࠥᕶ"): key,
                TestFramework.bstack11llllll11l_opy_: uuid4().__str__(),
                TestFramework.bstack1l1111l1ll1_opy_: TestFramework.bstack1l1111l11ll_opy_,
                TestFramework.bstack11llll1111l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11llll1l111_opy_: [],
                TestFramework.bstack1l1111ll11l_opy_: args[1] if len(args) > 1 else bstack1l1l11l_opy_ (u"ࠧࠨᕷ"),
                TestFramework.bstack1l111111l11_opy_: bstack1lll1111l1l_opy_.bstack1l111l111ll_opy_()
            }
            bstack11llll11l1l_opy_[key].append(hook)
            bstack1l1111ll111_opy_[bstack1ll1l1111l1_opy_.bstack1l1111lll1l_opy_] = key
        elif test_hook_state == bstack1ll1lll111l_opy_.POST:
            bstack11lllllll1l_opy_ = bstack11llll11l1l_opy_.get(key, [])
            hook = bstack11lllllll1l_opy_.pop() if bstack11lllllll1l_opy_ else None
            if hook:
                result = self.__1l111l11l1l_opy_(*args)
                if result:
                    bstack11lllllll11_opy_ = result.get(bstack1l1l11l_opy_ (u"ࠣࡱࡸࡸࡨࡵ࡭ࡦࠤᕸ"), TestFramework.bstack1l1111l11ll_opy_)
                    if bstack11lllllll11_opy_ != TestFramework.bstack1l1111l11ll_opy_:
                        hook[TestFramework.bstack1l1111l1ll1_opy_] = bstack11lllllll11_opy_
                hook[TestFramework.bstack1l1111111ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l111111l11_opy_]= bstack1lll1111l1l_opy_.bstack1l111l111ll_opy_()
                self.bstack1l11111l1l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l11111_opy_, [])
                if logs: self.bstack1l1ll111ll1_opy_(instance, logs)
                bstack11llllll1ll_opy_[key].append(hook)
                bstack1l1111ll111_opy_[bstack1ll1l1111l1_opy_.bstack1l1111l111l_opy_] = key
        TestFramework.bstack1l11111llll_opy_(instance, bstack1l1111ll111_opy_)
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽ࡮ࡩࡾࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡷࡹࡧࡲࡵࡧࡧࡁࢀ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࢂࠦࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࠽ࠣᕹ") + str(bstack11llllll1ll_opy_) + bstack1l1l11l_opy_ (u"ࠥࠦᕺ"))
    def __11llll1lll1_opy_(
        self,
        context: bstack11llll111l1_opy_,
        test_framework_state: bstack1lll1lll1ll_opy_,
        test_hook_state: bstack1ll1lll111l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1ll111111_opy_(args[0], [bstack1l1l11l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᕻ"), bstack1l1l11l_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᕼ"), bstack1l1l11l_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᕽ"), bstack1l1l11l_opy_ (u"ࠢࡪࡦࡶࠦᕾ"), bstack1l1l11l_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᕿ"), bstack1l1l11l_opy_ (u"ࠤࡥࡥࡸ࡫ࡩࡥࠤᖀ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1l11l_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᖁ")) else fixturedef.get(bstack1l1l11l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᖂ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1l11l_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᖃ")) else None
        node = request.node if hasattr(request, bstack1l1l11l_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᖄ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1l11l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᖅ")) else None
        baseid = fixturedef.get(bstack1l1l11l_opy_ (u"ࠣࡤࡤࡷࡪ࡯ࡤࠣᖆ"), None) or bstack1l1l11l_opy_ (u"ࠤࠥᖇ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1l11l_opy_ (u"ࠥࡣࡵࡿࡦࡶࡰࡦ࡭ࡹ࡫࡭ࠣᖈ")):
            target = bstack1ll1l1111l1_opy_.__11lllll11ll_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1l11l_opy_ (u"ࠦࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᖉ")) else None
            if target and not TestFramework.bstack1llll111l1l_opy_(target):
                self.__1l1111l1l1l_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥ࡬ࡡ࡭࡮ࡥࡥࡨࡱࠠࡵࡣࡵ࡫ࡪࡺ࠽ࡼࡶࡤࡶ࡬࡫ࡴࡾࠢࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫࠽ࡼࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࢃࠠ࡯ࡱࡧࡩࡂࢁ࡮ࡰࡦࡨࢁࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᖊ") + str(test_hook_state) + bstack1l1l11l_opy_ (u"ࠨࠢᖋ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡦࡨࡪࡂࢁࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࢀࠤࡸࡩ࡯ࡱࡧࡀࡿࡸࡩ࡯ࡱࡧࢀࠤࡹࡧࡲࡨࡧࡷࡁࠧᖌ") + str(target) + bstack1l1l11l_opy_ (u"ࠣࠤᖍ"))
            return None
        instance = TestFramework.bstack1llll111l1l_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡤࡤࡷࡪ࡯ࡤ࠾ࡽࡥࡥࡸ࡫ࡩࡥࡿࠣࡸࡦࡸࡧࡦࡶࡀࠦᖎ") + str(target) + bstack1l1l11l_opy_ (u"ࠥࠦᖏ"))
            return None
        bstack1l111l1l11l_opy_ = TestFramework.bstack1llll11ll11_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l111l1l1l1_opy_, {})
        if os.getenv(bstack1l1l11l_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡊࡎ࡞ࡔࡖࡔࡈࡗࠧᖐ"), bstack1l1l11l_opy_ (u"ࠧ࠷ࠢᖑ")) == bstack1l1l11l_opy_ (u"ࠨ࠱ࠣᖒ"):
            bstack1l11111l111_opy_ = bstack1l1l11l_opy_ (u"ࠢ࠻ࠤᖓ").join((scope, fixturename))
            bstack1l11111lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l1111l11l1_opy_ = {
                bstack1l1l11l_opy_ (u"ࠣ࡭ࡨࡽࠧᖔ"): bstack1l11111l111_opy_,
                bstack1l1l11l_opy_ (u"ࠤࡷࡥ࡬ࡹࠢᖕ"): bstack1ll1l1111l1_opy_.__1l111l11lll_opy_(request.node),
                bstack1l1l11l_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࠦᖖ"): fixturedef,
                bstack1l1l11l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᖗ"): scope,
                bstack1l1l11l_opy_ (u"ࠧࡺࡹࡱࡧࠥᖘ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lll111l_opy_.POST and callable(getattr(args[-1], bstack1l1l11l_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᖙ"), None)):
                    bstack1l1111l11l1_opy_[bstack1l1l11l_opy_ (u"ࠢࡵࡻࡳࡩࠧᖚ")] = TestFramework.bstack1l1ll11l1l1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lll111l_opy_.PRE:
                bstack1l1111l11l1_opy_[bstack1l1l11l_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᖛ")] = uuid4().__str__()
                bstack1l1111l11l1_opy_[bstack1ll1l1111l1_opy_.bstack11llll1111l_opy_] = bstack1l11111lll1_opy_
            elif test_hook_state == bstack1ll1lll111l_opy_.POST:
                bstack1l1111l11l1_opy_[bstack1ll1l1111l1_opy_.bstack1l1111111ll_opy_] = bstack1l11111lll1_opy_
            if bstack1l11111l111_opy_ in bstack1l111l1l11l_opy_:
                bstack1l111l1l11l_opy_[bstack1l11111l111_opy_].update(bstack1l1111l11l1_opy_)
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡸࡴࡩࡧࡴࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࠥᖜ") + str(bstack1l111l1l11l_opy_[bstack1l11111l111_opy_]) + bstack1l1l11l_opy_ (u"ࠥࠦᖝ"))
            else:
                bstack1l111l1l11l_opy_[bstack1l11111l111_opy_] = bstack1l1111l11l1_opy_
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥ࠾ࡽࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦ࠿ࡾࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡿࠣࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࡃࠢᖞ") + str(len(bstack1l111l1l11l_opy_)) + bstack1l1l11l_opy_ (u"ࠧࠨᖟ"))
        TestFramework.bstack1llll11lll1_opy_(instance, bstack1ll1l1111l1_opy_.bstack1l111l1l1l1_opy_, bstack1l111l1l11l_opy_)
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡬ࡩࡹࡶࡸࡶࡪࡹ࠽ࡼ࡮ࡨࡲ࠭ࡺࡲࡢࡥ࡮ࡩࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠪࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᖠ") + str(instance.ref()) + bstack1l1l11l_opy_ (u"ࠢࠣᖡ"))
        return instance
    def __1l1111l1l1l_opy_(
        self,
        context: bstack11llll111l1_opy_,
        test_framework_state: bstack1lll1lll1ll_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1llll111111_opy_.create_context(target)
        ob = bstack1lll1l11111_opy_(ctx, self.bstack1l1llll1l1l_opy_, self.bstack11lll1ll1l1_opy_, test_framework_state)
        TestFramework.bstack1l11111llll_opy_(ob, {
            TestFramework.bstack1ll11l11111_opy_: context.test_framework_name,
            TestFramework.bstack1l1l11l11l1_opy_: context.test_framework_version,
            TestFramework.bstack1l11111l11l_opy_: [],
            bstack1ll1l1111l1_opy_.bstack1l111l1l1l1_opy_: {},
            bstack1ll1l1111l1_opy_.bstack11llll1ll11_opy_: {},
            bstack1ll1l1111l1_opy_.bstack11llll11lll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llll11lll1_opy_(ob, TestFramework.bstack11lll1lllll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llll11lll1_opy_(ob, TestFramework.bstack1l1llll1lll_opy_, context.platform_index)
        TestFramework.bstack1lllll1l11l_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡦࡸࡽ࠴ࡩࡥ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᖢ") + str(TestFramework.bstack1lllll1l11l_opy_.keys()) + bstack1l1l11l_opy_ (u"ࠤࠥᖣ"))
        return ob
    def bstack1l1l1l11lll_opy_(self, instance: bstack1lll1l11111_opy_, bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_]):
        bstack11llllll1l1_opy_ = (
            bstack1ll1l1111l1_opy_.bstack1l1111lll1l_opy_
            if bstack1llll1l1ll1_opy_[1] == bstack1ll1lll111l_opy_.PRE
            else bstack1ll1l1111l1_opy_.bstack1l1111l111l_opy_
        )
        hook = bstack1ll1l1111l1_opy_.bstack1l1111llll1_opy_(instance, bstack11llllll1l1_opy_)
        entries = hook.get(TestFramework.bstack11llll1l111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l11111l11l_opy_, []))
        return entries
    def bstack1l1l1l1l1ll_opy_(self, instance: bstack1lll1l11111_opy_, bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_]):
        bstack11llllll1l1_opy_ = (
            bstack1ll1l1111l1_opy_.bstack1l1111lll1l_opy_
            if bstack1llll1l1ll1_opy_[1] == bstack1ll1lll111l_opy_.PRE
            else bstack1ll1l1111l1_opy_.bstack1l1111l111l_opy_
        )
        bstack1ll1l1111l1_opy_.bstack1l111l11l11_opy_(instance, bstack11llllll1l1_opy_)
        TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l11111l11l_opy_, []).clear()
    def bstack1l11111l1l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1l11l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸ࡭࡫ࠠࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡯ࡳࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡄࡪࡨࡧࡰࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡭ࡳࡹࡩࡥࡧࠣࢂ࠴࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠴࡛ࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡊࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠮ࠣࡶࡪࡶ࡬ࡢࡥࡨࡷࠥࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧࠦࡩ࡯ࠢ࡬ࡸࡸࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡍ࡫ࠦࡡࠡࡨ࡬ࡰࡪࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡰࡥࡹࡩࡨࡦࡵࠣࡥࠥࡳ࡯ࡥ࡫ࡩ࡭ࡪࡪࠠࡩࡱࡲ࡯࠲ࡲࡥࡷࡧ࡯ࠤ࡫࡯࡬ࡦ࠮ࠣ࡭ࡹࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࠤࡼ࡯ࡴࡩࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡓࡪ࡯࡬ࡰࡦࡸ࡬ࡺ࠮ࠣ࡭ࡹࠦࡰࡳࡱࡦࡩࡸࡹࡥࡴࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡱࡵࡣࡢࡶࡨࡨࠥ࡯࡮ࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡦࡾࠦࡲࡦࡲ࡯ࡥࡨ࡯࡮ࡨࠢࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮࠲ࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡗ࡬ࡪࠦࡣࡳࡧࡤࡸࡪࡪࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡥࡷ࡫ࠠࡢࡦࡧࡩࡩࠦࡴࡰࠢࡷ࡬ࡪࠦࡨࡰࡱ࡮ࠫࡸࠦࠢ࡭ࡱࡪࡷࠧࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫࠻ࠢࡗ࡬ࡪࠦࡥࡷࡧࡱࡸࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭ࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡺ࡯࡬ࡥࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡓࡥࡹ࡮ࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠ࡮ࡱࡱ࡭ࡹࡵࡲࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᖤ")
        global _1l1ll1l1l11_opy_
        platform_index = os.environ[bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᖥ")]
        bstack1l1ll1111l1_opy_ = os.path.join(bstack1l1l11l1l11_opy_, (bstack1l1l1llllll_opy_ + str(platform_index)), bstack11lll1ll11l_opy_)
        if not os.path.exists(bstack1l1ll1111l1_opy_) or not os.path.isdir(bstack1l1ll1111l1_opy_):
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵࡵࠣࡸࡴࠦࡰࡳࡱࡦࡩࡸࡹࠠࡼࡿࠥᖦ").format(bstack1l1ll1111l1_opy_))
            return
        logs = hook.get(bstack1l1l11l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᖧ"), [])
        with os.scandir(bstack1l1ll1111l1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1ll1l1l11_opy_:
                    self.logger.info(bstack1l1l11l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᖨ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1l11l_opy_ (u"ࠣࠤᖩ")
                    log_entry = bstack1ll1l111l1l_opy_(
                        kind=bstack1l1l11l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᖪ"),
                        message=bstack1l1l11l_opy_ (u"ࠥࠦᖫ"),
                        level=bstack1l1l11l_opy_ (u"ࠦࠧᖬ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1l11ll1l1_opy_=entry.stat().st_size,
                        bstack1l1l1ll1lll_opy_=bstack1l1l11l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᖭ"),
                        bstack11l111l_opy_=os.path.abspath(entry.path),
                        bstack11llll1l1ll_opy_=hook.get(TestFramework.bstack11llllll11l_opy_)
                    )
                    logs.append(log_entry)
                    _1l1ll1l1l11_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᖮ")]
        bstack11lllll1l11_opy_ = os.path.join(bstack1l1l11l1l11_opy_, (bstack1l1l1llllll_opy_ + str(platform_index)), bstack11lll1ll11l_opy_, bstack11lll1l1ll1_opy_)
        if not os.path.exists(bstack11lllll1l11_opy_) or not os.path.isdir(bstack11lllll1l11_opy_):
            self.logger.info(bstack1l1l11l_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᖯ").format(bstack11lllll1l11_opy_))
        else:
            self.logger.info(bstack1l1l11l_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᖰ").format(bstack11lllll1l11_opy_))
            with os.scandir(bstack11lllll1l11_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1ll1l1l11_opy_:
                        self.logger.info(bstack1l1l11l_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᖱ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1l11l_opy_ (u"ࠥࠦᖲ")
                        log_entry = bstack1ll1l111l1l_opy_(
                            kind=bstack1l1l11l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᖳ"),
                            message=bstack1l1l11l_opy_ (u"ࠧࠨᖴ"),
                            level=bstack1l1l11l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᖵ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1l11ll1l1_opy_=entry.stat().st_size,
                            bstack1l1l1ll1lll_opy_=bstack1l1l11l_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᖶ"),
                            bstack11l111l_opy_=os.path.abspath(entry.path),
                            bstack1l1l11lll1l_opy_=hook.get(TestFramework.bstack11llllll11l_opy_)
                        )
                        logs.append(log_entry)
                        _1l1ll1l1l11_opy_.add(abs_path)
        hook[bstack1l1l11l_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᖷ")] = logs
    def bstack1l1ll111ll1_opy_(
        self,
        bstack1l1l1l1lll1_opy_: bstack1lll1l11111_opy_,
        entries: List[bstack1ll1l111l1l_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1l11l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᖸ"))
        req.platform_index = TestFramework.bstack1llll11ll11_opy_(bstack1l1l1l1lll1_opy_, TestFramework.bstack1l1llll1lll_opy_)
        req.execution_context.hash = str(bstack1l1l1l1lll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l1lll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l1lll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llll11ll11_opy_(bstack1l1l1l1lll1_opy_, TestFramework.bstack1ll11l11111_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llll11ll11_opy_(bstack1l1l1l1lll1_opy_, TestFramework.bstack1l1l11l11l1_opy_)
            log_entry.uuid = entry.bstack11llll1l1ll_opy_
            log_entry.test_framework_state = bstack1l1l1l1lll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1l11l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᖹ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1l11l_opy_ (u"ࠦࠧᖺ")
            if entry.kind == bstack1l1l11l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᖻ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l11ll1l1_opy_
                log_entry.file_path = entry.bstack11l111l_opy_
        def bstack1l1l1l1111l_opy_():
            bstack1l11lll11_opy_ = datetime.now()
            try:
                self.bstack1ll1lllll11_opy_.LogCreatedEvent(req)
                bstack1l1l1l1lll1_opy_.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᖼ"), datetime.now() - bstack1l11lll11_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1l11l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᖽ").format(str(e)))
                traceback.print_exc()
        self.bstack1lllll1llll_opy_.enqueue(bstack1l1l1l1111l_opy_)
    def __11llll1l1l1_opy_(self, instance) -> None:
        bstack1l1l11l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᖾ")
        bstack1l1111ll111_opy_ = {bstack1l1l11l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᖿ"): bstack1lll1111l1l_opy_.bstack1l111l111ll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11111llll_opy_(instance, bstack1l1111ll111_opy_)
    @staticmethod
    def bstack1l1111llll1_opy_(instance: bstack1lll1l11111_opy_, bstack11llllll1l1_opy_: str):
        bstack1l111111111_opy_ = (
            bstack1ll1l1111l1_opy_.bstack11llll1ll11_opy_
            if bstack11llllll1l1_opy_ == bstack1ll1l1111l1_opy_.bstack1l1111l111l_opy_
            else bstack1ll1l1111l1_opy_.bstack11llll11lll_opy_
        )
        bstack11lllll1l1l_opy_ = TestFramework.bstack1llll11ll11_opy_(instance, bstack11llllll1l1_opy_, None)
        bstack11llll111ll_opy_ = TestFramework.bstack1llll11ll11_opy_(instance, bstack1l111111111_opy_, None) if bstack11lllll1l1l_opy_ else None
        return (
            bstack11llll111ll_opy_[bstack11lllll1l1l_opy_][-1]
            if isinstance(bstack11llll111ll_opy_, dict) and len(bstack11llll111ll_opy_.get(bstack11lllll1l1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111l11l11_opy_(instance: bstack1lll1l11111_opy_, bstack11llllll1l1_opy_: str):
        hook = bstack1ll1l1111l1_opy_.bstack1l1111llll1_opy_(instance, bstack11llllll1l1_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack11llll1l111_opy_, []).clear()
    @staticmethod
    def __11llllll111_opy_(instance: bstack1lll1l11111_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1l11l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡦࡳࡷࡪࡳࠣᗀ"), None)):
            return
        if os.getenv(bstack1l1l11l_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡐࡔࡍࡓࠣᗁ"), bstack1l1l11l_opy_ (u"ࠧ࠷ࠢᗂ")) != bstack1l1l11l_opy_ (u"ࠨ࠱ࠣᗃ"):
            bstack1ll1l1111l1_opy_.logger.warning(bstack1l1l11l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡯࡮ࡨࠢࡦࡥࡵࡲ࡯ࡨࠤᗄ"))
            return
        bstack11llll1llll_opy_ = {
            bstack1l1l11l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᗅ"): (bstack1ll1l1111l1_opy_.bstack1l1111lll1l_opy_, bstack1ll1l1111l1_opy_.bstack11llll11lll_opy_),
            bstack1l1l11l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᗆ"): (bstack1ll1l1111l1_opy_.bstack1l1111l111l_opy_, bstack1ll1l1111l1_opy_.bstack11llll1ll11_opy_),
        }
        for when in (bstack1l1l11l_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᗇ"), bstack1l1l11l_opy_ (u"ࠦࡨࡧ࡬࡭ࠤᗈ"), bstack1l1l11l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᗉ")):
            bstack11lllllllll_opy_ = args[1].get_records(when)
            if not bstack11lllllllll_opy_:
                continue
            records = [
                bstack1ll1l111l1l_opy_(
                    kind=TestFramework.bstack1l1l11ll1ll_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1l11l_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠤᗊ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1l11l_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࠣᗋ")) and r.created
                        else None
                    ),
                )
                for r in bstack11lllllllll_opy_
                if isinstance(getattr(r, bstack1l1l11l_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤᗌ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11111ll1l_opy_, bstack1l111111111_opy_ = bstack11llll1llll_opy_.get(when, (None, None))
            bstack1l11111l1ll_opy_ = TestFramework.bstack1llll11ll11_opy_(instance, bstack1l11111ll1l_opy_, None) if bstack1l11111ll1l_opy_ else None
            bstack11llll111ll_opy_ = TestFramework.bstack1llll11ll11_opy_(instance, bstack1l111111111_opy_, None) if bstack1l11111l1ll_opy_ else None
            if isinstance(bstack11llll111ll_opy_, dict) and len(bstack11llll111ll_opy_.get(bstack1l11111l1ll_opy_, [])) > 0:
                hook = bstack11llll111ll_opy_[bstack1l11111l1ll_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack11llll1l111_opy_ in hook:
                    hook[TestFramework.bstack11llll1l111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l11111l11l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l111l1111l_opy_(test) -> Dict[str, Any]:
        bstack111lll111_opy_ = bstack1ll1l1111l1_opy_.__11lllll11ll_opy_(test.location) if hasattr(test, bstack1l1l11l_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᗍ")) else getattr(test, bstack1l1l11l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᗎ"), None)
        test_name = test.name if hasattr(test, bstack1l1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᗏ")) else None
        bstack11lllll1ll1_opy_ = test.fspath.strpath if hasattr(test, bstack1l1l11l_opy_ (u"ࠧ࡬ࡳࡱࡣࡷ࡬ࠧᗐ")) and test.fspath else None
        if not bstack111lll111_opy_ or not test_name or not bstack11lllll1ll1_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1l11l_opy_ (u"ࠨ࡯ࡣ࡬ࠥᗑ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack11lll1ll111_opy_ = []
        try:
            bstack11lll1ll111_opy_ = bstack11l11l1l1l_opy_.bstack1111l1l11l_opy_(test)
        except:
            bstack1ll1l1111l1_opy_.logger.warning(bstack1l1l11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡶࡨࡷࡹࠦࡳࡤࡱࡳࡩࡸ࠲ࠠࡵࡧࡶࡸࠥࡹࡣࡰࡲࡨࡷࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡲࡦࡵࡲࡰࡻ࡫ࡤࠡ࡫ࡱࠤࡈࡒࡉࠣᗒ"))
        return {
            TestFramework.bstack1ll111111l1_opy_: uuid4().__str__(),
            TestFramework.bstack11lllll11l1_opy_: bstack111lll111_opy_,
            TestFramework.bstack1ll11l1l1ll_opy_: test_name,
            TestFramework.bstack1l1l111l111_opy_: getattr(test, bstack1l1l11l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᗓ"), None),
            TestFramework.bstack1l1111l1lll_opy_: bstack11lllll1ll1_opy_,
            TestFramework.bstack1l1111lll11_opy_: bstack1ll1l1111l1_opy_.__1l111l11lll_opy_(test),
            TestFramework.bstack1l111111l1l_opy_: code,
            TestFramework.bstack1l11ll1111l_opy_: TestFramework.bstack1l111l1l1ll_opy_,
            TestFramework.bstack1l111lll1ll_opy_: bstack111lll111_opy_,
            TestFramework.bstack11lll1l1l11_opy_: bstack11lll1ll111_opy_
        }
    @staticmethod
    def __1l111l11lll_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack1l1l11l_opy_ (u"ࠤࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠢᗔ"), [])
            markers.extend([getattr(m, bstack1l1l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᗕ"), None) for m in own_markers if getattr(m, bstack1l1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᗖ"), None)])
            current = getattr(current, bstack1l1l11l_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᗗ"), None)
        return markers
    @staticmethod
    def __11lllll11ll_opy_(location):
        return bstack1l1l11l_opy_ (u"ࠨ࠺࠻ࠤᗘ").join(filter(lambda x: isinstance(x, str), location))
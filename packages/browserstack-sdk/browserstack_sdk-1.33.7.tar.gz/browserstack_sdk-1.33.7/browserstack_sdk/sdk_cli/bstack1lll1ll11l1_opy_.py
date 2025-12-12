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
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1111l1_opy_,
    bstack1lllll1ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1lll1ll11ll_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll11l111l_opy_(bstack1lll1llll1l_opy_):
    bstack1ll111l1ll1_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1lll1ll11ll_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll111l1_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1l1lll1l111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1l111_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1l1lll11lll_opy_(hub_url):
            if not bstack1lll11l111l_opy_.bstack1ll111l1ll1_opy_:
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠢ࡭ࡱࡦࡥࡱࠦࡳࡦ࡮ࡩ࠱࡭࡫ࡡ࡭ࠢࡩࡰࡴࡽࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥ࡯࡮ࡧࡴࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠦࡨࡶࡤࡢࡹࡷࡲ࠽ࠣኃ") + str(hub_url) + bstack1l1l11l_opy_ (u"ࠣࠤኄ"))
                bstack1lll11l111l_opy_.bstack1ll111l1ll1_opy_ = True
            return
        command_name = f.bstack1ll1111l1ll_opy_(*args)
        bstack1l1lll1ll11_opy_ = f.bstack1l1lll1l1ll_opy_(*args)
        if command_name and command_name.lower() == bstack1l1l11l_opy_ (u"ࠤࡩ࡭ࡳࡪࡥ࡭ࡧࡰࡩࡳࡺࠢኅ") and bstack1l1lll1ll11_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1l1lll1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠥࡹࡸ࡯࡮ࡨࠤኆ"), None), bstack1l1lll1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥኇ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠧࢁࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࢂࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠡࡱࡵࠤࡦࡸࡧࡴ࠰ࡸࡷ࡮ࡴࡧ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡺࡦࡲࡵࡦ࠿ࠥኈ") + str(locator_value) + bstack1l1l11l_opy_ (u"ࠨࠢ኉"))
                return
            def bstack1llll1l11ll_opy_(driver, bstack1l1lll1llll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1l1lll1llll_opy_(driver, *args, **kwargs)
                    response = self.bstack1l1lll1l11l_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l1l11l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳ࠮ࡵࡦࡶ࡮ࡶࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࠥኊ") + str(locator_value) + bstack1l1l11l_opy_ (u"ࠣࠤኋ"))
                    else:
                        self.logger.warning(bstack1l1l11l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵ࠰ࡲࡴ࠳ࡳࡤࡴ࡬ࡴࡹࡀࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࡃࡻ࡭ࡱࡦࡥࡹࡵࡲࡠࡶࡼࡴࡪࢃࠠ࡭ࡱࡦࡥࡹࡵࡲࡠࡸࡤࡰࡺ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥࡾࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࡁࠧኌ") + str(response) + bstack1l1l11l_opy_ (u"ࠥࠦኍ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1l1lll1l1l1_opy_(
                        driver, bstack1l1lll1llll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1llll1l11ll_opy_.__name__ = command_name
            return bstack1llll1l11ll_opy_
    def __1l1lll1l1l1_opy_(
        self,
        driver,
        bstack1l1lll1llll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1l1lll1l11l_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l1l11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡴࡳ࡫ࡪ࡫ࡪࡸࡥࡥ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦ኎") + str(locator_value) + bstack1l1l11l_opy_ (u"ࠧࠨ኏"))
                bstack1l1llll1111_opy_ = self.bstack1l1lll1lll1_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l1l11l_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭ࡩࡧࡤࡰ࡮ࡴࡧ࠮ࡴࡨࡷࡺࡲࡴ࠻ࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡸࡾࡶࡥࡾࠢ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࢀࠤ࡭࡫ࡡ࡭࡫ࡱ࡫ࡤࡸࡥࡴࡷ࡯ࡸࡂࠨነ") + str(bstack1l1llll1111_opy_) + bstack1l1l11l_opy_ (u"ࠢࠣኑ"))
                if bstack1l1llll1111_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l1l11l_opy_ (u"ࠣࡷࡶ࡭ࡳ࡭ࠢኒ"): bstack1l1llll1111_opy_.locator_type,
                            bstack1l1l11l_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣና"): bstack1l1llll1111_opy_.locator_value,
                        }
                    )
                    return bstack1l1lll1llll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l1l11l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡍࡤࡊࡅࡃࡗࡊࠦኔ"), False):
                    self.logger.info(bstack1lll1l111l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡷࡵࡩ࠲࡮ࡥࡢ࡮࡬ࡲ࡬࠳ࡲࡦࡵࡸࡰࡹ࠳࡭ࡪࡵࡶ࡭ࡳ࡭࠺ࠡࡵ࡯ࡩࡪࡶࠨ࠴࠲ࠬࠤࡱ࡫ࡴࡵ࡫ࡱ࡫ࠥࡿ࡯ࡶࠢ࡬ࡲࡸࡶࡥࡤࡶࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡧࡻࡸࡪࡴࡳࡪࡱࡱࠤࡱࡵࡧࡴࠤን"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳࡮ࡰ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠽ࠣኖ") + str(response) + bstack1l1l11l_opy_ (u"ࠨࠢኗ"))
        except Exception as err:
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦኘ") + str(err) + bstack1l1l11l_opy_ (u"ࠣࠤኙ"))
        raise exception
    @measure(event_name=EVENTS.bstack1l1lll1ll1l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l1lll1l11l_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l1l11l_opy_ (u"ࠤ࠳ࠦኚ"),
    ):
        self.bstack1ll111l111l_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l1l11l_opy_ (u"ࠥࠦኛ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1ll1lllll11_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l1l11l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨኜ") + str(r) + bstack1l1l11l_opy_ (u"ࠧࠨኝ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦኞ") + str(e) + bstack1l1l11l_opy_ (u"ࠢࠣኟ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1lll11ll1_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l1lll1lll1_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l1l11l_opy_ (u"ࠣ࠲ࠥአ")):
        self.bstack1ll111l111l_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1ll1lllll11_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l1l11l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦኡ") + str(r) + bstack1l1l11l_opy_ (u"ࠥࠦኢ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤኣ") + str(e) + bstack1l1l11l_opy_ (u"ࠧࠨኤ"))
            traceback.print_exc()
            raise e
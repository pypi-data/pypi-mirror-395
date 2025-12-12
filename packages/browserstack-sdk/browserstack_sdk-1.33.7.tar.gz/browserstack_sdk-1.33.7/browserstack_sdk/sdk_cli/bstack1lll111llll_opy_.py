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
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1111l1_opy_,
    bstack1lllll1ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1lll1ll11ll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
class bstack1ll1ll1l11l_opy_(bstack1lll1llll1l_opy_):
    bstack1l11l1l111l_opy_ = bstack1l1l11l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵࠤᏇ")
    bstack1l11l11llll_opy_ = bstack1l1l11l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦᏈ")
    bstack1l11l1l11ll_opy_ = bstack1l1l11l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦᏉ")
    def __init__(self, bstack1ll1l1ll111_opy_):
        super().__init__()
        bstack1lll1ll11ll_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1llll1ll11l_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1l11l1l1111_opy_)
        bstack1lll1ll11ll_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll111l1_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1l1lll1l111_opy_)
        bstack1lll1ll11ll_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll111l1_opy_, bstack1llll1111l1_opy_.POST), self.bstack1l11l1111ll_opy_)
        bstack1lll1ll11ll_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll111l1_opy_, bstack1llll1111l1_opy_.POST), self.bstack1l11l11l1l1_opy_)
        bstack1lll1ll11ll_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.QUIT, bstack1llll1111l1_opy_.POST), self.bstack1l11l111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1l1111_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l11l_opy_ (u"ࠧࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠢᏊ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            url = None
            try:
                if isinstance(kwargs.get(bstack1l1l11l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤᏋ")), str):
                    url = kwargs.get(bstack1l1l11l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᏌ"))
                elif hasattr(kwargs.get(bstack1l1l11l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᏍ")), bstack1l1l11l_opy_ (u"ࠩࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠪᏎ")):
                    url = kwargs.get(bstack1l1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᏏ"))._client_config.remote_server_addr
                else:
                    url = kwargs.get(bstack1l1l11l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᏐ"))._url
            except Exception as e:
                url = bstack1l1l11l_opy_ (u"ࠬ࠭Ꮡ")
                self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡲ࡭ࠢࡩࡶࡴࡳࠠࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽࢀࠦᏒ").format(e))
            self.logger.info(bstack1l1l11l_opy_ (u"ࠢࡓࡧࡰࡳࡹ࡫ࠠࡔࡧࡵࡺࡪࡸࠠࡂࡦࡧࡶࡪࡹࡳࠡࡤࡨ࡭ࡳ࡭ࠠࡱࡣࡶࡷࡪࡪࠠࡢࡵࠣ࠾ࠥࢁࡽࠣᏓ").format(str(url)))
            self.bstack1l11l1l1l1l_opy_(instance, url, f, kwargs)
            self.logger.info(bstack1l1l11l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁ࠿ࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨᏔ").format(method_name=method_name, platform_index=f.platform_index, args=args, kwargs=kwargs))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
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
        instance, method_name = exec
        if f.bstack1llll11ll11_opy_(instance, bstack1ll1ll1l11l_opy_.bstack1l11l1l111l_opy_, False):
            return
        if not f.bstack1llll1ll1l1_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1llll1lll_opy_):
            return
        platform_index = f.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1llll1lll_opy_)
        if f.bstack1l1llll1ll1_opy_(method_name, *args) and len(args) > 1:
            bstack1l11lll11_opy_ = datetime.now()
            hub_url = bstack1lll1ll11ll_opy_.hub_url(driver)
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦᏕ") + str(hub_url) + bstack1l1l11l_opy_ (u"ࠥࠦᏖ"))
            bstack1l11l11ll11_opy_ = args[1][bstack1l1l11l_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᏗ")] if isinstance(args[1], dict) and bstack1l1l11l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᏘ") in args[1] else None
            bstack1l11l1ll1l1_opy_ = bstack1l1l11l_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦᏙ")
            if isinstance(bstack1l11l11ll11_opy_, dict):
                bstack1l11lll11_opy_ = datetime.now()
                r = self.bstack1l11l11ll1l_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧᏚ"), datetime.now() - bstack1l11lll11_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1l1l11l_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥᏛ") + str(r) + bstack1l1l11l_opy_ (u"ࠤࠥᏜ"))
                        return
                    if r.hub_url:
                        f.bstack1l11l1l1l11_opy_(instance, driver, r.hub_url)
                        f.bstack1llll11lll1_opy_(instance, bstack1ll1ll1l11l_opy_.bstack1l11l1l111l_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1l1l11l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᏝ"), e)
    def bstack1l11l1111ll_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll1ll11ll_opy_.session_id(driver)
            if session_id:
                bstack1l11l11lll1_opy_ = bstack1l1l11l_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨᏞ").format(session_id)
                bstack1lll1ll111l_opy_.mark(bstack1l11l11lll1_opy_)
    def bstack1l11l11l1l1_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llll11ll11_opy_(instance, bstack1ll1ll1l11l_opy_.bstack1l11l11llll_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll1ll11ll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᏟ") + str(hub_url) + bstack1l1l11l_opy_ (u"ࠨࠢᏠ"))
            return
        framework_session_id = bstack1lll1ll11ll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1l1l11l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥᏡ") + str(framework_session_id) + bstack1l1l11l_opy_ (u"ࠣࠤᏢ"))
            return
        if bstack1lll1ll11ll_opy_.bstack1l11l11l111_opy_(*args) == bstack1lll1ll11ll_opy_.bstack1l11l1ll1ll_opy_:
            bstack1l11l111l11_opy_ = bstack1l1l11l_opy_ (u"ࠤࡾࢁ࠿࡫࡮ࡥࠤᏣ").format(framework_session_id)
            bstack1l11l11lll1_opy_ = bstack1l1l11l_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧᏤ").format(framework_session_id)
            bstack1lll1ll111l_opy_.end(
                label=bstack1l1l11l_opy_ (u"ࠦࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠢᏥ"),
                start=bstack1l11l11lll1_opy_,
                end=bstack1l11l111l11_opy_,
                status=True,
                failure=None
            )
            bstack1l11lll11_opy_ = datetime.now()
            r = self.bstack1l11l1llll1_opy_(
                ref,
                f.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1llll1lll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦᏦ"), datetime.now() - bstack1l11lll11_opy_)
            f.bstack1llll11lll1_opy_(instance, bstack1ll1ll1l11l_opy_.bstack1l11l11llll_opy_, r.success)
    def bstack1l11l111lll_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack1llll11ll11_opy_(instance, bstack1ll1ll1l11l_opy_.bstack1l11l1l11ll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll1ll11ll_opy_.session_id(driver)
        hub_url = bstack1lll1ll11ll_opy_.hub_url(driver)
        bstack1l11lll11_opy_ = datetime.now()
        r = self.bstack1l11l1lll11_opy_(
            ref,
            f.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1llll1lll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦᏧ"), datetime.now() - bstack1l11lll11_opy_)
        f.bstack1llll11lll1_opy_(instance, bstack1ll1ll1l11l_opy_.bstack1l11l1l11ll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1lll1l11_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l11lll1l1l_opy_(self, platform_index: int, url: str, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.hub_url = url
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧᏨ") + str(req) + bstack1l1l11l_opy_ (u"ࠣࠤᏩ"))
        try:
            r = self.bstack1ll1lllll11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧᏪ") + str(r.success) + bstack1l1l11l_opy_ (u"ࠥࠦᏫ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᏬ") + str(e) + bstack1l1l11l_opy_ (u"ࠧࠨᏭ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1ll111_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l11l11ll1l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll111l111l_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣᏮ") + str(req) + bstack1l1l11l_opy_ (u"ࠢࠣᏯ"))
        try:
            r = self.bstack1ll1lllll11_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦᏰ") + str(r.success) + bstack1l1l11l_opy_ (u"ࠤࠥᏱ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᏲ") + str(e) + bstack1l1l11l_opy_ (u"ࠦࠧᏳ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l1lll1l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l11l1llll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll111l111l_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࡀࠠࠣᏴ") + str(req) + bstack1l1l11l_opy_ (u"ࠨࠢᏵ"))
        try:
            r = self.bstack1ll1lllll11_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤ᏶") + str(r) + bstack1l1l11l_opy_ (u"ࠣࠤ᏷"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᏸ") + str(e) + bstack1l1l11l_opy_ (u"ࠥࠦᏹ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11l11l1ll_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l11l1lll11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll111l111l_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨᏺ") + str(req) + bstack1l1l11l_opy_ (u"ࠧࠨᏻ"))
        try:
            r = self.bstack1ll1lllll11_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᏼ") + str(r) + bstack1l1l11l_opy_ (u"ࠢࠣᏽ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ᏾") + str(e) + bstack1l1l11l_opy_ (u"ࠤࠥ᏿"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack11lll1l1ll_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1l11l1l1l1l_opy_(self, instance: bstack1lllll1ll11_opy_, url: str, f: bstack1lll1ll11ll_opy_, kwargs):
        bstack1l11l1l1lll_opy_ = version.parse(f.framework_version)
        bstack1l11l111ll1_opy_ = kwargs.get(bstack1l1l11l_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦ᐀"))
        bstack1l11l1ll11l_opy_ = kwargs.get(bstack1l1l11l_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᐁ"))
        bstack1l11lll1lll_opy_ = {}
        bstack1l11l111l1l_opy_ = {}
        bstack1l11l1l11l1_opy_ = None
        bstack1l11l11l11l_opy_ = {}
        if bstack1l11l1ll11l_opy_ is not None or bstack1l11l111ll1_opy_ is not None: # check top level caps
            if bstack1l11l1ll11l_opy_ is not None:
                bstack1l11l11l11l_opy_[bstack1l1l11l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᐂ")] = bstack1l11l1ll11l_opy_
            if bstack1l11l111ll1_opy_ is not None and callable(getattr(bstack1l11l111ll1_opy_, bstack1l1l11l_opy_ (u"ࠨࡴࡰࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᐃ"))):
                bstack1l11l11l11l_opy_[bstack1l1l11l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࡠࡣࡶࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᐄ")] = bstack1l11l111ll1_opy_.to_capabilities()
        response = self.bstack1l11lll1l1l_opy_(f.platform_index, url, instance.ref(), json.dumps(bstack1l11l11l11l_opy_).encode(bstack1l1l11l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᐅ")))
        if response is not None and response.capabilities:
            bstack1l11lll1lll_opy_ = json.loads(response.capabilities.decode(bstack1l1l11l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᐆ")))
            if not bstack1l11lll1lll_opy_: # empty caps bstack1l11llll1l1_opy_ bstack1l1l11111ll_opy_ bstack1l11lll11l1_opy_ bstack1ll1ll1llll_opy_ or error in processing
                return
            bstack1l11l1l11l1_opy_ = f.bstack1ll1ll11ll1_opy_[bstack1l1l11l_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢᐇ")](bstack1l11lll1lll_opy_)
        if bstack1l11l111ll1_opy_ is not None and bstack1l11l1l1lll_opy_ >= version.parse(bstack1l1l11l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᐈ")):
            bstack1l11l111l1l_opy_ = None
        if (
                not bstack1l11l111ll1_opy_ and not bstack1l11l1ll11l_opy_
        ) or (
                bstack1l11l1l1lll_opy_ < version.parse(bstack1l1l11l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᐉ"))
        ):
            bstack1l11l111l1l_opy_ = {}
            bstack1l11l111l1l_opy_.update(bstack1l11lll1lll_opy_)
        self.logger.info(bstack1l11111l1_opy_)
        if os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤᐊ")).lower().__eq__(bstack1l1l11l_opy_ (u"ࠢࡵࡴࡸࡩࠧᐋ")):
            kwargs.update(
                {
                    bstack1l1l11l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦᐌ"): f.bstack1l11l1l1ll1_opy_,
                }
            )
        if bstack1l11l1l1lll_opy_ >= version.parse(bstack1l1l11l_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩᐍ")):
            if bstack1l11l1ll11l_opy_ is not None:
                del kwargs[bstack1l1l11l_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᐎ")]
            kwargs.update(
                {
                    bstack1l1l11l_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧᐏ"): bstack1l11l1l11l1_opy_,
                    bstack1l1l11l_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤᐐ"): True,
                    bstack1l1l11l_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨᐑ"): None,
                }
            )
        elif bstack1l11l1l1lll_opy_ >= version.parse(bstack1l1l11l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᐒ")):
            kwargs.update(
                {
                    bstack1l1l11l_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᐓ"): bstack1l11l111l1l_opy_,
                    bstack1l1l11l_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᐔ"): bstack1l11l1l11l1_opy_,
                    bstack1l1l11l_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᐕ"): True,
                    bstack1l1l11l_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᐖ"): None,
                }
            )
        elif bstack1l11l1l1lll_opy_ >= version.parse(bstack1l1l11l_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬᐗ")):
            kwargs.update(
                {
                    bstack1l1l11l_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᐘ"): bstack1l11l111l1l_opy_,
                    bstack1l1l11l_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦᐙ"): True,
                    bstack1l1l11l_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣᐚ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1l1l11l_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᐛ"): bstack1l11l111l1l_opy_,
                    bstack1l1l11l_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢᐜ"): True,
                    bstack1l1l11l_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦᐝ"): None,
                }
            )
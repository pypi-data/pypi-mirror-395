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
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1111l1_opy_,
    bstack1lllll1ll11_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll1llllll_opy_ import bstack1ll1l111l11_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11111l1_opy_
from bstack_utils.helper import bstack1l1l11lll11_opy_
import threading
import os
import urllib.parse
class bstack1lll1lll111_opy_(bstack1lll1llll1l_opy_):
    def __init__(self, bstack1lll11lll1l_opy_):
        super().__init__()
        bstack1ll1l111l11_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1llll1ll11l_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1l1l111111l_opy_)
        bstack1ll1l111l11_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1llll1ll11l_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1l1l11111l1_opy_)
        bstack1ll1l111l11_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1llll11111l_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1l11lllllll_opy_)
        bstack1ll1l111l11_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll111l1_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1l1l1111111_opy_)
        bstack1ll1l111l11_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1llll1ll11l_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1l11lllll1l_opy_)
        bstack1ll1l111l11_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.QUIT, bstack1llll1111l1_opy_.PRE), self.on_close)
        self.bstack1lll11lll1l_opy_ = bstack1lll11lll1l_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111111l_opy_(
        self,
        f: bstack1ll1l111l11_opy_,
        bstack1l11llll111_opy_: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l11l_opy_ (u"ࠣ࡮ࡤࡹࡳࡩࡨࠣፏ"):
            return
        if not bstack1l1l11lll11_opy_():
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡ࡮ࡤࡹࡳࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨፐ"))
            return
        def wrapped(bstack1l11llll111_opy_, launch, *args, **kwargs):
            response = self.bstack1l11lll1l1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1l11l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩፑ"): True}).encode(bstack1l1l11l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥፒ")))
            if response is not None and response.capabilities:
                if not bstack1l1l11lll11_opy_():
                    browser = launch(bstack1l11llll111_opy_)
                    return browser
                bstack1l11lll1lll_opy_ = json.loads(response.capabilities.decode(bstack1l1l11l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦፓ")))
                if not bstack1l11lll1lll_opy_: # empty caps bstack1l11llll1l1_opy_ bstack1l1l11111ll_opy_ bstack1l11lll11l1_opy_ bstack1ll1ll1llll_opy_ or error in processing
                    return
                bstack1l11lll1l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11lll1lll_opy_))
                f.bstack1llll11lll1_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11lll11ll_opy_, bstack1l11lll1l11_opy_)
                f.bstack1llll11lll1_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11lll1ll1_opy_, bstack1l11lll1lll_opy_)
                browser = bstack1l11llll111_opy_.connect(bstack1l11lll1l11_opy_)
                return browser
        return wrapped
    def bstack1l11lllllll_opy_(
        self,
        f: bstack1ll1l111l11_opy_,
        Connection: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l11l_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨࠣፔ"):
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨፕ"))
            return
        if not bstack1l1l11lll11_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1l1l11l_opy_ (u"ࠨࡲࡤࡶࡦࡳࡳࠨፖ"), {}).get(bstack1l1l11l_opy_ (u"ࠩࡥࡷࡕࡧࡲࡢ࡯ࡶࠫፗ")):
                    bstack1l11lll111l_opy_ = args[0][bstack1l1l11l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥፘ")][bstack1l1l11l_opy_ (u"ࠦࡧࡹࡐࡢࡴࡤࡱࡸࠨፙ")]
                    session_id = bstack1l11lll111l_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࡏࡤࠣፚ"))
                    f.bstack1llll11lll1_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11lllll11_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡪࡩࡴࡲࡤࡸࡨ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࠤ፛"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l11lllll1l_opy_(
        self,
        f: bstack1ll1l111l11_opy_,
        bstack1l11llll111_opy_: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l11l_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࠣ፜"):
            return
        if not bstack1l1l11lll11_opy_():
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤࡱࡱࡲࡪࡩࡴࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨ፝"))
            return
        def wrapped(bstack1l11llll111_opy_, connect, *args, **kwargs):
            response = self.bstack1l11lll1l1l_opy_(f.platform_index, instance.ref(), json.dumps({bstack1l1l11l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ፞"): True}).encode(bstack1l1l11l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ፟")))
            if response is not None and response.capabilities:
                bstack1l11lll1lll_opy_ = json.loads(response.capabilities.decode(bstack1l1l11l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ፠")))
                if not bstack1l11lll1lll_opy_:
                    return
                bstack1l11lll1l11_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l11lll1lll_opy_))
                if bstack1l11lll1lll_opy_.get(bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ፡")):
                    browser = bstack1l11llll111_opy_.bstack1l11llll11l_opy_(bstack1l11lll1l11_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l11lll1l11_opy_
                    return connect(bstack1l11llll111_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1l11111l1_opy_(
        self,
        f: bstack1ll1l111l11_opy_,
        bstack1l1ll1lll11_opy_: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l11l_opy_ (u"ࠨ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠣ።"):
            return
        if not bstack1l1l11lll11_opy_():
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡮ࡦࡹࡢࡴࡦ࡭ࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨ፣"))
            return
        def wrapped(bstack1l1ll1lll11_opy_, bstack1l11llll1ll_opy_, *args, **kwargs):
            contexts = bstack1l1ll1lll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1l11l_opy_ (u"ࠣࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠨ፤") in page.url:
                                return page
                            else:
                                return bstack1l11llll1ll_opy_(bstack1l1ll1lll11_opy_)
                    else:
                        return bstack1l11llll1ll_opy_(bstack1l1ll1lll11_opy_)
        return wrapped
    def bstack1l11lll1l1l_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸ࠿ࠦࠢ፥") + str(req) + bstack1l1l11l_opy_ (u"ࠥࠦ፦"))
        try:
            r = self.bstack1ll1lllll11_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢ፧") + str(r.success) + bstack1l1l11l_opy_ (u"ࠧࠨ፨"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦ፩") + str(e) + bstack1l1l11l_opy_ (u"ࠢࠣ፪"))
            traceback.print_exc()
            raise e
    def bstack1l1l1111111_opy_(
        self,
        f: bstack1ll1l111l11_opy_,
        Connection: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l11l_opy_ (u"ࠣࡡࡶࡩࡳࡪ࡟࡮ࡧࡶࡷࡦ࡭ࡥࡠࡶࡲࡣࡸ࡫ࡲࡷࡧࡵࠦ፫"):
            return
        if not bstack1l1l11lll11_opy_():
            return
        def wrapped(Connection, bstack1l11llllll1_opy_, *args, **kwargs):
            return bstack1l11llllll1_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1ll1l111l11_opy_,
        bstack1l11llll111_opy_: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1l11l_opy_ (u"ࠤࡦࡰࡴࡹࡥࠣ፬"):
            return
        if not bstack1l1l11lll11_opy_():
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢࡦࡰࡴࡹࡥࠡ࡯ࡨࡸ࡭ࡵࡤ࠭ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠨ፭"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped
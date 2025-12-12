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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1llll1ll1ll_opy_,
    bstack1lllll1ll11_opy_,
    bstack1lllll1l111_opy_,
    bstack1llll1111l1_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
from bstack_utils.constants import EVENTS
class bstack1lll1ll11ll_opy_(bstack1llll1ll1ll_opy_):
    bstack1l111ll1l11_opy_ = bstack1l1l11l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᗙ")
    NAME = bstack1l1l11l_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᗚ")
    bstack1l11lll11ll_opy_ = bstack1l1l11l_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࠥᗛ")
    bstack1l11lllll11_opy_ = bstack1l1l11l_opy_ (u"ࠥࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠥᗜ")
    bstack11lll1l111l_opy_ = bstack1l1l11l_opy_ (u"ࠦ࡮ࡴࡰࡶࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᗝ")
    bstack1l11lll1ll1_opy_ = bstack1l1l11l_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦᗞ")
    bstack1l111lll11l_opy_ = bstack1l1l11l_opy_ (u"ࠨࡩࡴࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡪࡸࡦࠧᗟ")
    bstack11lll11l1l1_opy_ = bstack1l1l11l_opy_ (u"ࠢࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᗠ")
    bstack11lll11l1ll_opy_ = bstack1l1l11l_opy_ (u"ࠣࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᗡ")
    bstack1l1llll1lll_opy_ = bstack1l1l11l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᗢ")
    bstack1l11l1ll1ll_opy_ = bstack1l1l11l_opy_ (u"ࠥࡲࡪࡽࡳࡦࡵࡶ࡭ࡴࡴࠢᗣ")
    bstack11lll1l1111_opy_ = bstack1l1l11l_opy_ (u"ࠦ࡬࡫ࡴࠣᗤ")
    bstack1l1l1ll1ll1_opy_ = bstack1l1l11l_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᗥ")
    bstack1l111ll111l_opy_ = bstack1l1l11l_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᗦ")
    bstack1l111l1llll_opy_ = bstack1l1l11l_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᗧ")
    bstack11lll1l11l1_opy_ = bstack1l1l11l_opy_ (u"ࠣࡳࡸ࡭ࡹࠨᗨ")
    bstack11lll11llll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11l1l1ll1_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1ll1ll11ll1_opy_: Any
    bstack1l111ll11ll_opy_: Dict
    def __init__(
        self,
        bstack1l11l1l1ll1_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1ll1ll11ll1_opy_: Dict[str, Any],
        methods=[bstack1l1l11l_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᗩ"), bstack1l1l11l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᗪ"), bstack1l1l11l_opy_ (u"ࠦࡪࡾࡥࡤࡷࡷࡩࠧᗫ"), bstack1l1l11l_opy_ (u"ࠧࡷࡵࡪࡶࠥᗬ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l11l1l1ll1_opy_ = bstack1l11l1l1ll1_opy_
        self.platform_index = platform_index
        self.bstack1llll11l111_opy_(methods)
        self.bstack1ll1ll11ll1_opy_ = bstack1ll1ll11ll1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1llll1ll1ll_opy_.get_data(bstack1lll1ll11ll_opy_.bstack1l11lllll11_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1llll1ll1ll_opy_.get_data(bstack1lll1ll11ll_opy_.bstack1l11lll11ll_opy_, target, strict)
    @staticmethod
    def bstack11lll11ll1l_opy_(target: object, strict=True):
        return bstack1llll1ll1ll_opy_.get_data(bstack1lll1ll11ll_opy_.bstack11lll1l111l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1llll1ll1ll_opy_.get_data(bstack1lll1ll11ll_opy_.bstack1l11lll1ll1_opy_, target, strict)
    @staticmethod
    def bstack1l1ll1ll111_opy_(instance: bstack1lllll1ll11_opy_) -> bool:
        return bstack1llll1ll1ll_opy_.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l111lll11l_opy_, False)
    @staticmethod
    def bstack1ll111ll111_opy_(instance: bstack1lllll1ll11_opy_, default_value=None):
        return bstack1llll1ll1ll_opy_.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l11lll11ll_opy_, default_value)
    @staticmethod
    def bstack1ll11l11l1l_opy_(instance: bstack1lllll1ll11_opy_, default_value=None):
        return bstack1llll1ll1ll_opy_.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l11lll1ll1_opy_, default_value)
    @staticmethod
    def bstack1l1lll11lll_opy_(hub_url: str, bstack11lll1l11ll_opy_=bstack1l1l11l_opy_ (u"ࠨ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠥᗭ")):
        try:
            bstack11lll11lll1_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack11lll11lll1_opy_.endswith(bstack11lll1l11ll_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll11111l1l_opy_(method_name: str):
        return method_name == bstack1l1l11l_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᗮ")
    @staticmethod
    def bstack1l1llll1ll1_opy_(method_name: str, *args):
        return (
            bstack1lll1ll11ll_opy_.bstack1ll11111l1l_opy_(method_name)
            and bstack1lll1ll11ll_opy_.bstack1l11l11l111_opy_(*args) == bstack1lll1ll11ll_opy_.bstack1l11l1ll1ll_opy_
        )
    @staticmethod
    def bstack1ll111llll1_opy_(method_name: str, *args):
        if not bstack1lll1ll11ll_opy_.bstack1ll11111l1l_opy_(method_name):
            return False
        if not bstack1lll1ll11ll_opy_.bstack1l111ll111l_opy_ in bstack1lll1ll11ll_opy_.bstack1l11l11l111_opy_(*args):
            return False
        bstack1l1lll1ll11_opy_ = bstack1lll1ll11ll_opy_.bstack1l1lll1l1ll_opy_(*args)
        return bstack1l1lll1ll11_opy_ and bstack1l1l11l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᗯ") in bstack1l1lll1ll11_opy_ and bstack1l1l11l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᗰ") in bstack1l1lll1ll11_opy_[bstack1l1l11l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥᗱ")]
    @staticmethod
    def bstack1l1llll11l1_opy_(method_name: str, *args):
        if not bstack1lll1ll11ll_opy_.bstack1ll11111l1l_opy_(method_name):
            return False
        if not bstack1lll1ll11ll_opy_.bstack1l111ll111l_opy_ in bstack1lll1ll11ll_opy_.bstack1l11l11l111_opy_(*args):
            return False
        bstack1l1lll1ll11_opy_ = bstack1lll1ll11ll_opy_.bstack1l1lll1l1ll_opy_(*args)
        return (
            bstack1l1lll1ll11_opy_
            and bstack1l1l11l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᗲ") in bstack1l1lll1ll11_opy_
            and bstack1l1l11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡦࡶ࡮ࡶࡴࠣᗳ") in bstack1l1lll1ll11_opy_[bstack1l1l11l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᗴ")]
        )
    @staticmethod
    def bstack1l11l11l111_opy_(*args):
        return str(bstack1lll1ll11ll_opy_.bstack1ll1111l1ll_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1111l1ll_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1l1lll1l1ll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack11l11ll11l_opy_(driver):
        command_executor = getattr(driver, bstack1l1l11l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡠࡧࡻࡩࡨࡻࡴࡰࡴࠥᗵ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l1l11l_opy_ (u"ࠣࡡࡸࡶࡱࠨᗶ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l1l11l_opy_ (u"ࠤࡢࡧࡱ࡯ࡥ࡯ࡶࡢࡧࡴࡴࡦࡪࡩࠥᗷ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l1l11l_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡢࡷࡪࡸࡶࡦࡴࡢࡥࡩࡪࡲࠣᗸ"), None)
        return hub_url
    def bstack1l11l1l1l11_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l1l11l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢᗹ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l1l11l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᗺ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l1l11l_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᗻ")):
                setattr(command_executor, bstack1l1l11l_opy_ (u"ࠢࡠࡷࡵࡰࠧᗼ"), hub_url)
                result = True
        if result:
            self.bstack1l11l1l1ll1_opy_ = hub_url
            bstack1lll1ll11ll_opy_.bstack1llll11lll1_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l11lll11ll_opy_, hub_url)
            bstack1lll1ll11ll_opy_.bstack1llll11lll1_opy_(
                instance, bstack1lll1ll11ll_opy_.bstack1l111lll11l_opy_, bstack1lll1ll11ll_opy_.bstack1l1lll11lll_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l111ll11l1_opy_(bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_]):
        return bstack1l1l11l_opy_ (u"ࠣ࠼ࠥᗽ").join((bstack1lllll1l111_opy_(bstack1llll1l1ll1_opy_[0]).name, bstack1llll1111l1_opy_(bstack1llll1l1ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll1111ll1l_opy_(bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_], callback: Callable):
        bstack1l111l1ll1l_opy_ = bstack1lll1ll11ll_opy_.bstack1l111ll11l1_opy_(bstack1llll1l1ll1_opy_)
        if not bstack1l111l1ll1l_opy_ in bstack1lll1ll11ll_opy_.bstack11lll11llll_opy_:
            bstack1lll1ll11ll_opy_.bstack11lll11llll_opy_[bstack1l111l1ll1l_opy_] = []
        bstack1lll1ll11ll_opy_.bstack11lll11llll_opy_[bstack1l111l1ll1l_opy_].append(callback)
    def bstack1lllll11l1l_opy_(self, instance: bstack1lllll1ll11_opy_, method_name: str, bstack1llll11llll_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l1l11l_opy_ (u"ࠤࡶࡸࡦࡸࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࠤᗾ")):
            return
        cmd = args[0] if method_name == bstack1l1l11l_opy_ (u"ࠥࡩࡽ࡫ࡣࡶࡶࡨࠦᗿ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack11lll11ll11_opy_ = bstack1l1l11l_opy_ (u"ࠦ࠿ࠨᘀ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠨᘁ") + bstack11lll11ll11_opy_, bstack1llll11llll_opy_)
    def bstack1llll1l1111_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1lllll11l11_opy_, bstack1l111l1lll1_opy_ = bstack1llll1l1ll1_opy_
        bstack1l111l1ll1l_opy_ = bstack1lll1ll11ll_opy_.bstack1l111ll11l1_opy_(bstack1llll1l1ll1_opy_)
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠨ࡯࡯ࡡ࡫ࡳࡴࡱ࠺ࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᘂ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠢࠣᘃ"))
        if bstack1lllll11l11_opy_ == bstack1lllll1l111_opy_.QUIT:
            if bstack1l111l1lll1_opy_ == bstack1llll1111l1_opy_.PRE:
                bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_.bstack1l1llll111l_opy_(EVENTS.bstack11lll1l11l_opy_.value)
                bstack1llll1ll1ll_opy_.bstack1llll11lll1_opy_(instance, EVENTS.bstack11lll1l11l_opy_.value, bstack1ll11l1lll1_opy_)
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠣ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠧᘄ").format(instance, method_name, bstack1lllll11l11_opy_, bstack1l111l1lll1_opy_))
        if bstack1lllll11l11_opy_ == bstack1lllll1l111_opy_.bstack1llll1ll11l_opy_:
            if bstack1l111l1lll1_opy_ == bstack1llll1111l1_opy_.POST and not bstack1lll1ll11ll_opy_.bstack1l11lllll11_opy_ in instance.data:
                session_id = getattr(target, bstack1l1l11l_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨᘅ"), None)
                if session_id:
                    instance.data[bstack1lll1ll11ll_opy_.bstack1l11lllll11_opy_] = session_id
        elif (
            bstack1lllll11l11_opy_ == bstack1lllll1l111_opy_.bstack1lllll111l1_opy_
            and bstack1lll1ll11ll_opy_.bstack1l11l11l111_opy_(*args) == bstack1lll1ll11ll_opy_.bstack1l11l1ll1ll_opy_
        ):
            if bstack1l111l1lll1_opy_ == bstack1llll1111l1_opy_.PRE:
                hub_url = bstack1lll1ll11ll_opy_.bstack11l11ll11l_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll1ll11ll_opy_.bstack1l11lll11ll_opy_: hub_url,
                            bstack1lll1ll11ll_opy_.bstack1l111lll11l_opy_: bstack1lll1ll11ll_opy_.bstack1l1lll11lll_opy_(hub_url),
                            bstack1lll1ll11ll_opy_.bstack1l1llll1lll_opy_: int(
                                os.environ.get(bstack1l1l11l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠥᘆ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1l1lll1ll11_opy_ = bstack1lll1ll11ll_opy_.bstack1l1lll1l1ll_opy_(*args)
                bstack11lll11ll1l_opy_ = bstack1l1lll1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᘇ"), None) if bstack1l1lll1ll11_opy_ else None
                if isinstance(bstack11lll11ll1l_opy_, dict):
                    instance.data[bstack1lll1ll11ll_opy_.bstack11lll1l111l_opy_] = copy.deepcopy(bstack11lll11ll1l_opy_)
                    instance.data[bstack1lll1ll11ll_opy_.bstack1l11lll1ll1_opy_] = bstack11lll11ll1l_opy_
            elif bstack1l111l1lll1_opy_ == bstack1llll1111l1_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l1l11l_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᘈ"), dict()).get(bstack1l1l11l_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤᘉ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll1ll11ll_opy_.bstack1l11lllll11_opy_: framework_session_id,
                                bstack1lll1ll11ll_opy_.bstack11lll11l1l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1lllll11l11_opy_ == bstack1lllll1l111_opy_.bstack1lllll111l1_opy_
            and bstack1lll1ll11ll_opy_.bstack1l11l11l111_opy_(*args) == bstack1lll1ll11ll_opy_.bstack11lll1l11l1_opy_
            and bstack1l111l1lll1_opy_ == bstack1llll1111l1_opy_.POST
        ):
            instance.data[bstack1lll1ll11ll_opy_.bstack11lll11l1ll_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l111l1ll1l_opy_ in bstack1lll1ll11ll_opy_.bstack11lll11llll_opy_:
            bstack1l111ll1111_opy_ = None
            for callback in bstack1lll1ll11ll_opy_.bstack11lll11llll_opy_[bstack1l111l1ll1l_opy_]:
                try:
                    bstack1l111ll1l1l_opy_ = callback(self, target, exec, bstack1llll1l1ll1_opy_, result, *args, **kwargs)
                    if bstack1l111ll1111_opy_ == None:
                        bstack1l111ll1111_opy_ = bstack1l111ll1l1l_opy_
                except Exception as e:
                    self.logger.error(bstack1l1l11l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᘊ") + str(e) + bstack1l1l11l_opy_ (u"ࠣࠤᘋ"))
                    traceback.print_exc()
            if bstack1lllll11l11_opy_ == bstack1lllll1l111_opy_.QUIT:
                if bstack1l111l1lll1_opy_ == bstack1llll1111l1_opy_.POST:
                    bstack1ll11l1lll1_opy_ = bstack1llll1ll1ll_opy_.bstack1llll11ll11_opy_(instance, EVENTS.bstack11lll1l11l_opy_.value)
                    if bstack1ll11l1lll1_opy_!=None:
                        bstack1lll1ll111l_opy_.end(EVENTS.bstack11lll1l11l_opy_.value, bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘌ"), bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘍ"), True, None)
            if bstack1l111l1lll1_opy_ == bstack1llll1111l1_opy_.PRE and callable(bstack1l111ll1111_opy_):
                return bstack1l111ll1111_opy_
            elif bstack1l111l1lll1_opy_ == bstack1llll1111l1_opy_.POST and bstack1l111ll1111_opy_:
                return bstack1l111ll1111_opy_
    def bstack1llll11l11l_opy_(
        self, method_name, previous_state: bstack1lllll1l111_opy_, *args, **kwargs
    ) -> bstack1lllll1l111_opy_:
        if method_name == bstack1l1l11l_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᘎ") or method_name == bstack1l1l11l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᘏ"):
            return bstack1lllll1l111_opy_.bstack1llll1ll11l_opy_
        if method_name == bstack1l1l11l_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᘐ"):
            return bstack1lllll1l111_opy_.QUIT
        if method_name == bstack1l1l11l_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᘑ"):
            if previous_state != bstack1lllll1l111_opy_.NONE:
                command_name = bstack1lll1ll11ll_opy_.bstack1l11l11l111_opy_(*args)
                if command_name == bstack1lll1ll11ll_opy_.bstack1l11l1ll1ll_opy_:
                    return bstack1lllll1l111_opy_.bstack1llll1ll11l_opy_
            return bstack1lllll1l111_opy_.bstack1lllll111l1_opy_
        return bstack1lllll1l111_opy_.NONE
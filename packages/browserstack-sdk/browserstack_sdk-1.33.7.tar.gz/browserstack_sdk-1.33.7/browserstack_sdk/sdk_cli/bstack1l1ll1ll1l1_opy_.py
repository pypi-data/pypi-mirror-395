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
    bstack1llll1ll1ll_opy_,
    bstack1lllll1ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1lll1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1llllll_opy_ import bstack1ll1l111l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll1llll1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1llll1l_opy_
import weakref
class bstack1l1ll1lll1l_opy_(bstack1lll1llll1l_opy_):
    bstack1l1lll111l1_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, bstack1lllll1ll11_opy_]]
    pages: Dict[str, Tuple[Callable, bstack1lllll1ll11_opy_]]
    def __init__(self, bstack1l1lll111l1_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack1l1ll1lllll_opy_ = dict()
        self.bstack1l1lll111l1_opy_ = bstack1l1lll111l1_opy_
        self.frameworks = frameworks
        bstack1ll1l111l11_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1llll1ll11l_opy_, bstack1llll1111l1_opy_.POST), self.__1l1lll11l11_opy_)
        if any(bstack1lll1ll11ll_opy_.NAME in f.lower().strip() for f in frameworks):
            bstack1lll1ll11ll_opy_.bstack1ll1111ll1l_opy_(
                (bstack1lllll1l111_opy_.bstack1lllll111l1_opy_, bstack1llll1111l1_opy_.PRE), self.__1l1lll1111l_opy_
            )
            bstack1lll1ll11ll_opy_.bstack1ll1111ll1l_opy_(
                (bstack1lllll1l111_opy_.QUIT, bstack1llll1111l1_opy_.POST), self.__1l1lll111ll_opy_
            )
    def __1l1lll11l11_opy_(
        self,
        f: bstack1ll1l111l11_opy_,
        bstack1l1ll1lll11_opy_: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1l11l_opy_ (u"ࠤࡱࡩࡼࡥࡰࡢࡩࡨࠦከ"):
                return
            contexts = bstack1l1ll1lll11_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1l11l_opy_ (u"ࠥࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠣኩ") in page.url:
                                self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡘࡺ࡯ࡳ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡱࡩࡼࠦࡰࡢࡩࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨኪ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1llll1ll1ll_opy_.bstack1llll11lll1_opy_(instance, self.bstack1l1lll111l1_opy_, True)
                                self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡴࡦ࡭ࡥࡠ࡫ࡱ࡭ࡹࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥካ") + str(instance.ref()) + bstack1l1l11l_opy_ (u"ࠨࠢኬ"))
        except Exception as e:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠ࡯ࡧࡺࠤࡵࡧࡧࡦࠢ࠽ࠦክ"),e)
    def __1l1lll1111l_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1llll1ll1ll_opy_.bstack1llll11ll11_opy_(instance, self.bstack1l1lll111l1_opy_, False):
            return
        if not f.bstack1l1lll11lll_opy_(f.hub_url(driver)):
            self.bstack1l1ll1lllll_opy_[instance.ref()] = weakref.ref(driver), instance
            bstack1llll1ll1ll_opy_.bstack1llll11lll1_opy_(instance, self.bstack1l1lll111l1_opy_, True)
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡡࡢࡳࡳࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠ࡫ࡱ࡭ࡹࡀࠠ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨኮ") + str(instance.ref()) + bstack1l1l11l_opy_ (u"ࠤࠥኯ"))
            return
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        bstack1llll1ll1ll_opy_.bstack1llll11lll1_opy_(instance, self.bstack1l1lll111l1_opy_, True)
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧኰ") + str(instance.ref()) + bstack1l1l11l_opy_ (u"ࠦࠧ኱"))
    def __1l1lll111ll_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llll1l1ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1111l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack1l1lll11l1l_opy_(instance)
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡷࡵࡪࡶ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࠢኲ") + str(instance.ref()) + bstack1l1l11l_opy_ (u"ࠨࠢኳ"))
    def bstack1l1ll1ll11l_opy_(self, context: bstack1llll1llll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1ll11_opy_]]:
        matches = []
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack1l1ll1llll1_opy_(context):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    bstack1lll1ll11ll_opy_.bstack1l1ll1ll111_opy_(data[1])
                    and data[1].bstack1l1ll1llll1_opy_(context)
                    and getattr(data[0](), bstack1l1l11l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦኴ"), False)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll11ll1l_opy_, reverse=reverse)
    def bstack1l1lll11111_opy_(self, context: bstack1llll1llll1_opy_, reverse=True) -> List[Tuple[Callable, bstack1lllll1ll11_opy_]]:
        matches = []
        for data in self.bstack1l1ll1lllll_opy_.values():
            if (
                data[1].bstack1l1ll1llll1_opy_(context)
                and getattr(data[0](), bstack1l1l11l_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧኵ"), False)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1llll11ll1l_opy_, reverse=reverse)
    def bstack1l1ll1ll1ll_opy_(self, instance: bstack1lllll1ll11_opy_) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack1l1lll11l1l_opy_(self, instance: bstack1lllll1ll11_opy_) -> bool:
        if self.bstack1l1ll1ll1ll_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1llll1ll1ll_opy_.bstack1llll11lll1_opy_(instance, self.bstack1l1lll111l1_opy_, False)
            return True
        return False
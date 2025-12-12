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
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1111l1_opy_,
    bstack1llll1ll1ll_opy_,
    bstack1lllll1ll11_opy_,
    bstack1llll1llll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1lll1ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_, bstack1lll1l11111_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1ll1l1_opy_ import bstack1l1ll1lll1l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1l1l11lll11_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1ll1llll111_opy_(bstack1l1ll1lll1l_opy_):
    bstack1l11ll111l1_opy_ = bstack1l1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡷ࡯ࡶࡦࡴࡶࠦᐞ")
    bstack1l1l11lllll_opy_ = bstack1l1l11l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧᐟ")
    bstack1l11ll1l1ll_opy_ = bstack1l1l11l_opy_ (u"ࠢ࡯ࡱࡱࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᐠ")
    bstack1l11ll11ll1_opy_ = bstack1l1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࡳࠣᐡ")
    bstack1l11ll11l11_opy_ = bstack1l1l11l_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡠࡴࡨࡪࡸࠨᐢ")
    bstack1l1l1lll11l_opy_ = bstack1l1l11l_opy_ (u"ࠥࡧࡧࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡥࡵࡩࡦࡺࡥࡥࠤᐣ")
    bstack1l11ll1l111_opy_ = bstack1l1l11l_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢᐤ")
    bstack1l11ll1l1l1_opy_ = bstack1l1l11l_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠥᐥ")
    def __init__(self):
        super().__init__(bstack1l1lll111l1_opy_=self.bstack1l11ll111l1_opy_, frameworks=[bstack1lll1ll11ll_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1111ll1l_opy_((bstack1lll1lll1ll_opy_.BEFORE_EACH, bstack1ll1lll111l_opy_.POST), self.bstack1l111lllll1_opy_)
        TestFramework.bstack1ll1111ll1l_opy_((bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.PRE), self.bstack1ll11l111l1_opy_)
        TestFramework.bstack1ll1111ll1l_opy_((bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.POST), self.bstack1ll1111ll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1ll11ll1l_opy_ = self.bstack1l11l111111_opy_(instance.context)
        if not bstack1l1ll11ll1l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡳࡦࡶࡢࡥࡨࡺࡩࡷࡧࡢࡨࡷ࡯ࡶࡦࡴࡶ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᐦ") + str(bstack1llll1l1ll1_opy_) + bstack1l1l11l_opy_ (u"ࠢࠣᐧ"))
        f.bstack1llll11lll1_opy_(instance, bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_, bstack1l1ll11ll1l_opy_)
        bstack1l111llll1l_opy_ = self.bstack1l11l111111_opy_(instance.context, bstack1l111llll11_opy_=False)
        f.bstack1llll11lll1_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l1ll_opy_, bstack1l111llll1l_opy_)
    def bstack1ll11l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111lllll1_opy_(f, instance, bstack1llll1l1ll1_opy_, *args, **kwargs)
        if not f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l111_opy_, False):
            self.__1l11l1111l1_opy_(f,instance,bstack1llll1l1ll1_opy_)
    def bstack1ll1111ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111lllll1_opy_(f, instance, bstack1llll1l1ll1_opy_, *args, **kwargs)
        if not f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l111_opy_, False):
            self.__1l11l1111l1_opy_(f, instance, bstack1llll1l1ll1_opy_)
        if not f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l1l1_opy_, False):
            self.__1l111ll1ll1_opy_(f, instance, bstack1llll1l1ll1_opy_)
    def bstack1l11l11111l_opy_(
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
        if not f.bstack1l1ll1ll111_opy_(instance):
            return
        if f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l1l1_opy_, False):
            return
        driver.execute_script(
            bstack1l1l11l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂࠨᐨ").format(
                json.dumps(
                    {
                        bstack1l1l11l_opy_ (u"ࠤࡤࡧࡹ࡯࡯࡯ࠤᐩ"): bstack1l1l11l_opy_ (u"ࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨᐪ"),
                        bstack1l1l11l_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢᐫ"): {bstack1l1l11l_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᐬ"): result},
                    }
                )
            )
        )
        f.bstack1llll11lll1_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l1l1_opy_, True)
    def bstack1l11l111111_opy_(self, context: bstack1llll1llll1_opy_, bstack1l111llll11_opy_= True):
        if bstack1l111llll11_opy_:
            bstack1l1ll11ll1l_opy_ = self.bstack1l1ll1ll11l_opy_(context, reverse=True)
        else:
            bstack1l1ll11ll1l_opy_ = self.bstack1l1lll11111_opy_(context, reverse=True)
        return [f for f in bstack1l1ll11ll1l_opy_ if f[1].state != bstack1lllll1l111_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l11l1ll1l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def __1l111ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᐭ")).get(bstack1l1l11l_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᐮ")):
            bstack1l1ll11ll1l_opy_ = f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_, [])
            if not bstack1l1ll11ll1l_opy_:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡵࡨࡸࡤࡧࡣࡵ࡫ࡹࡩࡤࡪࡲࡪࡸࡨࡶࡸࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᐯ") + str(bstack1llll1l1ll1_opy_) + bstack1l1l11l_opy_ (u"ࠤࠥᐰ"))
                return
            driver = bstack1l1ll11ll1l_opy_[0][0]()
            status = f.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l11ll1111l_opy_, None)
            if not status:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᐱ") + str(bstack1llll1l1ll1_opy_) + bstack1l1l11l_opy_ (u"ࠦࠧᐲ"))
                return
            bstack1l11ll1l11l_opy_ = {bstack1l1l11l_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᐳ"): status.lower()}
            bstack1l11ll1ll11_opy_ = f.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l11ll11lll_opy_, None)
            if status.lower() == bstack1l1l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐴ") and bstack1l11ll1ll11_opy_ is not None:
                bstack1l11ll1l11l_opy_[bstack1l1l11l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᐵ")] = bstack1l11ll1ll11_opy_[0][bstack1l1l11l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᐶ")][0] if isinstance(bstack1l11ll1ll11_opy_, list) else str(bstack1l11ll1ll11_opy_)
            driver.execute_script(
                bstack1l1l11l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢᐷ").format(
                    json.dumps(
                        {
                            bstack1l1l11l_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥᐸ"): bstack1l1l11l_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢᐹ"),
                            bstack1l1l11l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣᐺ"): bstack1l11ll1l11l_opy_,
                        }
                    )
                )
            )
            f.bstack1llll11lll1_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l1l1_opy_, True)
    @measure(event_name=EVENTS.bstack11ll111ll1_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def __1l11l1111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠦᐻ")).get(bstack1l1l11l_opy_ (u"ࠢࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤᐼ")):
            test_name = f.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l111lll1ll_opy_, None)
            if not test_name:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᐽ"))
                return
            bstack1l1ll11ll1l_opy_ = f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_, [])
            if not bstack1l1ll11ll1l_opy_:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦᐾ") + str(bstack1llll1l1ll1_opy_) + bstack1l1l11l_opy_ (u"ࠥࠦᐿ"))
                return
            for bstack1l1l111l1l1_opy_, bstack1l111lll1l1_opy_ in bstack1l1ll11ll1l_opy_:
                if not bstack1lll1ll11ll_opy_.bstack1l1ll1ll111_opy_(bstack1l111lll1l1_opy_):
                    continue
                driver = bstack1l1l111l1l1_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack1l1l11l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤᑀ").format(
                        json.dumps(
                            {
                                bstack1l1l11l_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧᑁ"): bstack1l1l11l_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᑂ"),
                                bstack1l1l11l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥᑃ"): {bstack1l1l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᑄ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1llll11lll1_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l111_opy_, True)
    def bstack1l1ll111l11_opy_(
        self,
        instance: bstack1lll1l11111_opy_,
        f: TestFramework,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111lllll1_opy_(f, instance, bstack1llll1l1ll1_opy_, *args, **kwargs)
        bstack1l1ll11ll1l_opy_ = [d for d, _ in f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_, [])]
        if not bstack1l1ll11ll1l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤᑅ"))
            return
        if not bstack1l1l11lll11_opy_():
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᑆ"))
            return
        for bstack1l111llllll_opy_ in bstack1l1ll11ll1l_opy_:
            driver = bstack1l111llllll_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1l11l_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤᑇ") + str(timestamp)
            driver.execute_script(
                bstack1l1l11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥᑈ").format(
                    json.dumps(
                        {
                            bstack1l1l11l_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨᑉ"): bstack1l1l11l_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤᑊ"),
                            bstack1l1l11l_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦᑋ"): {
                                bstack1l1l11l_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᑌ"): bstack1l1l11l_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢᑍ"),
                                bstack1l1l11l_opy_ (u"ࠦࡩࡧࡴࡢࠤᑎ"): data,
                                bstack1l1l11l_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦᑏ"): bstack1l1l11l_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧᑐ")
                            }
                        }
                    )
                )
            )
    def bstack1l1l1lll1ll_opy_(
        self,
        instance: bstack1lll1l11111_opy_,
        f: TestFramework,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l111lllll1_opy_(f, instance, bstack1llll1l1ll1_opy_, *args, **kwargs)
        keys = [
            bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_,
            bstack1ll1llll111_opy_.bstack1l11ll1l1ll_opy_,
        ]
        bstack1l1ll11ll1l_opy_ = []
        for key in keys:
            bstack1l1ll11ll1l_opy_.extend(f.bstack1llll11ll11_opy_(instance, key, []))
        if not bstack1l1ll11ll1l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡲࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤᑑ"))
            return
        if f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l1l1lll11l_opy_, False):
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡆࡆ࡙ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡤࡴࡨࡥࡹ࡫ࡤࠣᑒ"))
            return
        self.bstack1ll111l111l_opy_()
        bstack1l11lll11_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l1llll1lll_opy_)
        req.test_framework_name = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1ll11l11111_opy_)
        req.test_framework_version = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_)
        req.test_framework_state = bstack1llll1l1ll1_opy_[0].name
        req.test_hook_state = bstack1llll1l1ll1_opy_[1].name
        req.test_uuid = TestFramework.bstack1llll11ll11_opy_(instance, TestFramework.bstack1ll111111l1_opy_)
        for bstack1l1l111l1l1_opy_, driver in bstack1l1ll11ll1l_opy_:
            try:
                webdriver = bstack1l1l111l1l1_opy_()
                if webdriver is None:
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠤ࡚ࡩࡧࡊࡲࡪࡸࡨࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡪࡵࠣࡒࡴࡴࡥࠡࠪࡵࡩ࡫࡫ࡲࡦࡰࡦࡩࠥ࡫ࡸࡱ࡫ࡵࡩࡩ࠯ࠢᑓ"))
                    continue
                session = req.automation_sessions.add()
                session.provider = (
                    bstack1l1l11l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤᑔ")
                    if bstack1lll1ll11ll_opy_.bstack1llll11ll11_opy_(driver, bstack1lll1ll11ll_opy_.bstack1l111lll11l_opy_, False)
                    else bstack1l1l11l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥᑕ")
                )
                session.ref = driver.ref()
                session.hub_url = bstack1lll1ll11ll_opy_.bstack1llll11ll11_opy_(driver, bstack1lll1ll11ll_opy_.bstack1l11lll11ll_opy_, bstack1l1l11l_opy_ (u"ࠧࠨᑖ"))
                session.framework_name = driver.framework_name
                session.framework_version = driver.framework_version
                session.framework_session_id = bstack1lll1ll11ll_opy_.bstack1llll11ll11_opy_(driver, bstack1lll1ll11ll_opy_.bstack1l11lllll11_opy_, bstack1l1l11l_opy_ (u"ࠨࠢᑗ"))
                caps = None
                if hasattr(webdriver, bstack1l1l11l_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᑘ")):
                    try:
                        caps = webdriver.capabilities
                        self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡧ࡭ࡷ࡫ࡣࡵ࡮ࡼࠤ࡫ࡸ࡯࡮ࠢࡧࡶ࡮ࡼࡥࡳ࠰ࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᑙ"))
                    except Exception as e:
                        self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡵࡳࡲࠦࡤࡳ࡫ࡹࡩࡷ࠴ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠦࠢᑚ") + str(e) + bstack1l1l11l_opy_ (u"ࠥࠦᑛ"))
                try:
                    bstack1l111lll111_opy_ = json.dumps(caps).encode(bstack1l1l11l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᑜ")) if caps else bstack1l111ll1lll_opy_ (u"ࠧࢁࡽࠣᑝ")
                    req.capabilities = bstack1l111lll111_opy_
                except Exception as e:
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡵࡨࡶ࡮ࡧ࡬ࡪࡼࡨࠤࡨࡧࡰࡴࠢࡩࡳࡷࠦࡲࡦࡳࡸࡩࡸࡺ࠺ࠡࠤᑞ") + str(e) + bstack1l1l11l_opy_ (u"ࠢࠣᑟ"))
            except Exception as e:
                self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡩࡸࡩࡷࡧࡵࠤ࡮ࡺࡥ࡮࠼ࠣࠦᑠ") + str(str(e)) + bstack1l1l11l_opy_ (u"ࠤࠥᑡ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11l1l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll11ll1l_opy_ = f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_, [])
        if not bstack1l1l11lll11_opy_() and len(bstack1l1ll11ll1l_opy_) == 0:
            bstack1l1ll11ll1l_opy_ = f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l1ll_opy_, [])
        if not bstack1l1ll11ll1l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᑢ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠦࠧᑣ"))
            return {}
        if len(bstack1l1ll11ll1l_opy_) > 1:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᑤ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠨࠢᑥ"))
            return {}
        bstack1l1l111l1l1_opy_, bstack1l1l111l11l_opy_ = bstack1l1ll11ll1l_opy_[0]
        driver = bstack1l1l111l1l1_opy_()
        if not driver:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᑦ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠣࠤᑧ"))
            return {}
        capabilities = f.bstack1llll11ll11_opy_(bstack1l1l111l11l_opy_, bstack1lll1ll11ll_opy_.bstack1l11lll1ll1_opy_)
        if not capabilities:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᑨ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠥࠦᑩ"))
            return {}
        return capabilities.get(bstack1l1l11l_opy_ (u"ࠦࡦࡲࡷࡢࡻࡶࡑࡦࡺࡣࡩࠤᑪ"), {})
    def bstack1ll11l11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1ll11ll1l_opy_ = f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l1l11lllll_opy_, [])
        if not bstack1l1l11lll11_opy_() and len(bstack1l1ll11ll1l_opy_) == 0:
            bstack1l1ll11ll1l_opy_ = f.bstack1llll11ll11_opy_(instance, bstack1ll1llll111_opy_.bstack1l11ll1l1ll_opy_, [])
        if not bstack1l1ll11ll1l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᑫ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠨࠢᑬ"))
            return
        if len(bstack1l1ll11ll1l_opy_) > 1:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᑭ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠣࠤᑮ"))
        bstack1l1l111l1l1_opy_, bstack1l1l111l11l_opy_ = bstack1l1ll11ll1l_opy_[0]
        driver = bstack1l1l111l1l1_opy_()
        if not driver:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᑯ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠥࠦᑰ"))
            return
        return driver
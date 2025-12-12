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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1111l1_opy_,
    bstack1llll1ll1ll_opy_,
    bstack1lllll1ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1lll1ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_, bstack1lll1l11111_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111lll_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1ll1_opy_ import bstack1lll1l11lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1llllll_opy_ import bstack1ll1l111l11_opy_
from bstack_utils.helper import bstack1ll111ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
import grpc
import traceback
import json
class bstack1lll1l1llll_opy_(bstack1lll1llll1l_opy_):
    bstack1ll111l1ll1_opy_ = False
    bstack1l1llllll1l_opy_ = bstack1l1l11l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤᇑ")
    bstack1ll1111l111_opy_ = bstack1l1l11l_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᇒ")
    bstack1l1lllll11l_opy_ = bstack1l1l11l_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦᇓ")
    bstack1ll1111111l_opy_ = bstack1l1l11l_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧᇔ")
    bstack1l1llll1l11_opy_ = bstack1l1l11l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤᇕ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1ll111ll_opy_, bstack1lll11lll1l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1ll11l1l11l_opy_ = False
        self.bstack1ll11ll1l11_opy_ = dict()
        self.bstack1ll1111llll_opy_ = False
        self.bstack1l1lllll1l1_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1ll11l11l11_opy_ = bstack1lll11lll1l_opy_
        bstack1ll1ll111ll_opy_.bstack1ll1111ll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll111l1_opy_, bstack1llll1111l1_opy_.PRE), self.bstack1ll111l1lll_opy_)
        TestFramework.bstack1ll1111ll1l_opy_((bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.PRE), self.bstack1ll11l111l1_opy_)
        TestFramework.bstack1ll1111ll1l_opy_((bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.POST), self.bstack1ll1111ll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11ll11ll_opy_(instance, args)
        test_framework = f.bstack1llll11ll11_opy_(instance, TestFramework.bstack1ll11l11111_opy_)
        if self.bstack1ll11l1l11l_opy_:
            self.bstack1ll11ll1l11_opy_[bstack1l1l11l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤᇖ")] = f.bstack1llll11ll11_opy_(instance, TestFramework.bstack1ll111111l1_opy_)
        if bstack1l1l11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᇗ") in instance.bstack1l1llll1l1l_opy_:
            platform_index = f.bstack1llll11ll11_opy_(instance, TestFramework.bstack1l1llll1lll_opy_)
            self.accessibility = self.bstack1ll1111l11l_opy_(tags, self.config[bstack1l1l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᇘ")][platform_index])
        else:
            capabilities = self.bstack1ll11l11l11_opy_.bstack1ll11l1l1l1_opy_(f, instance, bstack1llll1l1ll1_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᇙ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠨࠢᇚ"))
                return
            self.accessibility = self.bstack1ll1111l11l_opy_(tags, capabilities)
        if self.bstack1ll11l11l11_opy_.pages and self.bstack1ll11l11l11_opy_.pages.values():
            bstack1ll11l1ll1l_opy_ = list(self.bstack1ll11l11l11_opy_.pages.values())
            if bstack1ll11l1ll1l_opy_ and isinstance(bstack1ll11l1ll1l_opy_[0], (list, tuple)) and bstack1ll11l1ll1l_opy_[0]:
                bstack1ll111lll11_opy_ = bstack1ll11l1ll1l_opy_[0][0]
                if callable(bstack1ll111lll11_opy_):
                    page = bstack1ll111lll11_opy_()
                    def bstack1llll1l11l_opy_():
                        self.get_accessibility_results(page, bstack1l1l11l_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᇛ"))
                    def bstack1ll111l1111_opy_():
                        self.get_accessibility_results_summary(page, bstack1l1l11l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᇜ"))
                    setattr(page, bstack1l1l11l_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧᇝ"), bstack1llll1l11l_opy_)
                    setattr(page, bstack1l1l11l_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧᇞ"), bstack1ll111l1111_opy_)
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣᇟ") + str(self.accessibility) + bstack1l1l11l_opy_ (u"ࠧࠨᇠ"))
    def bstack1ll111l1lll_opy_(
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
            bstack1l11lll11_opy_ = datetime.now()
            self.bstack1l1lllllll1_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᇡ"), datetime.now() - bstack1l11lll11_opy_)
            if (
                not f.bstack1ll11111l1l_opy_(method_name)
                or f.bstack1ll111llll1_opy_(method_name, *args)
                or f.bstack1l1llll11l1_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llll11ll11_opy_(instance, bstack1lll1l1llll_opy_.bstack1l1lllll11l_opy_, False):
                if not bstack1lll1l1llll_opy_.bstack1ll111l1ll1_opy_:
                    self.logger.warning(bstack1l1l11l_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᇢ") + str(f.platform_index) + bstack1l1l11l_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᇣ"))
                    bstack1lll1l1llll_opy_.bstack1ll111l1ll1_opy_ = True
                return
            bstack1ll11l1l111_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll11l1l111_opy_:
                platform_index = f.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1llll1lll_opy_, 0)
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᇤ") + str(f.framework_name) + bstack1l1l11l_opy_ (u"ࠥࠦᇥ"))
                return
            command_name = f.bstack1ll1111l1ll_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᇦ") + str(method_name) + bstack1l1l11l_opy_ (u"ࠧࠨᇧ"))
                return
            bstack1ll11111111_opy_ = f.bstack1llll11ll11_opy_(instance, bstack1lll1l1llll_opy_.bstack1l1llll1l11_opy_, False)
            if command_name == bstack1l1l11l_opy_ (u"ࠨࡧࡦࡶࠥᇨ") and not bstack1ll11111111_opy_:
                f.bstack1llll11lll1_opy_(instance, bstack1lll1l1llll_opy_.bstack1l1llll1l11_opy_, True)
                bstack1ll11111111_opy_ = True
            if not bstack1ll11111111_opy_ and not self.bstack1ll11l1l11l_opy_:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᇩ") + str(command_name) + bstack1l1l11l_opy_ (u"ࠣࠤᇪ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᇫ") + str(command_name) + bstack1l1l11l_opy_ (u"ࠥࠦᇬ"))
                return
            self.logger.info(bstack1l1l11l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᇭ") + str(command_name) + bstack1l1l11l_opy_ (u"ࠧࠨᇮ"))
            scripts = [(s, bstack1ll11l1l111_opy_[s]) for s in scripts_to_run if s in bstack1ll11l1l111_opy_]
            for script_name, bstack1ll111ll11l_opy_ in scripts:
                try:
                    bstack1l11lll11_opy_ = datetime.now()
                    if script_name == bstack1l1l11l_opy_ (u"ࠨࡳࡤࡣࡱࠦᇯ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                    instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿ࠨᇰ") + script_name, datetime.now() - bstack1l11lll11_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l1l11l_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᇱ"), True):
                        self.logger.warning(bstack1l1l11l_opy_ (u"ࠤࡶ࡯࡮ࡶࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡶࡪࡳࡡࡪࡰ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡹ࠺ࠡࠤᇲ") + str(result) + bstack1l1l11l_opy_ (u"ࠥࠦᇳ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l1l11l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡃࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࠦࡥࡳࡴࡲࡶࡂࠨᇴ") + str(e) + bstack1l1l11l_opy_ (u"ࠧࠨᇵ"))
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧࠣࡩࡷࡸ࡯ࡳ࠿ࠥᇶ") + str(e) + bstack1l1l11l_opy_ (u"ࠢࠣᇷ"))
    def bstack1ll1111ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11ll11ll_opy_(instance, args)
        capabilities = self.bstack1ll11l11l11_opy_.bstack1ll11l1l1l1_opy_(f, instance, bstack1llll1l1ll1_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll1111l11l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᇸ"))
            return
        driver = self.bstack1ll11l11l11_opy_.bstack1ll11l11lll_opy_(f, instance, bstack1llll1l1ll1_opy_, *args, **kwargs)
        test_name = f.bstack1llll11ll11_opy_(instance, TestFramework.bstack1ll11l1l1ll_opy_)
        if not test_name:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᇹ"))
            return
        test_uuid = f.bstack1llll11ll11_opy_(instance, TestFramework.bstack1ll111111l1_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᇺ"))
            return
        if isinstance(self.bstack1ll11l11l11_opy_, bstack1lll1l11lll_opy_):
            framework_name = bstack1l1l11l_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᇻ")
        else:
            framework_name = bstack1l1l11l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᇼ")
        self.bstack1lll11l111_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_.bstack1l1llll111l_opy_(EVENTS.bstack1llll1l1l1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࠢᇽ"))
            return
        bstack1l11lll11_opy_ = datetime.now()
        bstack1ll111ll11l_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l11l_opy_ (u"ࠢࡴࡥࡤࡲࠧᇾ"), None)
        if not bstack1ll111ll11l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡨࡧ࡮ࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᇿ") + str(framework_name) + bstack1l1l11l_opy_ (u"ࠤࠣࠦሀ"))
            return
        if self.bstack1ll11l1l11l_opy_:
            arg = dict()
            arg[bstack1l1l11l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥሁ")] = method if method else bstack1l1l11l_opy_ (u"ࠦࠧሂ")
            arg[bstack1l1l11l_opy_ (u"ࠧࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠧሃ")] = self.bstack1ll11ll1l11_opy_[bstack1l1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨሄ")]
            arg[bstack1l1l11l_opy_ (u"ࠢࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠧህ")] = self.bstack1ll11ll1l11_opy_[bstack1l1l11l_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨሆ")]
            arg[bstack1l1l11l_opy_ (u"ࠤࡤࡹࡹ࡮ࡈࡦࡣࡧࡩࡷࠨሇ")] = self.bstack1ll11ll1l11_opy_[bstack1l1l11l_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠣለ")]
            arg[bstack1l1l11l_opy_ (u"ࠦࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠣሉ")] = self.bstack1ll11ll1l11_opy_[bstack1l1l11l_opy_ (u"ࠧࡺࡨࡠ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠦሊ")]
            arg[bstack1l1l11l_opy_ (u"ࠨࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵࠨላ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l1llllll11_opy_ = self.bstack1ll11l111ll_opy_(bstack1l1l11l_opy_ (u"ࠢࡴࡥࡤࡲࠧሌ"), self.bstack1ll11ll1l11_opy_[bstack1l1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣል")])
            if bstack1l1l11l_opy_ (u"ࠤࡦࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠧሎ") in bstack1l1llllll11_opy_:
                bstack1l1llllll11_opy_ = bstack1l1llllll11_opy_.copy()
                bstack1l1llllll11_opy_[bstack1l1l11l_opy_ (u"ࠥࡧࡪࡴࡴࡳࡣ࡯ࡅࡺࡺࡨࡉࡧࡤࡨࡪࡸࠢሏ")] = bstack1l1llllll11_opy_.pop(bstack1l1l11l_opy_ (u"ࠦࡨ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡖࡲ࡯ࡪࡴࠢሐ"))
            arg = bstack1ll111ll1ll_opy_(arg, bstack1l1llllll11_opy_)
            bstack1ll11111ll1_opy_ = bstack1ll111ll11l_opy_ % json.dumps(arg)
            driver.execute_script(bstack1ll11111ll1_opy_)
            return
        instance = bstack1llll1ll1ll_opy_.bstack1llll111l1l_opy_(driver)
        if instance:
            if not bstack1llll1ll1ll_opy_.bstack1llll11ll11_opy_(instance, bstack1lll1l1llll_opy_.bstack1ll1111111l_opy_, False):
                bstack1llll1ll1ll_opy_.bstack1llll11lll1_opy_(instance, bstack1lll1l1llll_opy_.bstack1ll1111111l_opy_, True)
            else:
                self.logger.info(bstack1l1l11l_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡯ࠢࡳࡶࡴ࡭ࡲࡦࡵࡶࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤሑ") + str(method) + bstack1l1l11l_opy_ (u"ࠨࠢሒ"))
                return
        self.logger.info(bstack1l1l11l_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧሓ") + str(method) + bstack1l1l11l_opy_ (u"ࠣࠤሔ"))
        if framework_name == bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ሕ"):
            result = self.bstack1ll11l11l11_opy_.bstack1ll11ll11l1_opy_(driver, bstack1ll111ll11l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll111ll11l_opy_, {bstack1l1l11l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥሖ"): method if method else bstack1l1l11l_opy_ (u"ࠦࠧሗ")})
        bstack1lll1ll111l_opy_.end(EVENTS.bstack1llll1l1l1_opy_.value, bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧመ"), bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦሙ"), True, None, command=method)
        if instance:
            bstack1llll1ll1ll_opy_.bstack1llll11lll1_opy_(instance, bstack1lll1l1llll_opy_.bstack1ll1111111l_opy_, False)
            instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿ࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱࠦሚ"), datetime.now() - bstack1l11lll11_opy_)
        return result
        def bstack1ll1111l1l1_opy_(self, driver: object, framework_name, bstack1l1111111_opy_: str):
            self.bstack1ll111l111l_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1ll11l1111l_opy_ = self.bstack1ll11ll1l11_opy_[bstack1l1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣማ")]
            req.bstack1l1111111_opy_ = bstack1l1111111_opy_
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1ll1lllll11_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦሜ") + str(r) + bstack1l1l11l_opy_ (u"ࠥࠦም"))
                else:
                    bstack1ll111lll1l_opy_ = json.loads(r.bstack1ll111l11l1_opy_.decode(bstack1l1l11l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪሞ")))
                    if bstack1l1111111_opy_ == bstack1l1l11l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩሟ"):
                        return bstack1ll111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠨࡤࡢࡶࡤࠦሠ"), [])
                    else:
                        return bstack1ll111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠢࡥࡣࡷࡥࠧሡ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡴࡵࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤࡨࡲࡩ࠻ࠢࠥሢ") + str(e) + bstack1l1l11l_opy_ (u"ࠤࠥሣ"))
    @measure(event_name=EVENTS.bstack11lll1ll_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧሤ"))
            return
        if self.bstack1ll11l1l11l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡥࡵࡶࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧሥ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll1111l1l1_opy_(driver, framework_name, bstack1l1l11l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤሦ"))
        bstack1ll111ll11l_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l11l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥሧ"), None)
        if not bstack1ll111ll11l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨረ") + str(framework_name) + bstack1l1l11l_opy_ (u"ࠣࠤሩ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l11lll11_opy_ = datetime.now()
        if framework_name == bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ሪ"):
            result = self.bstack1ll11l11l11_opy_.bstack1ll11ll11l1_opy_(driver, bstack1ll111ll11l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll111ll11l_opy_)
        instance = bstack1llll1ll1ll_opy_.bstack1llll111l1l_opy_(driver)
        if instance:
            instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨራ"), datetime.now() - bstack1l11lll11_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l1111ll_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢሬ"))
            return
        if self.bstack1ll11l1l11l_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll1111l1l1_opy_(driver, framework_name, bstack1l1l11l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩር"))
        bstack1ll111ll11l_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l11l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥሮ"), None)
        if not bstack1ll111ll11l_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨሯ") + str(framework_name) + bstack1l1l11l_opy_ (u"ࠣࠤሰ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l11lll11_opy_ = datetime.now()
        if framework_name == bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ሱ"):
            result = self.bstack1ll11l11l11_opy_.bstack1ll11ll11l1_opy_(driver, bstack1ll111ll11l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll111ll11l_opy_)
        instance = bstack1llll1ll1ll_opy_.bstack1llll111l1l_opy_(driver)
        if instance:
            instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿࠢሲ"), datetime.now() - bstack1l11lll11_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1111lll1_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1ll11111lll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll111l111l_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1ll1lllll11_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨሳ") + str(r) + bstack1l1l11l_opy_ (u"ࠧࠨሴ"))
            else:
                self.bstack1ll11ll1111_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦስ") + str(e) + bstack1l1l11l_opy_ (u"ࠢࠣሶ"))
            traceback.print_exc()
            raise e
    def bstack1ll11ll1111_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣ࡮ࡲࡥࡩࡥࡣࡰࡰࡩ࡭࡬ࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣሷ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1ll11l1l11l_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1ll11ll1l11_opy_[bstack1l1l11l_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢሸ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1ll11ll1l11_opy_[bstack1l1l11l_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤሹ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1ll11ll1l11_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll11ll1l1l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1llllll1l_opy_ and command.module == self.bstack1ll1111l111_opy_:
                        if command.method and not command.method in bstack1ll11ll1l1l_opy_:
                            bstack1ll11ll1l1l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll11ll1l1l_opy_[command.method]:
                            bstack1ll11ll1l1l_opy_[command.method][command.name] = list()
                        bstack1ll11ll1l1l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll11ll1l1l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1lllllll1_opy_(
        self,
        f: bstack1lll1ll11ll_opy_,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11l11l11_opy_, bstack1lll1l11lll_opy_) and method_name != bstack1l1l11l_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬሺ"):
            return
        if bstack1llll1ll1ll_opy_.bstack1llll1ll1l1_opy_(instance, bstack1lll1l1llll_opy_.bstack1l1lllll11l_opy_):
            return
        if f.bstack1l1llll1ll1_opy_(method_name, *args):
            bstack1ll11l11ll1_opy_ = False
            desired_capabilities = f.bstack1ll11l11l1l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll111ll111_opy_(instance)
                platform_index = f.bstack1llll11ll11_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1llll1lll_opy_, 0)
                bstack1ll11l1llll_opy_ = datetime.now()
                r = self.bstack1ll11111lll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥሻ"), datetime.now() - bstack1ll11l1llll_opy_)
                bstack1ll11l11ll1_opy_ = r.success
            else:
                self.logger.error(bstack1l1l11l_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡥࡧࡶ࡭ࡷ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠽ࠣሼ") + str(desired_capabilities) + bstack1l1l11l_opy_ (u"ࠢࠣሽ"))
            f.bstack1llll11lll1_opy_(instance, bstack1lll1l1llll_opy_.bstack1l1lllll11l_opy_, bstack1ll11l11ll1_opy_)
    def bstack1111ll11l_opy_(self, test_tags):
        bstack1ll11111lll_opy_ = self.config.get(bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨሾ"))
        if not bstack1ll11111lll_opy_:
            return True
        try:
            include_tags = bstack1ll11111lll_opy_[bstack1l1l11l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧሿ")] if bstack1l1l11l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨቀ") in bstack1ll11111lll_opy_ and isinstance(bstack1ll11111lll_opy_[bstack1l1l11l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩቁ")], list) else []
            exclude_tags = bstack1ll11111lll_opy_[bstack1l1l11l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪቂ")] if bstack1l1l11l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫቃ") in bstack1ll11111lll_opy_ and isinstance(bstack1ll11111lll_opy_[bstack1l1l11l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬቄ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣቅ") + str(error))
        return False
    def bstack11ll1l11ll_opy_(self, caps):
        try:
            if self.bstack1ll11l1l11l_opy_:
                bstack1ll111l1l11_opy_ = caps.get(bstack1l1l11l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣቆ"))
                if bstack1ll111l1l11_opy_ is not None and str(bstack1ll111l1l11_opy_).lower() == bstack1l1l11l_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦቇ"):
                    bstack1l1lllll1ll_opy_ = caps.get(bstack1l1l11l_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨቈ")) or caps.get(bstack1l1l11l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ቉"))
                    if bstack1l1lllll1ll_opy_ is not None and int(bstack1l1lllll1ll_opy_) < 11:
                        self.logger.warning(bstack1l1l11l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠ࠲࠳ࠣࡥࡳࡪࠠࡢࡤࡲࡺࡪ࠴ࠠࡄࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤࡂࠨቊ") + str(bstack1l1lllll1ll_opy_) + bstack1l1l11l_opy_ (u"ࠢࠣቋ"))
                        return False
                return True
            bstack1ll111ll1l1_opy_ = caps.get(bstack1l1l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩቌ"), {}).get(bstack1l1l11l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ቍ"), caps.get(bstack1l1l11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ቎"), bstack1l1l11l_opy_ (u"ࠫࠬ቏")))
            if bstack1ll111ll1l1_opy_:
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤቐ"))
                return False
            browser = caps.get(bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫቑ"), bstack1l1l11l_opy_ (u"ࠧࠨቒ")).lower()
            if browser != bstack1l1l11l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨቓ"):
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧቔ"))
                return False
            bstack1ll111111ll_opy_ = bstack1l1llll11ll_opy_
            if not self.config.get(bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬቕ")) or self.config.get(bstack1l1l11l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨቖ")):
                bstack1ll111111ll_opy_ = bstack1ll111l11ll_opy_
            browser_version = caps.get(bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭቗"))
            if not browser_version:
                browser_version = caps.get(bstack1l1l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧቘ"), {}).get(bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ቙"), bstack1l1l11l_opy_ (u"ࠨࠩቚ"))
            if browser_version and browser_version != bstack1l1l11l_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩቛ") and int(browser_version.split(bstack1l1l11l_opy_ (u"ࠪ࠲ࠬቜ"))[0]) <= bstack1ll111111ll_opy_:
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥࠨቝ") + str(bstack1ll111111ll_opy_) + bstack1l1l11l_opy_ (u"ࠧ࠴ࠢ቞"))
                return False
            bstack1l1lllll111_opy_ = caps.get(bstack1l1l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ቟"), {}).get(bstack1l1l11l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧበ"))
            if not bstack1l1lllll111_opy_:
                bstack1l1lllll111_opy_ = caps.get(bstack1l1l11l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ቡ"), {})
            if bstack1l1lllll111_opy_ and bstack1l1l11l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ቢ") in bstack1l1lllll111_opy_.get(bstack1l1l11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨባ"), []):
                self.logger.warning(bstack1l1l11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨቤ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢብ") + str(error))
            return False
    def bstack1ll11ll111l_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll11111l11_opy_ = {
            bstack1l1l11l_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭ቦ"): test_uuid,
        }
        bstack1l1llllllll_opy_ = {}
        if result.success:
            bstack1l1llllllll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll111ll1ll_opy_(bstack1ll11111l11_opy_, bstack1l1llllllll_opy_)
    def bstack1ll11l111ll_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1l1l11l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡋ࡫ࡴࡤࡪࠣࡧࡪࡴࡴࡳࡣ࡯ࠤࡦࡻࡴࡩࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡶࡧࡷ࡯ࡰࡵࠢࡱࡥࡲ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡧࡦࡩࡨࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣ࡭࡫ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡧࡧࡷࡧ࡭࡫ࡤ࠭ࠢࡲࡸ࡭࡫ࡲࡸ࡫ࡶࡩࠥࡲ࡯ࡢࡦࡶࠤࡦࡴࡤࠡࡥࡤࡧ࡭࡫ࡳࠡ࡫ࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥ࠻ࠢࡑࡥࡲ࡫ࠠࡰࡨࠣࡸ࡭࡫ࠠࡴࡥࡵ࡭ࡵࡺࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡦࡳࡳ࡬ࡩࡨࠢࡩࡳࡷࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪ࠺ࠡࡗࡘࡍࡉࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡣࡰࡰࡩ࡭࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠯ࠤࡪࡳࡰࡵࡻࠣࡨ࡮ࡩࡴࠡ࡫ࡩࠤࡪࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢቧ")
        try:
            if self.bstack1ll1111llll_opy_:
                return self.bstack1l1lllll1l1_opy_
            self.bstack1ll111l111l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1l11l_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣቨ")
            req.script_name = script_name
            r = self.bstack1ll1lllll11_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1lllll1l1_opy_ = self.bstack1ll11ll111l_opy_(test_uuid, r)
                self.bstack1ll1111llll_opy_ = True
            else:
                self.logger.error(bstack1l1l11l_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾ࠼ࠣࠦቩ") + str(r.error) + bstack1l1l11l_opy_ (u"ࠥࠦቪ"))
                self.bstack1l1lllll1l1_opy_ = dict()
            return self.bstack1l1lllll1l1_opy_
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠦ࡫࡫ࡴࡤࡪࡆࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡁ࠲࠳ࡼࡇࡴࡴࡦࡪࡩ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡱࡵࠤࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨቫ") + str(traceback.format_exc()) + bstack1l1l11l_opy_ (u"ࠧࠨቬ"))
            return dict()
    def bstack1lll11l111_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll11l1lll1_opy_ = None
        try:
            self.bstack1ll111l111l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1l11l_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨቭ")
            req.script_name = bstack1l1l11l_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧቮ")
            r = self.bstack1ll1lllll11_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦቯ") + str(r.error) + bstack1l1l11l_opy_ (u"ࠤࠥተ"))
            else:
                bstack1ll11111l11_opy_ = self.bstack1ll11ll111l_opy_(test_uuid, r)
                bstack1ll111ll11l_opy_ = r.script
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ቱ") + str(bstack1ll11111l11_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll111ll11l_opy_:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦቲ") + str(framework_name) + bstack1l1l11l_opy_ (u"ࠧࠦࠢታ"))
                return
            bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_.bstack1l1llll111l_opy_(EVENTS.bstack1ll111l1l1l_opy_.value)
            self.bstack1ll11l1ll11_opy_(driver, bstack1ll111ll11l_opy_, bstack1ll11111l11_opy_, framework_name)
            self.logger.info(bstack1l1l11l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤቴ"))
            bstack1lll1ll111l_opy_.end(EVENTS.bstack1ll111l1l1l_opy_.value, bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢት"), bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨቶ"), True, None, command=bstack1l1l11l_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧቷ"),test_name=name)
        except Exception as bstack1ll111lllll_opy_:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧቸ") + bstack1l1l11l_opy_ (u"ࠦࡸࡺࡲࠩࡲࡤࡸ࡭࠯ࠢቹ") + bstack1l1l11l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢቺ") + str(bstack1ll111lllll_opy_))
            bstack1lll1ll111l_opy_.end(EVENTS.bstack1ll111l1l1l_opy_.value, bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨቻ"), bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧቼ"), False, bstack1ll111lllll_opy_, command=bstack1l1l11l_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ች"),test_name=name)
    def bstack1ll11l1ll11_opy_(self, driver, bstack1ll111ll11l_opy_, bstack1ll11111l11_opy_, framework_name):
        if framework_name == bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ቾ"):
            self.bstack1ll11l11l11_opy_.bstack1ll11ll11l1_opy_(driver, bstack1ll111ll11l_opy_, bstack1ll11111l11_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll111ll11l_opy_, bstack1ll11111l11_opy_))
    def _1ll11ll11ll_opy_(self, instance: bstack1lll1l11111_opy_, args: Tuple) -> list:
        bstack1l1l11l_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡴࡢࡩࡶࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࠧࠨࠢቿ")
        if bstack1l1l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨኀ") in instance.bstack1l1llll1l1l_opy_:
            return args[2].tags if hasattr(args[2], bstack1l1l11l_opy_ (u"ࠬࡺࡡࡨࡵࠪኁ")) else []
        if hasattr(args[0], bstack1l1l11l_opy_ (u"࠭࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠫኂ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll1111l11l_opy_(self, tags, capabilities):
        return self.bstack1111ll11l_opy_(tags) and self.bstack11ll1l11ll_opy_(capabilities)
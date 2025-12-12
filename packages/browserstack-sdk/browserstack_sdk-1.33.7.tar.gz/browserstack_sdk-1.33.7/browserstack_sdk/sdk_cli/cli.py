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
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lllll1llll_opy_ import bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll111_opy_ import bstack1lll1l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11l1_opy_ import bstack1lll11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111ll1l_opy_ import bstack1lll11l1111_opy_
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1ll1ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111lll_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1ll1_opy_ import bstack1lll1l11lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11lllll1_opy_ import bstack1lll111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack111l1l111_opy_ import bstack111l1l111_opy_, bstack11l11l1l_opy_, bstack1ll1llll1l_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lll111l111_opy_ import bstack1ll1l1111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11ll11_opy_ import bstack1lll1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import bstack1llll1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1llllll_opy_ import bstack1ll1l111l11_opy_
from bstack_utils.helper import Notset, bstack1lll111111l_opy_, get_cli_dir, bstack1ll1l1l1ll1_opy_, bstack1ll111l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from browserstack_sdk.sdk_cli.utils.bstack1ll1l11l1l1_opy_ import bstack1lll1111l1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l11_opy_ import bstack111l1lll1_opy_
from bstack_utils.helper import Notset, bstack1lll111111l_opy_, get_cli_dir, bstack1ll1l1l1ll1_opy_, bstack1ll111l11l_opy_, bstack11l1l1l111_opy_, bstack1ll111l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lll1ll_opy_, bstack1lll1l11111_opy_, bstack1ll1lll111l_opy_, bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import bstack1lllll1ll11_opy_, bstack1lllll1l111_opy_, bstack1llll1111l1_opy_
from bstack_utils.constants import *
from bstack_utils.bstack1l1llll11_opy_ import bstack1l1ll1l11l_opy_
from bstack_utils import bstack11l1l11111_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11lll1ll1_opy_, bstack11lll1l1l1_opy_
logger = bstack11l1l11111_opy_.get_logger(__name__, bstack11l1l11111_opy_.bstack1lll11l1l1l_opy_())
def bstack1ll1l1l11ll_opy_(bs_config):
    bstack1lll1l1l111_opy_ = None
    bstack1ll1l1l1l1l_opy_ = None
    try:
        bstack1ll1l1l1l1l_opy_ = get_cli_dir()
        bstack1lll1l1l111_opy_ = bstack1ll1l1l1ll1_opy_(bstack1ll1l1l1l1l_opy_)
        bstack1ll1l11llll_opy_ = bstack1lll111111l_opy_(bstack1lll1l1l111_opy_, bstack1ll1l1l1l1l_opy_, bs_config)
        bstack1lll1l1l111_opy_ = bstack1ll1l11llll_opy_ if bstack1ll1l11llll_opy_ else bstack1lll1l1l111_opy_
        if not bstack1lll1l1l111_opy_:
            raise ValueError(bstack1l1l11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠤჲ"))
    except Exception as ex:
        logger.debug(bstack1l1l11l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡷ࡬ࡪࠦ࡬ࡢࡶࡨࡷࡹࠦࡢࡪࡰࡤࡶࡾࠦࡻࡾࠤჳ").format(ex))
        bstack1lll1l1l111_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤࡖࡁࡕࡊࠥჴ"))
        if bstack1lll1l1l111_opy_:
            logger.debug(bstack1l1l11l_opy_ (u"ࠣࡈࡤࡰࡱ࡯࡮ࡨࠢࡥࡥࡨࡱࠠࡵࡱࠣࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠦࡦࡳࡱࡰࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵ࠼ࠣࠦჵ") + str(bstack1lll1l1l111_opy_) + bstack1l1l11l_opy_ (u"ࠤࠥჶ"))
        else:
            logger.debug(bstack1l1l11l_opy_ (u"ࠥࡒࡴࠦࡶࡢ࡮࡬ࡨ࡙ࠥࡄࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡔࡆ࡚ࡈࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴ࠼ࠢࡶࡩࡹࡻࡰࠡ࡯ࡤࡽࠥࡨࡥࠡ࡫ࡱࡧࡴࡳࡰ࡭ࡧࡷࡩ࠳ࠨჷ"))
    return bstack1lll1l1l111_opy_, bstack1ll1l1l1l1l_opy_
bstack1ll1l111111_opy_ = bstack1l1l11l_opy_ (u"ࠦ࠾࠿࠹࠺ࠤჸ")
bstack1ll1l11lll1_opy_ = bstack1l1l11l_opy_ (u"ࠧࡸࡥࡢࡦࡼࠦჹ")
bstack1ll1lll11ll_opy_ = bstack1l1l11l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥჺ")
bstack1ll1ll1l1l1_opy_ = bstack1l1l11l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡍࡋࡖࡘࡊࡔ࡟ࡂࡆࡇࡖࠧ჻")
bstack1l1l11l1l1_opy_ = bstack1l1l11l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠦჼ")
bstack1ll1llll1l1_opy_ = re.compile(bstack1l1l11l_opy_ (u"ࡴࠥࠬࡄ࡯ࠩ࠯ࠬࠫࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡾࡅࡗ࠮࠴ࠪࠣჽ"))
bstack1ll1l1lll1l_opy_ = bstack1l1l11l_opy_ (u"ࠥࡨࡪࡼࡥ࡭ࡱࡳࡱࡪࡴࡴࠣჾ")
bstack1lll11ll1ll_opy_ = bstack1l1l11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡔࡘࡃࡆࡡࡉࡅࡑࡒࡂࡂࡅࡎࠦჿ")
bstack1ll1ll1ll11_opy_ = [
    bstack11l11l1l_opy_.bstack11lll11ll_opy_,
    bstack11l11l1l_opy_.CONNECT,
    bstack11l11l1l_opy_.bstack11lll1l11_opy_,
]
class SDKCLI:
    _1lll11l11ll_opy_ = None
    process: Union[None, Any]
    bstack1lll1ll1l11_opy_: bool
    bstack1ll1l11l111_opy_: bool
    bstack1lll1111lll_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1lll1l1ll1l_opy_: Union[None, grpc.Channel]
    bstack1lll1lll1l1_opy_: str
    test_framework: TestFramework
    bstack1lllll111ll_opy_: bstack1llll1ll1ll_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1ll1l1111ll_opy_: bstack1lll111l1ll_opy_
    accessibility: bstack1lll1l1llll_opy_
    bstack1l1l1l11_opy_: bstack111l1lll1_opy_
    ai: bstack1lll11l111l_opy_
    bstack1lll1ll1l1l_opy_: bstack1lll11l1111_opy_
    bstack1lll11lllll_opy_: List[bstack1lll1llll1l_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll11111l1_opy_: Any
    bstack1lll1111ll1_opy_: Dict[str, timedelta]
    bstack1lll11l1lll_opy_: str
    bstack1lllll1llll_opy_: bstack1llllll11ll_opy_
    def __new__(cls):
        if not cls._1lll11l11ll_opy_:
            cls._1lll11l11ll_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lll11l11ll_opy_
    def __init__(self):
        self.process = None
        self.bstack1lll1ll1l11_opy_ = False
        self.bstack1lll1l1ll1l_opy_ = None
        self.bstack1ll1lllll11_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1ll1ll1l1l1_opy_, None)
        self.bstack1ll1ll11111_opy_ = os.environ.get(bstack1ll1lll11ll_opy_, bstack1l1l11l_opy_ (u"ࠧࠨᄀ")) == bstack1l1l11l_opy_ (u"ࠨࠢᄁ")
        self.bstack1ll1l11l111_opy_ = False
        self.bstack1lll1111lll_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll11111l1_opy_ = None
        self.test_framework = None
        self.bstack1lllll111ll_opy_ = None
        self.bstack1lll1lll1l1_opy_=bstack1l1l11l_opy_ (u"ࠢࠣᄂ")
        self.session_framework = None
        self.logger = bstack11l1l11111_opy_.get_logger(self.__class__.__name__, bstack11l1l11111_opy_.bstack1lll11l1l1l_opy_())
        self.bstack1lll1111ll1_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1lllll1llll_opy_ = bstack1llllll11ll_opy_()
        self.bstack1ll1ll111ll_opy_ = None
        self.bstack1lll11lll1l_opy_ = None
        self.bstack1ll1l1111ll_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1lll11lllll_opy_ = []
    def bstack1lll11lll1_opy_(self):
        return os.environ.get(bstack1l1l11l1l1_opy_).lower().__eq__(bstack1l1l11l_opy_ (u"ࠣࡶࡵࡹࡪࠨᄃ"))
    def is_enabled(self, config):
        if os.environ.get(bstack1lll11ll1ll_opy_, bstack1l1l11l_opy_ (u"ࠩࠪᄄ")).lower() in [bstack1l1l11l_opy_ (u"ࠪࡸࡷࡻࡥࠨᄅ"), bstack1l1l11l_opy_ (u"ࠫ࠶࠭ᄆ"), bstack1l1l11l_opy_ (u"ࠬࡿࡥࡴࠩᄇ")]:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡆࡰࡴࡦ࡭ࡳ࡭ࠠࡧࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡰࡳࡩ࡫ࠠࡥࡷࡨࠤࡹࡵࠠࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡐࡔࡆࡉࡤࡌࡁࡍࡎࡅࡅࡈࡑࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠢᄈ"))
            os.environ[bstack1l1l11l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡉࡔࡡࡕ࡙ࡓࡔࡉࡏࡉࠥᄉ")] = bstack1l1l11l_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᄊ")
            return False
        if bstack1l1l11l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᄋ") in config and str(config[bstack1l1l11l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᄌ")]).lower() != bstack1l1l11l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᄍ"):
            return False
        bstack1ll1lll1l1l_opy_ = [bstack1l1l11l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᄎ"), bstack1l1l11l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᄏ")]
        bstack1ll1l1llll1_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠥᄐ")) in bstack1ll1lll1l1l_opy_ or os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩᄑ")) in bstack1ll1lll1l1l_opy_
        os.environ[bstack1l1l11l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡋࡖࡣࡗ࡛ࡎࡏࡋࡑࡋࠧᄒ")] = str(bstack1ll1l1llll1_opy_) # bstack1ll1l11111l_opy_ bstack1ll1l1ll11l_opy_ VAR to bstack1ll1l11ll1l_opy_ is binary running
        return bstack1ll1l1llll1_opy_
    def bstack1ll111l1l1_opy_(self):
        for event in bstack1ll1ll1ll11_opy_:
            bstack111l1l111_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack111l1l111_opy_.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡿࡪࡼࡥ࡯ࡶࡢࡲࡦࡳࡥࡾࠢࡀࡂࠥࢁࡡࡳࡩࡶࢁࠥࠨᄓ") + str(kwargs) + bstack1l1l11l_opy_ (u"ࠦࠧᄔ"))
            )
        bstack111l1l111_opy_.register(bstack11l11l1l_opy_.bstack11lll11ll_opy_, self.__1ll1ll111l1_opy_)
        bstack111l1l111_opy_.register(bstack11l11l1l_opy_.CONNECT, self.__1ll1lll1l11_opy_)
        bstack111l1l111_opy_.register(bstack11l11l1l_opy_.bstack11lll1l11_opy_, self.__1ll1l1l111l_opy_)
        bstack111l1l111_opy_.register(bstack11l11l1l_opy_.bstack1l11lll1l_opy_, self.__1ll1ll1111l_opy_)
    def bstack1ll1l11111_opy_(self):
        return not self.bstack1ll1ll11111_opy_ and os.environ.get(bstack1ll1lll11ll_opy_, bstack1l1l11l_opy_ (u"ࠧࠨᄕ")) != bstack1l1l11l_opy_ (u"ࠨࠢᄖ")
    def is_running(self):
        if self.bstack1ll1ll11111_opy_:
            return self.bstack1lll1ll1l11_opy_
        else:
            return bool(self.bstack1lll1l1ll1l_opy_)
    def bstack1ll11llllll_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1lll11lllll_opy_) and cli.is_running()
    def __1ll1lll11l1_opy_(self, bstack1ll1l1lll11_opy_=10):
        if self.bstack1ll1lllll11_opy_:
            return
        bstack1l11lll11_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1ll1ll1l1l1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠢ࡜ࠤᄗ") + str(id(self)) + bstack1l1l11l_opy_ (u"ࠣ࡟ࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡳ࡭ࠢᄘ"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack1l1l11l_opy_ (u"ࠤࡪࡶࡵࡩ࠮ࡦࡰࡤࡦࡱ࡫࡟ࡩࡶࡷࡴࡤࡶࡲࡰࡺࡼࠦᄙ"), 0), (bstack1l1l11l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠯ࡧࡱࡥࡧࡲࡥࡠࡪࡷࡸࡵࡹ࡟ࡱࡴࡲࡼࡾࠨᄚ"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1ll1l1lll11_opy_)
        self.bstack1lll1l1ll1l_opy_ = channel
        self.bstack1ll1lllll11_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1lll1l1ll1l_opy_)
        self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡦࡳࡳࡴࡥࡤࡶࠥᄛ"), datetime.now() - bstack1l11lll11_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1ll1ll1l1l1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡨࡵ࡮࡯ࡧࡦࡸࡪࡪ࠺ࠡ࡫ࡶࡣࡨ࡮ࡩ࡭ࡦࡢࡴࡷࡵࡣࡦࡵࡶࡁࠧᄜ") + str(self.bstack1ll1l11111_opy_()) + bstack1l1l11l_opy_ (u"ࠨࠢᄝ"))
    def __1ll1l1l111l_opy_(self, event_name):
        if self.bstack1ll1l11111_opy_():
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡵࡷࡳࡵࡶࡩ࡯ࡩࠣࡇࡑࡏࠢᄞ"))
        self.__1lll11l1l11_opy_()
    def __1ll1ll1111l_opy_(self, event_name, bstack1ll1ll1lll1_opy_ = None, exit_code=1):
        if exit_code == 1:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠣᄟ"))
        bstack1lll11ll111_opy_ = Path(bstack1lll1l111l1_opy_ (u"ࠤࡾࡷࡪࡲࡦ࠯ࡥ࡯࡭ࡤࡪࡩࡳࡿ࠲ࡹࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࡷ࠳ࡰࡳࡰࡰࠥᄠ"))
        if self.bstack1ll1l1l1l1l_opy_ and bstack1lll11ll111_opy_.exists():
            with open(bstack1lll11ll111_opy_, bstack1l1l11l_opy_ (u"ࠪࡶࠬᄡ"), encoding=bstack1l1l11l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᄢ")) as fp:
                data = json.load(fp)
                try:
                    bstack11l1l1l111_opy_(bstack1l1l11l_opy_ (u"ࠬࡖࡏࡔࡖࠪᄣ"), bstack1l1ll1l11l_opy_(bstack1l1l1lll11_opy_), data, {
                        bstack1l1l11l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᄤ"): (self.config[bstack1l1l11l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᄥ")], self.config[bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᄦ")])
                    })
                except Exception as e:
                    logger.debug(bstack11lll1l1l1_opy_.format(str(e)))
            bstack1lll11ll111_opy_.unlink()
        sys.exit(exit_code)
    @measure(event_name=EVENTS.bstack1lll11llll1_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def __1ll1ll111l1_opy_(self, event_name: str, data):
        from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
        self.bstack1lll1lll1l1_opy_, self.bstack1ll1l1l1l1l_opy_ = bstack1ll1l1l11ll_opy_(data.bs_config)
        os.environ[bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠ࡙ࡕࡍ࡙ࡇࡂࡍࡇࡢࡈࡎࡘࠧᄧ")] = self.bstack1ll1l1l1l1l_opy_
        if not self.bstack1lll1lll1l1_opy_ or not self.bstack1ll1l1l1l1l_opy_:
            raise ValueError(bstack1l1l11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡉࡌࡊࠢࡥ࡭ࡳࡧࡲࡺࠤᄨ"))
        if self.bstack1ll1l11111_opy_():
            self.__1ll1lll1l11_opy_(event_name, bstack1ll1llll1l_opy_())
            return
        try:
            bstack1lll1ll111l_opy_.end(EVENTS.bstack1llll1ll11_opy_.value, EVENTS.bstack1llll1ll11_opy_.value + bstack1l1l11l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᄩ"), EVENTS.bstack1llll1ll11_opy_.value + bstack1l1l11l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᄪ"), status=True, failure=None, test_name=None)
            logger.debug(bstack1l1l11l_opy_ (u"ࠨࡃࡰ࡯ࡳࡰࡪࡺࡥࠡࡕࡇࡏ࡙ࠥࡥࡵࡷࡳ࠲ࠧᄫ"))
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳࠡࡽࢀࠦᄬ").format(e))
        start = datetime.now()
        is_started = self.__1lll1l1l11l_opy_()
        self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠣࡵࡳࡥࡼࡴ࡟ࡵ࡫ࡰࡩࠧᄭ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1ll1lll11l1_opy_()
            self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࡢࡸ࡮ࡳࡥࠣᄮ"), datetime.now() - start)
            start = datetime.now()
            self.__1ll1l11l1ll_opy_(data)
            self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣᄯ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll1111l11_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def __1ll1lll1l11_opy_(self, event_name: str, data: bstack1ll1llll1l_opy_):
        if not self.bstack1ll1l11111_opy_():
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱࡱࡲࡪࡩࡴ࠻ࠢࡱࡳࡹࠦࡡࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᄰ"))
            return
        bin_session_id = os.environ.get(bstack1ll1lll11ll_opy_)
        start = datetime.now()
        self.__1ll1lll11l1_opy_()
        self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦᄱ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥࠢࡷࡳࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡄࡎࡌࠤࠧᄲ") + str(bin_session_id) + bstack1l1l11l_opy_ (u"ࠢࠣᄳ"))
        start = datetime.now()
        self.__1ll1l1lllll_opy_()
        self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨᄴ"), datetime.now() - start)
    def __1ll1l1l11l1_opy_(self):
        if not self.bstack1ll1lllll11_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡦࡥࡳࡴ࡯ࡵࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࠥࡳ࡯ࡥࡷ࡯ࡩࡸࠨᄵ"))
            return
        bstack1lll1ll1lll_opy_ = {
            bstack1l1l11l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᄶ"): (bstack1lll1lll111_opy_, bstack1lll1l11lll_opy_, bstack1ll1l111l11_opy_),
            bstack1l1l11l_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᄷ"): (bstack1ll1ll1l11l_opy_, bstack1ll1llll111_opy_, bstack1lll1ll11ll_opy_),
        }
        if not self.bstack1ll1ll111ll_opy_ and self.session_framework in bstack1lll1ll1lll_opy_:
            bstack1ll1ll11l11_opy_, bstack1lll11111ll_opy_, bstack1ll1ll11l1l_opy_ = bstack1lll1ll1lll_opy_[self.session_framework]
            bstack1lll1lllll1_opy_ = bstack1lll11111ll_opy_()
            self.bstack1lll11lll1l_opy_ = bstack1lll1lllll1_opy_
            self.bstack1ll1ll111ll_opy_ = bstack1ll1ll11l1l_opy_
            self.bstack1lll11lllll_opy_.append(bstack1lll1lllll1_opy_)
            self.bstack1lll11lllll_opy_.append(bstack1ll1ll11l11_opy_(self.bstack1lll11lll1l_opy_))
        if not self.bstack1ll1l1111ll_opy_ and self.config_observability and self.config_observability.success: # bstack1ll1ll1llll_opy_
            self.bstack1ll1l1111ll_opy_ = bstack1lll111l1ll_opy_(self.bstack1ll1ll111ll_opy_, self.bstack1lll11lll1l_opy_) # bstack1lll1l111ll_opy_
            self.bstack1lll11lllll_opy_.append(self.bstack1ll1l1111ll_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lll1l1llll_opy_(self.bstack1ll1ll111ll_opy_, self.bstack1lll11lll1l_opy_)
            self.bstack1lll11lllll_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack1l1l11l_opy_ (u"ࠧࡹࡥ࡭ࡨࡋࡩࡦࡲࠢᄸ"), False) == True:
            self.ai = bstack1lll11l111l_opy_()
            self.bstack1lll11lllll_opy_.append(self.ai)
        if not self.percy and self.bstack1lll11111l1_opy_ and self.bstack1lll11111l1_opy_.success:
            self.percy = bstack1lll11l1111_opy_(self.bstack1lll11111l1_opy_)
            self.bstack1lll11lllll_opy_.append(self.percy)
        for mod in self.bstack1lll11lllll_opy_:
            if not mod.bstack1lll1ll1111_opy_():
                mod.configure(self.bstack1ll1lllll11_opy_, self.config, self.cli_bin_session_id, self.bstack1lllll1llll_opy_)
    def __1lll1lll11l_opy_(self):
        for mod in self.bstack1lll11lllll_opy_:
            if mod.bstack1lll1ll1111_opy_():
                mod.configure(self.bstack1ll1lllll11_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1lll11ll11l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def __1ll1l11l1ll_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1ll1l11l111_opy_:
            return
        self.__1lll1ll1ll1_opy_(data)
        bstack1l11lll11_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack1l1l11l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࠨᄹ")
        req.sdk_language = bstack1l1l11l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢᄺ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1ll1llll1l1_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣ࡝ࠥᄻ") + str(id(self)) + bstack1l1l11l_opy_ (u"ࠤࡠࠤࡲࡧࡩ࡯࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡸࡺࡡࡳࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᄼ"))
            r = self.bstack1ll1lllll11_opy_.StartBinSession(req)
            self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡷࡥࡷࡺ࡟ࡣ࡫ࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᄽ"), datetime.now() - bstack1l11lll11_opy_)
            os.environ[bstack1ll1lll11ll_opy_] = r.bin_session_id
            self.__1lll1l1ll11_opy_(r)
            self.__1ll1l1l11l1_opy_()
            self.bstack1lllll1llll_opy_.start()
            self.bstack1ll1l11l111_opy_ = True
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡠࠨᄾ") + str(id(self)) + bstack1l1l11l_opy_ (u"ࠧࡣࠠ࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠥᄿ"))
        except grpc.bstack1lll1l11l1l_opy_ as bstack1ll1lllllll_opy_:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨ࡛ࡼ࡫ࡧࠬࡸ࡫࡬ࡧࠫࢀࡡࠥࡺࡩ࡮ࡧࡲࡩࡺࡺ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᅀ") + str(bstack1ll1lllllll_opy_) + bstack1l1l11l_opy_ (u"ࠢࠣᅁ"))
            traceback.print_exc()
            raise bstack1ll1lllllll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᅂ") + str(e) + bstack1l1l11l_opy_ (u"ࠤࠥᅃ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1l11l11l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def __1ll1l1lllll_opy_(self):
        if not self.bstack1ll1l11111_opy_() or not self.cli_bin_session_id or self.bstack1lll1111lll_opy_:
            return
        bstack1l11lll11_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᅄ"), bstack1l1l11l_opy_ (u"ࠫ࠵࠭ᅅ")))
        try:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡡࠢᅆ") + str(id(self)) + bstack1l1l11l_opy_ (u"ࠨ࡝ࠡࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᅇ"))
            r = self.bstack1ll1lllll11_opy_.ConnectBinSession(req)
            self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡩ࡯࡯ࡰࡨࡧࡹࡥࡢࡪࡰࡢࡷࡪࡹࡳࡪࡱࡱࠦᅈ"), datetime.now() - bstack1l11lll11_opy_)
            self.__1lll1l1ll11_opy_(r)
            self.__1ll1l1l11l1_opy_()
            self.bstack1lllll1llll_opy_.start()
            self.bstack1lll1111lll_opy_ = True
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣ࡝ࠥᅉ") + str(id(self)) + bstack1l1l11l_opy_ (u"ࠤࡠࠤࡨ࡮ࡩ࡭ࡦ࠰ࡴࡷࡵࡣࡦࡵࡶ࠾ࠥࡩ࡯࡯ࡰࡨࡧࡹ࡫ࡤࠣᅊ"))
        except grpc.bstack1lll1l11l1l_opy_ as bstack1ll1lllllll_opy_:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡷ࡭ࡲ࡫࡯ࡦࡷࡷ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᅋ") + str(bstack1ll1lllllll_opy_) + bstack1l1l11l_opy_ (u"ࠦࠧᅌ"))
            traceback.print_exc()
            raise bstack1ll1lllllll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᅍ") + str(e) + bstack1l1l11l_opy_ (u"ࠨࠢᅎ"))
            traceback.print_exc()
            raise e
    def __1lll1l1ll11_opy_(self, r):
        self.bstack1lll1l1lll1_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack1l1l11l_opy_ (u"ࠢࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᅏ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack1l1l11l_opy_ (u"ࠣࡧࡰࡴࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡸࡲࡩࠨᅐ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack1l1l11l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡐࡦࡴࡦࡽࠥ࡯ࡳࠡࡵࡨࡲࡹࠦ࡯࡯࡮ࡼࠤࡦࡹࠠࡱࡣࡵࡸࠥࡵࡦࠡࡶ࡫ࡩࠥࠨࡃࡰࡰࡱࡩࡨࡺࡂࡪࡰࡖࡩࡸࡹࡩࡰࡰ࠯ࠦࠥࡧ࡮ࡥࠢࡷ࡬࡮ࡹࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢ࡬ࡷࠥࡧ࡬ࡴࡱࠣࡹࡸ࡫ࡤࠡࡤࡼࠤࡘࡺࡡࡳࡶࡅ࡭ࡳ࡙ࡥࡴࡵ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫ࡩࡷ࡫ࡦࡰࡴࡨ࠰ࠥࡔ࡯࡯ࡧࠣ࡬ࡦࡴࡤ࡭࡫ࡱ࡫ࠥ࡯ࡳࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᅑ")
        self.bstack1lll11111l1_opy_ = getattr(r, bstack1l1l11l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᅒ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᅓ")] = self.config_testhub.jwt
        os.environ[bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᅔ")] = self.config_testhub.build_hashed_id
    def bstack1ll1lll1lll_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lll1ll1l11_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1lll111l11l_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1lll111l11l_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1ll1lll1lll_opy_(event_name=EVENTS.bstack1lll11ll1l1_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def __1lll1l1l11l_opy_(self, bstack1ll1l1lll11_opy_=10):
        if self.bstack1lll1ll1l11_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡳࡵࡣࡵࡸ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡳࡷࡱࡲ࡮ࡴࡧࠣᅕ"))
            return True
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨᅖ"))
        if os.getenv(bstack1l1l11l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡊࡔࡖࠣᅗ")) == bstack1ll1l1lll1l_opy_:
            self.cli_bin_session_id = bstack1ll1l1lll1l_opy_
            self.cli_listen_addr = bstack1l1l11l_opy_ (u"ࠤࡸࡲ࡮ࡾ࠺࠰ࡶࡰࡴ࠴ࡹࡤ࡬࠯ࡳࡰࡦࡺࡦࡰࡴࡰ࠱ࠪࡹ࠮ࡴࡱࡦ࡯ࠧᅘ") % (self.cli_bin_session_id)
            self.bstack1lll1ll1l11_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll1lll1l1_opy_, bstack1l1l11l_opy_ (u"ࠥࡷࡩࡱࠢᅙ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1lll1l11l11_opy_ compat for text=True in bstack1lll111ll11_opy_ python
            encoding=bstack1l1l11l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᅚ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1lll1l11ll1_opy_ = threading.Thread(target=self.__1ll1ll1l111_opy_, args=(bstack1ll1l1lll11_opy_,))
        bstack1lll1l11ll1_opy_.start()
        bstack1lll1l11ll1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡸࡶࡡࡸࡰ࠽ࠤࡷ࡫ࡴࡶࡴࡱࡧࡴࡪࡥ࠾ࡽࡶࡩࡱ࡬࠮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡴࡨࡸࡺࡸ࡮ࡤࡱࡧࡩࢂࠦ࡯ࡶࡶࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡷࡹࡪ࡯ࡶࡶ࠱ࡶࡪࡧࡤࠩࠫࢀࠤࡪࡸࡲ࠾ࠤᅛ") + str(self.process.stderr.read()) + bstack1l1l11l_opy_ (u"ࠨࠢᅜ"))
        if not self.bstack1lll1ll1l11_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢ࡜ࠤᅝ") + str(id(self)) + bstack1l1l11l_opy_ (u"ࠣ࡟ࠣࡧࡱ࡫ࡡ࡯ࡷࡳࠦᅞ"))
            self.__1lll11l1l11_opy_()
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠤ࡞ࡿ࡮ࡪࠨࡴࡧ࡯ࡪ࠮ࢃ࡝ࠡࡲࡵࡳࡨ࡫ࡳࡴࡡࡵࡩࡦࡪࡹ࠻ࠢࠥᅟ") + str(self.bstack1lll1ll1l11_opy_) + bstack1l1l11l_opy_ (u"ࠥࠦᅠ"))
        return self.bstack1lll1ll1l11_opy_
    def __1ll1ll1l111_opy_(self, bstack1lll1l1111l_opy_=10):
        bstack1ll1l1ll1l1_opy_ = time.time()
        while self.process and time.time() - bstack1ll1l1ll1l1_opy_ < bstack1lll1l1111l_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack1l1l11l_opy_ (u"ࠦ࡮ࡪ࠽ࠣᅡ") in line:
                    self.cli_bin_session_id = line.split(bstack1l1l11l_opy_ (u"ࠧ࡯ࡤ࠾ࠤᅢ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡣ࡭࡫ࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ࠾ࠧᅣ") + str(self.cli_bin_session_id) + bstack1l1l11l_opy_ (u"ࠢࠣᅤ"))
                    continue
                if bstack1l1l11l_opy_ (u"ࠣ࡮࡬ࡷࡹ࡫࡮࠾ࠤᅥ") in line:
                    self.cli_listen_addr = line.split(bstack1l1l11l_opy_ (u"ࠤ࡯࡭ࡸࡺࡥ࡯࠿ࠥᅦ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡧࡱ࡯࡟࡭࡫ࡶࡸࡪࡴ࡟ࡢࡦࡧࡶ࠿ࠨᅧ") + str(self.cli_listen_addr) + bstack1l1l11l_opy_ (u"ࠦࠧᅨ"))
                    continue
                if bstack1l1l11l_opy_ (u"ࠧࡶ࡯ࡳࡶࡀࠦᅩ") in line:
                    port = line.split(bstack1l1l11l_opy_ (u"ࠨࡰࡰࡴࡷࡁࠧᅪ"))[-1:][0].strip()
                    self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡱࡱࡵࡸ࠿ࠨᅫ") + str(port) + bstack1l1l11l_opy_ (u"ࠣࠤᅬ"))
                    continue
                if line.strip() == bstack1ll1l11lll1_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack1l1l11l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡋࡒࡣࡘ࡚ࡒࡆࡃࡐࠦᅭ"), bstack1l1l11l_opy_ (u"ࠥ࠵ࠧᅮ")) == bstack1l1l11l_opy_ (u"ࠦ࠶ࠨᅯ"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lll1ll1l11_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵ࠾ࠥࠨᅰ") + str(e) + bstack1l1l11l_opy_ (u"ࠨࠢᅱ"))
        return False
    @measure(event_name=EVENTS.bstack1ll1l1l1l11_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def __1lll11l1l11_opy_(self):
        if self.bstack1lll1l1ll1l_opy_:
            self.bstack1lllll1llll_opy_.stop()
            start = datetime.now()
            if self.bstack1lll111l1l1_opy_():
                self.cli_bin_session_id = None
                if self.bstack1lll1111lll_opy_:
                    self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠢࡴࡶࡲࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡴࡪ࡯ࡨࠦᅲ"), datetime.now() - start)
                else:
                    self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠣࡵࡷࡳࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡵ࡫ࡰࡩࠧᅳ"), datetime.now() - start)
            self.__1lll1lll11l_opy_()
            start = datetime.now()
            self.bstack1lll1l1ll1l_opy_.close()
            self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠤࡧ࡭ࡸࡩ࡯࡯ࡰࡨࡧࡹࡥࡴࡪ࡯ࡨࠦᅴ"), datetime.now() - start)
            self.bstack1lll1l1ll1l_opy_ = None
        if self.process:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡷࡹࡵࡰࠣᅵ"))
            start = datetime.now()
            self.process.terminate()
            self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠦࡰ࡯࡬࡭ࡡࡷ࡭ࡲ࡫ࠢᅶ"), datetime.now() - start)
            self.process = None
            if self.bstack1ll1ll11111_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack1l1lll1ll_opy_()
                self.logger.info(
                    bstack1l1l11l_opy_ (u"ࠧ࡜ࡩࡴ࡫ࡷࠤ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠧᅷ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack1l1l11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᅸ")] = self.config_testhub.build_hashed_id
        self.bstack1lll1ll1l11_opy_ = False
    def __1lll1ll1ll1_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack1l1l11l_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤᅹ")] = selenium.__version__
            data.frameworks.append(bstack1l1l11l_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᅺ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack1l1l11l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᅻ")] = __version__
            data.frameworks.append(bstack1l1l11l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᅼ"))
        except:
            pass
    def bstack1ll1ll1l1ll_opy_(self, hub_url: str, platform_index: int, bstack11l1l11l_opy_: Any):
        if self.bstack1lllll111ll_opy_:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡸࡱࡩࡱࡲࡨࡨࠥࡹࡥࡵࡷࡳࠤࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡵࡨࡸࠥࡻࡰࠣᅽ"))
            return
        try:
            bstack1l11lll11_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack1l1l11l_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᅾ")
            self.bstack1lllll111ll_opy_ = bstack1lll1ll11ll_opy_(
                cli.config.get(bstack1l1l11l_opy_ (u"ࠨࡨࡶࡤࡘࡶࡱࠨᅿ"), hub_url),
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1ll1ll11ll1_opy_={bstack1l1l11l_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࡠࡨࡵࡳࡲࡥࡣࡢࡲࡶࠦᆀ"): bstack11l1l11l_opy_}
            )
            def bstack1ll1l1l1111_opy_(self):
                return
            if self.config.get(bstack1l1l11l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠥᆁ"), True):
                Service.start = bstack1ll1l1l1111_opy_
                Service.stop = bstack1ll1l1l1111_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.upload_attachment = staticmethod(bstack111l1lll1_opy_.upload_attachment)
            WebDriver.set_custom_tag = staticmethod(bstack1lll1111l1l_opy_.set_custom_tag)
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᆂ"), datetime.now() - bstack1l11lll11_opy_)
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠺ࠡࠤᆃ") + str(e) + bstack1l1l11l_opy_ (u"ࠦࠧᆄ"))
    def bstack1ll1ll1ll1l_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack11l1l1lll_opy_
            self.bstack1lllll111ll_opy_ = bstack1ll1l111l11_opy_(
                platform_index,
                framework_name=bstack1l1l11l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᆅ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࠿ࠦࠢᆆ") + str(e) + bstack1l1l11l_opy_ (u"ࠢࠣᆇ"))
            pass
    def bstack1ll1lllll1l_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥᆈ"))
            return
        if bstack1ll111l11l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack1l1l11l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᆉ"): pytest.__version__ }, [bstack1l1l11l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᆊ")], self.bstack1lllll1llll_opy_, self.bstack1ll1lllll11_opy_)
            return
        try:
            import pytest
            self.test_framework = bstack1ll1l1111l1_opy_({ bstack1l1l11l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࠦᆋ"): pytest.__version__ }, [bstack1l1l11l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧᆌ")], self.bstack1lllll1llll_opy_, self.bstack1ll1lllll11_opy_)
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡼࡸࡪࡹࡴ࠻ࠢࠥᆍ") + str(e) + bstack1l1l11l_opy_ (u"ࠢࠣᆎ"))
        self.bstack1lll1111111_opy_()
    def bstack1lll1111111_opy_(self):
        if not self.bstack1lll11lll1_opy_():
            return
        bstack11lll1111_opy_ = None
        def bstack11ll1111ll_opy_(config, startdir):
            return bstack1l1l11l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨᆏ").format(bstack1l1l11l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᆐ"))
        def bstack1l1lll1l1l_opy_():
            return
        def bstack1llllllll_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack1l1l11l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪᆑ"):
                return bstack1l1l11l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥᆒ")
            else:
                return bstack11lll1111_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack11lll1111_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack11ll1111ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1lll1l1l_opy_
            Config.getoption = bstack1llllllll_opy_
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡸࡨ࡮ࠠࡱࡻࡷࡩࡸࡺࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡩࡳࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠿ࠦࠢᆓ") + str(e) + bstack1l1l11l_opy_ (u"ࠨࠢᆔ"))
    def bstack1ll1lll1ll1_opy_(self):
        bstack111lll1l_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack111lll1l_opy_, dict):
            if cli.config_observability:
                bstack111lll1l_opy_.update(
                    {bstack1l1l11l_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᆕ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack1l1l11l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࡢࡸࡴࡥࡷࡳࡣࡳࠦᆖ") in accessibility.get(bstack1l1l11l_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥᆗ"), {}):
                    bstack1lll1l1l1ll_opy_ = accessibility.get(bstack1l1l11l_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦᆘ"))
                    bstack1lll1l1l1ll_opy_.update({ bstack1l1l11l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠧᆙ"): bstack1lll1l1l1ll_opy_.pop(bstack1l1l11l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹ࡟ࡵࡱࡢࡻࡷࡧࡰࠣᆚ")) })
                bstack111lll1l_opy_.update({bstack1l1l11l_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᆛ"): accessibility })
        return bstack111lll1l_opy_
    @measure(event_name=EVENTS.bstack1ll1l1l1lll_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack1lll111l1l1_opy_(self, bstack1lll1llll11_opy_: str = None, bstack1ll1llllll1_opy_: str = None, exit_code: int = None):
        if not self.cli_bin_session_id or not self.bstack1ll1lllll11_opy_:
            return
        bstack1l11lll11_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if exit_code:
            req.exit_code = exit_code
        if bstack1lll1llll11_opy_:
            req.bstack1lll1llll11_opy_ = bstack1lll1llll11_opy_
        if bstack1ll1llllll1_opy_:
            req.bstack1ll1llllll1_opy_ = bstack1ll1llllll1_opy_
        try:
            r = self.bstack1ll1lllll11_opy_.StopBinSession(req)
            SDKCLI.automate_buildlink = r.automate_buildlink
            SDKCLI.hashed_id = r.hashed_id
            self.bstack11ll1l111_opy_(bstack1l1l11l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡴࡰࡲࡢࡦ࡮ࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᆜ"), datetime.now() - bstack1l11lll11_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack11ll1l111_opy_(self, key: str, value: timedelta):
        tag = bstack1l1l11l_opy_ (u"ࠣࡥ࡫࡭ࡱࡪ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᆝ") if self.bstack1ll1l11111_opy_() else bstack1l1l11l_opy_ (u"ࠤࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳࠣᆞ")
        self.bstack1lll1111ll1_opy_[bstack1l1l11l_opy_ (u"ࠥ࠾ࠧᆟ").join([tag + bstack1l1l11l_opy_ (u"ࠦ࠲ࠨᆠ") + str(id(self)), key])] += value
    def bstack1l1lll1ll_opy_(self):
        if not os.getenv(bstack1l1l11l_opy_ (u"ࠧࡊࡅࡃࡗࡊࡣࡕࡋࡒࡇࠤᆡ"), bstack1l1l11l_opy_ (u"ࠨ࠰ࠣᆢ")) == bstack1l1l11l_opy_ (u"ࠢ࠲ࠤᆣ"):
            return
        bstack1lll111lll1_opy_ = dict()
        bstack1lllll1l11l_opy_ = []
        if self.test_framework:
            bstack1lllll1l11l_opy_.extend(list(self.test_framework.bstack1lllll1l11l_opy_.values()))
        if self.bstack1lllll111ll_opy_:
            bstack1lllll1l11l_opy_.extend(list(self.bstack1lllll111ll_opy_.bstack1lllll1l11l_opy_.values()))
        for instance in bstack1lllll1l11l_opy_:
            if not instance.platform_index in bstack1lll111lll1_opy_:
                bstack1lll111lll1_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll111lll1_opy_[instance.platform_index]
            for k, v in instance.bstack1ll1lll1111_opy_().items():
                report[k] += v
                report[k.split(bstack1l1l11l_opy_ (u"ࠣ࠼ࠥᆤ"))[0]] += v
        bstack1lll11l11l1_opy_ = sorted([(k, v) for k, v in self.bstack1lll1111ll1_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1lll11lll11_opy_ = 0
        for r in bstack1lll11l11l1_opy_:
            bstack1ll1ll11lll_opy_ = r[1].total_seconds()
            bstack1lll11lll11_opy_ += bstack1ll1ll11lll_opy_
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡻࡳ࡝࠳ࡡࢂࡃࠢᆥ") + str(bstack1ll1ll11lll_opy_) + bstack1l1l11l_opy_ (u"ࠥࠦᆦ"))
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠦ࠲࠳ࠢᆧ"))
        bstack1lll1l1l1l1_opy_ = []
        for platform_index, report in bstack1lll111lll1_opy_.items():
            bstack1lll1l1l1l1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lll1l1l1l1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1l1llll1l1_opy_ = set()
        bstack1ll1l111ll1_opy_ = 0
        for r in bstack1lll1l1l1l1_opy_:
            bstack1ll1ll11lll_opy_ = r[2].total_seconds()
            bstack1ll1l111ll1_opy_ += bstack1ll1ll11lll_opy_
            bstack1l1llll1l1_opy_.add(r[0])
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡡࡰࡦࡴࡩࡡࠥࡺࡥࡴࡶ࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࠲ࢁࡲ࡜࠲ࡠࢁ࠿ࢁࡲ࡜࠳ࡠࢁࡂࠨᆨ") + str(bstack1ll1ll11lll_opy_) + bstack1l1l11l_opy_ (u"ࠨࠢᆩ"))
        if self.bstack1ll1l11111_opy_():
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠢ࠮࠯ࠥᆪ"))
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠣ࡝ࡳࡩࡷ࡬࡝ࠡࡥ࡯࡭࠿ࡩࡨࡪ࡮ࡧ࠱ࡵࡸ࡯ࡤࡧࡶࡷࡂࢁࡴࡰࡶࡤࡰࡤࡩ࡬ࡪࡿࠣࡸࡪࡹࡴ࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ࠱ࢀࡹࡴࡳࠪࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠮ࢃ࠽ࠣᆫ") + str(bstack1ll1l111ll1_opy_) + bstack1l1l11l_opy_ (u"ࠤࠥᆬ"))
        else:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺࡮ࡣ࡬ࡲ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࠢᆭ") + str(bstack1lll11lll11_opy_) + bstack1l1l11l_opy_ (u"ࠦࠧᆮ"))
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠧ࠳࠭ࠣᆯ"))
    def test_orchestration_session(self, test_files: list, orchestration_strategy: str, orchestration_metadata: str):
        request = structs.TestOrchestrationRequest(
            bin_session_id=self.cli_bin_session_id,
            orchestration_strategy=orchestration_strategy,
            test_files=test_files,
            orchestration_metadata=orchestration_metadata
        )
        if not self.bstack1ll1lllll11_opy_:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡣ࡭࡫ࡢࡷࡪࡸࡶࡪࡥࡨࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡇࡦࡴ࡮ࡰࡶࠣࡴࡪࡸࡦࡰࡴࡰࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥᆰ"))
            return None
        response = self.bstack1ll1lllll11_opy_.TestOrchestration(request)
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡵࡧࡶࡸ࠲ࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠲ࡹࡥࡴࡵ࡬ࡳࡳࡃࡻࡾࠤᆱ").format(response))
        if response.success:
            return list(response.ordered_test_files)
        return None
    def bstack1lll1l1lll1_opy_(self, r):
        if r is not None and getattr(r, bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࠩᆲ"), None) and getattr(r.testhub, bstack1l1l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᆳ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack1l1l11l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᆴ")))
            for bstack1ll1llll11l_opy_, err in errors.items():
                if err[bstack1l1l11l_opy_ (u"ࠫࡹࡿࡰࡦࠩᆵ")] == bstack1l1l11l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᆶ"):
                    self.logger.info(err[bstack1l1l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᆷ")])
                else:
                    self.logger.error(err[bstack1l1l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᆸ")])
    def bstack1111lll11_opy_(self):
        return SDKCLI.automate_buildlink, SDKCLI.hashed_id
cli = SDKCLI()
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
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1lllll1llll_opy_ import bstack1llllll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1llll111111_opy_, bstack1llll1llll1_opy_
class bstack1ll1lll111l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1l11l_opy_ (u"ࠣࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᘒ").format(self.name)
class bstack1lll1lll1ll_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l1l11l_opy_ (u"ࠤࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᘓ").format(self.name)
class bstack1lll1l11111_opy_(bstack1llll111111_opy_):
    bstack1l1llll1l1l_opy_: List[str]
    bstack11lll1ll1l1_opy_: Dict[str, str]
    state: bstack1lll1lll1ll_opy_
    bstack1llll11ll1l_opy_: datetime
    bstack1llll111l11_opy_: datetime
    def __init__(
        self,
        context: bstack1llll1llll1_opy_,
        bstack1l1llll1l1l_opy_: List[str],
        bstack11lll1ll1l1_opy_: Dict[str, str],
        state=bstack1lll1lll1ll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1llll1l1l_opy_ = bstack1l1llll1l1l_opy_
        self.bstack11lll1ll1l1_opy_ = bstack11lll1ll1l1_opy_
        self.state = state
        self.bstack1llll11ll1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llll111l11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llll11lll1_opy_(self, bstack1llll1l1lll_opy_: bstack1lll1lll1ll_opy_):
        bstack1llll11l1ll_opy_ = bstack1lll1lll1ll_opy_(bstack1llll1l1lll_opy_).name
        if not bstack1llll11l1ll_opy_:
            return False
        if bstack1llll1l1lll_opy_ == self.state:
            return False
        self.state = bstack1llll1l1lll_opy_
        self.bstack1llll111l11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack11llll111l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1l111l1l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1l11ll1l1_opy_: int = None
    bstack1l1l1ll1lll_opy_: str = None
    bstack11l111l_opy_: str = None
    bstack1lll1l1ll_opy_: str = None
    bstack1l1l11lll1l_opy_: str = None
    bstack11llll1l1ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll111111l1_opy_ = bstack1l1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨᘔ")
    bstack11lllll11l1_opy_ = bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᘕ")
    bstack1ll11l1l1ll_opy_ = bstack1l1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡲࡦࡳࡥࠣᘖ")
    bstack1l1111l1lll_opy_ = bstack1l1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠢᘗ")
    bstack1l1111lll11_opy_ = bstack1l1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡺࡡࡨࡵࠥᘘ")
    bstack1l11ll1111l_opy_ = bstack1l1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࠨᘙ")
    bstack1l1l1ll111l_opy_ = bstack1l1l11l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺ࡟ࡢࡶࠥᘚ")
    bstack1l1l1l11111_opy_ = bstack1l1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᘛ")
    bstack1l1ll11l1ll_opy_ = bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᘜ")
    bstack11lll1lllll_opy_ = bstack1l1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᘝ")
    bstack1ll11l11111_opy_ = bstack1l1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠧᘞ")
    bstack1l1l11l11l1_opy_ = bstack1l1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᘟ")
    bstack1l111111l1l_opy_ = bstack1l1l11l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡣࡰࡦࡨࠦᘠ")
    bstack1l1l111l111_opy_ = bstack1l1l11l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠦᘡ")
    bstack1l1llll1lll_opy_ = bstack1l1l11l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᘢ")
    bstack1l11ll11lll_opy_ = bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࠥᘣ")
    bstack11llll1l11l_opy_ = bstack1l1l11l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠤᘤ")
    bstack1l11111l11l_opy_ = bstack1l1l11l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡧࡴࠤᘥ")
    bstack11lllll1lll_opy_ = bstack1l1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡳࡥࡵࡣࠥᘦ")
    bstack11lll1l1l11_opy_ = bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡳࡤࡱࡳࡩࡸ࠭ᘧ")
    bstack1l111lll1ll_opy_ = bstack1l1l11l_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᘨ")
    bstack11llll1111l_opy_ = bstack1l1l11l_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᘩ")
    bstack1l1111111ll_opy_ = bstack1l1l11l_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᘪ")
    bstack11llllll11l_opy_ = bstack1l1l11l_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢ࡭ࡩࠨᘫ")
    bstack1l1111l1ll1_opy_ = bstack1l1l11l_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷ࡫ࡳࡶ࡮ࡷࠦᘬ")
    bstack11llll1l111_opy_ = bstack1l1l11l_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡲ࡯ࡨࡵࠥᘭ")
    bstack1l1111ll11l_opy_ = bstack1l1l11l_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠦᘮ")
    bstack1l111l11111_opy_ = bstack1l1l11l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᘯ")
    bstack1l111111l11_opy_ = bstack1l1l11l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᘰ")
    bstack1l111l1l1ll_opy_ = bstack1l1l11l_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᘱ")
    bstack1l1111l11ll_opy_ = bstack1l1l11l_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᘲ")
    bstack1l1l11ll11l_opy_ = bstack1l1l11l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠣᘳ")
    bstack1l1l11ll1ll_opy_ = bstack1l1l11l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡒࡏࡈࠤᘴ")
    bstack1l1ll11ll11_opy_ = bstack1l1l11l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᘵ")
    bstack1lllll1l11l_opy_: Dict[str, bstack1lll1l11111_opy_] = dict()
    bstack11lll11llll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1llll1l1l_opy_: List[str]
    bstack11lll1ll1l1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1llll1l1l_opy_: List[str],
        bstack11lll1ll1l1_opy_: Dict[str, str],
        bstack1lllll1llll_opy_: bstack1llllll11ll_opy_
    ):
        self.bstack1l1llll1l1l_opy_ = bstack1l1llll1l1l_opy_
        self.bstack11lll1ll1l1_opy_ = bstack11lll1ll1l1_opy_
        self.bstack1lllll1llll_opy_ = bstack1lllll1llll_opy_
    def track_event(
        self,
        context: bstack11llll111l1_opy_,
        test_framework_state: bstack1lll1lll1ll_opy_,
        test_hook_state: bstack1ll1lll111l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࢂࠨᘶ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11lll1ll1ll_opy_(
        self,
        instance: bstack1lll1l11111_opy_,
        bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l111l1ll1l_opy_ = TestFramework.bstack1l111ll11l1_opy_(bstack1llll1l1ll1_opy_)
        if not bstack1l111l1ll1l_opy_ in TestFramework.bstack11lll11llll_opy_:
            return
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠥ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࢁࡽࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠦᘷ").format(len(TestFramework.bstack11lll11llll_opy_[bstack1l111l1ll1l_opy_])))
        for callback in TestFramework.bstack11lll11llll_opy_[bstack1l111l1ll1l_opy_]:
            try:
                callback(self, instance, bstack1llll1l1ll1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1l11l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠦᘸ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1l1lll111_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1l1l11lll_opy_(self, instance, bstack1llll1l1ll1_opy_):
        return
    @abc.abstractmethod
    def bstack1l1l1l1l1ll_opy_(self, instance, bstack1llll1l1ll1_opy_):
        return
    @staticmethod
    def bstack1llll111l1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1llll111111_opy_.create_context(target)
        instance = TestFramework.bstack1lllll1l11l_opy_.get(ctx.id, None)
        if instance and instance.bstack1lllll1ll1l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1l11l1lll_opy_(reverse=True) -> List[bstack1lll1l11111_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllll1l11l_opy_.values(),
            ),
            key=lambda t: t.bstack1llll11ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llll111lll_opy_(ctx: bstack1llll1llll1_opy_, reverse=True) -> List[bstack1lll1l11111_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllll1l11l_opy_.values(),
            ),
            key=lambda t: t.bstack1llll11ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llll1ll1l1_opy_(instance: bstack1lll1l11111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llll11ll11_opy_(instance: bstack1lll1l11111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llll11lll1_opy_(instance: bstack1lll1l11111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤᘹ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11111llll_opy_(instance: bstack1lll1l11111_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡲࡹࡸࡩࡦࡵࡀࡿࢂࠨᘺ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11lll11l11l_opy_(instance: bstack1lll1lll1ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᘻ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1llll111l1l_opy_(target, strict)
        return TestFramework.bstack1llll11ll11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1llll111l1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1111ll1l1_opy_(instance: bstack1lll1l11111_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11lll1llll1_opy_(instance: bstack1lll1l11111_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l111ll11l1_opy_(bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_]):
        return bstack1l1l11l_opy_ (u"ࠣ࠼ࠥᘼ").join((bstack1lll1lll1ll_opy_(bstack1llll1l1ll1_opy_[0]).name, bstack1ll1lll111l_opy_(bstack1llll1l1ll1_opy_[1]).name))
    @staticmethod
    def bstack1ll1111ll1l_opy_(bstack1llll1l1ll1_opy_: Tuple[bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_], callback: Callable):
        bstack1l111l1ll1l_opy_ = TestFramework.bstack1l111ll11l1_opy_(bstack1llll1l1ll1_opy_)
        TestFramework.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡶࡩࡹࡥࡨࡰࡱ࡮ࡣࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡩࡱࡲ࡯ࡤࡸࡥࡨ࡫ࡶࡸࡷࡿ࡟࡬ࡧࡼࡁࢀࢃࠢᘽ").format(bstack1l111l1ll1l_opy_))
        if not bstack1l111l1ll1l_opy_ in TestFramework.bstack11lll11llll_opy_:
            TestFramework.bstack11lll11llll_opy_[bstack1l111l1ll1l_opy_] = []
        TestFramework.bstack11lll11llll_opy_[bstack1l111l1ll1l_opy_].append(callback)
    @staticmethod
    def bstack1l1ll11l1l1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡵ࡫ࡱࡷࠧᘾ"):
            return klass.__qualname__
        return module + bstack1l1l11l_opy_ (u"ࠦ࠳ࠨᘿ") + klass.__qualname__
    @staticmethod
    def bstack1l1ll111111_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}
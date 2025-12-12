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
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1llll1llll1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1llll111111_opy_:
    bstack11lll11l111_opy_ = bstack1l1l11l_opy_ (u"ࠧࡨࡥ࡯ࡥ࡫ࡱࡦࡸ࡫ࠣᙀ")
    context: bstack1llll1llll1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1llll1llll1_opy_):
        self.context = context
        self.data = dict({bstack1llll111111_opy_.bstack11lll11l111_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᙁ"), bstack1l1l11l_opy_ (u"ࠧ࠱ࠩᙂ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack1lllll1ll1l_opy_(self, target: object):
        return bstack1llll111111_opy_.create_context(target) == self.context
    def bstack1l1ll1llll1_opy_(self, context: bstack1llll1llll1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack11ll1l111_opy_(self, key: str, value: timedelta):
        self.data[bstack1llll111111_opy_.bstack11lll11l111_opy_][key] += value
    def bstack1ll1lll1111_opy_(self) -> dict:
        return self.data[bstack1llll111111_opy_.bstack11lll11l111_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1llll1llll1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )
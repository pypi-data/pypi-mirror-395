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
import threading
from collections import deque
from bstack_utils.constants import *
class bstack111l11l1l_opy_:
    def __init__(self):
        self._1lllll1lll11_opy_ = deque()
        self._1llllll111ll_opy_ = {}
        self._1llllll11l1l_opy_ = False
        self._lock = threading.RLock()
    def bstack1lllll1llll1_opy_(self, test_name, bstack1llllll11111_opy_):
        with self._lock:
            bstack1llllll111l1_opy_ = self._1llllll111ll_opy_.get(test_name, {})
            return bstack1llllll111l1_opy_.get(bstack1llllll11111_opy_, 0)
    def bstack1llllll1111l_opy_(self, test_name, bstack1llllll11111_opy_):
        with self._lock:
            bstack1lllll1ll1ll_opy_ = self.bstack1lllll1llll1_opy_(test_name, bstack1llllll11111_opy_)
            self.bstack1llllll11l11_opy_(test_name, bstack1llllll11111_opy_)
            return bstack1lllll1ll1ll_opy_
    def bstack1llllll11l11_opy_(self, test_name, bstack1llllll11111_opy_):
        with self._lock:
            if test_name not in self._1llllll111ll_opy_:
                self._1llllll111ll_opy_[test_name] = {}
            bstack1llllll111l1_opy_ = self._1llllll111ll_opy_[test_name]
            bstack1lllll1ll1ll_opy_ = bstack1llllll111l1_opy_.get(bstack1llllll11111_opy_, 0)
            bstack1llllll111l1_opy_[bstack1llllll11111_opy_] = bstack1lllll1ll1ll_opy_ + 1
    def bstack111lllll_opy_(self, bstack1llllll11ll1_opy_, bstack1lllll1ll1l1_opy_):
        bstack1lllll1lllll_opy_ = self.bstack1llllll1111l_opy_(bstack1llllll11ll1_opy_, bstack1lllll1ll1l1_opy_)
        event_name = bstack11l1l11l11l_opy_[bstack1lllll1ll1l1_opy_]
        bstack1l1l111ll11_opy_ = bstack1l1l11l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤ‶").format(bstack1llllll11ll1_opy_, event_name, bstack1lllll1lllll_opy_)
        with self._lock:
            self._1lllll1lll11_opy_.append(bstack1l1l111ll11_opy_)
    def bstack1ll1l1ll11_opy_(self):
        with self._lock:
            return len(self._1lllll1lll11_opy_) == 0
    def bstack1ll1l111_opy_(self):
        with self._lock:
            if self._1lllll1lll11_opy_:
                bstack1lllll1lll1l_opy_ = self._1lllll1lll11_opy_.popleft()
                return bstack1lllll1lll1l_opy_
            return None
    def capturing(self):
        with self._lock:
            return self._1llllll11l1l_opy_
    def bstack111lllllll_opy_(self):
        with self._lock:
            self._1llllll11l1l_opy_ = True
    def bstack1lll1ll11l_opy_(self):
        with self._lock:
            self._1llllll11l1l_opy_ = False
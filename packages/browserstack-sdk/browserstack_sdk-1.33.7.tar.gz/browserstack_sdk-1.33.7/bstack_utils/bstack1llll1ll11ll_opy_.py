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
import logging
logger = logging.getLogger(__name__)
bstack1llll1lll1ll_opy_ = 1000
bstack1llll1lll111_opy_ = 2
class bstack1llll1lll1l1_opy_:
    def __init__(self, handler, bstack1llll1ll1l11_opy_=bstack1llll1lll1ll_opy_, bstack1llll1ll1l1l_opy_=bstack1llll1lll111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1llll1ll1l11_opy_ = bstack1llll1ll1l11_opy_
        self.bstack1llll1ll1l1l_opy_ = bstack1llll1ll1l1l_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1llllll1111_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1llll1ll1ll1_opy_()
    def bstack1llll1ll1ll1_opy_(self):
        self.bstack1llllll1111_opy_ = threading.Event()
        def bstack1llll1lll11l_opy_():
            self.bstack1llllll1111_opy_.wait(self.bstack1llll1ll1l1l_opy_)
            if not self.bstack1llllll1111_opy_.is_set():
                self.bstack1llll1llll11_opy_()
        self.timer = threading.Thread(target=bstack1llll1lll11l_opy_, daemon=True)
        self.timer.start()
    def bstack1llll1ll1lll_opy_(self):
        try:
            if self.bstack1llllll1111_opy_ and not self.bstack1llllll1111_opy_.is_set():
                self.bstack1llllll1111_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠪ࡟ࡸࡺ࡯ࡱࡡࡷ࡭ࡲ࡫ࡲ࡞ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࠧ₩") + (str(e) or bstack1l1l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡣࡰࡰࡹࡩࡷࡺࡥࡥࠢࡷࡳࠥࡹࡴࡳ࡫ࡱ࡫ࠧ₪")))
        finally:
            self.timer = None
    def bstack1llll1ll11l1_opy_(self):
        if self.timer:
            self.bstack1llll1ll1lll_opy_()
        self.bstack1llll1ll1ll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1llll1ll1l11_opy_:
                threading.Thread(target=self.bstack1llll1llll11_opy_).start()
    def bstack1llll1llll11_opy_(self, source = bstack1l1l11l_opy_ (u"ࠬ࠭₫")):
        with self.lock:
            if not self.queue:
                self.bstack1llll1ll11l1_opy_()
                return
            data = self.queue[:self.bstack1llll1ll1l11_opy_]
            del self.queue[:self.bstack1llll1ll1l11_opy_]
        self.handler(data)
        if source != bstack1l1l11l_opy_ (u"࠭ࡳࡩࡷࡷࡨࡴࡽ࡮ࠨ€"):
            self.bstack1llll1ll11l1_opy_()
    def shutdown(self):
        self.bstack1llll1ll1lll_opy_()
        while self.queue:
            self.bstack1llll1llll11_opy_(source=bstack1l1l11l_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩ₭"))
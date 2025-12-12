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
import builtins
import logging
class bstack111ll11111_opy_:
    def __init__(self, handler):
        self._11l1l1l111l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11l1l1l1l11_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1l11l_opy_ (u"ࠧࡪࡰࡩࡳࠬᡖ"), bstack1l1l11l_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᡗ"), bstack1l1l11l_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᡘ"), bstack1l1l11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᡙ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11l1l1l11ll_opy_
        self._11l1l1l1l1l_opy_()
    def _11l1l1l11ll_opy_(self, *args, **kwargs):
        self._11l1l1l111l_opy_(*args, **kwargs)
        message = bstack1l1l11l_opy_ (u"ࠫࠥ࠭ᡚ").join(map(str, args)) + bstack1l1l11l_opy_ (u"ࠬࡢ࡮ࠨᡛ")
        self._log_message(bstack1l1l11l_opy_ (u"࠭ࡉࡏࡈࡒࠫᡜ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1l11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᡝ"): level, bstack1l1l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᡞ"): msg})
    def _11l1l1l1l1l_opy_(self):
        for level, bstack11l1l1l11l1_opy_ in self._11l1l1l1l11_opy_.items():
            setattr(logging, level, self._11l1l1l1111_opy_(level, bstack11l1l1l11l1_opy_))
    def _11l1l1l1111_opy_(self, level, bstack11l1l1l11l1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11l1l1l11l1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11l1l1l111l_opy_
        for level, bstack11l1l1l11l1_opy_ in self._11l1l1l1l11_opy_.items():
            setattr(logging, level, bstack11l1l1l11l1_opy_)
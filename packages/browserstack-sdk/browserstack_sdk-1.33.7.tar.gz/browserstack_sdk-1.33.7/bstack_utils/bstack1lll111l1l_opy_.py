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
class bstack111lll1lll_opy_:
    def __init__(self, handler):
        self._1llll1l11l1l_opy_ = None
        self.handler = handler
        self._1llll1l11ll1_opy_ = self.bstack1llll1l11l11_opy_()
        self.patch()
    def patch(self):
        self._1llll1l11l1l_opy_ = self._1llll1l11ll1_opy_.execute
        self._1llll1l11ll1_opy_.execute = self.bstack1llll1l11lll_opy_()
    def bstack1llll1l11lll_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1l11l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨ⃹"), driver_command, None, this, args)
            response = self._1llll1l11l1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1l11l_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨ⃺"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1l11ll1_opy_.execute = self._1llll1l11l1l_opy_
    @staticmethod
    def bstack1llll1l11l11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver
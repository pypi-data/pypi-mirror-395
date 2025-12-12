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
class RobotHandler():
    def __init__(self, args, logger, bstack11111l1ll1_opy_, bstack11111ll1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11111l1ll1_opy_ = bstack11111l1ll1_opy_
        self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1111l1l11l_opy_(bstack1llllll1l1l_opy_):
        bstack1llllll1lll_opy_ = []
        if bstack1llllll1l1l_opy_:
            tokens = str(os.path.basename(bstack1llllll1l1l_opy_)).split(bstack1l1l11l_opy_ (u"ࠣࡡࠥკ"))
            camelcase_name = bstack1l1l11l_opy_ (u"ࠤࠣࠦლ").join(t.title() for t in tokens)
            suite_name, bstack1lllllll111_opy_ = os.path.splitext(camelcase_name)
            bstack1llllll1lll_opy_.append(suite_name)
        return bstack1llllll1lll_opy_
    @staticmethod
    def bstack1llllll1ll1_opy_(typename):
        if bstack1l1l11l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨმ") in typename:
            return bstack1l1l11l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧნ")
        return bstack1l1l11l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨო")
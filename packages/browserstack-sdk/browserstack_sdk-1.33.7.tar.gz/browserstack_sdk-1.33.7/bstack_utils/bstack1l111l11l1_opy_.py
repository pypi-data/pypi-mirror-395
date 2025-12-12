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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l1l1ll1ll_opy_ import bstack11l1l1lll1l_opy_
from bstack_utils.constants import *
import json
class bstack11l1llll1_opy_:
    def __init__(self, bstack1lll1l1ll_opy_, bstack11l1l1ll11l_opy_):
        self.bstack1lll1l1ll_opy_ = bstack1lll1l1ll_opy_
        self.bstack11l1l1ll11l_opy_ = bstack11l1l1ll11l_opy_
        self.bstack11l1l1llll1_opy_ = None
    def __call__(self):
        bstack11l1l1lll11_opy_ = {}
        while True:
            self.bstack11l1l1llll1_opy_ = bstack11l1l1lll11_opy_.get(
                bstack1l1l11l_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᡃ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l1l1ll1l1_opy_ = self.bstack11l1l1llll1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l1l1ll1l1_opy_ > 0:
                sleep(bstack11l1l1ll1l1_opy_ / 1000)
            params = {
                bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᡄ"): self.bstack1lll1l1ll_opy_,
                bstack1l1l11l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᡅ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l1l1l1lll_opy_ = bstack1l1l11l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᡆ") + bstack11l1l1ll111_opy_ + bstack1l1l11l_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥᡇ")
            if self.bstack11l1l1ll11l_opy_.lower() == bstack1l1l11l_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣᡈ"):
                bstack11l1l1lll11_opy_ = bstack11l1l1lll1l_opy_.results(bstack11l1l1l1lll_opy_, params)
            else:
                bstack11l1l1lll11_opy_ = bstack11l1l1lll1l_opy_.bstack11l1l1l1ll1_opy_(bstack11l1l1l1lll_opy_, params)
            if str(bstack11l1l1lll11_opy_.get(bstack1l1l11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᡉ"), bstack1l1l11l_opy_ (u"ࠩ࠵࠴࠵࠭ᡊ"))) != bstack1l1l11l_opy_ (u"ࠪ࠸࠵࠺ࠧᡋ"):
                break
        return bstack11l1l1lll11_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡩࡧࡴࡢࠩᡌ"), bstack11l1l1lll11_opy_)
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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll11l1l1l_opy_, bstack11lllllll_opy_, bstack111111l11_opy_, bstack111l1lll_opy_, \
    bstack11ll11l11ll_opy_
from bstack_utils.measure import measure
def bstack1l1l1ll11_opy_(bstack11ll11l1ll1_opy_):
    for driver in bstack11ll11l1ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11l1ll1l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
def bstack1ll1l1ll_opy_(driver, status, reason=bstack1l1l11l_opy_ (u"࠭ࠧᚸ")):
    bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
    if bstack1ll1l111l1_opy_.bstack111111l1l1_opy_():
        return
    bstack1l1l1ll1_opy_ = bstack1l1ll111_opy_(bstack1l1l11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᚹ"), bstack1l1l11l_opy_ (u"ࠨࠩᚺ"), status, reason, bstack1l1l11l_opy_ (u"ࠩࠪᚻ"), bstack1l1l11l_opy_ (u"ࠪࠫᚼ"))
    driver.execute_script(bstack1l1l1ll1_opy_)
@measure(event_name=EVENTS.bstack1l11l1ll1l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
def bstack1lll11l1l1_opy_(page, status, reason=bstack1l1l11l_opy_ (u"ࠫࠬᚽ")):
    try:
        if page is None:
            return
        bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
        if bstack1ll1l111l1_opy_.bstack111111l1l1_opy_():
            return
        bstack1l1l1ll1_opy_ = bstack1l1ll111_opy_(bstack1l1l11l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᚾ"), bstack1l1l11l_opy_ (u"࠭ࠧᚿ"), status, reason, bstack1l1l11l_opy_ (u"ࠧࠨᛀ"), bstack1l1l11l_opy_ (u"ࠨࠩᛁ"))
        page.evaluate(bstack1l1l11l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᛂ"), bstack1l1l1ll1_opy_)
    except Exception as e:
        print(bstack1l1l11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࢁࡽࠣᛃ"), e)
def bstack1l1ll111_opy_(type, name, status, reason, bstack11lll1llll_opy_, bstack1ll11l111l_opy_):
    bstack1l11lllll1_opy_ = {
        bstack1l1l11l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫᛄ"): type,
        bstack1l1l11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᛅ"): {}
    }
    if type == bstack1l1l11l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨᛆ"):
        bstack1l11lllll1_opy_[bstack1l1l11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᛇ")][bstack1l1l11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᛈ")] = bstack11lll1llll_opy_
        bstack1l11lllll1_opy_[bstack1l1l11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᛉ")][bstack1l1l11l_opy_ (u"ࠪࡨࡦࡺࡡࠨᛊ")] = json.dumps(str(bstack1ll11l111l_opy_))
    if type == bstack1l1l11l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᛋ"):
        bstack1l11lllll1_opy_[bstack1l1l11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᛌ")][bstack1l1l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᛍ")] = name
    if type == bstack1l1l11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᛎ"):
        bstack1l11lllll1_opy_[bstack1l1l11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᛏ")][bstack1l1l11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᛐ")] = status
        if status == bstack1l1l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᛑ") and str(reason) != bstack1l1l11l_opy_ (u"ࠦࠧᛒ"):
            bstack1l11lllll1_opy_[bstack1l1l11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᛓ")][bstack1l1l11l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ᛔ")] = json.dumps(str(reason))
    bstack1ll11l1lll_opy_ = bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬᛕ").format(json.dumps(bstack1l11lllll1_opy_))
    return bstack1ll11l1lll_opy_
def bstack11llllllll_opy_(url, config, logger, bstack1l1l111l1l_opy_=False):
    hostname = bstack11lllllll_opy_(url)
    is_private = bstack111l1lll_opy_(hostname)
    try:
        if is_private or bstack1l1l111l1l_opy_:
            file_path = bstack11ll11l1l1l_opy_(bstack1l1l11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᛖ"), bstack1l1l11l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᛗ"), logger)
            if os.environ.get(bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᛘ")) and eval(
                    os.environ.get(bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᛙ"))):
                return
            if (bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᛚ") in config and not config[bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᛛ")]):
                os.environ[bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᛜ")] = str(True)
                bstack11ll11l1lll_opy_ = {bstack1l1l11l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪᛝ"): hostname}
                bstack11ll11l11ll_opy_(bstack1l1l11l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨᛞ"), bstack1l1l11l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨᛟ"), bstack11ll11l1lll_opy_, logger)
    except Exception as e:
        pass
def bstack11l1l1llll_opy_(caps, bstack11ll11l111l_opy_):
    if bstack1l1l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᛠ") in caps:
        caps[bstack1l1l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᛡ")][bstack1l1l11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬᛢ")] = True
        if bstack11ll11l111l_opy_:
            caps[bstack1l1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᛣ")][bstack1l1l11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᛤ")] = bstack11ll11l111l_opy_
    else:
        caps[bstack1l1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧᛥ")] = True
        if bstack11ll11l111l_opy_:
            caps[bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᛦ")] = bstack11ll11l111l_opy_
def bstack11ll11l1l11_opy_(bstack1111ll1ll1_opy_):
    bstack11ll11l11l1_opy_ = bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᛧ"), bstack1l1l11l_opy_ (u"ࠬ࠭ᛨ"))
    if bstack11ll11l11l1_opy_ == bstack1l1l11l_opy_ (u"࠭ࠧᛩ") or bstack11ll11l11l1_opy_ == bstack1l1l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᛪ"):
        threading.current_thread().testStatus = bstack1111ll1ll1_opy_
    else:
        if bstack1111ll1ll1_opy_ == bstack1l1l11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᛫"):
            threading.current_thread().testStatus = bstack1111ll1ll1_opy_
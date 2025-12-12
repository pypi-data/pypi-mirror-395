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
from browserstack_sdk.bstack1ll1l11l1_opy_ import bstack11ll111111_opy_
from browserstack_sdk.bstack111l111111_opy_ import RobotHandler
def bstack1lll1ll1l1_opy_(framework):
    if framework.lower() == bstack1l1l11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᯙ"):
        return bstack11ll111111_opy_.version()
    elif framework.lower() == bstack1l1l11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᯚ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1l11l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᯛ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1l11l_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧᯜ")
def bstack11l1l11ll1_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1l11l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᯝ"))
        framework_version.append(importlib.metadata.version(bstack1l1l11l_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯ࠥᯞ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᯟ"))
        framework_version.append(importlib.metadata.version(bstack1l1l11l_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᯠ")))
    except:
        pass
    return {
        bstack1l1l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᯡ"): bstack1l1l11l_opy_ (u"ࠬࡥࠧᯢ").join(framework_name),
        bstack1l1l11l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᯣ"): bstack1l1l11l_opy_ (u"ࠧࡠࠩᯤ").join(framework_version)
    }
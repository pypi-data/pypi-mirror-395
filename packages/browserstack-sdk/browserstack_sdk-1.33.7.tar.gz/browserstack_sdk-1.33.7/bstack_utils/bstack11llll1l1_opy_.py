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
import re
from bstack_utils.bstack1111l11l_opy_ import bstack11ll11l1l11_opy_
def bstack1lllll11111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⁶")):
        return bstack1l1l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ⁷")
    elif fixture_name.startswith(bstack1l1l11l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⁸")):
        return bstack1l1l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⁹")
    elif fixture_name.startswith(bstack1l1l11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⁺")):
        return bstack1l1l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪ⁻")
    elif fixture_name.startswith(bstack1l1l11l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⁼")):
        return bstack1l1l11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ⁽")
def bstack1llll1lllll1_opy_(fixture_name):
    return bool(re.match(bstack1l1l11l_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧ⁾"), fixture_name))
def bstack1lllll111l11_opy_(fixture_name):
    return bool(re.match(bstack1l1l11l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫⁿ"), fixture_name))
def bstack1lllll11l111_opy_(fixture_name):
    return bool(re.match(bstack1l1l11l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫ₀"), fixture_name))
def bstack1lllll111ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1l11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ₁")):
        return bstack1l1l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ₂"), bstack1l1l11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ₃")
    elif fixture_name.startswith(bstack1l1l11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ₄")):
        return bstack1l1l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨ₅"), bstack1l1l11l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ₆")
    elif fixture_name.startswith(bstack1l1l11l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ₇")):
        return bstack1l1l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ₈"), bstack1l1l11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ₉")
    elif fixture_name.startswith(bstack1l1l11l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ₊")):
        return bstack1l1l11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪ₋"), bstack1l1l11l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ₌")
    return None, None
def bstack1lllll1111l1_opy_(hook_name):
    if hook_name in [bstack1l1l11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ₍"), bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭₎")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lllll1111ll_opy_(hook_name):
    if hook_name in [bstack1l1l11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭₏"), bstack1l1l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬₐ")]:
        return bstack1l1l11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬₑ")
    elif hook_name in [bstack1l1l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧₒ"), bstack1l1l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧₓ")]:
        return bstack1l1l11l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧₔ")
    elif hook_name in [bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨₕ"), bstack1l1l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧₖ")]:
        return bstack1l1l11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪₗ")
    elif hook_name in [bstack1l1l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩₘ"), bstack1l1l11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩₙ")]:
        return bstack1l1l11l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬₚ")
    return hook_name
def bstack1lllll111111_opy_(node, scenario):
    if hasattr(node, bstack1l1l11l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬₛ")):
        parts = node.nodeid.rsplit(bstack1l1l11l_opy_ (u"ࠦࡠࠨₜ"))
        params = parts[-1]
        return bstack1l1l11l_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧ₝").format(scenario.name, params)
    return scenario.name
def bstack11ll11lllll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1l11l_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨ₞")):
            examples = list(node.callspec.params[bstack1l1l11l_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭₟")].values())
        return examples
    except:
        return []
def bstack1lllll111lll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llll1llllll_opy_(report):
    try:
        status = bstack1l1l11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ₠")
        if report.passed or (report.failed and hasattr(report, bstack1l1l11l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦ₡"))):
            status = bstack1l1l11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ₢")
        elif report.skipped:
            status = bstack1l1l11l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ₣")
        bstack11ll11l1l11_opy_(status)
    except:
        pass
def bstack111lll1ll1_opy_(status):
    try:
        bstack1lllll111l1l_opy_ = bstack1l1l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ₤")
        if status == bstack1l1l11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭₥"):
            bstack1lllll111l1l_opy_ = bstack1l1l11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ₦")
        elif status == bstack1l1l11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ₧"):
            bstack1lllll111l1l_opy_ = bstack1l1l11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ₨")
        bstack11ll11l1l11_opy_(bstack1lllll111l1l_opy_)
    except:
        pass
def bstack1llll1llll1l_opy_(item=None, report=None, summary=None, extra=None):
    return
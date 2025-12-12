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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll111l1l1_opy_, bstack1lll11ll11_opy_, get_host_info, bstack111l1l11111_opy_, \
 bstack1lll11lll1_opy_, bstack111111l11_opy_, error_handler, bstack11l11111l1l_opy_, bstack11l1lllll_opy_
import bstack_utils.accessibility as bstack11ll1lllll_opy_
from bstack_utils.bstack111l1l1ll_opy_ import bstack1llllll111_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11l11l1l1l_opy_
from bstack_utils.percy import bstack11l1111ll_opy_
from bstack_utils.config import Config
bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
logger = logging.getLogger(__name__)
percy = bstack11l1111ll_opy_()
@error_handler(class_method=False)
def bstack1llll11l111l_opy_(bs_config, bstack1l1111lll1_opy_):
  try:
    data = {
        bstack1l1l11l_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ∽"): bstack1l1l11l_opy_ (u"ࠩ࡭ࡷࡴࡴࠧ∾"),
        bstack1l1l11l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩ∿"): bs_config.get(bstack1l1l11l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ≀"), bstack1l1l11l_opy_ (u"ࠬ࠭≁")),
        bstack1l1l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ≂"): bs_config.get(bstack1l1l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ≃"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ≄"): bs_config.get(bstack1l1l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ≅")),
        bstack1l1l11l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ≆"): bs_config.get(bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ≇"), bstack1l1l11l_opy_ (u"ࠬ࠭≈")),
        bstack1l1l11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ≉"): bstack11l1lllll_opy_(),
        bstack1l1l11l_opy_ (u"ࠧࡵࡣࡪࡷࠬ≊"): bstack111l1l11111_opy_(bs_config),
        bstack1l1l11l_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ≋"): get_host_info(),
        bstack1l1l11l_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ≌"): bstack1lll11ll11_opy_(),
        bstack1l1l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ≍"): os.environ.get(bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ≎")),
        bstack1l1l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪ≏"): os.environ.get(bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ≐"), False),
        bstack1l1l11l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ≑"): bstack11ll111l1l1_opy_(),
        bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ≒"): bstack1lll1ll1lll1_opy_(bs_config),
        bstack1l1l11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭≓"): bstack1lll1lll11ll_opy_(bstack1l1111lll1_opy_),
        bstack1l1l11l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ≔"): bstack1lll1lll11l1_opy_(bs_config, bstack1l1111lll1_opy_.get(bstack1l1l11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ≕"), bstack1l1l11l_opy_ (u"ࠬ࠭≖"))),
        bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ≗"): bstack1lll11lll1_opy_(bs_config),
        bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬ≘"): bstack1lll1lll1111_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1l1l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ≙").format(str(error)))
    return None
def bstack1lll1lll11ll_opy_(framework):
  return {
    bstack1l1l11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ≚"): framework.get(bstack1l1l11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ≛"), bstack1l1l11l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ≜")),
    bstack1l1l11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ≝"): framework.get(bstack1l1l11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ≞")),
    bstack1l1l11l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ≟"): framework.get(bstack1l1l11l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭≠")),
    bstack1l1l11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ≡"): bstack1l1l11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ≢"),
    bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ≣"): framework.get(bstack1l1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ≤"))
  }
def bstack1lll1lll1111_opy_(bs_config):
  bstack1l1l11l_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡵࡷࡥࡷࡺ࠮ࠋࠢࠣࠦࠧࠨ≥")
  if not bs_config:
    return {}
  bstack1111l1l1lll_opy_ = bstack1llllll111_opy_(bs_config).bstack1111l11ll11_opy_(bs_config)
  return bstack1111l1l1lll_opy_
def bstack1l1111lll_opy_(bs_config, framework):
  bstack1ll1ll1l1_opy_ = False
  bstack11l111111l_opy_ = False
  bstack1lll1lll1lll_opy_ = False
  if bstack1l1l11l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ≦") in bs_config:
    bstack1lll1lll1lll_opy_ = True
  elif bstack1l1l11l_opy_ (u"ࠨࡣࡳࡴࠬ≧") in bs_config:
    bstack1ll1ll1l1_opy_ = True
  else:
    bstack11l111111l_opy_ = True
  bstack11l11l11_opy_ = {
    bstack1l1l11l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ≨"): bstack11l11l1l1l_opy_.bstack1lll1ll1ll1l_opy_(bs_config, framework),
    bstack1l1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ≩"): bstack11ll1lllll_opy_.bstack1ll1l1111_opy_(bs_config),
    bstack1l1l11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ≪"): bs_config.get(bstack1l1l11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ≫"), False),
    bstack1l1l11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ≬"): bstack11l111111l_opy_,
    bstack1l1l11l_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭≭"): bstack1ll1ll1l1_opy_,
    bstack1l1l11l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ≮"): bstack1lll1lll1lll_opy_
  }
  return bstack11l11l11_opy_
@error_handler(class_method=False)
def bstack1lll1ll1lll1_opy_(bs_config):
  try:
    bstack1lll1lll111l_opy_ = json.loads(os.getenv(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ≯"), bstack1l1l11l_opy_ (u"ࠪࡿࢂ࠭≰")))
    bstack1lll1lll111l_opy_ = bstack1lll1lll1l1l_opy_(bs_config, bstack1lll1lll111l_opy_)
    return {
        bstack1l1l11l_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭≱"): bstack1lll1lll111l_opy_
    }
  except Exception as error:
    logger.error(bstack1l1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ≲").format(str(error)))
    return {}
def bstack1lll1lll1l1l_opy_(bs_config, bstack1lll1lll111l_opy_):
  if ((bstack1l1l11l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ≳") in bs_config or not bstack1lll11lll1_opy_(bs_config)) and bstack11ll1lllll_opy_.bstack1ll1l1111_opy_(bs_config)):
    bstack1lll1lll111l_opy_[bstack1l1l11l_opy_ (u"ࠢࡪࡰࡦࡰࡺࡪࡥࡆࡰࡦࡳࡩ࡫ࡤࡆࡺࡷࡩࡳࡹࡩࡰࡰࠥ≴")] = True
  return bstack1lll1lll111l_opy_
def bstack1llll111l111_opy_(array, bstack1lll1lll1l11_opy_, bstack1lll1llll111_opy_):
  result = {}
  for o in array:
    key = o[bstack1lll1lll1l11_opy_]
    result[key] = o[bstack1lll1llll111_opy_]
  return result
def bstack1llll1111111_opy_(bstack1l1l1l11ll_opy_=bstack1l1l11l_opy_ (u"ࠨࠩ≵")):
  bstack1lll1ll1llll_opy_ = bstack11ll1lllll_opy_.on()
  bstack1lll1lll1ll1_opy_ = bstack11l11l1l1l_opy_.on()
  bstack1lll1ll1ll11_opy_ = percy.bstack11lllll1_opy_()
  if bstack1lll1ll1ll11_opy_ and not bstack1lll1lll1ll1_opy_ and not bstack1lll1ll1llll_opy_:
    return bstack1l1l1l11ll_opy_ not in [bstack1l1l11l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭≶"), bstack1l1l11l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ≷")]
  elif bstack1lll1ll1llll_opy_ and not bstack1lll1lll1ll1_opy_:
    return bstack1l1l1l11ll_opy_ not in [bstack1l1l11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ≸"), bstack1l1l11l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ≹"), bstack1l1l11l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ≺")]
  return bstack1lll1ll1llll_opy_ or bstack1lll1lll1ll1_opy_ or bstack1lll1ll1ll11_opy_
@error_handler(class_method=False)
def bstack1llll111111l_opy_(bstack1l1l1l11ll_opy_, test=None):
  bstack1lll1ll1l1ll_opy_ = bstack11ll1lllll_opy_.on()
  if not bstack1lll1ll1l1ll_opy_ or bstack1l1l1l11ll_opy_ not in [bstack1l1l11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ≻")] or test == None:
    return None
  return {
    bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ≼"): bstack1lll1ll1l1ll_opy_ and bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ≽"), None) == True and bstack11ll1lllll_opy_.bstack1111ll11l_opy_(test[bstack1l1l11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ≾")])
  }
def bstack1lll1lll11l1_opy_(bs_config, framework):
  bstack1ll1ll1l1_opy_ = False
  bstack11l111111l_opy_ = False
  bstack1lll1lll1lll_opy_ = False
  if bstack1l1l11l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ≿") in bs_config:
    bstack1lll1lll1lll_opy_ = True
  elif bstack1l1l11l_opy_ (u"ࠬࡧࡰࡱࠩ⊀") in bs_config:
    bstack1ll1ll1l1_opy_ = True
  else:
    bstack11l111111l_opy_ = True
  bstack11l11l11_opy_ = {
    bstack1l1l11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⊁"): bstack11l11l1l1l_opy_.bstack1lll1ll1ll1l_opy_(bs_config, framework),
    bstack1l1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⊂"): bstack11ll1lllll_opy_.bstack1l1l1l111l_opy_(bs_config),
    bstack1l1l11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⊃"): bs_config.get(bstack1l1l11l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⊄"), False),
    bstack1l1l11l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⊅"): bstack11l111111l_opy_,
    bstack1l1l11l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⊆"): bstack1ll1ll1l1_opy_,
    bstack1l1l11l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⊇"): bstack1lll1lll1lll_opy_
  }
  return bstack11l11l11_opy_
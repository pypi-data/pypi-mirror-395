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
import requests
import logging
import threading
import bstack_utils.constants as bstack11l1ll11ll1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l1lllllll_opy_ as bstack11l1llllll1_opy_, EVENTS
from bstack_utils.bstack1lll111l_opy_ import bstack1lll111l_opy_
from bstack_utils.helper import bstack11l1lllll_opy_, bstack1111ll11ll_opy_, bstack1lll11lll1_opy_, bstack11l1lll1ll1_opy_, \
  bstack11ll11111l1_opy_, bstack1lll11ll11_opy_, get_host_info, bstack11ll111l1l1_opy_, bstack11l1l1l111_opy_, error_handler, bstack11l1llll11l_opy_, bstack11l1ll1l1ll_opy_, bstack111111l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11l1l11111_opy_ import get_logger
from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1llll11111_opy_ = bstack1lll1ll111l_opy_()
@error_handler(class_method=False)
def _11ll111l1ll_opy_(driver, bstack11111l1l11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1l11l_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪ᛬"): caps.get(bstack1l1l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ᛭"), None),
        bstack1l1l11l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᛮ"): bstack11111l1l11_opy_.get(bstack1l1l11l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᛯ"), None),
        bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᛰ"): caps.get(bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᛱ"), None),
        bstack1l1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᛲ"): caps.get(bstack1l1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᛳ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1l11l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᛴ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1l11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᛵ"), None) is None or os.environ[bstack1l1l11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᛶ")] == bstack1l1l11l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᛷ"):
        return False
    return True
def bstack1ll1l1111_opy_(config):
  return config.get(bstack1l1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᛸ"), False) or any([p.get(bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᛹"), False) == True for p in config.get(bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᛺"), [])])
def bstack1ll1lll1l_opy_(config, bstack1ll1l1111l_opy_):
  try:
    bstack11ll111111l_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᛻"), False)
    if int(bstack1ll1l1111l_opy_) < len(config.get(bstack1l1l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᛼"), [])) and config[bstack1l1l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᛽")][bstack1ll1l1111l_opy_]:
      bstack11ll1111ll1_opy_ = config[bstack1l1l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᛾")][bstack1ll1l1111l_opy_].get(bstack1l1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᛿"), None)
    else:
      bstack11ll1111ll1_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜀ"), None)
    if bstack11ll1111ll1_opy_ != None:
      bstack11ll111111l_opy_ = bstack11ll1111ll1_opy_
    bstack11ll11111ll_opy_ = os.getenv(bstack1l1l11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᜁ")) is not None and len(os.getenv(bstack1l1l11l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᜂ"))) > 0 and os.getenv(bstack1l1l11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᜃ")) != bstack1l1l11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᜄ")
    return bstack11ll111111l_opy_ and bstack11ll11111ll_opy_
  except Exception as error:
    logger.debug(bstack1l1l11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᜅ") + str(error))
  return False
def bstack1111ll11l_opy_(test_tags):
  bstack1ll11111lll_opy_ = os.getenv(bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᜆ"))
  if bstack1ll11111lll_opy_ is None:
    return True
  bstack1ll11111lll_opy_ = json.loads(bstack1ll11111lll_opy_)
  try:
    include_tags = bstack1ll11111lll_opy_[bstack1l1l11l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᜇ")] if bstack1l1l11l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᜈ") in bstack1ll11111lll_opy_ and isinstance(bstack1ll11111lll_opy_[bstack1l1l11l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᜉ")], list) else []
    exclude_tags = bstack1ll11111lll_opy_[bstack1l1l11l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᜊ")] if bstack1l1l11l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᜋ") in bstack1ll11111lll_opy_ and isinstance(bstack1ll11111lll_opy_[bstack1l1l11l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᜌ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1l11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᜍ") + str(error))
  return False
def bstack11l1lll11l1_opy_(config, bstack11ll1111l11_opy_, bstack11l1ll1llll_opy_, bstack11ll1111l1l_opy_):
  bstack11l1lll1111_opy_ = bstack11l1lll1ll1_opy_(config)
  bstack11l1lllll1l_opy_ = bstack11ll11111l1_opy_(config)
  if bstack11l1lll1111_opy_ is None or bstack11l1lllll1l_opy_ is None:
    logger.error(bstack1l1l11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᜎ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᜏ"), bstack1l1l11l_opy_ (u"ࠪࡿࢂ࠭ᜐ")))
    data = {
        bstack1l1l11l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᜑ"): config[bstack1l1l11l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᜒ")],
        bstack1l1l11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᜓ"): config.get(bstack1l1l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ᜔ࠪ"), os.path.basename(os.getcwd())),
        bstack1l1l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨ᜕ࠫ"): bstack11l1lllll_opy_(),
        bstack1l1l11l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ᜖"): config.get(bstack1l1l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭᜗"), bstack1l1l11l_opy_ (u"ࠫࠬ᜘")),
        bstack1l1l11l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ᜙"): {
            bstack1l1l11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭᜚"): bstack11ll1111l11_opy_,
            bstack1l1l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ᜛"): bstack11l1ll1llll_opy_,
            bstack1l1l11l_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ᜜"): __version__,
            bstack1l1l11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ᜝"): bstack1l1l11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ᜞"),
            bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᜟ"): bstack1l1l11l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᜠ"),
            bstack1l1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᜡ"): bstack11ll1111l1l_opy_
        },
        bstack1l1l11l_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩᜢ"): settings,
        bstack1l1l11l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩᜣ"): bstack11ll111l1l1_opy_(),
        bstack1l1l11l_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩᜤ"): bstack1lll11ll11_opy_(),
        bstack1l1l11l_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬᜥ"): get_host_info(),
        bstack1l1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᜦ"): bstack1lll11lll1_opy_(config)
    }
    headers = {
        bstack1l1l11l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᜧ"): bstack1l1l11l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᜨ"),
    }
    config = {
        bstack1l1l11l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᜩ"): (bstack11l1lll1111_opy_, bstack11l1lllll1l_opy_),
        bstack1l1l11l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᜪ"): headers
    }
    response = bstack11l1l1l111_opy_(bstack1l1l11l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᜫ"), bstack11l1llllll1_opy_ + bstack1l1l11l_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪᜬ"), data, config)
    bstack11ll111ll11_opy_ = response.json()
    if bstack11ll111ll11_opy_[bstack1l1l11l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᜭ")]:
      parsed = json.loads(os.getenv(bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᜮ"), bstack1l1l11l_opy_ (u"࠭ࡻࡾࠩᜯ")))
      parsed[bstack1l1l11l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᜰ")] = bstack11ll111ll11_opy_[bstack1l1l11l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᜱ")][bstack1l1l11l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᜲ")]
      os.environ[bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᜳ")] = json.dumps(parsed)
      bstack1lll111l_opy_.bstack111lll11l_opy_(bstack11ll111ll11_opy_[bstack1l1l11l_opy_ (u"ࠫࡩࡧࡴࡢ᜴ࠩ")][bstack1l1l11l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭᜵")])
      bstack1lll111l_opy_.bstack11ll11l1111_opy_(bstack11ll111ll11_opy_[bstack1l1l11l_opy_ (u"࠭ࡤࡢࡶࡤࠫ᜶")][bstack1l1l11l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ᜷")])
      bstack1lll111l_opy_.store()
      return bstack11ll111ll11_opy_[bstack1l1l11l_opy_ (u"ࠨࡦࡤࡸࡦ࠭᜸")][bstack1l1l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ᜹")], bstack11ll111ll11_opy_[bstack1l1l11l_opy_ (u"ࠪࡨࡦࡺࡡࠨ᜺")][bstack1l1l11l_opy_ (u"ࠫ࡮ࡪࠧ᜻")]
    else:
      logger.error(bstack1l1l11l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭᜼") + bstack11ll111ll11_opy_[bstack1l1l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᜽")])
      if bstack11ll111ll11_opy_[bstack1l1l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᜾")] == bstack1l1l11l_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪ᜿"):
        for bstack11l1llll1ll_opy_ in bstack11ll111ll11_opy_[bstack1l1l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᝀ")]:
          logger.error(bstack11l1llll1ll_opy_[bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᝁ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧᝂ") +  str(error))
    return None, None
def bstack11l1llll111_opy_():
  if os.getenv(bstack1l1l11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᝃ")) is None:
    return {
        bstack1l1l11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᝄ"): bstack1l1l11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᝅ"),
        bstack1l1l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᝆ"): bstack1l1l11l_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨᝇ")
    }
  data = {bstack1l1l11l_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫᝈ"): bstack11l1lllll_opy_()}
  headers = {
      bstack1l1l11l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᝉ"): bstack1l1l11l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭ᝊ") + os.getenv(bstack1l1l11l_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦᝋ")),
      bstack1l1l11l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᝌ"): bstack1l1l11l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᝍ")
  }
  response = bstack11l1l1l111_opy_(bstack1l1l11l_opy_ (u"ࠩࡓ࡙࡙࠭ᝎ"), bstack11l1llllll1_opy_ + bstack1l1l11l_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬᝏ"), data, { bstack1l1l11l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᝐ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1l11l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨᝑ") + bstack1111ll11ll_opy_().isoformat() + bstack1l1l11l_opy_ (u"࡚࠭ࠨᝒ"))
      return {bstack1l1l11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᝓ"): bstack1l1l11l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ᝔"), bstack1l1l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᝕"): bstack1l1l11l_opy_ (u"ࠪࠫ᝖")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢ᝗") + str(error))
    return {
        bstack1l1l11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ᝘"): bstack1l1l11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᝙"),
        bstack1l1l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᝚"): str(error)
    }
def bstack11l1ll1lll1_opy_(bstack11l1lllll11_opy_):
    return re.match(bstack1l1l11l_opy_ (u"ࡳࠩࡡࡠࡩ࠱ࠨ࡝࠰࡟ࡨ࠰࠯࠿ࠥࠩ᝛"), bstack11l1lllll11_opy_.strip()) is not None
def bstack11ll1l11ll_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l1lll1l1l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l1lll1l1l_opy_ = desired_capabilities
        else:
          bstack11l1lll1l1l_opy_ = {}
        bstack1ll111l1l11_opy_ = (bstack11l1lll1l1l_opy_.get(bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᝜"), bstack1l1l11l_opy_ (u"ࠪࠫ᝝")).lower() or caps.get(bstack1l1l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ᝞"), bstack1l1l11l_opy_ (u"ࠬ࠭᝟")).lower())
        if bstack1ll111l1l11_opy_ == bstack1l1l11l_opy_ (u"࠭ࡩࡰࡵࠪᝠ"):
            return True
        if bstack1ll111l1l11_opy_ == bstack1l1l11l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᝡ"):
            bstack1l1lllll1ll_opy_ = str(float(caps.get(bstack1l1l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᝢ")) or bstack11l1lll1l1l_opy_.get(bstack1l1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᝣ"), {}).get(bstack1l1l11l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᝤ"),bstack1l1l11l_opy_ (u"ࠫࠬᝥ"))))
            if bstack1ll111l1l11_opy_ == bstack1l1l11l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᝦ") and int(bstack1l1lllll1ll_opy_.split(bstack1l1l11l_opy_ (u"࠭࠮ࠨᝧ"))[0]) < float(bstack11l1ll1l1l1_opy_):
                logger.warning(str(bstack11l1ll11lll_opy_))
                return False
            return True
        bstack1ll111ll1l1_opy_ = caps.get(bstack1l1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᝨ"), {}).get(bstack1l1l11l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᝩ"), caps.get(bstack1l1l11l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᝪ"), bstack1l1l11l_opy_ (u"ࠪࠫᝫ")))
        if bstack1ll111ll1l1_opy_:
            logger.warning(bstack1l1l11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᝬ"))
            return False
        browser = caps.get(bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ᝭"), bstack1l1l11l_opy_ (u"࠭ࠧᝮ")).lower() or bstack11l1lll1l1l_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᝯ"), bstack1l1l11l_opy_ (u"ࠨࠩᝰ")).lower()
        if browser != bstack1l1l11l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ᝱"):
            logger.warning(bstack1l1l11l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᝲ"))
            return False
        browser_version = caps.get(bstack1l1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᝳ")) or caps.get(bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᝴")) or bstack11l1lll1l1l_opy_.get(bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᝵")) or bstack11l1lll1l1l_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᝶"), {}).get(bstack1l1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᝷")) or bstack11l1lll1l1l_opy_.get(bstack1l1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᝸"), {}).get(bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᝹"))
        bstack1ll111111ll_opy_ = bstack11l1ll11ll1_opy_.bstack1l1llll11ll_opy_
        bstack11ll111ll1l_opy_ = False
        if config is not None:
          bstack11ll111ll1l_opy_ = bstack1l1l11l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᝺") in config and str(config[bstack1l1l11l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᝻")]).lower() != bstack1l1l11l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ᝼")
        if os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬ᝽"), bstack1l1l11l_opy_ (u"ࠨࠩ᝾")).lower() == bstack1l1l11l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᝿") or bstack11ll111ll1l_opy_:
          bstack1ll111111ll_opy_ = bstack11l1ll11ll1_opy_.bstack1ll111l11ll_opy_
        if browser_version and browser_version != bstack1l1l11l_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪក") and int(browser_version.split(bstack1l1l11l_opy_ (u"ࠫ࠳࠭ខ"))[0]) <= bstack1ll111111ll_opy_:
          logger.warning(bstack1lll1l111l1_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡻ࡮࡫ࡱࡣࡦ࠷࠱ࡺࡡࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࡤࡩࡨࡳࡱࡰࡩࡤࡼࡥࡳࡵ࡬ࡳࡳࢃ࠮ࠨគ"))
          return False
        if not options:
          bstack1l1lllll111_opy_ = caps.get(bstack1l1l11l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫឃ")) or bstack11l1lll1l1l_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬង"), {})
          if bstack1l1l11l_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬច") in bstack1l1lllll111_opy_.get(bstack1l1l11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧឆ"), []):
              logger.warning(bstack1l1l11l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧជ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1l1l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨឈ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll1l1l1ll_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬញ"), {})
    bstack1lll1l1l1ll_opy_[bstack1l1l11l_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩដ")] = os.getenv(bstack1l1l11l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬឋ"))
    bstack11ll111lll1_opy_ = json.loads(os.getenv(bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩឌ"), bstack1l1l11l_opy_ (u"ࠩࡾࢁࠬឍ"))).get(bstack1l1l11l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫណ"))
    if not config[bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ត")].get(bstack1l1l11l_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦថ")):
      if bstack1l1l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧទ") in caps:
        caps[bstack1l1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨធ")][bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨន")] = bstack1lll1l1l1ll_opy_
        caps[bstack1l1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪប")][bstack1l1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪផ")][bstack1l1l11l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬព")] = bstack11ll111lll1_opy_
      else:
        caps[bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫភ")] = bstack1lll1l1l1ll_opy_
        caps[bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬម")][bstack1l1l11l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨយ")] = bstack11ll111lll1_opy_
  except Exception as error:
    logger.debug(bstack1l1l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤរ") +  str(error))
def bstack1ll111lll1_opy_(driver, bstack11l1ll1l11l_opy_):
  try:
    setattr(driver, bstack1l1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩល"), True)
    session = driver.session_id
    if session:
      bstack11ll111llll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll111llll_opy_ = False
      bstack11ll111llll_opy_ = url.scheme in [bstack1l1l11l_opy_ (u"ࠥ࡬ࡹࡺࡰࠣវ"), bstack1l1l11l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥឝ")]
      if bstack11ll111llll_opy_:
        if bstack11l1ll1l11l_opy_:
          logger.info(bstack1l1l11l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧឞ"))
      return bstack11l1ll1l11l_opy_
  except Exception as e:
    logger.error(bstack1l1l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤស") + str(e))
    return False
def bstack1lll11l111_opy_(driver, name, path):
  try:
    bstack1ll11111l11_opy_ = {
        bstack1l1l11l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧហ"): threading.current_thread().current_test_uuid,
        bstack1l1l11l_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ឡ"): os.environ.get(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧអ"), bstack1l1l11l_opy_ (u"ࠪࠫឣ")),
        bstack1l1l11l_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨឤ"): os.environ.get(bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩឥ"), bstack1l1l11l_opy_ (u"࠭ࠧឦ"))
    }
    bstack1ll11l1lll1_opy_ = bstack1llll11111_opy_.bstack1l1llll111l_opy_(EVENTS.bstack1llll1l1l1_opy_.value)
    logger.debug(bstack1l1l11l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪឧ"))
    try:
      if (bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨឨ"), None) and bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫឩ"), None)):
        scripts = {bstack1l1l11l_opy_ (u"ࠪࡷࡨࡧ࡮ࠨឪ"): bstack1lll111l_opy_.perform_scan}
        bstack11ll111l11l_opy_ = json.loads(scripts[bstack1l1l11l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤឫ")].replace(bstack1l1l11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣឬ"), bstack1l1l11l_opy_ (u"ࠨࠢឭ")))
        bstack11ll111l11l_opy_[bstack1l1l11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪឮ")][bstack1l1l11l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨឯ")] = None
        scripts[bstack1l1l11l_opy_ (u"ࠤࡶࡧࡦࡴࠢឰ")] = bstack1l1l11l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨឱ") + json.dumps(bstack11ll111l11l_opy_)
        bstack1lll111l_opy_.bstack111lll11l_opy_(scripts)
        bstack1lll111l_opy_.store()
        logger.debug(driver.execute_script(bstack1lll111l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1lll111l_opy_.perform_scan, {bstack1l1l11l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦឲ"): name}))
      bstack1llll11111_opy_.end(EVENTS.bstack1llll1l1l1_opy_.value, bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧឳ"), bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ឴"), True, None)
    except Exception as error:
      bstack1llll11111_opy_.end(EVENTS.bstack1llll1l1l1_opy_.value, bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ឵"), bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨា"), False, str(error))
    bstack1ll11l1lll1_opy_ = bstack1llll11111_opy_.bstack11l1lll11ll_opy_(EVENTS.bstack1ll111l1l1l_opy_.value)
    bstack1llll11111_opy_.mark(bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤិ"))
    try:
      if (bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪី"), None) and bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ឹ"), None)):
        scripts = {bstack1l1l11l_opy_ (u"ࠬࡹࡣࡢࡰࠪឺ"): bstack1lll111l_opy_.perform_scan}
        bstack11ll111l11l_opy_ = json.loads(scripts[bstack1l1l11l_opy_ (u"ࠨࡳࡤࡣࡱࠦុ")].replace(bstack1l1l11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥូ"), bstack1l1l11l_opy_ (u"ࠣࠤួ")))
        bstack11ll111l11l_opy_[bstack1l1l11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬើ")][bstack1l1l11l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪឿ")] = None
        scripts[bstack1l1l11l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤៀ")] = bstack1l1l11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣេ") + json.dumps(bstack11ll111l11l_opy_)
        bstack1lll111l_opy_.bstack111lll11l_opy_(scripts)
        bstack1lll111l_opy_.store()
        logger.debug(driver.execute_script(bstack1lll111l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1lll111l_opy_.bstack11ll1111111_opy_, bstack1ll11111l11_opy_))
      bstack1llll11111_opy_.end(bstack1ll11l1lll1_opy_, bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨែ"), bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧៃ"),True, None)
    except Exception as error:
      bstack1llll11111_opy_.end(bstack1ll11l1lll1_opy_, bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣោ"), bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢៅ"),False, str(error))
    logger.info(bstack1l1l11l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨំ"))
  except Exception as bstack1ll111lllll_opy_:
    logger.error(bstack1l1l11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨះ") + str(path) + bstack1l1l11l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢៈ") + str(bstack1ll111lllll_opy_))
def bstack11l1ll1ll1l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l1l11l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ៉")) and str(caps.get(bstack1l1l11l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ៊"))).lower() == bstack1l1l11l_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤ់"):
        bstack1l1lllll1ll_opy_ = caps.get(bstack1l1l11l_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ៌")) or caps.get(bstack1l1l11l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ៍"))
        if bstack1l1lllll1ll_opy_ and int(str(bstack1l1lllll1ll_opy_)) < bstack11l1ll1l1l1_opy_:
            return False
    return True
def bstack1l1l1l111l_opy_(config):
  if bstack1l1l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ៎") in config:
        return config[bstack1l1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ៏")]
  for platform in config.get(bstack1l1l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ័"), []):
      if bstack1l1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ៑") in platform:
          return platform[bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ្")]
  return None
def bstack1lll1l111_opy_(bstack1l1l11lll1_opy_):
  try:
    browser_name = bstack1l1l11lll1_opy_[bstack1l1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨ៓")]
    browser_version = bstack1l1l11lll1_opy_[bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ។")]
    chrome_options = bstack1l1l11lll1_opy_[bstack1l1l11l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡣࡴࡶࡴࡪࡱࡱࡷࠬ៕")]
    try:
        bstack11l1lll1l11_opy_ = int(browser_version.split(bstack1l1l11l_opy_ (u"ࠬ࠴ࠧ៖"))[0])
    except ValueError as e:
        logger.error(bstack1l1l11l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡨࡵ࡮ࡷࡧࡵࡸ࡮ࡴࡧࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠥៗ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1l1l11l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ៘")):
        logger.warning(bstack1l1l11l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ៙"))
        return False
    if bstack11l1lll1l11_opy_ < bstack11l1ll11ll1_opy_.bstack1ll111l11ll_opy_:
        logger.warning(bstack1lll1l111l1_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡳࠡࡅ࡫ࡶࡴࡳࡥࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡾࡇࡔࡔࡓࡕࡃࡑࡘࡘ࠴ࡍࡊࡐࡌࡑ࡚ࡓ࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡘࡔࡕࡕࡒࡕࡇࡇࡣࡈࡎࡒࡐࡏࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࢂࠦ࡯ࡳࠢ࡫࡭࡬࡮ࡥࡳ࠰ࠪ៚"))
        return False
    if chrome_options and any(bstack1l1l11l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ៛") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1l1l11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨៜ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1l1l11l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡻࡰࡱࡱࡵࡸࠥ࡬࡯ࡳࠢ࡯ࡳࡨࡧ࡬ࠡࡅ࡫ࡶࡴࡳࡥ࠻ࠢࠥ៝") + str(e))
    return False
def bstack1l11l1l1l1_opy_(bstack11ll1l1l1l_opy_, config):
    try:
      bstack1ll1111l11l_opy_ = bstack1l1l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭៞") in config and config[bstack1l1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ៟")] == True
      bstack11ll111ll1l_opy_ = bstack1l1l11l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ០") in config and str(config[bstack1l1l11l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭១")]).lower() != bstack1l1l11l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ២")
      if not (bstack1ll1111l11l_opy_ and (not bstack1lll11lll1_opy_(config) or bstack11ll111ll1l_opy_)):
        return bstack11ll1l1l1l_opy_
      bstack11ll1111lll_opy_ = bstack1lll111l_opy_.bstack11l1lll1lll_opy_
      if bstack11ll1111lll_opy_ is None:
        logger.debug(bstack1l1l11l_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥࡧࡲࡦࠢࡑࡳࡳ࡫ࠢ៣"))
        return bstack11ll1l1l1l_opy_
      bstack11l1llll1l1_opy_ = int(str(bstack11l1ll1l1ll_opy_()).split(bstack1l1l11l_opy_ (u"ࠬ࠴ࠧ៤"))[0])
      logger.debug(bstack1l1l11l_opy_ (u"ࠨࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧ࠾ࠥࠨ៥") + str(bstack11l1llll1l1_opy_) + bstack1l1l11l_opy_ (u"ࠢࠣ៦"))
      if bstack11l1llll1l1_opy_ == 3 and isinstance(bstack11ll1l1l1l_opy_, dict) and bstack1l1l11l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ៧") in bstack11ll1l1l1l_opy_ and bstack11ll1111lll_opy_ is not None:
        if bstack1l1l11l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ៨") not in bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ៩")]:
          bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ៪")][bstack1l1l11l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៫")] = {}
        if bstack1l1l11l_opy_ (u"࠭ࡡࡳࡩࡶࠫ៬") in bstack11ll1111lll_opy_:
          if bstack1l1l11l_opy_ (u"ࠧࡢࡴࡪࡷࠬ៭") not in bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ៮")][bstack1l1l11l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ៯")]:
            bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ៰")][bstack1l1l11l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៱")][bstack1l1l11l_opy_ (u"ࠬࡧࡲࡨࡵࠪ៲")] = []
          for arg in bstack11ll1111lll_opy_[bstack1l1l11l_opy_ (u"࠭ࡡࡳࡩࡶࠫ៳")]:
            if arg not in bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ៴")][bstack1l1l11l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭៵")][bstack1l1l11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ៶")]:
              bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ៷")][bstack1l1l11l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៸")][bstack1l1l11l_opy_ (u"ࠬࡧࡲࡨࡵࠪ៹")].append(arg)
        if bstack1l1l11l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ៺") in bstack11ll1111lll_opy_:
          if bstack1l1l11l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ៻") not in bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ៼")][bstack1l1l11l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ៽")]:
            bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ៾")][bstack1l1l11l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៿")][bstack1l1l11l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᠀")] = []
          for ext in bstack11ll1111lll_opy_[bstack1l1l11l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᠁")]:
            if ext not in bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᠂")][bstack1l1l11l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᠃")][bstack1l1l11l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᠄")]:
              bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᠅")][bstack1l1l11l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᠆")][bstack1l1l11l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᠇")].append(ext)
        if bstack1l1l11l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᠈") in bstack11ll1111lll_opy_:
          if bstack1l1l11l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᠉") not in bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᠊")][bstack1l1l11l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᠋")]:
            bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᠌")][bstack1l1l11l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᠍")][bstack1l1l11l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᠎")] = {}
          bstack11l1llll11l_opy_(bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᠏")][bstack1l1l11l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᠐")][bstack1l1l11l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᠑")],
                    bstack11ll1111lll_opy_[bstack1l1l11l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᠒")])
        os.environ[bstack1l1l11l_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨ᠓")] = bstack1l1l11l_opy_ (u"ࠫࡹࡸࡵࡦࠩ᠔")
        return bstack11ll1l1l1l_opy_
      else:
        chrome_options = None
        if isinstance(bstack11ll1l1l1l_opy_, ChromeOptions):
          chrome_options = bstack11ll1l1l1l_opy_
        elif isinstance(bstack11ll1l1l1l_opy_, dict):
          for value in bstack11ll1l1l1l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack11ll1l1l1l_opy_, dict):
            bstack11ll1l1l1l_opy_[bstack1l1l11l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭᠕")] = chrome_options
          else:
            bstack11ll1l1l1l_opy_ = chrome_options
        if bstack11ll1111lll_opy_ is not None:
          if bstack1l1l11l_opy_ (u"࠭ࡡࡳࡩࡶࠫ᠖") in bstack11ll1111lll_opy_:
                bstack11l1ll1l111_opy_ = chrome_options.arguments or []
                new_args = bstack11ll1111lll_opy_[bstack1l1l11l_opy_ (u"ࠧࡢࡴࡪࡷࠬ᠗")]
                for arg in new_args:
                    if arg not in bstack11l1ll1l111_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l1l11l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᠘") in bstack11ll1111lll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l1l11l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᠙"), [])
                bstack11ll111l111_opy_ = bstack11ll1111lll_opy_[bstack1l1l11l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᠚")]
                for extension in bstack11ll111l111_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l1l11l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᠛") in bstack11ll1111lll_opy_:
                bstack11l1lll111l_opy_ = chrome_options.experimental_options.get(bstack1l1l11l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᠜"), {})
                bstack11l1ll1ll11_opy_ = bstack11ll1111lll_opy_[bstack1l1l11l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᠝")]
                bstack11l1llll11l_opy_(bstack11l1lll111l_opy_, bstack11l1ll1ll11_opy_)
                chrome_options.add_experimental_option(bstack1l1l11l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᠞"), bstack11l1lll111l_opy_)
        os.environ[bstack1l1l11l_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭᠟")] = bstack1l1l11l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᠠ")
        return bstack11ll1l1l1l_opy_
    except Exception as e:
      logger.error(bstack1l1l11l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡧࡨ࡮ࡴࡧࠡࡰࡲࡲ࠲ࡈࡓࠡ࡫ࡱࡪࡷࡧࠠࡢ࠳࠴ࡽࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࠣᠡ") + str(e))
      return bstack11ll1l1l1l_opy_
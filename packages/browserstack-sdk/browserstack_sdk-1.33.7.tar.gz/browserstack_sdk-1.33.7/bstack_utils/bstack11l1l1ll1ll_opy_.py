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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l11ll1ll1_opy_
logger = logging.getLogger(__name__)
class bstack11l1l1lll1l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1llll1l1l11l_opy_ = urljoin(builder, bstack1l1l11l_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳࠨ₮"))
        if params:
            bstack1llll1l1l11l_opy_ += bstack1l1l11l_opy_ (u"ࠤࡂࡿࢂࠨ₯").format(urlencode({bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ₰"): params.get(bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ₱"))}))
        return bstack11l1l1lll1l_opy_.bstack1llll1l1ll11_opy_(bstack1llll1l1l11l_opy_)
    @staticmethod
    def bstack11l1l1l1ll1_opy_(builder,params=None):
        bstack1llll1l1l11l_opy_ = urljoin(builder, bstack1l1l11l_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭₲"))
        if params:
            bstack1llll1l1l11l_opy_ += bstack1l1l11l_opy_ (u"ࠨ࠿ࡼࡿࠥ₳").format(urlencode({bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ₴"): params.get(bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ₵"))}))
        return bstack11l1l1lll1l_opy_.bstack1llll1l1ll11_opy_(bstack1llll1l1l11l_opy_)
    @staticmethod
    def bstack1llll1l1ll11_opy_(bstack1llll1ll1111_opy_):
        bstack1llll1l1l1ll_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ₶"), os.environ.get(bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ₷"), bstack1l1l11l_opy_ (u"ࠫࠬ₸")))
        headers = {bstack1l1l11l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ₹"): bstack1l1l11l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ₺").format(bstack1llll1l1l1ll_opy_)}
        response = requests.get(bstack1llll1ll1111_opy_, headers=headers)
        bstack1llll1l1l111_opy_ = {}
        try:
            bstack1llll1l1l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ₻").format(e))
            pass
        if bstack1llll1l1l111_opy_ is not None:
            bstack1llll1l1l111_opy_[bstack1l1l11l_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ₼")] = response.headers.get(bstack1l1l11l_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ₽"), str(int(datetime.now().timestamp() * 1000)))
            bstack1llll1l1l111_opy_[bstack1l1l11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ₾")] = response.status_code
        return bstack1llll1l1l111_opy_
    @staticmethod
    def bstack1llll1l1lll1_opy_(bstack1llll1l1llll_opy_, data):
        logger.debug(bstack1l1l11l_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡖࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࠨ₿"))
        return bstack11l1l1lll1l_opy_.bstack1llll1l1ll1l_opy_(bstack1l1l11l_opy_ (u"ࠬࡖࡏࡔࡖࠪ⃀"), bstack1llll1l1llll_opy_, data=data)
    @staticmethod
    def bstack1llll1l1l1l1_opy_(bstack1llll1l1llll_opy_, data):
        logger.debug(bstack1l1l11l_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡩࡨࡸ࡙࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡸࠨ⃁"))
        res = bstack11l1l1lll1l_opy_.bstack1llll1l1ll1l_opy_(bstack1l1l11l_opy_ (u"ࠧࡈࡇࡗࠫ⃂"), bstack1llll1l1llll_opy_, data=data)
        return res
    @staticmethod
    def bstack1llll1l1ll1l_opy_(method, bstack1llll1l1llll_opy_, data=None, params=None, extra_headers=None):
        bstack1llll1l1l1ll_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⃃"), bstack1l1l11l_opy_ (u"ࠩࠪ⃄"))
        headers = {
            bstack1l1l11l_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ⃅"): bstack1l1l11l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⃆").format(bstack1llll1l1l1ll_opy_),
            bstack1l1l11l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⃇"): bstack1l1l11l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⃈"),
            bstack1l1l11l_opy_ (u"ࠧࡂࡥࡦࡩࡵࡺࠧ⃉"): bstack1l1l11l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⃊")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l11ll1ll1_opy_ + bstack1l1l11l_opy_ (u"ࠤ࠲ࠦ⃋") + bstack1llll1l1llll_opy_.lstrip(bstack1l1l11l_opy_ (u"ࠪ࠳ࠬ⃌"))
        try:
            if method == bstack1l1l11l_opy_ (u"ࠫࡌࡋࡔࠨ⃍"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l1l11l_opy_ (u"ࠬࡖࡏࡔࡖࠪ⃎"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l1l11l_opy_ (u"࠭ࡐࡖࡖࠪ⃏"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l1l11l_opy_ (u"ࠢࡖࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢ⃐").format(method))
            logger.debug(bstack1l1l11l_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡰࡥࡩ࡫ࠠࡵࡱ࡙ࠣࡗࡒ࠺ࠡࡽࢀࠤࡼ࡯ࡴࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨ⃑").format(url, method))
            bstack1llll1l1l111_opy_ = {}
            try:
                bstack1llll1l1l111_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l1l11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ⃒").format(e, response.text))
            if bstack1llll1l1l111_opy_ is not None:
                bstack1llll1l1l111_opy_[bstack1l1l11l_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨ⃓ࠫ")] = response.headers.get(
                    bstack1l1l11l_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⃔"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1llll1l1l111_opy_[bstack1l1l11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⃕")] = response.status_code
            return bstack1llll1l1l111_opy_
        except Exception as e:
            logger.error(bstack1l1l11l_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤ⃖").format(e, url))
            return None
    @staticmethod
    def bstack11l111ll1ll_opy_(bstack1llll1ll1111_opy_, data):
        bstack1l1l11l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡖࡕࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡺࡨࡦࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⃗")
        bstack1llll1l1l1ll_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘ⃘ࠬ"), bstack1l1l11l_opy_ (u"⃙ࠩࠪ"))
        headers = {
            bstack1l1l11l_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰ⃚ࠪ"): bstack1l1l11l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⃛").format(bstack1llll1l1l1ll_opy_),
            bstack1l1l11l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⃜"): bstack1l1l11l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⃝")
        }
        response = requests.put(bstack1llll1ll1111_opy_, headers=headers, json=data)
        bstack1llll1l1l111_opy_ = {}
        try:
            bstack1llll1l1l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⃞").format(e))
            pass
        logger.debug(bstack1l1l11l_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠺ࠡࡲࡸࡸࡤ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⃟").format(bstack1llll1l1l111_opy_))
        if bstack1llll1l1l111_opy_ is not None:
            bstack1llll1l1l111_opy_[bstack1l1l11l_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⃠")] = response.headers.get(
                bstack1l1l11l_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⃡"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llll1l1l111_opy_[bstack1l1l11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⃢")] = response.status_code
        return bstack1llll1l1l111_opy_
    @staticmethod
    def bstack11l11l111ll_opy_(bstack1llll1ll1111_opy_):
        bstack1l1l11l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡋࡊ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡬࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⃣")
        bstack1llll1l1l1ll_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⃤"), bstack1l1l11l_opy_ (u"ࠧࠨ⃥"))
        headers = {
            bstack1l1l11l_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ⃦"): bstack1l1l11l_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ⃧").format(bstack1llll1l1l1ll_opy_),
            bstack1l1l11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦ⃨ࠩ"): bstack1l1l11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ⃩")
        }
        response = requests.get(bstack1llll1ll1111_opy_, headers=headers)
        bstack1llll1l1l111_opy_ = {}
        try:
            bstack1llll1l1l111_opy_ = response.json()
            logger.debug(bstack1l1l11l_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥ࡭ࡥࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃ⃪ࠢ").format(bstack1llll1l1l111_opy_))
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿ⃫ࠥ").format(e, response.text))
            pass
        if bstack1llll1l1l111_opy_ is not None:
            bstack1llll1l1l111_opy_[bstack1l1l11l_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⃬")] = response.headers.get(
                bstack1l1l11l_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦ⃭ࠩ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llll1l1l111_opy_[bstack1l1l11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴ⃮ࠩ")] = response.status_code
        return bstack1llll1l1l111_opy_
    @staticmethod
    def bstack1111l1ll11l_opy_(bstack11l1ll11111_opy_, payload):
        bstack1l1l11l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡎࡣ࡮ࡩࡸࠦࡡࠡࡒࡒࡗ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩࠥࡇࡐࡊࠢࡨࡲࡩࡶ࡯ࡪࡰࡷࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡽࡱࡵࡡࡥࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡲࡤࡽࡱࡵࡡࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡂࡒࡌ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨ⃯ࠢ")
        try:
            url = bstack1l1l11l_opy_ (u"ࠦࢀࢃ࠯ࡼࡿࠥ⃰").format(bstack11l11ll1ll1_opy_, bstack11l1ll11111_opy_)
            bstack1llll1l1l1ll_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⃱"), bstack1l1l11l_opy_ (u"࠭ࠧ⃲"))
            headers = {
                bstack1l1l11l_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⃳"): bstack1l1l11l_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⃴").format(bstack1llll1l1l1ll_opy_),
                bstack1l1l11l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⃵"): bstack1l1l11l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⃶")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1llll1ll111l_opy_ = [200, 202]
            if response.status_code in bstack1llll1ll111l_opy_:
                return response.json()
            else:
                logger.error(bstack1l1l11l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥ࠳ࠦࡓࡵࡣࡷࡹࡸࡀࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⃷").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡳࡵࡡࡦࡳࡱࡲࡥࡤࡶࡢࡦࡺ࡯࡬ࡥࡡࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ⃸").format(e))
            return None
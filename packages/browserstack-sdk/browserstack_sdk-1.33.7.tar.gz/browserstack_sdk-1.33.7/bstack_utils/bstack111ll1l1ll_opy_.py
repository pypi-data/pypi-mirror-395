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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1lll1ll1_opy_, bstack11ll11111l1_opy_, bstack11l1l1l111_opy_, error_handler, bstack111llllll11_opy_, bstack111l1l111l1_opy_, bstack11l11111l1l_opy_, bstack11l1lllll_opy_, bstack111111l11_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1llll1ll11ll_opy_ import bstack1llll1lll1l1_opy_
import bstack_utils.bstack1l1lll1111_opy_ as bstack1lll1l1111_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11l11l1l1l_opy_
import bstack_utils.accessibility as bstack11ll1lllll_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack1lll111l_opy_
from bstack_utils.bstack111l1llll1_opy_ import bstack111l1l1l11_opy_
from bstack_utils.constants import bstack1l111lll11_opy_
bstack1lll1lllll11_opy_ = bstack1l1l11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ⅀")
logger = logging.getLogger(__name__)
class bstack1l1111ll1l_opy_:
    bstack1llll1ll11ll_opy_ = None
    bs_config = None
    bstack1l1111lll1_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l11l1ll1l_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def launch(cls, bs_config, bstack1l1111lll1_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1111lll1_opy_ = bstack1l1111lll1_opy_
        try:
            cls.bstack1llll111l11l_opy_()
            bstack11l1lll1111_opy_ = bstack11l1lll1ll1_opy_(bs_config)
            bstack11l1lllll1l_opy_ = bstack11ll11111l1_opy_(bs_config)
            data = bstack1lll1l1111_opy_.bstack1llll11l111l_opy_(bs_config, bstack1l1111lll1_opy_)
            config = {
                bstack1l1l11l_opy_ (u"ࠨࡣࡸࡸ࡭࠭⅁"): (bstack11l1lll1111_opy_, bstack11l1lllll1l_opy_),
                bstack1l1l11l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ⅂"): cls.default_headers()
            }
            response = bstack11l1l1l111_opy_(bstack1l1l11l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ⅃"), cls.request_url(bstack1l1l11l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠵࠳ࡧࡻࡩ࡭ࡦࡶࠫ⅄")), data, config)
            if response.status_code != 200:
                bstack111lll1l_opy_ = response.json()
                if bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ⅅ")] == False:
                    cls.bstack1llll1111ll1_opy_(bstack111lll1l_opy_)
                    return
                cls.bstack1llll11l1111_opy_(bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ⅆ")])
                cls.bstack1lll1llll1l1_opy_(bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧⅇ")])
                return None
            bstack1llll11111l1_opy_ = cls.bstack1llll111ll1l_opy_(response)
            return bstack1llll11111l1_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l1l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨⅈ").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    def stop(cls, bstack1lll1llll11l_opy_=None):
        if not bstack11l11l1l1l_opy_.on() and not bstack11ll1lllll_opy_.on():
            return
        if os.environ.get(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ⅉ")) == bstack1l1l11l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⅊") or os.environ.get(bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⅋")) == bstack1l1l11l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⅌"):
            logger.error(bstack1l1l11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ⅍"))
            return {
                bstack1l1l11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧⅎ"): bstack1l1l11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⅏"),
                bstack1l1l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⅐"): bstack1l1l11l_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨ⅑")
            }
        try:
            cls.bstack1llll1ll11ll_opy_.shutdown()
            data = {
                bstack1l1l11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⅒"): bstack11l1lllll_opy_()
            }
            if not bstack1lll1llll11l_opy_ is None:
                data[bstack1l1l11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩ⅓")] = [{
                    bstack1l1l11l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭⅔"): bstack1l1l11l_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ⅕"),
                    bstack1l1l11l_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ⅖"): bstack1lll1llll11l_opy_
                }]
            config = {
                bstack1l1l11l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ⅗"): cls.default_headers()
            }
            bstack11l1ll11111_opy_ = bstack1l1l11l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫ⅘").format(os.environ[bstack1l1l11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⅙")])
            bstack1lll1llll1ll_opy_ = cls.request_url(bstack11l1ll11111_opy_)
            response = bstack11l1l1l111_opy_(bstack1l1l11l_opy_ (u"ࠬࡖࡕࡕࠩ⅚"), bstack1lll1llll1ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1l11l_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧ⅛"))
        except Exception as error:
            logger.error(bstack1l1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻࠼ࠣࠦ⅜") + str(error))
            return {
                bstack1l1l11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⅝"): bstack1l1l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⅞"),
                bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⅟"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll111ll1l_opy_(cls, response):
        bstack111lll1l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1llll11111l1_opy_ = {}
        if bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠫ࡯ࡽࡴࠨⅠ")) is None:
            os.environ[bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩⅡ")] = bstack1l1l11l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫⅢ")
        else:
            os.environ[bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫⅣ")] = bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠨ࡬ࡺࡸࠬⅤ"), bstack1l1l11l_opy_ (u"ࠩࡱࡹࡱࡲࠧⅥ"))
        os.environ[bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨⅦ")] = bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ⅷ"), bstack1l1l11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪⅨ"))
        logger.info(bstack1l1l11l_opy_ (u"࠭ࡔࡦࡵࡷ࡬ࡺࡨࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫⅩ") + os.getenv(bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬⅪ")));
        if bstack11l11l1l1l_opy_.bstack1llll111l1ll_opy_(cls.bs_config, cls.bstack1l1111lll1_opy_.get(bstack1l1l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩⅫ"), bstack1l1l11l_opy_ (u"ࠩࠪⅬ"))) is True:
            bstack1llll1l1l1ll_opy_, build_hashed_id, bstack1llll111ll11_opy_ = cls.bstack1llll111lll1_opy_(bstack111lll1l_opy_)
            if bstack1llll1l1l1ll_opy_ != None and build_hashed_id != None:
                bstack1llll11111l1_opy_[bstack1l1l11l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪⅭ")] = {
                    bstack1l1l11l_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧⅮ"): bstack1llll1l1l1ll_opy_,
                    bstack1l1l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧⅯ"): build_hashed_id,
                    bstack1l1l11l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪⅰ"): bstack1llll111ll11_opy_
                }
            else:
                bstack1llll11111l1_opy_[bstack1l1l11l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧⅱ")] = {}
        else:
            bstack1llll11111l1_opy_[bstack1l1l11l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨⅲ")] = {}
        bstack1lll1llllll1_opy_, build_hashed_id = cls.bstack1lll1lllll1l_opy_(bstack111lll1l_opy_)
        if bstack1lll1llllll1_opy_ != None and build_hashed_id != None:
            bstack1llll11111l1_opy_[bstack1l1l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩⅳ")] = {
                bstack1l1l11l_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧⅴ"): bstack1lll1llllll1_opy_,
                bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ⅵ"): build_hashed_id,
            }
        else:
            bstack1llll11111l1_opy_[bstack1l1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬⅶ")] = {}
        if bstack1llll11111l1_opy_[bstack1l1l11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ⅷ")].get(bstack1l1l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩⅸ")) != None or bstack1llll11111l1_opy_[bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨⅹ")].get(bstack1l1l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫⅺ")) != None:
            cls.bstack1llll111l1l1_opy_(bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠪ࡮ࡼࡺࠧⅻ")), bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ⅼ")))
        return bstack1llll11111l1_opy_
    @classmethod
    def bstack1llll111lll1_opy_(cls, bstack111lll1l_opy_):
        if bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬⅽ")) == None:
            cls.bstack1llll11l1111_opy_()
            return [None, None, None]
        if bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ⅾ")][bstack1l1l11l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨⅿ")] != True:
            cls.bstack1llll11l1111_opy_(bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨↀ")])
            return [None, None, None]
        logger.debug(bstack1l1l11l_opy_ (u"ࠩࡾࢁࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫↁ").format(bstack1l111lll11_opy_))
        os.environ[bstack1l1l11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩↂ")] = bstack1l1l11l_opy_ (u"ࠫࡹࡸࡵࡦࠩↃ")
        if bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠬࡰࡷࡵࠩↄ")):
            os.environ[bstack1l1l11l_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪↅ")] = json.dumps({
                bstack1l1l11l_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩↆ"): bstack11l1lll1ll1_opy_(cls.bs_config),
                bstack1l1l11l_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪↇ"): bstack11ll11111l1_opy_(cls.bs_config)
            })
        if bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫↈ")):
            os.environ[bstack1l1l11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ↉")] = bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭↊")]
        if bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ↋")].get(bstack1l1l11l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ↌"), {}).get(bstack1l1l11l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ↍")):
            os.environ[bstack1l1l11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ↎")] = str(bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ↏")][bstack1l1l11l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ←")][bstack1l1l11l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ↑")])
        else:
            os.environ[bstack1l1l11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭→")] = bstack1l1l11l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ↓")
        return [bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠧ࡫ࡹࡷࠫ↔")], bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ↕")], os.environ[bstack1l1l11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ↖")]]
    @classmethod
    def bstack1lll1lllll1l_opy_(cls, bstack111lll1l_opy_):
        if bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ↗")) == None:
            cls.bstack1lll1llll1l1_opy_()
            return [None, None]
        if bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ↘")][bstack1l1l11l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭↙")] != True:
            cls.bstack1lll1llll1l1_opy_(bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭↚")])
            return [None, None]
        if bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ↛")].get(bstack1l1l11l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ↜")):
            logger.debug(bstack1l1l11l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭↝"))
            parsed = json.loads(os.getenv(bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ↞"), bstack1l1l11l_opy_ (u"ࠫࢀࢃࠧ↟")))
            capabilities = bstack1lll1l1111_opy_.bstack1llll111l111_opy_(bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ↠")][bstack1l1l11l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ↡")][bstack1l1l11l_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭↢")], bstack1l1l11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭↣"), bstack1l1l11l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ↤"))
            bstack1lll1llllll1_opy_ = capabilities[bstack1l1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ↥")]
            os.environ[bstack1l1l11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ↦")] = bstack1lll1llllll1_opy_
            if bstack1l1l11l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ↧") in bstack111lll1l_opy_ and bstack111lll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ↨")) is None:
                parsed[bstack1l1l11l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ↩")] = capabilities[bstack1l1l11l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ↪")]
            os.environ[bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ↫")] = json.dumps(parsed)
            scripts = bstack1lll1l1111_opy_.bstack1llll111l111_opy_(bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ↬")][bstack1l1l11l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ↭")][bstack1l1l11l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭↮")], bstack1l1l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ↯"), bstack1l1l11l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨ↰"))
            bstack1lll111l_opy_.bstack111lll11l_opy_(scripts)
            commands = bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ↱")][bstack1l1l11l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ↲")][bstack1l1l11l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫ↳")].get(bstack1l1l11l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭↴"))
            bstack1lll111l_opy_.bstack11ll11l1111_opy_(commands)
            bstack11l1lll1lll_opy_ = capabilities.get(bstack1l1l11l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ↵"))
            bstack1lll111l_opy_.bstack11l1ll11l11_opy_(bstack11l1lll1lll_opy_)
            bstack1lll111l_opy_.store()
        return [bstack1lll1llllll1_opy_, bstack111lll1l_opy_[bstack1l1l11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ↶")]]
    @classmethod
    def bstack1llll11l1111_opy_(cls, response=None):
        os.environ[bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ↷")] = bstack1l1l11l_opy_ (u"ࠨࡰࡸࡰࡱ࠭↸")
        os.environ[bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭↹")] = bstack1l1l11l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ↺")
        os.environ[bstack1l1l11l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ↻")] = bstack1l1l11l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ↼")
        os.environ[bstack1l1l11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ↽")] = bstack1l1l11l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ↾")
        os.environ[bstack1l1l11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ↿")] = bstack1l1l11l_opy_ (u"ࠤࡱࡹࡱࡲࠢ⇀")
        cls.bstack1llll1111ll1_opy_(response, bstack1l1l11l_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ⇁"))
        return [None, None, None]
    @classmethod
    def bstack1lll1llll1l1_opy_(cls, response=None):
        os.environ[bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⇂")] = bstack1l1l11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⇃")
        os.environ[bstack1l1l11l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⇄")] = bstack1l1l11l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⇅")
        os.environ[bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⇆")] = bstack1l1l11l_opy_ (u"ࠩࡱࡹࡱࡲࠧ⇇")
        cls.bstack1llll1111ll1_opy_(response, bstack1l1l11l_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥ⇈"))
        return [None, None, None]
    @classmethod
    def bstack1llll111l1l1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⇉")] = jwt
        os.environ[bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⇊")] = build_hashed_id
    @classmethod
    def bstack1llll1111ll1_opy_(cls, response=None, product=bstack1l1l11l_opy_ (u"ࠨࠢ⇋")):
        if response == None or response.get(bstack1l1l11l_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ⇌")) == None:
            logger.error(product + bstack1l1l11l_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥ⇍"))
            return
        for error in response[bstack1l1l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ⇎")]:
            bstack111lll111l1_opy_ = error[bstack1l1l11l_opy_ (u"ࠪ࡯ࡪࡿࠧ⇏")]
            error_message = error[bstack1l1l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⇐")]
            if error_message:
                if bstack111lll111l1_opy_ == bstack1l1l11l_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦ⇑"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1l11l_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢ⇒") + product + bstack1l1l11l_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ⇓"))
    @classmethod
    def bstack1llll111l11l_opy_(cls):
        if cls.bstack1llll1ll11ll_opy_ is not None:
            return
        cls.bstack1llll1ll11ll_opy_ = bstack1llll1lll1l1_opy_(cls.bstack1llll11l11l1_opy_)
        cls.bstack1llll1ll11ll_opy_.start()
    @classmethod
    def bstack1111lll1l1_opy_(cls):
        if cls.bstack1llll1ll11ll_opy_ is None:
            return
        cls.bstack1llll1ll11ll_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll11l11l1_opy_(cls, bstack111l11111l_opy_, event_url=bstack1l1l11l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ⇔")):
        config = {
            bstack1l1l11l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ⇕"): cls.default_headers()
        }
        logger.debug(bstack1l1l11l_opy_ (u"ࠥࡴࡴࡹࡴࡠࡦࡤࡸࡦࡀࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡷࡩࡸࡺࡨࡶࡤࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡹࠠࡼࡿࠥ⇖").format(bstack1l1l11l_opy_ (u"ࠫ࠱ࠦࠧ⇗").join([event[bstack1l1l11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⇘")] for event in bstack111l11111l_opy_])))
        response = bstack11l1l1l111_opy_(bstack1l1l11l_opy_ (u"࠭ࡐࡐࡕࡗࠫ⇙"), cls.request_url(event_url), bstack111l11111l_opy_, config)
        bstack11ll111ll11_opy_ = response.json()
    @classmethod
    def bstack1ll1l111ll_opy_(cls, bstack111l11111l_opy_, event_url=bstack1l1l11l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭⇚")):
        logger.debug(bstack1l1l11l_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥࡧࡤࡥࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⇛").format(bstack111l11111l_opy_[bstack1l1l11l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⇜")]))
        if not bstack1lll1l1111_opy_.bstack1llll1111111_opy_(bstack111l11111l_opy_[bstack1l1l11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⇝")]):
            logger.debug(bstack1l1l11l_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡐࡲࡸࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⇞").format(bstack111l11111l_opy_[bstack1l1l11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⇟")]))
            return
        bstack11l11l11_opy_ = bstack1lll1l1111_opy_.bstack1llll111111l_opy_(bstack111l11111l_opy_[bstack1l1l11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⇠")], bstack111l11111l_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⇡")))
        if bstack11l11l11_opy_ != None:
            if bstack111l11111l_opy_.get(bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⇢")) != None:
                bstack111l11111l_opy_[bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⇣")][bstack1l1l11l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⇤")] = bstack11l11l11_opy_
            else:
                bstack111l11111l_opy_[bstack1l1l11l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ⇥")] = bstack11l11l11_opy_
        if event_url == bstack1l1l11l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ⇦"):
            cls.bstack1llll111l11l_opy_()
            logger.debug(bstack1l1l11l_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⇧").format(bstack111l11111l_opy_[bstack1l1l11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⇨")]))
            cls.bstack1llll1ll11ll_opy_.add(bstack111l11111l_opy_)
        elif event_url == bstack1l1l11l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭⇩"):
            cls.bstack1llll11l11l1_opy_([bstack111l11111l_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack11ll11ll11_opy_(cls, logs):
        for log in logs:
            bstack1llll111llll_opy_ = {
                bstack1l1l11l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ⇪"): bstack1l1l11l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬ⇫"),
                bstack1l1l11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⇬"): log[bstack1l1l11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⇭")],
                bstack1l1l11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⇮"): log[bstack1l1l11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⇯")],
                bstack1l1l11l_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨ⇰"): {},
                bstack1l1l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⇱"): log[bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⇲")],
            }
            if bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⇳") in log:
                bstack1llll111llll_opy_[bstack1l1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⇴")] = log[bstack1l1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⇵")]
            elif bstack1l1l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⇶") in log:
                bstack1llll111llll_opy_[bstack1l1l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⇷")] = log[bstack1l1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⇸")]
            cls.bstack1ll1l111ll_opy_({
                bstack1l1l11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⇹"): bstack1l1l11l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⇺"),
                bstack1l1l11l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ⇻"): [bstack1llll111llll_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1111l11_opy_(cls, steps):
        bstack1llll11111ll_opy_ = []
        for step in steps:
            bstack1lll1lllllll_opy_ = {
                bstack1l1l11l_opy_ (u"࠭࡫ࡪࡰࡧࠫ⇼"): bstack1l1l11l_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪ⇽"),
                bstack1l1l11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⇾"): step[bstack1l1l11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⇿")],
                bstack1l1l11l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭∀"): step[bstack1l1l11l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ∁")],
                bstack1l1l11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭∂"): step[bstack1l1l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ∃")],
                bstack1l1l11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ∄"): step[bstack1l1l11l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ∅")]
            }
            if bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ∆") in step:
                bstack1lll1lllllll_opy_[bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ∇")] = step[bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ∈")]
            elif bstack1l1l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ∉") in step:
                bstack1lll1lllllll_opy_[bstack1l1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭∊")] = step[bstack1l1l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ∋")]
            bstack1llll11111ll_opy_.append(bstack1lll1lllllll_opy_)
        cls.bstack1ll1l111ll_opy_({
            bstack1l1l11l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ∌"): bstack1l1l11l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭∍"),
            bstack1l1l11l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ∎"): bstack1llll11111ll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1l111lll_opy_, stage=STAGE.bstack1l1111l11l_opy_)
    def bstack11llll1lll_opy_(cls, screenshot):
        cls.bstack1ll1l111ll_opy_({
            bstack1l1l11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ∏"): bstack1l1l11l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ∐"),
            bstack1l1l11l_opy_ (u"࠭࡬ࡰࡩࡶࠫ∑"): [{
                bstack1l1l11l_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ−"): bstack1l1l11l_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪ∓"),
                bstack1l1l11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ∔"): datetime.datetime.utcnow().isoformat() + bstack1l1l11l_opy_ (u"ࠪ࡞ࠬ∕"),
                bstack1l1l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ∖"): screenshot[bstack1l1l11l_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ∗")],
                bstack1l1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭∘"): screenshot[bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ∙")]
            }]
        }, event_url=bstack1l1l11l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭√"))
    @classmethod
    @error_handler(class_method=True)
    def bstack11l111l111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1ll1l111ll_opy_({
            bstack1l1l11l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭∛"): bstack1l1l11l_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ∜"),
            bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭∝"): {
                bstack1l1l11l_opy_ (u"ࠧࡻࡵࡪࡦࠥ∞"): cls.current_test_uuid(),
                bstack1l1l11l_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧ∟"): cls.bstack111lll1111_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll11lll_opy_(cls, event: str, bstack111l11111l_opy_: bstack111l1l1l11_opy_):
        bstack111l11llll_opy_ = {
            bstack1l1l11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ∠"): event,
            bstack111l11111l_opy_.bstack111l1l1lll_opy_(): bstack111l11111l_opy_.bstack111l11l11l_opy_(event)
        }
        cls.bstack1ll1l111ll_opy_(bstack111l11llll_opy_)
        result = getattr(bstack111l11111l_opy_, bstack1l1l11l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ∡"), None)
        if event == bstack1l1l11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ∢"):
            threading.current_thread().bstackTestMeta = {bstack1l1l11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ∣"): bstack1l1l11l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ∤")}
        elif event == bstack1l1l11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ∥"):
            threading.current_thread().bstackTestMeta = {bstack1l1l11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭∦"): getattr(result, bstack1l1l11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ∧"), bstack1l1l11l_opy_ (u"ࠨࠩ∨"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭∩"), None) is None or os.environ[bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ∪")] == bstack1l1l11l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ∫")) and (os.environ.get(bstack1l1l11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ∬"), None) is None or os.environ[bstack1l1l11l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ∭")] == bstack1l1l11l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ∮")):
            return False
        return True
    @staticmethod
    def bstack1llll1111l1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1111ll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1l11l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ∯"): bstack1l1l11l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ∰"),
            bstack1l1l11l_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭∱"): bstack1l1l11l_opy_ (u"ࠫࡹࡸࡵࡦࠩ∲")
        }
        if os.environ.get(bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ∳"), None):
            headers[bstack1l1l11l_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭∴")] = bstack1l1l11l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ∵").format(os.environ[bstack1l1l11l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧ∶")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1l11l_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ∷").format(bstack1lll1lllll11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ∸"), None)
    @staticmethod
    def bstack111lll1111_opy_(driver):
        return {
            bstack111llllll11_opy_(): bstack111l1l111l1_opy_(driver)
        }
    @staticmethod
    def bstack1llll1111lll_opy_(exception_info, report):
        return [{bstack1l1l11l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ∹"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1llllll1ll1_opy_(typename):
        if bstack1l1l11l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ∺") in typename:
            return bstack1l1l11l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ∻")
        return bstack1l1l11l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ∼")
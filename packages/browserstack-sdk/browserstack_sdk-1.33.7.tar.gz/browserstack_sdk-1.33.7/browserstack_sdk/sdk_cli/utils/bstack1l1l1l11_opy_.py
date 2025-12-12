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
import shutil
import tempfile
import threading
import urllib.request
import uuid
from pathlib import Path
import logging
import re
from bstack_utils.helper import bstack1l1l1l111ll_opy_
bstack11ll1ll11ll_opy_ = 100 * 1024 * 1024 # 100 bstack11ll1lll11l_opy_
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
bstack1l1l11l1l11_opy_ = bstack1l1l1l111ll_opy_()
bstack1l1l1llllll_opy_ = bstack1l1l11l_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᙏ")
bstack11lll1l1lll_opy_ = bstack1l1l11l_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᙐ")
bstack11lll1l1l1l_opy_ = bstack1l1l11l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᙑ")
bstack11lll1ll11l_opy_ = bstack1l1l11l_opy_ (u"ࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰࠧᙒ")
bstack11ll1ll1lll_opy_ = bstack1l1l11l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠤᙓ")
_11ll1l1lll1_opy_ = threading.local()
def bstack11llll11l11_opy_(test_framework_state, test_hook_state):
    bstack1l1l11l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘ࡫ࡴࠡࡶ࡫ࡩࠥࡩࡵࡳࡴࡨࡲࡹࠦࡴࡦࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡺࡨࡳࡧࡤࡨ࠲ࡲ࡯ࡤࡣ࡯ࠤࡸࡺ࡯ࡳࡣࡪࡩ࠳ࠐࠠࠡࠢࠣࡘ࡭࡯ࡳࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡷ࡭ࡵࡵ࡭ࡦࠣࡦࡪࠦࡣࡢ࡮࡯ࡩࡩࠦࡢࡺࠢࡷ࡬ࡪࠦࡥࡷࡧࡱࡸࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࠨࡴࡷࡦ࡬ࠥࡧࡳࠡࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹ࠯ࠊࠡࠢࠣࠤࡧ࡫ࡦࡰࡴࡨࠤࡦࡴࡹࠡࡨ࡬ࡰࡪࠦࡵࡱ࡮ࡲࡥࡩࡹࠠࡰࡥࡦࡹࡷ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᙔ")
    _11ll1l1lll1_opy_.test_framework_state = test_framework_state
    _11ll1l1lll1_opy_.test_hook_state = test_hook_state
def bstack11ll1ll111l_opy_():
    bstack1l1l11l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡘࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࠥࡺࡥࡴࡶࠣࡩࡻ࡫࡮ࡵࠢࡶࡸࡦࡺࡥࠡࡨࡵࡳࡲࠦࡴࡩࡴࡨࡥࡩ࠳࡬ࡰࡥࡤࡰࠥࡹࡴࡰࡴࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡧࠠࡵࡷࡳࡰࡪࠦࠨࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࠬࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࠬࠤࡴࡸࠠࠩࡐࡲࡲࡪ࠲ࠠࡏࡱࡱࡩ࠮ࠦࡩࡧࠢࡱࡳࡹࠦࡳࡦࡶ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᙕ")
    return (
        getattr(_11ll1l1lll1_opy_, bstack1l1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪ࠭ᙖ"), None),
        getattr(_11ll1l1lll1_opy_, bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࠩᙗ"), None)
    )
class bstack111l1lll1_opy_:
    bstack1l1l11l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡈ࡬ࡰࡪ࡛ࡰ࡭ࡱࡤࡨࡪࡸࠠࡱࡴࡲࡺ࡮ࡪࡥࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱࡥࡱ࡯ࡴࡺࠢࡷࡳࠥࡻࡰ࡭ࡱࡤࡨࠥࡧ࡮ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡨࡡࡴࡧࡧࠤࡴࡴࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࡎࡺࠠࡴࡷࡳࡴࡴࡸࡴࡴࠢࡥࡳࡹ࡮ࠠ࡭ࡱࡦࡥࡱࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵࠣࡥࡳࡪࠠࡉࡖࡗࡔ࠴ࡎࡔࡕࡒࡖࠤ࡚ࡘࡌࡴ࠮ࠣࡥࡳࡪࠠࡤࡱࡳ࡭ࡪࡹࠠࡵࡪࡨࠤ࡫࡯࡬ࡦࠢ࡬ࡲࡹࡵࠠࡢࠢࡧࡩࡸ࡯ࡧ࡯ࡣࡷࡩࡩࠐࠠࠡࠢࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡷࡪࡶ࡫࡭ࡳࠦࡴࡩࡧࠣࡹࡸ࡫ࡲࠨࡵࠣ࡬ࡴࡳࡥࠡࡨࡲࡰࡩ࡫ࡲࠡࡷࡱࡨࡪࡸࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࡉࡧࠢࡤࡲࠥࡵࡰࡵ࡫ࡲࡲࡦࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࠠࠩ࡫ࡱࠤࡏ࡙ࡏࡏࠢࡩࡳࡷࡳࡡࡵࠫࠣ࡭ࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡣࡱࡨࠥࡩ࡯࡯ࡶࡤ࡭ࡳࡹࠠࡢࠢࡷࡶࡺࡺࡨࡺࠢࡹࡥࡱࡻࡥࠋࠢࠣࠤࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦ࡫ࡦࡻࠣࠦࡧࡻࡩ࡭ࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨࠬࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡵࡲࡡࡤࡧࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡪࡴࡲࡤࡦࡴ࠾ࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠬࠋࠢࠣࠤࠥ࡯ࡴࠡࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡱࡩࠤࡦࡪࡤࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡯ࡳࠡࡣࠣࡺࡴ࡯ࡤࠡ࡯ࡨࡸ࡭ࡵࡤ⠕࡫ࡷࠤ࡭ࡧ࡮ࡥ࡮ࡨࡷࠥࡧ࡬࡭ࠢࡨࡶࡷࡵࡲࡴࠢࡪࡶࡦࡩࡥࡧࡷ࡯ࡰࡾࠦࡢࡺࠢ࡯ࡳ࡬࡭ࡩ࡯ࡩࠍࠤࠥࠦࠠࡵࡪࡨࡱࠥࡧ࡮ࡥࠢࡶ࡭ࡲࡶ࡬ࡺࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡽࡩࡵࡪࡲࡹࡹࠦࡴࡩࡴࡲࡻ࡮ࡴࡧࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱࡷ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᙘ")
    @staticmethod
    def upload_attachment(bstack11ll1ll11l1_opy_: str, *bstack11ll1llll1l_opy_) -> None:
        if not bstack11ll1ll11l1_opy_ or not bstack11ll1ll11l1_opy_.strip():
            logger.error(bstack1l1l11l_opy_ (u"ࠤࡤࡨࡩࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡕࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࠢ࡬ࡷࠥ࡫࡭ࡱࡶࡼࠤࡴࡸࠠࡏࡱࡱࡩ࠳ࠨᙙ"))
            return
        bstack11ll1lll111_opy_ = bstack11ll1llll1l_opy_[0] if bstack11ll1llll1l_opy_ and len(bstack11ll1llll1l_opy_) > 0 else None
        bstack11ll1llll11_opy_ = None
        test_framework_state, test_hook_state = bstack11ll1ll111l_opy_()
        try:
            if bstack11ll1ll11l1_opy_.startswith(bstack1l1l11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᙚ")) or bstack11ll1ll11l1_opy_.startswith(bstack1l1l11l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᙛ")):
                logger.debug(bstack1l1l11l_opy_ (u"ࠧࡖࡡࡵࡪࠣ࡭ࡸࠦࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡦࠣࡥࡸࠦࡕࡓࡎ࠾ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲ࠧᙜ"))
                url = bstack11ll1ll11l1_opy_
                bstack11ll1l1llll_opy_ = str(uuid.uuid4())
                bstack11ll1ll1l11_opy_ = os.path.basename(urllib.request.urlparse(url).path)
                if not bstack11ll1ll1l11_opy_ or not bstack11ll1ll1l11_opy_.strip():
                    bstack11ll1ll1l11_opy_ = bstack11ll1l1llll_opy_
                temp_file = tempfile.NamedTemporaryFile(delete=False,
                                                        prefix=bstack1l1l11l_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩࡥࠢᙝ") + bstack11ll1l1llll_opy_ + bstack1l1l11l_opy_ (u"ࠢࡠࠤᙞ"),
                                                        suffix=bstack1l1l11l_opy_ (u"ࠣࡡࠥᙟ") + bstack11ll1ll1l11_opy_)
                with urllib.request.urlopen(url) as response, open(temp_file.name, bstack1l1l11l_opy_ (u"ࠩࡺࡦࠬᙠ")) as out_file:
                    shutil.copyfileobj(response, out_file)
                bstack11ll1llll11_opy_ = Path(temp_file.name)
                logger.debug(bstack1l1l11l_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡧ࡫࡯ࡩࠥࡺ࡯ࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡱࡵࡣࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᙡ").format(bstack11ll1llll11_opy_))
            else:
                bstack11ll1llll11_opy_ = Path(bstack11ll1ll11l1_opy_)
                logger.debug(bstack1l1l11l_opy_ (u"ࠦࡕࡧࡴࡩࠢ࡬ࡷࠥ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡥࠢࡤࡷࠥࡲ࡯ࡤࡣ࡯ࠤ࡫࡯࡬ࡦ࠼ࠣࡿࢂࠨᙢ").format(bstack11ll1llll11_opy_))
        except Exception as e:
            logger.error(bstack1l1l11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡱࡥࡸࡦ࡯࡮ࠡࡨ࡬ࡰࡪࠦࡦࡳࡱࡰࠤࡵࡧࡴࡩ࠱ࡘࡖࡑࡀࠠࡼࡿࠥᙣ").format(e))
            return
        if bstack11ll1llll11_opy_ is None or not bstack11ll1llll11_opy_.exists():
            logger.error(bstack1l1l11l_opy_ (u"ࠨࡓࡰࡷࡵࡧࡪࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠤᙤ").format(bstack11ll1llll11_opy_))
            return
        if bstack11ll1llll11_opy_.stat().st_size > bstack11ll1ll11ll_opy_:
            logger.error(bstack1l1l11l_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡹࡩࡻࡧࠣࡩࡽࡩࡥࡦࡦࡶࠤࡲࡧࡸࡪ࡯ࡸࡱࠥࡧ࡬࡭ࡱࡺࡩࡩࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡼࡿࠥᙥ").format(bstack11ll1ll11ll_opy_))
            return
        bstack11ll1ll1111_opy_ = bstack1l1l11l_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᙦ")
        if bstack11ll1lll111_opy_:
            try:
                params = json.loads(bstack11ll1lll111_opy_)
                if bstack1l1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᙧ") in params and params.get(bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᙨ")) is True:
                    bstack11ll1ll1111_opy_ = bstack1l1l11l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᙩ")
            except Exception as bstack11ll1l1ll11_opy_:
                logger.error(bstack1l1l11l_opy_ (u"ࠧࡐࡓࡐࡐࠣࡴࡦࡸࡳࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣ࡭ࡳࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡓࡥࡷࡧ࡭ࡴ࠼ࠣࡿࢂࠨᙪ").format(bstack11ll1l1ll11_opy_))
        bstack11ll1ll1ll1_opy_ = False
        from browserstack_sdk.sdk_cli.bstack1lll111l111_opy_ import bstack1ll1l1111l1_opy_
        if test_framework_state in bstack1ll1l1111l1_opy_.bstack11llllllll1_opy_:
            if bstack11ll1ll1111_opy_ == bstack11lll1l1l1l_opy_:
                bstack11ll1ll1ll1_opy_ = True
            bstack11ll1ll1111_opy_ = bstack11lll1ll11l_opy_
        try:
            platform_index = os.environ[bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᙫ")]
            target_dir = os.path.join(bstack1l1l11l1l11_opy_, bstack1l1l1llllll_opy_ + str(platform_index),
                                      bstack11ll1ll1111_opy_)
            if bstack11ll1ll1ll1_opy_:
                target_dir = os.path.join(target_dir, bstack11ll1ll1lll_opy_)
            os.makedirs(target_dir, exist_ok=True)
            logger.debug(bstack1l1l11l_opy_ (u"ࠢࡄࡴࡨࡥࡹ࡫ࡤ࠰ࡸࡨࡶ࡮࡬ࡩࡦࡦࠣࡸࡦࡸࡧࡦࡶࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᙬ").format(target_dir))
            file_name = os.path.basename(bstack11ll1llll11_opy_)
            bstack11ll1lll1l1_opy_ = os.path.join(target_dir, file_name)
            if os.path.exists(bstack11ll1lll1l1_opy_):
                base_name, extension = os.path.splitext(file_name)
                bstack11ll1lll1ll_opy_ = 1
                while os.path.exists(os.path.join(target_dir, base_name + str(bstack11ll1lll1ll_opy_) + extension)):
                    bstack11ll1lll1ll_opy_ += 1
                bstack11ll1lll1l1_opy_ = os.path.join(target_dir, base_name + str(bstack11ll1lll1ll_opy_) + extension)
            shutil.copy(bstack11ll1llll11_opy_, bstack11ll1lll1l1_opy_)
            logger.info(bstack1l1l11l_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡩ࡯ࡱ࡫ࡨࡨࠥࡺ࡯࠻ࠢࡾࢁࠧ᙭").format(bstack11ll1lll1l1_opy_))
        except Exception as e:
            logger.error(bstack1l1l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡯ࡲࡺ࡮ࡴࡧࠡࡨ࡬ࡰࡪࠦࡴࡰࠢࡷࡥࡷ࡭ࡥࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠿ࠦࡻࡾࠤ᙮").format(e))
            return
        finally:
            if bstack11ll1ll11l1_opy_.startswith(bstack1l1l11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᙯ")) or bstack11ll1ll11l1_opy_.startswith(bstack1l1l11l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᙰ")):
                try:
                    if bstack11ll1llll11_opy_ is not None and bstack11ll1llll11_opy_.exists():
                        bstack11ll1llll11_opy_.unlink()
                        logger.debug(bstack1l1l11l_opy_ (u"࡚ࠧࡥ࡮ࡲࡲࡶࡦࡸࡹࠡࡨ࡬ࡰࡪࠦࡤࡦ࡮ࡨࡸࡪࡪ࠺ࠡࡽࢀࠦᙱ").format(bstack11ll1llll11_opy_))
                except Exception as ex:
                    logger.error(bstack1l1l11l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡵࡧࡰࡴࡴࡸࡡࡳࡻࠣࡪ࡮ࡲࡥ࠻ࠢࡾࢁࠧᙲ").format(ex))
    @staticmethod
    def bstack1111l1ll1_opy_() -> None:
        bstack1l1l11l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡉ࡫࡬ࡦࡶࡨࡷࠥࡧ࡬࡭ࠢࡩࡳࡱࡪࡥࡳࡵࠣࡻ࡭ࡵࡳࡦࠢࡱࡥࡲ࡫ࡳࠡࡵࡷࡥࡷࡺࠠࡸ࡫ࡷ࡬ࠥࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨࠠࡧࡱ࡯ࡰࡴࡽࡥࡥࠢࡥࡽࠥࡧࠠ࡯ࡷࡰࡦࡪࡸࠠࡪࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡥࠡࡷࡶࡩࡷ࠭ࡳࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᙳ")
        bstack11ll1ll1l1l_opy_ = bstack1l1l1l111ll_opy_()
        pattern = re.compile(bstack1l1l11l_opy_ (u"ࡳࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮࡞ࡧ࠯ࠧᙴ"))
        if os.path.exists(bstack11ll1ll1l1l_opy_):
            for item in os.listdir(bstack11ll1ll1l1l_opy_):
                bstack11ll1l1ll1l_opy_ = os.path.join(bstack11ll1ll1l1l_opy_, item)
                if os.path.isdir(bstack11ll1l1ll1l_opy_) and pattern.fullmatch(item):
                    try:
                        shutil.rmtree(bstack11ll1l1ll1l_opy_)
                    except Exception as e:
                        logger.error(bstack1l1l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࡀࠠࡼࡿࠥᙵ").format(e))
        else:
            logger.info(bstack1l1l11l_opy_ (u"ࠥࡘ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠣᙶ").format(bstack11ll1ll1l1l_opy_))
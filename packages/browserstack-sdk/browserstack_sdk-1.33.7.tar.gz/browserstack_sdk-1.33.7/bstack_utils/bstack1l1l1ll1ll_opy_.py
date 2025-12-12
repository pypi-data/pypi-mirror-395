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
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11l1l1ll1ll_opy_ import bstack11l1l1lll1l_opy_
from bstack_utils.constants import bstack11l11ll1ll1_opy_, bstack1l111l1ll_opy_
from bstack_utils.bstack111l1l1ll_opy_ import bstack1llllll111_opy_
from bstack_utils import bstack11l1l11111_opy_
bstack11l11l11111_opy_ = 10
class bstack1111111l1_opy_:
    def __init__(self, bstack11llllll_opy_, config, bstack11l111l1lll_opy_=0):
        self.bstack11l111lll11_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l11l111l1_opy_ = bstack1l1l11l_opy_ (u"ࠧࢁࡽ࠰ࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴࡬ࡡࡪ࡮ࡨࡨ࠲ࡺࡥࡴࡶࡶࠦ᮱").format(bstack11l11ll1ll1_opy_)
        self.bstack11l111l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃࠢ᮲").format(os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ᮳"))))
        self.bstack11l111l11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡼࡿ࠱ࡸࡽࡺࠢ᮴").format(os.environ.get(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ᮵"))))
        self.bstack11l1111llll_opy_ = 2
        self.bstack11llllll_opy_ = bstack11llllll_opy_
        self.config = config
        self.logger = bstack11l1l11111_opy_.get_logger(__name__, bstack1l111l1ll_opy_)
        self.bstack11l111l1lll_opy_ = bstack11l111l1lll_opy_
        self.bstack11l111l1l1l_opy_ = False
        self.bstack11l111lll1l_opy_ = not (
                            os.environ.get(bstack1l1l11l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠤ᮶")) and
                            os.environ.get(bstack1l1l11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ᮷")) and
                            os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢ᮸"))
                        )
        if bstack1llllll111_opy_.bstack11l111l1ll1_opy_(config):
            self.bstack11l1111llll_opy_ = bstack1llllll111_opy_.bstack11l111ll1l1_opy_(config, self.bstack11l111l1lll_opy_)
            self.bstack11l111l11ll_opy_()
    def bstack11l111ll111_opy_(self):
        return bstack1l1l11l_opy_ (u"ࠨࡻࡾࡡࡾࢁࠧ᮹").format(self.config.get(bstack1l1l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᮺ")), os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᮻ")))
    def bstack11l111lllll_opy_(self):
        try:
            if self.bstack11l111lll1l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l111l11l1_opy_, bstack1l1l11l_opy_ (u"ࠤࡵࠦᮼ")) as f:
                        bstack11l111l1111_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l111l1111_opy_ = set()
                bstack11l111l111l_opy_ = bstack11l111l1111_opy_ - self.bstack11l111lll11_opy_
                if not bstack11l111l111l_opy_:
                    return
                self.bstack11l111lll11_opy_.update(bstack11l111l111l_opy_)
                data = {bstack1l1l11l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡗࡩࡸࡺࡳࠣᮽ"): list(self.bstack11l111lll11_opy_), bstack1l1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢᮾ"): self.config.get(bstack1l1l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᮿ")), bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦᯀ"): os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᯁ")), bstack1l1l11l_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨᯂ"): self.config.get(bstack1l1l11l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᯃ"))}
            response = bstack11l1l1lll1l_opy_.bstack11l111ll1ll_opy_(self.bstack11l11l111l1_opy_, data)
            if response.get(bstack1l1l11l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥᯄ")) == 200:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡷࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦᯅ").format(data))
            else:
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤᯆ").format(response))
        except Exception as e:
            self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨᯇ").format(e))
    def bstack11l11l111ll_opy_(self):
        if self.bstack11l111lll1l_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l111l11l1_opy_, bstack1l1l11l_opy_ (u"ࠢࡳࠤᯈ")) as f:
                        bstack11l111ll11l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l111ll11l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠣࡒࡲࡰࡱ࡫ࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࠦࠨ࡭ࡱࡦࡥࡱ࠯࠺ࠡࡽࢀࠦᯉ").format(failed_count))
                if failed_count >= self.bstack11l1111llll_opy_:
                    self.logger.info(bstack1l1l11l_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࠦࠨ࡭ࡱࡦࡥࡱ࠯࠺ࠡࡽࢀࠤࡃࡃࠠࡼࡿࠥᯊ").format(failed_count, self.bstack11l1111llll_opy_))
                    self.bstack11l11l1111l_opy_(failed_count)
                    self.bstack11l111l1l1l_opy_ = True
            return
        try:
            response = bstack11l1l1lll1l_opy_.bstack11l11l111ll_opy_(bstack1l1l11l_opy_ (u"ࠥࡿࢂࡅࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦ࠿ࡾࢁࠫࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࡀࡿࢂࠬࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࡁࢀࢃࠢᯋ").format(self.bstack11l11l111l1_opy_, self.config.get(bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᯌ")), os.environ.get(bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᯍ")), self.config.get(bstack1l1l11l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᯎ"))))
            if response.get(bstack1l1l11l_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢᯏ")) == 200:
                failed_count = response.get(bstack1l1l11l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࡉ࡯ࡶࡰࡷࠦᯐ"), 0)
                self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦᯑ").format(failed_count))
                if failed_count >= self.bstack11l1111llll_opy_:
                    self.logger.info(bstack1l1l11l_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪ࠺ࠡࡽࢀࠤࡃࡃࠠࡼࡿࠥᯒ").format(failed_count, self.bstack11l1111llll_opy_))
                    self.bstack11l11l1111l_opy_(failed_count)
                    self.bstack11l111l1l1l_opy_ = True
            else:
                self.logger.error(bstack1l1l11l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡱ࡯ࡰࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣᯓ").format(response))
        except Exception as e:
            self.logger.error(bstack1l1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡦࡸࡶ࡮ࡴࡧࠡࡲࡲࡰࡱ࡯࡮ࡨ࠼ࠣࡿࢂࠨᯔ").format(e))
    def bstack11l11l1111l_opy_(self, failed_count):
        with open(self.bstack11l111l1l11_opy_, bstack1l1l11l_opy_ (u"ࠨࡷࠣᯕ")) as f:
            f.write(bstack1l1l11l_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤࡦࡺࠠࡼࡿ࡟ࡲࠧᯖ").format(datetime.now()))
            f.write(bstack1l1l11l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿ࡟ࡲࠧᯗ").format(failed_count))
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡄࡦࡴࡸࡴࠡࡄࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥࡩࡲࡦࡣࡷࡩࡩࡀࠠࡼࡿࠥᯘ").format(self.bstack11l111l1l11_opy_))
    def bstack11l111l11ll_opy_(self):
        def bstack11l11l11l11_opy_():
            while not self.bstack11l111l1l1l_opy_:
                time.sleep(bstack11l11l11111_opy_)
                self.bstack11l111lllll_opy_()
                self.bstack11l11l111ll_opy_()
        bstack11l111llll1_opy_ = threading.Thread(target=bstack11l11l11l11_opy_, daemon=True)
        bstack11l111llll1_opy_.start()
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
from bstack_utils.bstack11l1l11111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11l1ll11l1l_opy_(object):
  bstack11l1l1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l1l11l_opy_ (u"ࠫࢃ࠭ᠢ")), bstack1l1l11l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᠣ"))
  bstack11l1ll111l1_opy_ = os.path.join(bstack11l1l1lll1_opy_, bstack1l1l11l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ࠭ᠤ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1llll1l11l_opy_ = None
  bstack1l11ll1l11_opy_ = None
  bstack11ll1111111_opy_ = None
  bstack11l1lll1lll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1l11l_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦࠩᠥ")):
      cls.instance = super(bstack11l1ll11l1l_opy_, cls).__new__(cls)
      cls.instance.bstack11l1ll111ll_opy_()
    return cls.instance
  def bstack11l1ll111ll_opy_(self):
    try:
      with open(self.bstack11l1ll111l1_opy_, bstack1l1l11l_opy_ (u"ࠨࡴࠪᠦ")) as bstack1ll11l11l1_opy_:
        bstack11l1ll1111l_opy_ = bstack1ll11l11l1_opy_.read()
        data = json.loads(bstack11l1ll1111l_opy_)
        if bstack1l1l11l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᠧ") in data:
          self.bstack11ll11l1111_opy_(data[bstack1l1l11l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᠨ")])
        if bstack1l1l11l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᠩ") in data:
          self.bstack111lll11l_opy_(data[bstack1l1l11l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᠪ")])
        if bstack1l1l11l_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᠫ") in data:
          self.bstack11l1ll11l11_opy_(data[bstack1l1l11l_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᠬ")])
    except:
      pass
  def bstack11l1ll11l11_opy_(self, bstack11l1lll1lll_opy_):
    if bstack11l1lll1lll_opy_ != None:
      self.bstack11l1lll1lll_opy_ = bstack11l1lll1lll_opy_
  def bstack111lll11l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1l11l_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᠭ"),bstack1l1l11l_opy_ (u"ࠩࠪᠮ"))
      self.bstack1llll1l11l_opy_ = scripts.get(bstack1l1l11l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧᠯ"),bstack1l1l11l_opy_ (u"ࠫࠬᠰ"))
      self.bstack1l11ll1l11_opy_ = scripts.get(bstack1l1l11l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩᠱ"),bstack1l1l11l_opy_ (u"࠭ࠧᠲ"))
      self.bstack11ll1111111_opy_ = scripts.get(bstack1l1l11l_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᠳ"),bstack1l1l11l_opy_ (u"ࠨࠩᠴ"))
  def bstack11ll11l1111_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11l1ll111l1_opy_, bstack1l1l11l_opy_ (u"ࠩࡺࠫᠵ")) as file:
        json.dump({
          bstack1l1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧᠶ"): self.commands_to_wrap,
          bstack1l1l11l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᠷ"): {
            bstack1l1l11l_opy_ (u"ࠧࡹࡣࡢࡰࠥᠸ"): self.perform_scan,
            bstack1l1l11l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᠹ"): self.bstack1llll1l11l_opy_,
            bstack1l1l11l_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᠺ"): self.bstack1l11ll1l11_opy_,
            bstack1l1l11l_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᠻ"): self.bstack11ll1111111_opy_
          },
          bstack1l1l11l_opy_ (u"ࠤࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸࠨᠼ"): self.bstack11l1lll1lll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1l11l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠾ࠥࢁࡽࠣᠽ").format(e))
      pass
  def bstack111llll1_opy_(self, command_name):
    try:
      return any(command.get(bstack1l1l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᠾ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1lll111l_opy_ = bstack11l1ll11l1l_opy_()
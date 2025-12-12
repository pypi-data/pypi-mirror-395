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
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1l1l1l1l_opy_():
  def __init__(self, args, logger, bstack11111l1ll1_opy_, bstack11111ll1ll_opy_, bstack1lllllll1l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack11111l1ll1_opy_ = bstack11111l1ll1_opy_
    self.bstack11111ll1ll_opy_ = bstack11111ll1ll_opy_
    self.bstack1lllllll1l1_opy_ = bstack1lllllll1l1_opy_
  def bstack1l11l11l11_opy_(self, bstack11111ll1l1_opy_, bstack1ll11ll1l1_opy_, bstack1lllllll11l_opy_=False):
    bstack1lll11lll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1llllllll1l_opy_ = manager.list()
    bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
    if bstack1lllllll11l_opy_:
      for index, platform in enumerate(self.bstack11111l1ll1_opy_[bstack1l1l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫგ")]):
        if index == 0:
          bstack1ll11ll1l1_opy_[bstack1l1l11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬდ")] = self.args
        bstack1lll11lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111ll1l1_opy_,
                                                    args=(bstack1ll11ll1l1_opy_, bstack1llllllll1l_opy_)))
    else:
      for index, platform in enumerate(self.bstack11111l1ll1_opy_[bstack1l1l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ე")]):
        bstack1lll11lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111ll1l1_opy_,
                                                    args=(bstack1ll11ll1l1_opy_, bstack1llllllll1l_opy_)))
    i = 0
    for t in bstack1lll11lll_opy_:
      try:
        if bstack1ll1l111l1_opy_.get_property(bstack1l1l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬვ")):
          os.environ[bstack1l1l11l_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ზ")] = json.dumps(self.bstack11111l1ll1_opy_[bstack1l1l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩთ")][i % self.bstack1lllllll1l1_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵ࠽ࠤࢀࢃࠢი").format(str(e)))
      i += 1
      t.start()
    for t in bstack1lll11lll_opy_:
      t.join()
    return list(bstack1llllllll1l_opy_)
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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11l1l1l111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1l1llll11_opy_ import bstack1l1ll1l11l_opy_
class bstack11l1111ll_opy_:
  working_dir = os.getcwd()
  bstack1ll1ll1111_opy_ = False
  config = {}
  bstack111l1l1llll_opy_ = bstack1l1l11l_opy_ (u"ࠩࠪᾳ")
  binary_path = bstack1l1l11l_opy_ (u"ࠪࠫᾴ")
  bstack1llllll1l1ll_opy_ = bstack1l1l11l_opy_ (u"ࠫࠬ᾵")
  bstack11111ll1l_opy_ = False
  bstack111111l1ll1_opy_ = None
  bstack1lllllll11l1_opy_ = {}
  bstack1lllllllll11_opy_ = 300
  bstack111111ll111_opy_ = False
  logger = None
  bstack111111lll11_opy_ = False
  bstack1l111lllll_opy_ = False
  percy_build_id = None
  bstack1llllll1ll11_opy_ = bstack1l1l11l_opy_ (u"ࠬ࠭ᾶ")
  bstack111111lllll_opy_ = {
    bstack1l1l11l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᾷ") : 1,
    bstack1l1l11l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᾸ") : 2,
    bstack1l1l11l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭Ᾱ") : 3,
    bstack1l1l11l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩᾺ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111111ll1l1_opy_(self):
    bstack111111l11l1_opy_ = bstack1l1l11l_opy_ (u"ࠪࠫΆ")
    bstack111111111l1_opy_ = sys.platform
    bstack1lllllll1111_opy_ = bstack1l1l11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᾼ")
    if re.match(bstack1l1l11l_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧ᾽"), bstack111111111l1_opy_) != None:
      bstack111111l11l1_opy_ = bstack11l1l11l1l1_opy_ + bstack1l1l11l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢι")
      self.bstack1llllll1ll11_opy_ = bstack1l1l11l_opy_ (u"ࠧ࡮ࡣࡦࠫ᾿")
    elif re.match(bstack1l1l11l_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨ῀"), bstack111111111l1_opy_) != None:
      bstack111111l11l1_opy_ = bstack11l1l11l1l1_opy_ + bstack1l1l11l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲࠥ῁")
      bstack1lllllll1111_opy_ = bstack1l1l11l_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨῂ")
      self.bstack1llllll1ll11_opy_ = bstack1l1l11l_opy_ (u"ࠫࡼ࡯࡮ࠨῃ")
    else:
      bstack111111l11l1_opy_ = bstack11l1l11l1l1_opy_ + bstack1l1l11l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣῄ")
      self.bstack1llllll1ll11_opy_ = bstack1l1l11l_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬ῅")
    return bstack111111l11l1_opy_, bstack1lllllll1111_opy_
  def bstack1111111lll1_opy_(self):
    try:
      bstack1llllllll11l_opy_ = [os.path.join(expanduser(bstack1l1l11l_opy_ (u"ࠢࡿࠤῆ")), bstack1l1l11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨῇ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1llllllll11l_opy_:
        if(self.bstack1111111l11l_opy_(path)):
          return path
      raise bstack1l1l11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨῈ")
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧΈ").format(e))
  def bstack1111111l11l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lllllll111l_opy_(self, bstack111111l111l_opy_):
    return os.path.join(bstack111111l111l_opy_, self.bstack111l1l1llll_opy_ + bstack1l1l11l_opy_ (u"ࠦ࠳࡫ࡴࡢࡩࠥῊ"))
  def bstack111111111ll_opy_(self, bstack111111l111l_opy_, bstack111111l1l1l_opy_):
    if not bstack111111l1l1l_opy_: return
    try:
      bstack111111lll1l_opy_ = self.bstack1lllllll111l_opy_(bstack111111l111l_opy_)
      with open(bstack111111lll1l_opy_, bstack1l1l11l_opy_ (u"ࠧࡽࠢΉ")) as f:
        f.write(bstack111111l1l1l_opy_)
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡓࡢࡸࡨࡨࠥࡴࡥࡸࠢࡈࡘࡦ࡭ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠥῌ"))
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡶ࡫ࡩࠥ࡫ࡴࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ῍").format(e))
  def bstack1llllll1lll1_opy_(self, bstack111111l111l_opy_):
    try:
      bstack111111lll1l_opy_ = self.bstack1lllllll111l_opy_(bstack111111l111l_opy_)
      if os.path.exists(bstack111111lll1l_opy_):
        with open(bstack111111lll1l_opy_, bstack1l1l11l_opy_ (u"ࠣࡴࠥ῎")) as f:
          bstack111111l1l1l_opy_ = f.read().strip()
          return bstack111111l1l1l_opy_ if bstack111111l1l1l_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡉ࡙ࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ῏").format(e))
  def bstack1llllll1l11l_opy_(self, bstack111111l111l_opy_, bstack111111l11l1_opy_):
    bstack1111111llll_opy_ = self.bstack1llllll1lll1_opy_(bstack111111l111l_opy_)
    if bstack1111111llll_opy_:
      try:
        bstack1lllllll1ll1_opy_ = self.bstack1llllllll111_opy_(bstack1111111llll_opy_, bstack111111l11l1_opy_)
        if not bstack1lllllll1ll1_opy_:
          self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡷࠥࡻࡰࠡࡶࡲࠤࡩࡧࡴࡦࠢࠫࡉ࡙ࡧࡧࠡࡷࡱࡧ࡭ࡧ࡮ࡨࡧࡧ࠭ࠧῐ"))
          return True
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠦࡓ࡫ࡷࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡹࡵࡪࡡࡵࡧࠥῑ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1l11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡧࡱࡵࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦῒ").format(e))
    return False
  def bstack1llllllll111_opy_(self, bstack1111111llll_opy_, bstack111111l11l1_opy_):
    try:
      headers = {
        bstack1l1l11l_opy_ (u"ࠨࡉࡧ࠯ࡑࡳࡳ࡫࠭ࡎࡣࡷࡧ࡭ࠨΐ"): bstack1111111llll_opy_
      }
      response = bstack11l1l1l111_opy_(bstack1l1l11l_opy_ (u"ࠧࡈࡇࡗࠫ῔"), bstack111111l11l1_opy_, {}, {bstack1l1l11l_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤ῕"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹ࠺ࠡࡽࢀࠦῖ").format(e))
  @measure(event_name=EVENTS.bstack11l11l11lll_opy_, stage=STAGE.bstack1l1111l11l_opy_)
  def bstack11111l11l11_opy_(self, bstack111111l11l1_opy_, bstack1lllllll1111_opy_):
    try:
      bstack11111111111_opy_ = self.bstack1111111lll1_opy_()
      bstack1llllll1llll_opy_ = os.path.join(bstack11111111111_opy_, bstack1l1l11l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭ῗ"))
      bstack1llllll1ll1l_opy_ = os.path.join(bstack11111111111_opy_, bstack1lllllll1111_opy_)
      if self.bstack1llllll1l11l_opy_(bstack11111111111_opy_, bstack111111l11l1_opy_): # if bstack1llllllllll1_opy_, bstack1l11llll1l1_opy_ bstack111111l1l1l_opy_ is bstack11111l1111l_opy_ to bstack111ll1l111l_opy_ version available (response 304)
        if os.path.exists(bstack1llllll1ll1l_opy_):
          self.logger.info(bstack1l1l11l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨῘ").format(bstack1llllll1ll1l_opy_))
          return bstack1llllll1ll1l_opy_
        if os.path.exists(bstack1llllll1llll_opy_):
          self.logger.info(bstack1l1l11l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥῙ").format(bstack1llllll1llll_opy_))
          return self.bstack1lllllll1l1l_opy_(bstack1llllll1llll_opy_, bstack1lllllll1111_opy_)
      self.logger.info(bstack1l1l11l_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦῚ").format(bstack111111l11l1_opy_))
      response = bstack11l1l1l111_opy_(bstack1l1l11l_opy_ (u"ࠧࡈࡇࡗࠫΊ"), bstack111111l11l1_opy_, {}, {})
      if response.status_code == 200:
        bstack111111l1lll_opy_ = response.headers.get(bstack1l1l11l_opy_ (u"ࠣࡇࡗࡥ࡬ࠨ῜"), bstack1l1l11l_opy_ (u"ࠤࠥ῝"))
        if bstack111111l1lll_opy_:
          self.bstack111111111ll_opy_(bstack11111111111_opy_, bstack111111l1lll_opy_)
        with open(bstack1llllll1llll_opy_, bstack1l1l11l_opy_ (u"ࠪࡻࡧ࠭῞")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1l11l_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡾࠤ῟").format(bstack1llllll1llll_opy_))
        return self.bstack1lllllll1l1l_opy_(bstack1llllll1llll_opy_, bstack1lllllll1111_opy_)
      else:
        raise(bstack1l1l11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡽࠣῠ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢῡ").format(e))
  def bstack111111llll1_opy_(self, bstack111111l11l1_opy_, bstack1lllllll1111_opy_):
    try:
      retry = 2
      bstack1llllll1ll1l_opy_ = None
      bstack11111111l1l_opy_ = False
      while retry > 0:
        bstack1llllll1ll1l_opy_ = self.bstack11111l11l11_opy_(bstack111111l11l1_opy_, bstack1lllllll1111_opy_)
        bstack11111111l1l_opy_ = self.bstack11111111lll_opy_(bstack111111l11l1_opy_, bstack1lllllll1111_opy_, bstack1llllll1ll1l_opy_)
        if bstack11111111l1l_opy_:
          break
        retry -= 1
      return bstack1llllll1ll1l_opy_, bstack11111111l1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦῢ").format(e))
    return bstack1llllll1ll1l_opy_, False
  def bstack11111111lll_opy_(self, bstack111111l11l1_opy_, bstack1lllllll1111_opy_, bstack1llllll1ll1l_opy_, bstack11111l11l1l_opy_ = 0):
    if bstack11111l11l1l_opy_ > 1:
      return False
    if bstack1llllll1ll1l_opy_ == None or os.path.exists(bstack1llllll1ll1l_opy_) == False:
      self.logger.warn(bstack1l1l11l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨΰ"))
      return False
    bstack111111l1l11_opy_ = bstack1l1l11l_opy_ (u"ࡴࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫ࠣࡠࡩ࠱࡜࠯࡞ࡧ࠯ࡡ࠴࡜ࡥ࠭ࠥῤ")
    command = bstack1l1l11l_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩῥ").format(bstack1llllll1ll1l_opy_)
    bstack1lllllllllll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111111l1l11_opy_, bstack1lllllllllll_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥῦ"))
      return False
  def bstack1lllllll1l1l_opy_(self, bstack1llllll1llll_opy_, bstack1lllllll1111_opy_):
    try:
      working_dir = os.path.dirname(bstack1llllll1llll_opy_)
      shutil.unpack_archive(bstack1llllll1llll_opy_, working_dir)
      bstack1llllll1ll1l_opy_ = os.path.join(working_dir, bstack1lllllll1111_opy_)
      os.chmod(bstack1llllll1ll1l_opy_, 0o755)
      return bstack1llllll1ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨῧ"))
  def bstack111111ll11l_opy_(self):
    try:
      bstack1llllllll1l1_opy_ = self.config.get(bstack1l1l11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬῨ"))
      bstack111111ll11l_opy_ = bstack1llllllll1l1_opy_ or (bstack1llllllll1l1_opy_ is None and self.bstack1ll1ll1111_opy_)
      if not bstack111111ll11l_opy_ or self.config.get(bstack1l1l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪῩ"), None) not in bstack11l11lllll1_opy_:
        return False
      self.bstack11111ll1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥῪ").format(e))
  def bstack11111l11111_opy_(self):
    try:
      bstack11111l11111_opy_ = self.percy_capture_mode
      return bstack11111l11111_opy_
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥΎ").format(e))
  def init(self, bstack1ll1ll1111_opy_, config, logger):
    self.bstack1ll1ll1111_opy_ = bstack1ll1ll1111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111111ll11l_opy_():
      return
    self.bstack1lllllll11l1_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩῬ"), {})
    self.percy_capture_mode = config.get(bstack1l1l11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ῭"))
    try:
      bstack111111l11l1_opy_, bstack1lllllll1111_opy_ = self.bstack111111ll1l1_opy_()
      self.bstack111l1l1llll_opy_ = bstack1lllllll1111_opy_
      bstack1llllll1ll1l_opy_, bstack11111111l1l_opy_ = self.bstack111111llll1_opy_(bstack111111l11l1_opy_, bstack1lllllll1111_opy_)
      if bstack11111111l1l_opy_:
        self.binary_path = bstack1llllll1ll1l_opy_
        thread = Thread(target=self.bstack11111l11lll_opy_)
        thread.start()
      else:
        self.bstack111111lll11_opy_ = True
        self.logger.error(bstack1l1l11l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤ΅").format(bstack1llllll1ll1l_opy_))
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ`").format(e))
  def bstack1111111l1ll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1l11l_opy_ (u"ࠧ࡭ࡱࡪࠫ῰"), bstack1l1l11l_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫ῱"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1l11l_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨῲ").format(logfile))
      self.bstack1llllll1l1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦῳ").format(e))
  @measure(event_name=EVENTS.bstack11l11l1llll_opy_, stage=STAGE.bstack1l1111l11l_opy_)
  def bstack11111l11lll_opy_(self):
    bstack1111111111l_opy_ = self.bstack11111111l11_opy_()
    if bstack1111111111l_opy_ == None:
      self.bstack111111lll11_opy_ = True
      self.logger.error(bstack1l1l11l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢῴ"))
      return False
    bstack11111l111ll_opy_ = [bstack1l1l11l_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨ῵") if self.bstack1ll1ll1111_opy_ else bstack1l1l11l_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪῶ")]
    bstack1111llllll1_opy_ = self.bstack111111l1111_opy_()
    if bstack1111llllll1_opy_ != None:
      bstack11111l111ll_opy_.append(bstack1l1l11l_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨῷ").format(bstack1111llllll1_opy_))
    env = os.environ.copy()
    env[bstack1l1l11l_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨῸ")] = bstack1111111111l_opy_
    env[bstack1l1l11l_opy_ (u"ࠤࡗࡌࡤࡈࡕࡊࡎࡇࡣ࡚࡛ࡉࡅࠤΌ")] = os.environ.get(bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨῺ"), bstack1l1l11l_opy_ (u"ࠫࠬΏ"))
    bstack1llllll11lll_opy_ = [self.binary_path]
    self.bstack1111111l1ll_opy_()
    self.bstack111111l1ll1_opy_ = self.bstack1lllllllll1l_opy_(bstack1llllll11lll_opy_ + bstack11111l111ll_opy_, env)
    self.logger.debug(bstack1l1l11l_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨῼ"))
    bstack11111l11l1l_opy_ = 0
    while self.bstack111111l1ll1_opy_.poll() == None:
      bstack1llllll1l111_opy_ = self.bstack111111ll1ll_opy_()
      if bstack1llllll1l111_opy_:
        self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤ´"))
        self.bstack111111ll111_opy_ = True
        return True
      bstack11111l11l1l_opy_ += 1
      self.logger.debug(bstack1l1l11l_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿࠥ῾").format(bstack11111l11l1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨ῿").format(bstack11111l11l1l_opy_))
    self.bstack111111lll11_opy_ = True
    return False
  def bstack111111ll1ll_opy_(self, bstack11111l11l1l_opy_ = 0):
    if bstack11111l11l1l_opy_ > 10:
      return False
    try:
      bstack1111111l1l1_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩ "), bstack1l1l11l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻ࠫ "))
      bstack11111111ll1_opy_ = bstack1111111l1l1_opy_ + bstack11l11l1l1l1_opy_
      response = requests.get(bstack11111111ll1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪ "), {}).get(bstack1l1l11l_opy_ (u"ࠬ࡯ࡤࠨ "), None)
      return True
    except:
      self.logger.debug(bstack1l1l11l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣ࡬ࡪࡧ࡬ࡵࡪࠣࡧ࡭࡫ࡣ࡬ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ "))
      return False
  def bstack11111111l11_opy_(self):
    bstack1lllllll1l11_opy_ = bstack1l1l11l_opy_ (u"ࠧࡢࡲࡳࠫ ") if self.bstack1ll1ll1111_opy_ else bstack1l1l11l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ ")
    bstack1lllllll11ll_opy_ = bstack1l1l11l_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧ ") if self.config.get(bstack1l1l11l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ ")) is None else True
    bstack11l1ll11111_opy_ = bstack1l1l11l_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠩࡴࡪࡸࡣࡺ࠿ࡾࢁࠧ ").format(self.config[bstack1l1l11l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ ")], bstack1lllllll1l11_opy_, bstack1lllllll11ll_opy_)
    if self.percy_capture_mode:
      bstack11l1ll11111_opy_ += bstack1l1l11l_opy_ (u"ࠨࠦࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࡂࢁࡽࠣ​").format(self.percy_capture_mode)
    uri = bstack1l1ll1l11l_opy_(bstack11l1ll11111_opy_)
    try:
      response = bstack11l1l1l111_opy_(bstack1l1l11l_opy_ (u"ࠧࡈࡇࡗࠫ‌"), uri, {}, {bstack1l1l11l_opy_ (u"ࠨࡣࡸࡸ࡭࠭‍"): (self.config[bstack1l1l11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ‎")], self.config[bstack1l1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭‏")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11111ll1l_opy_ = data.get(bstack1l1l11l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ‐"))
        self.percy_capture_mode = data.get(bstack1l1l11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࠪ‑"))
        os.environ[bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫ‒")] = str(self.bstack11111ll1l_opy_)
        os.environ[bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫ–")] = str(self.percy_capture_mode)
        if bstack1lllllll11ll_opy_ == bstack1l1l11l_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦ—") and str(self.bstack11111ll1l_opy_).lower() == bstack1l1l11l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ―"):
          self.bstack1l111lllll_opy_ = True
        if bstack1l1l11l_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤ‖") in data:
          return data[bstack1l1l11l_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥ‗")]
        else:
          raise bstack1l1l11l_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬ‘").format(data)
      else:
        raise bstack1l1l11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨ’").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣ‚").format(e))
  def bstack111111l1111_opy_(self):
    bstack1llllllll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦ‛"))
    try:
      if bstack1l1l11l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ“") not in self.bstack1lllllll11l1_opy_:
        self.bstack1lllllll11l1_opy_[bstack1l1l11l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ”")] = 2
      with open(bstack1llllllll1ll_opy_, bstack1l1l11l_opy_ (u"ࠫࡼ࠭„")) as fp:
        json.dump(self.bstack1lllllll11l1_opy_, fp)
      return bstack1llllllll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ‟").format(e))
  def bstack1lllllllll1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llllll1ll11_opy_ == bstack1l1l11l_opy_ (u"࠭ࡷࡪࡰࠪ†"):
        bstack11111l1l11l_opy_ = [bstack1l1l11l_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨ‡"), bstack1l1l11l_opy_ (u"ࠨ࠱ࡦࠫ•")]
        cmd = bstack11111l1l11l_opy_ + cmd
      cmd = bstack1l1l11l_opy_ (u"ࠩࠣࠫ‣").join(cmd)
      self.logger.debug(bstack1l1l11l_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢ․").format(cmd))
      with open(self.bstack1llllll1l1ll_opy_, bstack1l1l11l_opy_ (u"ࠦࡦࠨ‥")) as bstack1llllll1l1l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llllll1l1l1_opy_, text=True, stderr=bstack1llllll1l1l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111111lll11_opy_ = True
      self.logger.error(bstack1l1l11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ…").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111111ll111_opy_:
        self.logger.info(bstack1l1l11l_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢ‧"))
        cmd = [self.binary_path, bstack1l1l11l_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥ ")]
        self.bstack1lllllllll1l_opy_(cmd)
        self.bstack111111ll111_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣ ").format(cmd, e))
  def bstack1l11ll11_opy_(self):
    if not self.bstack11111ll1l_opy_:
      return
    try:
      bstack1lllllll1lll_opy_ = 0
      while not self.bstack111111ll111_opy_ and bstack1lllllll1lll_opy_ < self.bstack1lllllllll11_opy_:
        if self.bstack111111lll11_opy_:
          self.logger.info(bstack1l1l11l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢ‪"))
          return
        time.sleep(1)
        bstack1lllllll1lll_opy_ += 1
      os.environ[bstack1l1l11l_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩ‫")] = str(self.bstack11111l1l111_opy_())
      self.logger.info(bstack1l1l11l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧ‬"))
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ‭").format(e))
  def bstack11111l1l111_opy_(self):
    if self.bstack1ll1ll1111_opy_:
      return
    try:
      bstack11111l11ll1_opy_ = [platform[bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ‮")].lower() for platform in self.config.get(bstack1l1l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ "), [])]
      bstack11111l111l1_opy_ = sys.maxsize
      bstack1111111ll11_opy_ = bstack1l1l11l_opy_ (u"ࠨࠩ‰")
      for browser in bstack11111l11ll1_opy_:
        if browser in self.bstack111111lllll_opy_:
          bstack1111111l111_opy_ = self.bstack111111lllll_opy_[browser]
        if bstack1111111l111_opy_ < bstack11111l111l1_opy_:
          bstack11111l111l1_opy_ = bstack1111111l111_opy_
          bstack1111111ll11_opy_ = browser
      return bstack1111111ll11_opy_
    except Exception as e:
      self.logger.error(bstack1l1l11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ‱").format(e))
  @classmethod
  def bstack11lllll1_opy_(self):
    return os.getenv(bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ′"), bstack1l1l11l_opy_ (u"ࠫࡋࡧ࡬ࡴࡧࠪ″")).lower()
  @classmethod
  def bstack111l1111_opy_(self):
    return os.getenv(bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩ‴"), bstack1l1l11l_opy_ (u"࠭ࠧ‵"))
  @classmethod
  def bstack1l1l1111l1l_opy_(cls, value):
    cls.bstack1l111lllll_opy_ = value
  @classmethod
  def bstack1111111ll1l_opy_(cls):
    return cls.bstack1l111lllll_opy_
  @classmethod
  def bstack1l1l111llll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111111l11ll_opy_(cls):
    return cls.percy_build_id
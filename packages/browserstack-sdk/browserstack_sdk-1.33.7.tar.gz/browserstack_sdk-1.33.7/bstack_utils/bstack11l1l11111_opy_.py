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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l11ll1l11_opy_, bstack11l11l11l1l_opy_, bstack11l11llll1l_opy_
import tempfile
import json
bstack1111llll1ll_opy_ = os.getenv(bstack1l1l11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡇࡠࡈࡌࡐࡊࠨẉ"), None) or os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠣẊ"))
bstack1111llll111_opy_ = os.path.join(bstack1l1l11l_opy_ (u"ࠢ࡭ࡱࡪࠦẋ"), bstack1l1l11l_opy_ (u"ࠨࡵࡧ࡯࠲ࡩ࡬ࡪ࠯ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫ࠬẌ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1l11l_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬẍ"),
      datefmt=bstack1l1l11l_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨẎ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll11l1l1l_opy_():
  bstack1111lllll1l_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡈࡊࡈࡕࡈࠤẏ"), bstack1l1l11l_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦẐ"))
  return logging.DEBUG if bstack1111lllll1l_opy_.lower() == bstack1l1l11l_opy_ (u"ࠨࡴࡳࡷࡨࠦẑ") else logging.INFO
def bstack1l1l1l1l1ll_opy_():
  global bstack1111llll1ll_opy_
  if os.path.exists(bstack1111llll1ll_opy_):
    os.remove(bstack1111llll1ll_opy_)
  if os.path.exists(bstack1111llll111_opy_):
    os.remove(bstack1111llll111_opy_)
def bstack1ll11lll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack111l111ll11_opy_ = log_level
  if bstack1l1l11l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩẒ") in config and config[bstack1l1l11l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪẓ")] in bstack11l11l11l1l_opy_:
    bstack111l111ll11_opy_ = bstack11l11l11l1l_opy_[config[bstack1l1l11l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫẔ")]]
  if config.get(bstack1l1l11l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬẕ"), False):
    logging.getLogger().setLevel(bstack111l111ll11_opy_)
    return bstack111l111ll11_opy_
  global bstack1111llll1ll_opy_
  bstack1ll11lll_opy_()
  bstack111l111l11l_opy_ = logging.Formatter(
    fmt=bstack1l1l11l_opy_ (u"ࠫࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧẖ"),
    datefmt=bstack1l1l11l_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࡔࠦࡊ࠽ࠩࡒࡀࠥࡔ࡜ࠪẗ"),
  )
  bstack1111lllll11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111llll1ll_opy_)
  file_handler.setFormatter(bstack111l111l11l_opy_)
  bstack1111lllll11_opy_.setFormatter(bstack111l111l11l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111lllll11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1l11l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨẘ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111lllll11_opy_.setLevel(bstack111l111ll11_opy_)
  logging.getLogger().addHandler(bstack1111lllll11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l111ll11_opy_
def bstack1111lllllll_opy_(config):
  try:
    bstack111l111llll_opy_ = set(bstack11l11llll1l_opy_)
    bstack111l111ll1l_opy_ = bstack1l1l11l_opy_ (u"ࠧࠨẙ")
    with open(bstack1l1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫẚ")) as bstack111l111l1ll_opy_:
      bstack111l1111ll1_opy_ = bstack111l111l1ll_opy_.read()
      bstack111l111ll1l_opy_ = re.sub(bstack1l1l11l_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠧ࠳࠰ࠤ࡝ࡰࠪẛ"), bstack1l1l11l_opy_ (u"ࠪࠫẜ"), bstack111l1111ll1_opy_, flags=re.M)
      bstack111l111ll1l_opy_ = re.sub(
        bstack1l1l11l_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄ࠮ࠧẝ") + bstack1l1l11l_opy_ (u"ࠬࢂࠧẞ").join(bstack111l111llll_opy_) + bstack1l1l11l_opy_ (u"࠭ࠩ࠯ࠬࠧࠫẟ"),
        bstack1l1l11l_opy_ (u"ࡲࠨ࡞࠵࠾ࠥࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩẠ"),
        bstack111l111ll1l_opy_, flags=re.M | re.I
      )
    def bstack111l111l1l1_opy_(dic):
      bstack111l1111l1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l111llll_opy_:
          bstack111l1111l1l_opy_[key] = bstack1l1l11l_opy_ (u"ࠨ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬạ")
        else:
          if isinstance(value, dict):
            bstack111l1111l1l_opy_[key] = bstack111l111l1l1_opy_(value)
          else:
            bstack111l1111l1l_opy_[key] = value
      return bstack111l1111l1l_opy_
    bstack111l1111l1l_opy_ = bstack111l111l1l1_opy_(config)
    return {
      bstack1l1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬẢ"): bstack111l111ll1l_opy_,
      bstack1l1l11l_opy_ (u"ࠪࡪ࡮ࡴࡡ࡭ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ả"): json.dumps(bstack111l1111l1l_opy_)
    }
  except Exception as e:
    return {}
def bstack111l111l111_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1l11l_opy_ (u"ࠫࡱࡵࡧࠨẤ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack1111llllll1_opy_ = os.path.join(log_dir, bstack1l1l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠭ấ"))
  if not os.path.exists(bstack1111llllll1_opy_):
    bstack111l1111l11_opy_ = {
      bstack1l1l11l_opy_ (u"ࠨࡩ࡯࡫ࡳࡥࡹ࡮ࠢẦ"): str(inipath),
      bstack1l1l11l_opy_ (u"ࠢࡳࡱࡲࡸࡵࡧࡴࡩࠤầ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧẨ")), bstack1l1l11l_opy_ (u"ࠩࡺࠫẩ")) as bstack111l1111lll_opy_:
      bstack111l1111lll_opy_.write(json.dumps(bstack111l1111l11_opy_))
def bstack111l11111l1_opy_():
  try:
    bstack1111llllll1_opy_ = os.path.join(os.getcwd(), bstack1l1l11l_opy_ (u"ࠪࡰࡴ࡭ࠧẪ"), bstack1l1l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪẫ"))
    if os.path.exists(bstack1111llllll1_opy_):
      with open(bstack1111llllll1_opy_, bstack1l1l11l_opy_ (u"ࠬࡸࠧẬ")) as bstack111l1111lll_opy_:
        bstack1111llll1l1_opy_ = json.load(bstack111l1111lll_opy_)
      return bstack1111llll1l1_opy_.get(bstack1l1l11l_opy_ (u"࠭ࡩ࡯࡫ࡳࡥࡹ࡮ࠧậ"), bstack1l1l11l_opy_ (u"ࠧࠨẮ")), bstack1111llll1l1_opy_.get(bstack1l1l11l_opy_ (u"ࠨࡴࡲࡳࡹࡶࡡࡵࡪࠪắ"), bstack1l1l11l_opy_ (u"ࠩࠪẰ"))
  except:
    pass
  return None, None
def bstack111l1111111_opy_():
  try:
    bstack1111llllll1_opy_ = os.path.join(os.getcwd(), bstack1l1l11l_opy_ (u"ࠪࡰࡴ࡭ࠧằ"), bstack1l1l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪẲ"))
    if os.path.exists(bstack1111llllll1_opy_):
      os.remove(bstack1111llllll1_opy_)
  except:
    pass
def bstack11ll11ll11_opy_(config):
  try:
    from bstack_utils.helper import bstack1ll1l111l1_opy_, bstack111l11l11_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack1111llll1ll_opy_
    if config.get(bstack1l1l11l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧẳ"), False):
      return
    uuid = os.getenv(bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫẴ")) if os.getenv(bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬẵ")) else bstack1ll1l111l1_opy_.get_property(bstack1l1l11l_opy_ (u"ࠣࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠥẶ"))
    if not uuid or uuid == bstack1l1l11l_opy_ (u"ࠩࡱࡹࡱࡲࠧặ"):
      return
    bstack1111llll11l_opy_ = [bstack1l1l11l_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡱࡪࡴࡴࡴ࠰ࡷࡼࡹ࠭Ẹ"), bstack1l1l11l_opy_ (u"ࠫࡕ࡯ࡰࡧ࡫࡯ࡩࠬẹ"), bstack1l1l11l_opy_ (u"ࠬࡶࡹࡱࡴࡲ࡮ࡪࡩࡴ࠯ࡶࡲࡱࡱ࠭Ẻ"), bstack1111llll1ll_opy_, bstack1111llll111_opy_]
    bstack111l111lll1_opy_, root_path = bstack111l11111l1_opy_()
    if bstack111l111lll1_opy_ != None:
      bstack1111llll11l_opy_.append(bstack111l111lll1_opy_)
    if root_path != None:
      bstack1111llll11l_opy_.append(os.path.join(root_path, bstack1l1l11l_opy_ (u"࠭ࡣࡰࡰࡩࡸࡪࡹࡴ࠯ࡲࡼࠫẻ")))
    bstack1ll11lll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭Ẽ") + uuid + bstack1l1l11l_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩẽ"))
    with tarfile.open(output_file, bstack1l1l11l_opy_ (u"ࠤࡺ࠾࡬ࢀࠢẾ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111llll11l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1111lllllll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l11111ll_opy_ = data.encode()
        tarinfo.size = len(bstack111l11111ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l11111ll_opy_))
    bstack11ll11l111_opy_ = MultipartEncoder(
      fields= {
        bstack1l1l11l_opy_ (u"ࠪࡨࡦࡺࡡࠨế"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1l11l_opy_ (u"ࠫࡷࡨࠧỀ")), bstack1l1l11l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪề")),
        bstack1l1l11l_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨỂ"): uuid
      }
    )
    bstack111l111111l_opy_ = bstack111l11l11_opy_(cli.config, [bstack1l1l11l_opy_ (u"ࠢࡢࡲ࡬ࡷࠧể"), bstack1l1l11l_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣỄ"), bstack1l1l11l_opy_ (u"ࠤࡸࡴࡱࡵࡡࡥࠤễ")], bstack11l11ll1l11_opy_)
    response = requests.post(
      bstack1l1l11l_opy_ (u"ࠥࡿࢂ࠵ࡣ࡭࡫ࡨࡲࡹ࠳࡬ࡰࡩࡶ࠳ࡺࡶ࡬ࡰࡣࡧࠦỆ").format(bstack111l111111l_opy_),
      data=bstack11ll11l111_opy_,
      headers={bstack1l1l11l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪệ"): bstack11ll11l111_opy_.content_type},
      auth=(config[bstack1l1l11l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧỈ")], config[bstack1l1l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩỉ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1l11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭Ị") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1l11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧị") + str(e))
  finally:
    try:
      bstack1l1l1l1l1ll_opy_()
      bstack111l1111111_opy_()
    except:
      pass
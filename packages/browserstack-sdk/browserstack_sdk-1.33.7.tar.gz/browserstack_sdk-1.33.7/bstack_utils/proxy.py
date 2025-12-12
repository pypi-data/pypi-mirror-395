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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111lll1lll_opy_
bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
def bstack1lllll11l1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lllll11l11l_opy_(bstack1lllll11l1l1_opy_, bstack1lllll11llll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lllll11l1l1_opy_):
        with open(bstack1lllll11l1l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lllll11l1ll_opy_(bstack1lllll11l1l1_opy_):
        pac = get_pac(url=bstack1lllll11l1l1_opy_)
    else:
        raise Exception(bstack1l1l11l_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬ⁐").format(bstack1lllll11l1l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1l11l_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢ⁑"), 80))
        bstack1lllll11ll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lllll11ll11_opy_ = bstack1l1l11l_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨ⁒")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lllll11llll_opy_, bstack1lllll11ll11_opy_)
    return proxy_url
def bstack1l1ll1l1l_opy_(config):
    return bstack1l1l11l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ⁓") in config or bstack1l1l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭⁔") in config
def bstack1l1l11l11l_opy_(config):
    if not bstack1l1ll1l1l_opy_(config):
        return
    if config.get(bstack1l1l11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⁕")):
        return config.get(bstack1l1l11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⁖"))
    if config.get(bstack1l1l11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⁗")):
        return config.get(bstack1l1l11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ⁘"))
def bstack11l111ll11_opy_(config, bstack1lllll11llll_opy_):
    proxy = bstack1l1l11l11l_opy_(config)
    proxies = {}
    if config.get(bstack1l1l11l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⁙")) or config.get(bstack1l1l11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⁚")):
        if proxy.endswith(bstack1l1l11l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ⁛")):
            proxies = bstack111ll1ll_opy_(proxy, bstack1lllll11llll_opy_)
        else:
            proxies = {
                bstack1l1l11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ⁜"): proxy
            }
    bstack1ll1l111l1_opy_.bstack11ll11llll_opy_(bstack1l1l11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ⁝"), proxies)
    return proxies
def bstack111ll1ll_opy_(bstack1lllll11l1l1_opy_, bstack1lllll11llll_opy_):
    proxies = {}
    global bstack1lllll11ll1l_opy_
    if bstack1l1l11l_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨ⁞") in globals():
        return bstack1lllll11ll1l_opy_
    try:
        proxy = bstack1lllll11l11l_opy_(bstack1lllll11l1l1_opy_, bstack1lllll11llll_opy_)
        if bstack1l1l11l_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨ ") in proxy:
            proxies = {}
        elif bstack1l1l11l_opy_ (u"ࠢࡉࡖࡗࡔࠧ⁠") in proxy or bstack1l1l11l_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢ⁡") in proxy or bstack1l1l11l_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣ⁢") in proxy:
            bstack1lllll11lll1_opy_ = proxy.split(bstack1l1l11l_opy_ (u"ࠥࠤࠧ⁣"))
            if bstack1l1l11l_opy_ (u"ࠦ࠿࠵࠯ࠣ⁤") in bstack1l1l11l_opy_ (u"ࠧࠨ⁥").join(bstack1lllll11lll1_opy_[1:]):
                proxies = {
                    bstack1l1l11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⁦"): bstack1l1l11l_opy_ (u"ࠢࠣ⁧").join(bstack1lllll11lll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⁨"): str(bstack1lllll11lll1_opy_[0]).lower() + bstack1l1l11l_opy_ (u"ࠤ࠽࠳࠴ࠨ⁩") + bstack1l1l11l_opy_ (u"ࠥࠦ⁪").join(bstack1lllll11lll1_opy_[1:])
                }
        elif bstack1l1l11l_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥ⁫") in proxy:
            bstack1lllll11lll1_opy_ = proxy.split(bstack1l1l11l_opy_ (u"ࠧࠦࠢ⁬"))
            if bstack1l1l11l_opy_ (u"ࠨ࠺࠰࠱ࠥ⁭") in bstack1l1l11l_opy_ (u"ࠢࠣ⁮").join(bstack1lllll11lll1_opy_[1:]):
                proxies = {
                    bstack1l1l11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⁯"): bstack1l1l11l_opy_ (u"ࠤࠥ⁰").join(bstack1lllll11lll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩⁱ"): bstack1l1l11l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ⁲") + bstack1l1l11l_opy_ (u"ࠧࠨ⁳").join(bstack1lllll11lll1_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1l11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⁴"): proxy
            }
    except Exception as e:
        print(bstack1l1l11l_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦ⁵"), bstack1111lll1lll_opy_.format(bstack1lllll11l1l1_opy_, str(e)))
    bstack1lllll11ll1l_opy_ = proxies
    return proxies
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
from uuid import uuid4
from bstack_utils.helper import bstack11l1lllll_opy_, bstack11ll1l1l1l1_opy_
from bstack_utils.bstack11llll1l1_opy_ import bstack11ll11lllll_opy_
class bstack111l1l1l11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack11ll11lll1l_opy_=None, bstack11ll1l111l1_opy_=True, bstack1l111l1l111_opy_=None, bstack1l1l1l11ll_opy_=None, result=None, duration=None, bstack111l1l111l_opy_=None, meta={}):
        self.bstack111l1l111l_opy_ = bstack111l1l111l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11ll1l111l1_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11ll11lll1l_opy_ = bstack11ll11lll1l_opy_
        self.bstack1l111l1l111_opy_ = bstack1l111l1l111_opy_
        self.bstack1l1l1l11ll_opy_ = bstack1l1l1l11ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l11l1ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack111l1ll1ll_opy_(self, meta):
        self.meta = meta
    def bstack111ll1ll1l_opy_(self, hooks):
        self.hooks = hooks
    def bstack11ll1l111ll_opy_(self):
        bstack11ll11ll111_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1l11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᙷ"): bstack11ll11ll111_opy_,
            bstack1l1l11l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᙸ"): bstack11ll11ll111_opy_,
            bstack1l1l11l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᙹ"): bstack11ll11ll111_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1l11l_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣᙺ") + key)
            setattr(self, key, val)
    def bstack11ll11ll11l_opy_(self):
        return {
            bstack1l1l11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᙻ"): self.name,
            bstack1l1l11l_opy_ (u"ࠩࡥࡳࡩࡿࠧᙼ"): {
                bstack1l1l11l_opy_ (u"ࠪࡰࡦࡴࡧࠨᙽ"): bstack1l1l11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᙾ"),
                bstack1l1l11l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᙿ"): self.code
            },
            bstack1l1l11l_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ "): self.scope,
            bstack1l1l11l_opy_ (u"ࠧࡵࡣࡪࡷࠬᚁ"): self.tags,
            bstack1l1l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᚂ"): self.framework,
            bstack1l1l11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᚃ"): self.started_at
        }
    def bstack11ll1l11111_opy_(self):
        return {
         bstack1l1l11l_opy_ (u"ࠪࡱࡪࡺࡡࠨᚄ"): self.meta
        }
    def bstack11ll1l11l11_opy_(self):
        return {
            bstack1l1l11l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᚅ"): {
                bstack1l1l11l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᚆ"): self.bstack11ll11lll1l_opy_
            }
        }
    def bstack11ll11llll1_opy_(self, bstack11ll11lll11_opy_, details):
        step = next(filter(lambda st: st[bstack1l1l11l_opy_ (u"࠭ࡩࡥࠩᚇ")] == bstack11ll11lll11_opy_, self.meta[bstack1l1l11l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᚈ")]), None)
        step.update(details)
    def bstack1ll11ll1ll_opy_(self, bstack11ll11lll11_opy_):
        step = next(filter(lambda st: st[bstack1l1l11l_opy_ (u"ࠨ࡫ࡧࠫᚉ")] == bstack11ll11lll11_opy_, self.meta[bstack1l1l11l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᚊ")]), None)
        step.update({
            bstack1l1l11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᚋ"): bstack11l1lllll_opy_()
        })
    def bstack111ll11l1l_opy_(self, bstack11ll11lll11_opy_, result, duration=None):
        bstack1l111l1l111_opy_ = bstack11l1lllll_opy_()
        if bstack11ll11lll11_opy_ is not None and self.meta.get(bstack1l1l11l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚌ")):
            step = next(filter(lambda st: st[bstack1l1l11l_opy_ (u"ࠬ࡯ࡤࠨᚍ")] == bstack11ll11lll11_opy_, self.meta[bstack1l1l11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᚎ")]), None)
            step.update({
                bstack1l1l11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᚏ"): bstack1l111l1l111_opy_,
                bstack1l1l11l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᚐ"): duration if duration else bstack11ll1l1l1l1_opy_(step[bstack1l1l11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᚑ")], bstack1l111l1l111_opy_),
                bstack1l1l11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᚒ"): result.result,
                bstack1l1l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᚓ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack11ll1l11ll1_opy_):
        if self.meta.get(bstack1l1l11l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᚔ")):
            self.meta[bstack1l1l11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᚕ")].append(bstack11ll1l11ll1_opy_)
        else:
            self.meta[bstack1l1l11l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᚖ")] = [ bstack11ll1l11ll1_opy_ ]
    def bstack11ll1l11lll_opy_(self):
        return {
            bstack1l1l11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᚗ"): self.bstack111l11l1ll_opy_(),
            bstack1l1l11l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᚘ"): bstack1l1l11l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᚙ"),
            **self.bstack11ll11ll11l_opy_(),
            **self.bstack11ll1l111ll_opy_(),
            **self.bstack11ll1l11111_opy_()
        }
    def bstack11ll1l1l11l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1l11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᚚ"): self.bstack1l111l1l111_opy_,
            bstack1l1l11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭᚛"): self.duration,
            bstack1l1l11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᚜"): self.result.result
        }
        if data[bstack1l1l11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᚝")] == bstack1l1l11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᚞"):
            data[bstack1l1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ᚟")] = self.result.bstack1llllll1ll1_opy_()
            data[bstack1l1l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᚠ")] = [{bstack1l1l11l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᚡ"): self.result.bstack11ll1l1l111_opy_()}]
        return data
    def bstack11ll1l1l1ll_opy_(self):
        return {
            bstack1l1l11l_opy_ (u"ࠬࡻࡵࡪࡦࠪᚢ"): self.bstack111l11l1ll_opy_(),
            **self.bstack11ll11ll11l_opy_(),
            **self.bstack11ll1l111ll_opy_(),
            **self.bstack11ll1l1l11l_opy_(),
            **self.bstack11ll1l11111_opy_()
        }
    def bstack111l11l11l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1l11l_opy_ (u"࠭ࡓࡵࡣࡵࡸࡪࡪࠧᚣ") in event:
            return self.bstack11ll1l11lll_opy_()
        elif bstack1l1l11l_opy_ (u"ࠧࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᚤ") in event:
            return self.bstack11ll1l1l1ll_opy_()
    def bstack111l1l1lll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111l1l111_opy_ = time if time else bstack11l1lllll_opy_()
        self.duration = duration if duration else bstack11ll1l1l1l1_opy_(self.started_at, self.bstack1l111l1l111_opy_)
        if result:
            self.result = result
class bstack111ll111l1_opy_(bstack111l1l1l11_opy_):
    def __init__(self, hooks=[], bstack111l1ll111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack111l1ll111_opy_ = bstack111l1ll111_opy_
        super().__init__(*args, **kwargs, bstack1l1l1l11ll_opy_=bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᚥ"))
    @classmethod
    def bstack11ll11ll1l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1l11l_opy_ (u"ࠩ࡬ࡨࠬᚦ"): id(step),
                bstack1l1l11l_opy_ (u"ࠪࡸࡪࡾࡴࠨᚧ"): step.name,
                bstack1l1l11l_opy_ (u"ࠫࡰ࡫ࡹࡸࡱࡵࡨࠬᚨ"): step.keyword,
            })
        return bstack111ll111l1_opy_(
            **kwargs,
            meta={
                bstack1l1l11l_opy_ (u"ࠬ࡬ࡥࡢࡶࡸࡶࡪ࠭ᚩ"): {
                    bstack1l1l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᚪ"): feature.name,
                    bstack1l1l11l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬᚫ"): feature.filename,
                    bstack1l1l11l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᚬ"): feature.description
                },
                bstack1l1l11l_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫᚭ"): {
                    bstack1l1l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨᚮ"): scenario.name
                },
                bstack1l1l11l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᚯ"): steps,
                bstack1l1l11l_opy_ (u"ࠬ࡫ࡸࡢ࡯ࡳࡰࡪࡹࠧᚰ"): bstack11ll11lllll_opy_(test)
            }
        )
    def bstack11ll1l1111l_opy_(self):
        return {
            bstack1l1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᚱ"): self.hooks
        }
    def bstack11ll11ll1ll_opy_(self):
        if self.bstack111l1ll111_opy_:
            return {
                bstack1l1l11l_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᚲ"): self.bstack111l1ll111_opy_
            }
        return {}
    def bstack11ll1l1l1ll_opy_(self):
        return {
            **super().bstack11ll1l1l1ll_opy_(),
            **self.bstack11ll1l1111l_opy_()
        }
    def bstack11ll1l11lll_opy_(self):
        return {
            **super().bstack11ll1l11lll_opy_(),
            **self.bstack11ll11ll1ll_opy_()
        }
    def bstack111l1l1lll_opy_(self):
        return bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᚳ")
class bstack111ll111ll_opy_(bstack111l1l1l11_opy_):
    def __init__(self, hook_type, *args,bstack111l1ll111_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll11l1111l_opy_ = None
        self.bstack111l1ll111_opy_ = bstack111l1ll111_opy_
        super().__init__(*args, **kwargs, bstack1l1l1l11ll_opy_=bstack1l1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᚴ"))
    def bstack1111ll11l1_opy_(self):
        return self.hook_type
    def bstack11ll1l11l1l_opy_(self):
        return {
            bstack1l1l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᚵ"): self.hook_type
        }
    def bstack11ll1l1l1ll_opy_(self):
        return {
            **super().bstack11ll1l1l1ll_opy_(),
            **self.bstack11ll1l11l1l_opy_()
        }
    def bstack11ll1l11lll_opy_(self):
        return {
            **super().bstack11ll1l11lll_opy_(),
            bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᚶ"): self.bstack1ll11l1111l_opy_,
            **self.bstack11ll1l11l1l_opy_()
        }
    def bstack111l1l1lll_opy_(self):
        return bstack1l1l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᚷ")
    def bstack111ll1l11l_opy_(self, bstack1ll11l1111l_opy_):
        self.bstack1ll11l1111l_opy_ = bstack1ll11l1111l_opy_
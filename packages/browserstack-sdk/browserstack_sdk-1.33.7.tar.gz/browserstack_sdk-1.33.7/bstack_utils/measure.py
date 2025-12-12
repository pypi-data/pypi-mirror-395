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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11l1l11111_opy_ import get_logger
from bstack_utils.bstack1llll11111_opy_ import bstack1lll1ll111l_opy_
bstack1llll11111_opy_ = bstack1lll1ll111l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1111l1l11_opy_: Optional[str] = None):
    bstack1l1l11l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡇࡩࡨࡵࡲࡢࡶࡲࡶࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡺࡨࡦࠢࡶࡸࡦࡸࡴࠡࡶ࡬ࡱࡪࠦ࡯ࡧࠢࡤࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࡡ࡭ࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࠢࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡸࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦỌ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll11l1lll1_opy_: str = bstack1llll11111_opy_.bstack11l1lll11ll_opy_(label)
            start_mark: str = label + bstack1l1l11l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥọ")
            end_mark: str = label + bstack1l1l11l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤỎ")
            result = None
            try:
                if stage.value == STAGE.bstack1ll1ll111l_opy_.value:
                    bstack1llll11111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1llll11111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1111l1l11_opy_)
                elif stage.value == STAGE.bstack1l1111l11l_opy_.value:
                    start_mark: str = bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧỏ")
                    end_mark: str = bstack1ll11l1lll1_opy_ + bstack1l1l11l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦỐ")
                    bstack1llll11111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1llll11111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1111l1l11_opy_)
            except Exception as e:
                bstack1llll11111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1111l1l11_opy_)
            return result
        return wrapper
    return decorator
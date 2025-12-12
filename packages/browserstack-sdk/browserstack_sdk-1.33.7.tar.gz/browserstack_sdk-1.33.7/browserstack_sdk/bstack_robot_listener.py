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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l111111_opy_ import RobotHandler
from bstack_utils.capture import bstack111ll11111_opy_
from bstack_utils.bstack111l1llll1_opy_ import bstack111l1l1l11_opy_, bstack111ll111ll_opy_, bstack111ll111l1_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11l11l1l1l_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack1l1111ll1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack111111l11_opy_, bstack11l1lllll_opy_, Result, \
    error_handler, bstack1111ll11ll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    _lock = threading.Lock()
    store = {
        bstack1l1l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩྍ"): [],
        bstack1l1l11l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬྎ"): [],
        bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫྏ"): []
    }
    bstack1111ll1lll_opy_ = []
    bstack1111lll111_opy_ = []
    @staticmethod
    def bstack111ll1l111_opy_(log):
        if not ((isinstance(log[bstack1l1l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྐ")], list) or (isinstance(log[bstack1l1l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྑ")], dict)) and len(log[bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྒ")])>0) or (isinstance(log[bstack1l1l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྒྷ")], str) and log[bstack1l1l11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ྔ")].strip())):
            return
        active = bstack11l11l1l1l_opy_.bstack111l1lllll_opy_()
        log = {
            bstack1l1l11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬྕ"): log[bstack1l1l11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ྖ")],
            bstack1l1l11l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫྗ"): bstack1111ll11ll_opy_().isoformat() + bstack1l1l11l_opy_ (u"ࠩ࡝ࠫ྘"),
            bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྙ"): log[bstack1l1l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྚ")],
        }
        if active:
            if active[bstack1l1l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪྛ")] == bstack1l1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫྜ"):
                log[bstack1l1l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧྜྷ")] = active[bstack1l1l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨྞ")]
            elif active[bstack1l1l11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧྟ")] == bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࠨྠ"):
                log[bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫྡ")] = active[bstack1l1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬྡྷ")]
        bstack1l1111ll1l_opy_.bstack11ll11ll11_opy_([log])
    def __init__(self):
        self.messages = bstack111l1l11l1_opy_()
        self._111l11l1l1_opy_ = None
        self._111l1111ll_opy_ = None
        self._111l1111l1_opy_ = OrderedDict()
        self.bstack111l1ll1l1_opy_ = bstack111ll11111_opy_(self.bstack111ll1l111_opy_)
    @error_handler(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1111ll1l11_opy_()
        if not self._111l1111l1_opy_.get(attrs.get(bstack1l1l11l_opy_ (u"࠭ࡩࡥࠩྣ")), None):
            self._111l1111l1_opy_[attrs.get(bstack1l1l11l_opy_ (u"ࠧࡪࡦࠪྤ"))] = {}
        bstack111l11ll1l_opy_ = bstack111ll111l1_opy_(
                bstack111l1l111l_opy_=attrs.get(bstack1l1l11l_opy_ (u"ࠨ࡫ࡧࠫྥ")),
                name=name,
                started_at=bstack11l1lllll_opy_(),
                file_path=os.path.relpath(attrs[bstack1l1l11l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩྦ")], start=os.getcwd()) if attrs.get(bstack1l1l11l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪྦྷ")) != bstack1l1l11l_opy_ (u"ࠫࠬྨ") else bstack1l1l11l_opy_ (u"ࠬ࠭ྩ"),
                framework=bstack1l1l11l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬྪ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l1l11l_opy_ (u"ࠧࡪࡦࠪྫ"), None)
        self._111l1111l1_opy_[attrs.get(bstack1l1l11l_opy_ (u"ࠨ࡫ࡧࠫྫྷ"))][bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྭ")] = bstack111l11ll1l_opy_
    @error_handler(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1111l1llll_opy_()
        self._1111l1lll1_opy_(messages)
        with self._lock:
            for bstack111l111ll1_opy_ in self.bstack1111ll1lll_opy_:
                bstack111l111ll1_opy_[bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬྮ")][bstack1l1l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪྯ")].extend(self.store[bstack1l1l11l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫྰ")])
                bstack1l1111ll1l_opy_.bstack1ll1l111ll_opy_(bstack111l111ll1_opy_)
            self.bstack1111ll1lll_opy_ = []
            self.store[bstack1l1l11l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬྱ")] = []
    @error_handler(class_method=True)
    def start_test(self, name, attrs):
        self.bstack111l1ll1l1_opy_.start()
        if not self._111l1111l1_opy_.get(attrs.get(bstack1l1l11l_opy_ (u"ࠧࡪࡦࠪྲ")), None):
            self._111l1111l1_opy_[attrs.get(bstack1l1l11l_opy_ (u"ࠨ࡫ࡧࠫླ"))] = {}
        driver = bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨྴ"), None)
        bstack111l1llll1_opy_ = bstack111ll111l1_opy_(
            bstack111l1l111l_opy_=attrs.get(bstack1l1l11l_opy_ (u"ࠪ࡭ࡩ࠭ྵ")),
            name=name,
            started_at=bstack11l1lllll_opy_(),
            file_path=os.path.relpath(attrs[bstack1l1l11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫྶ")], start=os.getcwd()),
            scope=RobotHandler.bstack1111l1l11l_opy_(attrs.get(bstack1l1l11l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬྷ"), None)),
            framework=bstack1l1l11l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬྸ"),
            tags=attrs[bstack1l1l11l_opy_ (u"ࠧࡵࡣࡪࡷࠬྐྵ")],
            hooks=self.store[bstack1l1l11l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧྺ")],
            bstack111l1ll111_opy_=bstack1l1111ll1l_opy_.bstack111lll1111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l1l11l_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦྻ").format(bstack1l1l11l_opy_ (u"ࠥࠤࠧྼ").join(attrs[bstack1l1l11l_opy_ (u"ࠫࡹࡧࡧࡴࠩ྽")]), name) if attrs[bstack1l1l11l_opy_ (u"ࠬࡺࡡࡨࡵࠪ྾")] else name
        )
        self._111l1111l1_opy_[attrs.get(bstack1l1l11l_opy_ (u"࠭ࡩࡥࠩ྿"))][bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿀")] = bstack111l1llll1_opy_
        threading.current_thread().current_test_uuid = bstack111l1llll1_opy_.bstack111l11l1ll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l1l11l_opy_ (u"ࠨ࡫ࡧࠫ࿁"), None)
        self.bstack111ll11lll_opy_(bstack1l1l11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ࿂"), bstack111l1llll1_opy_)
    @error_handler(class_method=True)
    def end_test(self, name, attrs):
        self.bstack111l1ll1l1_opy_.reset()
        bstack1111ll1ll1_opy_ = bstack1111lll11l_opy_.get(attrs.get(bstack1l1l11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ࿃")), bstack1l1l11l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ࿄"))
        self._111l1111l1_opy_[attrs.get(bstack1l1l11l_opy_ (u"ࠬ࡯ࡤࠨ࿅"))][bstack1l1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢ࿆ࠩ")].stop(time=bstack11l1lllll_opy_(), duration=int(attrs.get(bstack1l1l11l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬ࿇"), bstack1l1l11l_opy_ (u"ࠨ࠲ࠪ࿈"))), result=Result(result=bstack1111ll1ll1_opy_, exception=attrs.get(bstack1l1l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿉")), bstack111l1lll11_opy_=[attrs.get(bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿊"))]))
        self.bstack111ll11lll_opy_(bstack1l1l11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭࿋"), self._111l1111l1_opy_[attrs.get(bstack1l1l11l_opy_ (u"ࠬ࡯ࡤࠨ࿌"))][bstack1l1l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ࿍")], True)
        with self._lock:
            self.store[bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ࿎")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @error_handler(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1111ll1l11_opy_()
        current_test_id = bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪ࿏"), None)
        bstack1111ll1111_opy_ = current_test_id if bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ࿐"), None) else bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭࿑"), None)
        if attrs.get(bstack1l1l11l_opy_ (u"ࠫࡹࡿࡰࡦࠩ࿒"), bstack1l1l11l_opy_ (u"ࠬ࠭࿓")).lower() in [bstack1l1l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ࿔"), bstack1l1l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ࿕")]:
            hook_type = bstack111l11ll11_opy_(attrs.get(bstack1l1l11l_opy_ (u"ࠨࡶࡼࡴࡪ࠭࿖")), bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭࿗"), None))
            hook_name = bstack1l1l11l_opy_ (u"ࠪࡿࢂ࠭࿘").format(attrs.get(bstack1l1l11l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ࿙"), bstack1l1l11l_opy_ (u"ࠬ࠭࿚")))
            if hook_type in [bstack1l1l11l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ࿛"), bstack1l1l11l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ࿜")]:
                hook_name = bstack1l1l11l_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩ࿝").format(bstack111l1l1111_opy_.get(hook_type), attrs.get(bstack1l1l11l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ࿞"), bstack1l1l11l_opy_ (u"ࠪࠫ࿟")))
            bstack111l111l1l_opy_ = bstack111ll111ll_opy_(
                bstack111l1l111l_opy_=bstack1111ll1111_opy_ + bstack1l1l11l_opy_ (u"ࠫ࠲࠭࿠") + attrs.get(bstack1l1l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿡"), bstack1l1l11l_opy_ (u"࠭ࠧ࿢")).lower(),
                name=hook_name,
                started_at=bstack11l1lllll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l1l11l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ࿣")), start=os.getcwd()),
                framework=bstack1l1l11l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ࿤"),
                tags=attrs[bstack1l1l11l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ࿥")],
                scope=RobotHandler.bstack1111l1l11l_opy_(attrs.get(bstack1l1l11l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ࿦"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l111l1l_opy_.bstack111l11l1ll_opy_()
            threading.current_thread().current_hook_id = bstack1111ll1111_opy_ + bstack1l1l11l_opy_ (u"ࠫ࠲࠭࿧") + attrs.get(bstack1l1l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿨"), bstack1l1l11l_opy_ (u"࠭ࠧ࿩")).lower()
            with self._lock:
                self.store[bstack1l1l11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ࿪")] = [bstack111l111l1l_opy_.bstack111l11l1ll_opy_()]
                if bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ࿫"), None):
                    self.store[bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭࿬")].append(bstack111l111l1l_opy_.bstack111l11l1ll_opy_())
                else:
                    self.store[bstack1l1l11l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩ࿭")].append(bstack111l111l1l_opy_.bstack111l11l1ll_opy_())
            if bstack1111ll1111_opy_:
                self._111l1111l1_opy_[bstack1111ll1111_opy_ + bstack1l1l11l_opy_ (u"ࠫ࠲࠭࿮") + attrs.get(bstack1l1l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪ࿯"), bstack1l1l11l_opy_ (u"࠭ࠧ࿰")).lower()] = { bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿱"): bstack111l111l1l_opy_ }
            bstack1l1111ll1l_opy_.bstack111ll11lll_opy_(bstack1l1l11l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ࿲"), bstack111l111l1l_opy_)
        else:
            bstack111ll11l11_opy_ = {
                bstack1l1l11l_opy_ (u"ࠩ࡬ࡨࠬ࿳"): uuid4().__str__(),
                bstack1l1l11l_opy_ (u"ࠪࡸࡪࡾࡴࠨ࿴"): bstack1l1l11l_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪ࿵").format(attrs.get(bstack1l1l11l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ࿶")), attrs.get(bstack1l1l11l_opy_ (u"࠭ࡡࡳࡩࡶࠫ࿷"), bstack1l1l11l_opy_ (u"ࠧࠨ࿸"))) if attrs.get(bstack1l1l11l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭࿹"), []) else attrs.get(bstack1l1l11l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩ࿺")),
                bstack1l1l11l_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶࠪ࿻"): attrs.get(bstack1l1l11l_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿼"), []),
                bstack1l1l11l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ࿽"): bstack11l1lllll_opy_(),
                bstack1l1l11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭࿾"): bstack1l1l11l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ࿿"),
                bstack1l1l11l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭က"): attrs.get(bstack1l1l11l_opy_ (u"ࠩࡧࡳࡨ࠭ခ"), bstack1l1l11l_opy_ (u"ࠪࠫဂ"))
            }
            if attrs.get(bstack1l1l11l_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬဃ"), bstack1l1l11l_opy_ (u"ࠬ࠭င")) != bstack1l1l11l_opy_ (u"࠭ࠧစ"):
                bstack111ll11l11_opy_[bstack1l1l11l_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨဆ")] = attrs.get(bstack1l1l11l_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩဇ"))
            if not self.bstack1111lll111_opy_:
                self._111l1111l1_opy_[self._111l1l1ll1_opy_()][bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬဈ")].add_step(bstack111ll11l11_opy_)
                threading.current_thread().current_step_uuid = bstack111ll11l11_opy_[bstack1l1l11l_opy_ (u"ࠪ࡭ࡩ࠭ဉ")]
            self.bstack1111lll111_opy_.append(bstack111ll11l11_opy_)
    @error_handler(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1111l1llll_opy_()
        self._1111l1lll1_opy_(messages)
        current_test_id = bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ည"), None)
        bstack1111ll1111_opy_ = current_test_id if current_test_id else bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨဋ"), None)
        bstack111l1l1l1l_opy_ = bstack1111lll11l_opy_.get(attrs.get(bstack1l1l11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ဌ")), bstack1l1l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨဍ"))
        bstack1111lll1ll_opy_ = attrs.get(bstack1l1l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩဎ"))
        if bstack111l1l1l1l_opy_ != bstack1l1l11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪဏ") and not attrs.get(bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫတ")) and self._111l11l1l1_opy_:
            bstack1111lll1ll_opy_ = self._111l11l1l1_opy_
        bstack111ll1111l_opy_ = Result(result=bstack111l1l1l1l_opy_, exception=bstack1111lll1ll_opy_, bstack111l1lll11_opy_=[bstack1111lll1ll_opy_])
        if attrs.get(bstack1l1l11l_opy_ (u"ࠫࡹࡿࡰࡦࠩထ"), bstack1l1l11l_opy_ (u"ࠬ࠭ဒ")).lower() in [bstack1l1l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬဓ"), bstack1l1l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩန")]:
            bstack1111ll1111_opy_ = current_test_id if current_test_id else bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫပ"), None)
            if bstack1111ll1111_opy_:
                bstack111ll1llll_opy_ = bstack1111ll1111_opy_ + bstack1l1l11l_opy_ (u"ࠤ࠰ࠦဖ") + attrs.get(bstack1l1l11l_opy_ (u"ࠪࡸࡾࡶࡥࠨဗ"), bstack1l1l11l_opy_ (u"ࠫࠬဘ")).lower()
                self._111l1111l1_opy_[bstack111ll1llll_opy_][bstack1l1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨမ")].stop(time=bstack11l1lllll_opy_(), duration=int(attrs.get(bstack1l1l11l_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫယ"), bstack1l1l11l_opy_ (u"ࠧ࠱ࠩရ"))), result=bstack111ll1111l_opy_)
                bstack1l1111ll1l_opy_.bstack111ll11lll_opy_(bstack1l1l11l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪလ"), self._111l1111l1_opy_[bstack111ll1llll_opy_][bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬဝ")])
        else:
            bstack1111ll1111_opy_ = current_test_id if current_test_id else bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬသ"), None)
            if bstack1111ll1111_opy_ and len(self.bstack1111lll111_opy_) == 1:
                current_step_uuid = bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨဟ"), None)
                self._111l1111l1_opy_[bstack1111ll1111_opy_][bstack1l1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨဠ")].bstack111ll11l1l_opy_(current_step_uuid, duration=int(attrs.get(bstack1l1l11l_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫအ"), bstack1l1l11l_opy_ (u"ࠧ࠱ࠩဢ"))), result=bstack111ll1111l_opy_)
            else:
                self.bstack111l1l11ll_opy_(attrs)
            self.bstack1111lll111_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l1l11l_opy_ (u"ࠨࡪࡷࡱࡱ࠭ဣ"), bstack1l1l11l_opy_ (u"ࠩࡱࡳࠬဤ")) == bstack1l1l11l_opy_ (u"ࠪࡽࡪࡹࠧဥ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l11l1l1l_opy_.bstack111l1lllll_opy_():
                logs.append({
                    bstack1l1l11l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧဦ"): bstack11l1lllll_opy_(),
                    bstack1l1l11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ဧ"): message.get(bstack1l1l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧဨ")),
                    bstack1l1l11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ဩ"): message.get(bstack1l1l11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧဪ")),
                    **bstack11l11l1l1l_opy_.bstack111l1lllll_opy_()
                })
                if len(logs) > 0:
                    bstack1l1111ll1l_opy_.bstack11ll11ll11_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1l1111ll1l_opy_.bstack1111lll1l1_opy_()
    def bstack111l1l11ll_opy_(self, bstack1111l1ll11_opy_):
        if not bstack11l11l1l1l_opy_.bstack111l1lllll_opy_():
            return
        kwname = bstack1l1l11l_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨါ").format(bstack1111l1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪာ")), bstack1111l1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡦࡸࡧࡴࠩိ"), bstack1l1l11l_opy_ (u"ࠬ࠭ီ"))) if bstack1111l1ll11_opy_.get(bstack1l1l11l_opy_ (u"࠭ࡡࡳࡩࡶࠫု"), []) else bstack1111l1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧူ"))
        error_message = bstack1l1l11l_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢေ").format(kwname, bstack1111l1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩဲ")), str(bstack1111l1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫဳ"))))
        bstack1111ll1l1l_opy_ = bstack1l1l11l_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥဴ").format(kwname, bstack1111l1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬဵ")))
        bstack1111l1l1ll_opy_ = error_message if bstack1111l1ll11_opy_.get(bstack1l1l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧံ")) else bstack1111ll1l1l_opy_
        bstack1111lllll1_opy_ = {
            bstack1l1l11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲ့ࠪ"): self.bstack1111lll111_opy_[-1].get(bstack1l1l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬး"), bstack11l1lllll_opy_()),
            bstack1l1l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧ္ࠪ"): bstack1111l1l1ll_opy_,
            bstack1l1l11l_opy_ (u"ࠪࡰࡪࡼࡥ࡭်ࠩ"): bstack1l1l11l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪျ") if bstack1111l1ll11_opy_.get(bstack1l1l11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬြ")) == bstack1l1l11l_opy_ (u"࠭ࡆࡂࡋࡏࠫွ") else bstack1l1l11l_opy_ (u"ࠧࡊࡐࡉࡓࠬှ"),
            **bstack11l11l1l1l_opy_.bstack111l1lllll_opy_()
        }
        bstack1l1111ll1l_opy_.bstack11ll11ll11_opy_([bstack1111lllll1_opy_])
    def _111l1l1ll1_opy_(self):
        for bstack111l1l111l_opy_ in reversed(self._111l1111l1_opy_):
            bstack1111l1ll1l_opy_ = bstack111l1l111l_opy_
            data = self._111l1111l1_opy_[bstack111l1l111l_opy_][bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫဿ")]
            if isinstance(data, bstack111ll111ll_opy_):
                if not bstack1l1l11l_opy_ (u"ࠩࡈࡅࡈࡎࠧ၀") in data.bstack1111ll11l1_opy_():
                    return bstack1111l1ll1l_opy_
            else:
                return bstack1111l1ll1l_opy_
    def _1111l1lll1_opy_(self, messages):
        try:
            bstack111l11lll1_opy_ = BuiltIn().get_variable_value(bstack1l1l11l_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤ၁")) in (bstack1111llll11_opy_.DEBUG, bstack1111llll11_opy_.TRACE)
            for message, bstack111l111lll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l1l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ၂"))
                level = message.get(bstack1l1l11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ၃"))
                if level == bstack1111llll11_opy_.FAIL:
                    self._111l11l1l1_opy_ = name or self._111l11l1l1_opy_
                    self._111l1111ll_opy_ = bstack111l111lll_opy_.get(bstack1l1l11l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ၄")) if bstack111l11lll1_opy_ and bstack111l111lll_opy_ else self._111l1111ll_opy_
        except:
            pass
    @classmethod
    def bstack111ll11lll_opy_(self, event: str, bstack111l11111l_opy_: bstack111l1l1l11_opy_, bstack1111llll1l_opy_=False):
        if event == bstack1l1l11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ၅"):
            bstack111l11111l_opy_.set(hooks=self.store[bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ၆")])
        if event == bstack1l1l11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ၇"):
            event = bstack1l1l11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ၈")
        if bstack1111llll1l_opy_:
            bstack111l11llll_opy_ = {
                bstack1l1l11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ၉"): event,
                bstack111l11111l_opy_.bstack111l1l1lll_opy_(): bstack111l11111l_opy_.bstack111l11l11l_opy_(event)
            }
            with self._lock:
                self.bstack1111ll1lll_opy_.append(bstack111l11llll_opy_)
        else:
            bstack1l1111ll1l_opy_.bstack111ll11lll_opy_(event, bstack111l11111l_opy_)
class bstack111l1l11l1_opy_:
    def __init__(self):
        self._1111l1l1l1_opy_ = []
    def bstack1111ll1l11_opy_(self):
        self._1111l1l1l1_opy_.append([])
    def bstack1111l1llll_opy_(self):
        return self._1111l1l1l1_opy_.pop() if self._1111l1l1l1_opy_ else list()
    def push(self, message):
        self._1111l1l1l1_opy_[-1].append(message) if self._1111l1l1l1_opy_ else self._1111l1l1l1_opy_.append([message])
class bstack1111llll11_opy_:
    FAIL = bstack1l1l11l_opy_ (u"ࠬࡌࡁࡊࡎࠪ၊")
    ERROR = bstack1l1l11l_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ။")
    WARNING = bstack1l1l11l_opy_ (u"ࠧࡘࡃࡕࡒࠬ၌")
    bstack1111ll111l_opy_ = bstack1l1l11l_opy_ (u"ࠨࡋࡑࡊࡔ࠭၍")
    DEBUG = bstack1l1l11l_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨ၎")
    TRACE = bstack1l1l11l_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩ၏")
    bstack111l11l111_opy_ = [FAIL, ERROR]
def bstack1111llllll_opy_(bstack111l111l11_opy_):
    if not bstack111l111l11_opy_:
        return None
    if bstack111l111l11_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧၐ"), None):
        return getattr(bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨၑ")], bstack1l1l11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫၒ"), None)
    return bstack111l111l11_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬၓ"), None)
def bstack111l11ll11_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l1l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧၔ"), bstack1l1l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫၕ")]:
        return
    if hook_type.lower() == bstack1l1l11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩၖ"):
        if current_test_uuid is None:
            return bstack1l1l11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨၗ")
        else:
            return bstack1l1l11l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪၘ")
    elif hook_type.lower() == bstack1l1l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨၙ"):
        if current_test_uuid is None:
            return bstack1l1l11l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪၚ")
        else:
            return bstack1l1l11l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬၛ")
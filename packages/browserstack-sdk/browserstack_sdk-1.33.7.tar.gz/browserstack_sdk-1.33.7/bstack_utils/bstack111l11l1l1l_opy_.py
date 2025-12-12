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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1111lll1_opy_
from browserstack_sdk.bstack1ll1l11l1_opy_ import bstack11ll111111_opy_
def _111l11ll11l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l11l111l_opy_:
    def __init__(self, handler):
        self._111l11lll11_opy_ = {}
        self._111l11l1ll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11ll111111_opy_.version()
        if bstack11l1111lll1_opy_(pytest_version, bstack1l1l11l_opy_ (u"ࠦ࠽࠴࠱࠯࠳ࠥṞ")) >= 0:
            self._111l11lll11_opy_[bstack1l1l11l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨṟ")] = Module._register_setup_function_fixture
            self._111l11lll11_opy_[bstack1l1l11l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧṠ")] = Module._register_setup_module_fixture
            self._111l11lll11_opy_[bstack1l1l11l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧṡ")] = Class._register_setup_class_fixture
            self._111l11lll11_opy_[bstack1l1l11l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṢ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111l11l1l11_opy_(bstack1l1l11l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬṣ"))
            Module._register_setup_module_fixture = self.bstack111l11l1l11_opy_(bstack1l1l11l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫṤ"))
            Class._register_setup_class_fixture = self.bstack111l11l1l11_opy_(bstack1l1l11l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫṥ"))
            Class._register_setup_method_fixture = self.bstack111l11l1l11_opy_(bstack1l1l11l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ṧ"))
        else:
            self._111l11lll11_opy_[bstack1l1l11l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩṧ")] = Module._inject_setup_function_fixture
            self._111l11lll11_opy_[bstack1l1l11l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨṨ")] = Module._inject_setup_module_fixture
            self._111l11lll11_opy_[bstack1l1l11l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨṩ")] = Class._inject_setup_class_fixture
            self._111l11lll11_opy_[bstack1l1l11l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪṪ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111l11l1l11_opy_(bstack1l1l11l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ṫ"))
            Module._inject_setup_module_fixture = self.bstack111l11l1l11_opy_(bstack1l1l11l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬṬ"))
            Class._inject_setup_class_fixture = self.bstack111l11l1l11_opy_(bstack1l1l11l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬṭ"))
            Class._inject_setup_method_fixture = self.bstack111l11l1l11_opy_(bstack1l1l11l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧṮ"))
    def bstack111l11ll1ll_opy_(self, bstack111l11l1lll_opy_, hook_type):
        bstack111l11lll1l_opy_ = id(bstack111l11l1lll_opy_.__class__)
        if (bstack111l11lll1l_opy_, hook_type) in self._111l11l1ll1_opy_:
            return
        meth = getattr(bstack111l11l1lll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l11l1ll1_opy_[(bstack111l11lll1l_opy_, hook_type)] = meth
            setattr(bstack111l11l1lll_opy_, hook_type, self.bstack111l11ll111_opy_(hook_type, bstack111l11lll1l_opy_))
    def bstack111l11ll1l1_opy_(self, instance, bstack111l11l1111_opy_):
        if bstack111l11l1111_opy_ == bstack1l1l11l_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥṯ"):
            self.bstack111l11ll1ll_opy_(instance.obj, bstack1l1l11l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤṰ"))
            self.bstack111l11ll1ll_opy_(instance.obj, bstack1l1l11l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨṱ"))
        if bstack111l11l1111_opy_ == bstack1l1l11l_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦṲ"):
            self.bstack111l11ll1ll_opy_(instance.obj, bstack1l1l11l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥṳ"))
            self.bstack111l11ll1ll_opy_(instance.obj, bstack1l1l11l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢṴ"))
        if bstack111l11l1111_opy_ == bstack1l1l11l_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨṵ"):
            self.bstack111l11ll1ll_opy_(instance.obj, bstack1l1l11l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧṶ"))
            self.bstack111l11ll1ll_opy_(instance.obj, bstack1l1l11l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤṷ"))
        if bstack111l11l1111_opy_ == bstack1l1l11l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥṸ"):
            self.bstack111l11ll1ll_opy_(instance.obj, bstack1l1l11l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤṹ"))
            self.bstack111l11ll1ll_opy_(instance.obj, bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨṺ"))
    @staticmethod
    def bstack111l11lllll_opy_(hook_type, func, args):
        if hook_type in [bstack1l1l11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫṻ"), bstack1l1l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨṼ")]:
            _111l11ll11l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l11ll111_opy_(self, hook_type, bstack111l11lll1l_opy_):
        def bstack111l11l11l1_opy_(arg=None):
            self.handler(hook_type, bstack1l1l11l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧṽ"))
            result = None
            try:
                bstack1llll1lll1l_opy_ = self._111l11l1ll1_opy_[(bstack111l11lll1l_opy_, hook_type)]
                self.bstack111l11lllll_opy_(hook_type, bstack1llll1lll1l_opy_, (arg,))
                result = Result(result=bstack1l1l11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨṾ"))
            except Exception as e:
                result = Result(result=bstack1l1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩṿ"), exception=e)
                self.handler(hook_type, bstack1l1l11l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩẀ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪẁ"), result)
        def bstack111l11llll1_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1l11l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬẂ"))
            result = None
            exception = None
            try:
                self.bstack111l11lllll_opy_(hook_type, self._111l11l1ll1_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1l11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ẃ"))
            except Exception as e:
                result = Result(result=bstack1l1l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧẄ"), exception=e)
                self.handler(hook_type, bstack1l1l11l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧẅ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l11l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨẆ"), result)
        if hook_type in [bstack1l1l11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩẇ"), bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ẉ")]:
            return bstack111l11llll1_opy_
        return bstack111l11l11l1_opy_
    def bstack111l11l1l11_opy_(self, bstack111l11l1111_opy_):
        def bstack111l11l11ll_opy_(this, *args, **kwargs):
            self.bstack111l11ll1l1_opy_(this, bstack111l11l1111_opy_)
            self._111l11lll11_opy_[bstack111l11l1111_opy_](this, *args, **kwargs)
        return bstack111l11l11ll_opy_
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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1llll11111_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1ll111l1ll_opy_, bstack1l11l1l11l_opy_, update, bstack11l1l11l_opy_,
                                       bstack11ll1111ll_opy_, bstack1l1lll1l1l_opy_, bstack1ll1111l11_opy_, bstack11ll1l11l_opy_,
                                       bstack1111ll1ll_opy_, bstack1llll11lll_opy_, bstack1lll111l1_opy_,
                                       bstack11llll1ll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack111ll11ll_opy_)
from browserstack_sdk.bstack1ll1l11l1_opy_ import bstack11ll111111_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11l1l11111_opy_
from bstack_utils.capture import bstack111ll11111_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l111l1ll_opy_, bstack11111lll1_opy_, bstack1l1l1l111_opy_, \
    bstack1lll1ll111_opy_
from bstack_utils.helper import bstack111111l11_opy_, bstack111llllllll_opy_, bstack1111ll11ll_opy_, bstack1ll1ll1l_opy_, bstack1l1l11lll11_opy_, bstack11l1lllll_opy_, \
    bstack111l1ll1l1l_opy_, \
    bstack111ll1111ll_opy_, bstack1l1l1111_opy_, bstack11l11ll11l_opy_, bstack111ll1l1111_opy_, bstack1ll111l11l_opy_, Notset, \
    bstack1ll11ll11l_opy_, bstack11ll1l1l1l1_opy_, bstack111ll111111_opy_, Result, bstack111ll11l1ll_opy_, bstack111l1lll111_opy_, error_handler, \
    bstack1ll1ll1l1l_opy_, bstack1ll11l1l1_opy_, bstack1llll111_opy_, bstack111lll11ll1_opy_
from bstack_utils.bstack111l11l1l1l_opy_ import bstack111l11l111l_opy_
from bstack_utils.messages import bstack111l11ll_opy_, bstack11ll1ll1l_opy_, bstack1l11111l1_opy_, bstack111ll111_opy_, bstack11l11ll1ll_opy_, \
    bstack1lll111ll1_opy_, bstack1ll1111l_opy_, bstack11l1llll11_opy_, bstack11l11lll11_opy_, bstack1l1ll1ll11_opy_, \
    bstack1l1lll11l_opy_, bstack1lll111111_opy_, bstack1l1l111l11_opy_
from bstack_utils.proxy import bstack1l1l11l11l_opy_, bstack111ll1ll_opy_
from bstack_utils.bstack11llll1l1_opy_ import bstack1llll1llll1l_opy_, bstack1lllll1111l1_opy_, bstack1lllll1111ll_opy_, bstack1lllll111l11_opy_, \
    bstack1lllll11l111_opy_, bstack1lllll111111_opy_, bstack1lllll111lll_opy_, bstack111lll1ll1_opy_, bstack1llll1llllll_opy_
from bstack_utils.bstack1lll111l1l_opy_ import bstack111lll1lll_opy_
from bstack_utils.bstack1111l11l_opy_ import bstack1l1ll111_opy_, bstack11llllllll_opy_, bstack11l1l1llll_opy_, \
    bstack1ll1l1ll_opy_, bstack1lll11l1l1_opy_
from bstack_utils.bstack111l1llll1_opy_ import bstack111ll111l1_opy_
from bstack_utils.bstack111l1ll11l_opy_ import bstack11l11l1l1l_opy_
import bstack_utils.accessibility as bstack11ll1lllll_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack1l1111ll1l_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack1lll111l_opy_
from bstack_utils.bstack111l1l1ll_opy_ import bstack1llllll111_opy_
from browserstack_sdk.__init__ import bstack111lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11lllll1_opy_ import bstack1lll111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack111l1l111_opy_ import bstack111l1l111_opy_, bstack11l11l1l_opy_, bstack1ll1llll1l_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack11llll111l1_opy_, bstack1lll1lll1ll_opy_, bstack1ll1lll111l_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack111l1l111_opy_ import bstack111l1l111_opy_, bstack11l11l1l_opy_, bstack1ll1llll1l_opy_
bstack111lll1l11_opy_ = None
bstack11lllll1ll_opy_ = None
bstack11lll111l_opy_ = None
bstack11l1l11lll_opy_ = None
bstack1llll11ll1_opy_ = None
bstack11l1lll1l_opy_ = None
bstack1l1lll1l1_opy_ = None
bstack1111111ll_opy_ = None
bstack11ll1lll1l_opy_ = None
bstack1l1l1111l_opy_ = None
bstack11lll1111_opy_ = None
bstack11ll1l1l1_opy_ = None
bstack1llll1l1l_opy_ = None
bstack1l1lllll_opy_ = bstack1l1l11l_opy_ (u"ࠬ࠭⊪")
CONFIG = {}
bstack1ll1l11ll_opy_ = False
bstack11ll11l11_opy_ = bstack1l1l11l_opy_ (u"࠭ࠧ⊫")
bstack1ll111ll1_opy_ = bstack1l1l11l_opy_ (u"ࠧࠨ⊬")
bstack11l1l1l11_opy_ = False
bstack1111l11l1_opy_ = []
bstack1l11ll11l_opy_ = bstack1l111l1ll_opy_
bstack1lll1l1l1lll_opy_ = bstack1l1l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ⊭")
bstack1lllllll1_opy_ = {}
bstack1l1l1l1111_opy_ = None
bstack1111l1lll_opy_ = False
logger = bstack11l1l11111_opy_.get_logger(__name__, bstack1l11ll11l_opy_)
store = {
    bstack1l1l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⊮"): []
}
bstack1lll1l1ll111_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l1111l1_opy_ = {}
current_test_uuid = None
cli_context = bstack11llll111l1_opy_(
    test_framework_name=bstack1l111ll11_opy_[bstack1l1l11l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖ࠰ࡆࡉࡊࠧ⊯")] if bstack1ll111l11l_opy_() else bstack1l111ll11_opy_[bstack1l1l11l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࠫ⊰")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1l1ll11ll1_opy_(page, bstack111l11lll_opy_):
    try:
        page.evaluate(bstack1l1l11l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ⊱"),
                      bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪ⊲") + json.dumps(
                          bstack111l11lll_opy_) + bstack1l1l11l_opy_ (u"ࠢࡾࡿࠥ⊳"))
    except Exception as e:
        print(bstack1l1l11l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ⊴"), e)
def bstack11l111ll1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1l11l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ⊵"), bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ⊶") + json.dumps(
            message) + bstack1l1l11l_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧ⊷") + json.dumps(level) + bstack1l1l11l_opy_ (u"ࠬࢃࡽࠨ⊸"))
    except Exception as e:
        print(bstack1l1l11l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ⊹"), e)
def pytest_configure(config):
    global bstack11ll11l11_opy_
    global CONFIG
    bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
    config.args = bstack11l11l1l1l_opy_.bstack1lll1ll11lll_opy_(config.args)
    bstack1ll1l111l1_opy_.bstack1l11ll1111_opy_(bstack1llll111_opy_(config.getoption(bstack1l1l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ⊺"))))
    try:
        bstack11l1l11111_opy_.bstack111l111l111_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack111l1l111_opy_.invoke(bstack11l11l1l_opy_.CONNECT, bstack1ll1llll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⊻"), bstack1l1l11l_opy_ (u"ࠩ࠳ࠫ⊼")))
        config = json.loads(os.environ.get(bstack1l1l11l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠤ⊽"), bstack1l1l11l_opy_ (u"ࠦࢀࢃࠢ⊾")))
        cli.bstack1ll1ll1l1ll_opy_(bstack11l11ll11l_opy_(bstack11ll11l11_opy_, CONFIG), cli_context.platform_index, bstack11l1l11l_opy_)
    if cli.bstack1ll11llllll_opy_(bstack1lll111l1ll_opy_):
        cli.bstack1ll1lllll1l_opy_()
        logger.debug(bstack1l1l11l_opy_ (u"ࠧࡉࡌࡊࠢ࡬ࡷࠥࡧࡣࡵ࡫ࡹࡩࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦ⊿") + str(cli_context.platform_index) + bstack1l1l11l_opy_ (u"ࠨࠢ⋀"))
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.BEFORE_ALL, bstack1ll1lll111l_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack1l1l11l_opy_ (u"ࠢࡸࡪࡨࡲࠧ⋁"), None)
    if cli.is_running() and when == bstack1l1l11l_opy_ (u"ࠣࡥࡤࡰࡱࠨ⋂"):
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.LOG_REPORT, bstack1ll1lll111l_opy_.PRE, item, call)
    outcome = yield
    if when == bstack1l1l11l_opy_ (u"ࠤࡦࡥࡱࡲࠢ⋃"):
        report = outcome.get_result()
        passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l11l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ⋄")))
        if not passed:
            config = json.loads(os.environ.get(bstack1l1l11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠥ⋅"), bstack1l1l11l_opy_ (u"ࠧࢁࡽࠣ⋆")))
            if bstack1llllll111_opy_.bstack11l111llll_opy_(config):
                bstack11111l11l1l_opy_ = bstack1llllll111_opy_.bstack1llll1llll_opy_(config)
                if item.execution_count > bstack11111l11l1l_opy_:
                    print(bstack1l1l11l_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡶࡪࡺࡲࡪࡧࡶ࠾ࠥ࠭⋇"), report.nodeid, os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⋈")))
                    bstack1llllll111_opy_.bstack11111ll1111_opy_(report.nodeid)
            else:
                print(bstack1l1l11l_opy_ (u"ࠨࡖࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠨ⋉"), report.nodeid, os.environ.get(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⋊")))
                bstack1llllll111_opy_.bstack11111ll1111_opy_(report.nodeid)
        else:
            print(bstack1l1l11l_opy_ (u"ࠪࡘࡪࡹࡴࠡࡲࡤࡷࡸ࡫ࡤ࠻ࠢࠪ⋋"), report.nodeid, os.environ.get(bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⋌")))
    if cli.is_running():
        if when == bstack1l1l11l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦ⋍"):
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.BEFORE_EACH, bstack1ll1lll111l_opy_.POST, item, call, outcome)
        elif when == bstack1l1l11l_opy_ (u"ࠨࡣࡢ࡮࡯ࠦ⋎"):
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.LOG_REPORT, bstack1ll1lll111l_opy_.POST, item, call, outcome)
        elif when == bstack1l1l11l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤ⋏"):
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.AFTER_EACH, bstack1ll1lll111l_opy_.POST, item, call, outcome)
        return # skip all existing operations
    skipSessionName = item.config.getoption(bstack1l1l11l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⋐"))
    plugins = item.config.getoption(bstack1l1l11l_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥ⋑"))
    report = outcome.get_result()
    os.environ[bstack1l1l11l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⋒")] = report.nodeid
    bstack1lll1l1ll1ll_opy_(item, call, report)
    if bstack1l1l11l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤ⋓") not in plugins or bstack1ll111l11l_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1l11l_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨ⋔"), None)
    page = getattr(item, bstack1l1l11l_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧ⋕"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack1lll1ll1111l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack1lll1l1llll1_opy_(item, report, summary, skipSessionName)
def bstack1lll1ll1111l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack1l1l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⋖") and report.skipped:
        bstack1llll1llllll_opy_(report)
    if report.when in [bstack1l1l11l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢ⋗"), bstack1l1l11l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦ⋘")]:
        return
    if not bstack1l1l11lll11_opy_():
        return
    try:
        if ((str(skipSessionName).lower() != bstack1l1l11l_opy_ (u"ࠪࡸࡷࡻࡥࠨ⋙")) and (not cli.is_running())) and item._driver.session_id:
            item._driver.execute_script(
                bstack1l1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ⋚") + json.dumps(
                    report.nodeid) + bstack1l1l11l_opy_ (u"ࠬࢃࡽࠨ⋛"))
        os.environ[bstack1l1l11l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ⋜")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1l11l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢ⋝").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l11l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥ⋞")))
    bstack1ll1ll1ll_opy_ = bstack1l1l11l_opy_ (u"ࠤࠥ⋟")
    bstack1llll1llllll_opy_(report)
    if not passed:
        try:
            bstack1ll1ll1ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1l11l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥ⋠").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1ll1ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1l11l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨ⋡")))
        bstack1ll1ll1ll_opy_ = bstack1l1l11l_opy_ (u"ࠧࠨ⋢")
        if not passed:
            try:
                bstack1ll1ll1ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l11l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨ⋣").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1ll1ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫ⋤")
                    + json.dumps(bstack1l1l11l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤ⋥"))
                    + bstack1l1l11l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧ⋦")
                )
            else:
                item._driver.execute_script(
                    bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨ⋧")
                    + json.dumps(str(bstack1ll1ll1ll_opy_))
                    + bstack1l1l11l_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢ⋨")
                )
        except Exception as e:
            summary.append(bstack1l1l11l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥ⋩").format(e))
def bstack1lll1l11ll11_opy_(test_name, error_message):
    try:
        bstack1lll1l11l1l1_opy_ = []
        bstack1ll1l1111l_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭⋪"), bstack1l1l11l_opy_ (u"ࠧ࠱ࠩ⋫"))
        bstack1lll1l1l1_opy_ = {bstack1l1l11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭⋬"): test_name, bstack1l1l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⋭"): error_message, bstack1l1l11l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ⋮"): bstack1ll1l1111l_opy_}
        bstack1lll1l1l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ⋯"))
        if os.path.exists(bstack1lll1l1l111l_opy_):
            with open(bstack1lll1l1l111l_opy_) as f:
                bstack1lll1l11l1l1_opy_ = json.load(f)
        bstack1lll1l11l1l1_opy_.append(bstack1lll1l1l1_opy_)
        with open(bstack1lll1l1l111l_opy_, bstack1l1l11l_opy_ (u"ࠬࡽࠧ⋰")) as f:
            json.dump(bstack1lll1l11l1l1_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫ⋱") + str(e))
def bstack1lll1l1llll1_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack1l1l11l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ⋲"), bstack1l1l11l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ⋳")]:
        return
    if (str(skipSessionName).lower() != bstack1l1l11l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⋴")):
        bstack1l1ll11ll1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l11l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ⋵")))
    bstack1ll1ll1ll_opy_ = bstack1l1l11l_opy_ (u"ࠦࠧ⋶")
    bstack1llll1llllll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll1ll1ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l11l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧ⋷").format(e)
                )
        try:
            if passed:
                bstack1lll11l1l1_opy_(getattr(item, bstack1l1l11l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ⋸"), None), bstack1l1l11l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ⋹"))
            else:
                error_message = bstack1l1l11l_opy_ (u"ࠨࠩ⋺")
                if bstack1ll1ll1ll_opy_:
                    bstack11l111ll1l_opy_(item._page, str(bstack1ll1ll1ll_opy_), bstack1l1l11l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ⋻"))
                    bstack1lll11l1l1_opy_(getattr(item, bstack1l1l11l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ⋼"), None), bstack1l1l11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ⋽"), str(bstack1ll1ll1ll_opy_))
                    error_message = str(bstack1ll1ll1ll_opy_)
                else:
                    bstack1lll11l1l1_opy_(getattr(item, bstack1l1l11l_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫ⋾"), None), bstack1l1l11l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ⋿"))
                bstack1lll1l11ll11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1l11l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦ⌀").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack1l1l11l_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ⌁"), default=bstack1l1l11l_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣ⌂"), help=bstack1l1l11l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤ⌃"))
    parser.addoption(bstack1l1l11l_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ⌄"), default=bstack1l1l11l_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ⌅"), help=bstack1l1l11l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ⌆"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1l11l_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤ⌇"), action=bstack1l1l11l_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢ⌈"), default=bstack1l1l11l_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤ⌉"),
                         help=bstack1l1l11l_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤ⌊"))
def bstack111ll1l111_opy_(log):
    if not (log[bstack1l1l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⌋")] and log[bstack1l1l11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⌌")].strip()):
        return
    active = bstack111l1lllll_opy_()
    log = {
        bstack1l1l11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⌍"): log[bstack1l1l11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⌎")],
        bstack1l1l11l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⌏"): bstack1111ll11ll_opy_().isoformat() + bstack1l1l11l_opy_ (u"ࠩ࡝ࠫ⌐"),
        bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⌑"): log[bstack1l1l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⌒")],
    }
    if active:
        if active[bstack1l1l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⌓")] == bstack1l1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⌔"):
            log[bstack1l1l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⌕")] = active[bstack1l1l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⌖")]
        elif active[bstack1l1l11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⌗")] == bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࠨ⌘"):
            log[bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⌙")] = active[bstack1l1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⌚")]
    bstack1l1111ll1l_opy_.bstack11ll11ll11_opy_([log])
def bstack111l1lllll_opy_():
    if len(store[bstack1l1l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ⌛")]) > 0 and store[bstack1l1l11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⌜")][-1]:
        return {
            bstack1l1l11l_opy_ (u"ࠨࡶࡼࡴࡪ࠭⌝"): bstack1l1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ⌞"),
            bstack1l1l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⌟"): store[bstack1l1l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ⌠")][-1]
        }
    if store.get(bstack1l1l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⌡"), None):
        return {
            bstack1l1l11l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⌢"): bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࠬ⌣"),
            bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⌤"): store[bstack1l1l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⌥")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.INIT_TEST, bstack1ll1lll111l_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.INIT_TEST, bstack1ll1lll111l_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._1lll1l1ll11l_opy_ = True
        bstack1ll111ll11_opy_ = bstack11ll1lllll_opy_.bstack1111ll11l_opy_(bstack111ll1111ll_opy_(item.own_markers))
        if not cli.bstack1ll11llllll_opy_(bstack1lll111l1ll_opy_):
            item._a11y_test_case = bstack1ll111ll11_opy_
            if bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⌦"), None):
                driver = getattr(item, bstack1l1l11l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬ⌧"), None)
                item._a11y_started = bstack11ll1lllll_opy_.bstack1ll111lll1_opy_(driver, bstack1ll111ll11_opy_)
        if not bstack1l1111ll1l_opy_.on() or bstack1lll1l1l1lll_opy_ != bstack1l1l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⌨"):
            return
        global current_test_uuid #, bstack111l1ll1l1_opy_
        bstack111l111l11_opy_ = {
            bstack1l1l11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ〈"): uuid4().__str__(),
            bstack1l1l11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ〉"): bstack1111ll11ll_opy_().isoformat() + bstack1l1l11l_opy_ (u"ࠨ࡜ࠪ⌫")
        }
        current_test_uuid = bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⌬")]
        store[bstack1l1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⌭")] = bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⌮")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l1111l1_opy_[item.nodeid] = {**_111l1111l1_opy_[item.nodeid], **bstack111l111l11_opy_}
        bstack1lll1l1l11l1_opy_(item, _111l1111l1_opy_[item.nodeid], bstack1l1l11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⌯"))
    except Exception as err:
        print(bstack1l1l11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨ⌰"), str(err))
def pytest_runtest_setup(item):
    store[bstack1l1l11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⌱")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.BEFORE_EACH, bstack1ll1lll111l_opy_.PRE, item, bstack1l1l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⌲"))
    if bstack1llllll111_opy_.bstack1111l1111ll_opy_():
            bstack1lll1l1l1ll1_opy_ = bstack1l1l11l_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡤࡷࠥࡺࡨࡦࠢࡤࡦࡴࡸࡴࠡࡤࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥ࡫ࡸࡪࡵࡷࡷ࠳ࠨ⌳")
            logger.error(bstack1lll1l1l1ll1_opy_)
            bstack111l111l11_opy_ = {
                bstack1l1l11l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⌴"): uuid4().__str__(),
                bstack1l1l11l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⌵"): bstack1111ll11ll_opy_().isoformat() + bstack1l1l11l_opy_ (u"ࠬࡠࠧ⌶"),
                bstack1l1l11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⌷"): bstack1111ll11ll_opy_().isoformat() + bstack1l1l11l_opy_ (u"࡛ࠧࠩ⌸"),
                bstack1l1l11l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⌹"): bstack1l1l11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⌺"),
                bstack1l1l11l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ⌻"): bstack1lll1l1l1ll1_opy_,
                bstack1l1l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⌼"): [],
                bstack1l1l11l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧ⌽"): []
            }
            bstack1lll1l1l11l1_opy_(item, bstack111l111l11_opy_, bstack1l1l11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧ⌾"))
            pytest.skip(bstack1lll1l1l1ll1_opy_)
            return # skip all existing operations
    global bstack1lll1l1ll111_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111ll1l1111_opy_():
        atexit.register(bstack1l1l1ll11_opy_)
        if not bstack1lll1l1ll111_opy_:
            try:
                bstack1lll1l1ll1l1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111lll11ll1_opy_():
                    bstack1lll1l1ll1l1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll1l1ll1l1_opy_:
                    signal.signal(s, bstack1lll1l11ll1l_opy_)
                bstack1lll1l1ll111_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l1l11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣ⌿") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llll1llll1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1l11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ⍀")
    try:
        if not bstack1l1111ll1l_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l111l11_opy_ = {
            bstack1l1l11l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⍁"): uuid,
            bstack1l1l11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⍂"): bstack1111ll11ll_opy_().isoformat() + bstack1l1l11l_opy_ (u"ࠫ࡟࠭⍃"),
            bstack1l1l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪ⍄"): bstack1l1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ⍅"),
            bstack1l1l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ⍆"): bstack1l1l11l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⍇"),
            bstack1l1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ⍈"): bstack1l1l11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ⍉")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l1l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ⍊")] = item
        store[bstack1l1l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ⍋")] = [uuid]
        if not _111l1111l1_opy_.get(item.nodeid, None):
            _111l1111l1_opy_[item.nodeid] = {bstack1l1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ⍌"): [], bstack1l1l11l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⍍"): []}
        _111l1111l1_opy_[item.nodeid][bstack1l1l11l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⍎")].append(bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ⍏")])
        _111l1111l1_opy_[item.nodeid + bstack1l1l11l_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪ⍐")] = bstack111l111l11_opy_
        bstack1lll1ll11l11_opy_(item, bstack111l111l11_opy_, bstack1l1l11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⍑"))
    except Exception as err:
        print(bstack1l1l11l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ⍒"), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.AFTER_EACH, bstack1ll1lll111l_opy_.PRE, item, bstack1l1l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⍓"))
        return # skip all existing operations
    try:
        global bstack1lllllll1_opy_
        bstack1ll1l1111l_opy_ = 0
        if bstack11l1l1l11_opy_ is True:
            bstack1ll1l1111l_opy_ = int(os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ⍔")))
        if bstack11l1111ll_opy_.bstack11lllll1_opy_() == bstack1l1l11l_opy_ (u"ࠣࡶࡵࡹࡪࠨ⍕"):
            if bstack11l1111ll_opy_.bstack111l1111_opy_() == bstack1l1l11l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ⍖"):
                bstack1lll1l1lll11_opy_ = bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⍗"), None)
                bstack1lll1lll1l_opy_ = bstack1lll1l1lll11_opy_ + bstack1l1l11l_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ⍘")
                driver = getattr(item, bstack1l1l11l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⍙"), None)
                bstack1llllll1l1_opy_ = getattr(item, bstack1l1l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⍚"), None)
                bstack1l111ll1l_opy_ = getattr(item, bstack1l1l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⍛"), None)
                PercySDK.screenshot(driver, bstack1lll1lll1l_opy_, bstack1llllll1l1_opy_=bstack1llllll1l1_opy_, bstack1l111ll1l_opy_=bstack1l111ll1l_opy_, bstack1lll111ll_opy_=bstack1ll1l1111l_opy_)
        if not cli.bstack1ll11llllll_opy_(bstack1lll111l1ll_opy_):
            if getattr(item, bstack1l1l11l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ⍜"), False):
                bstack11ll111111_opy_.bstack111l11111_opy_(getattr(item, bstack1l1l11l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⍝"), None), bstack1lllllll1_opy_, logger, item)
        if not bstack1l1111ll1l_opy_.on():
            return
        bstack111l111l11_opy_ = {
            bstack1l1l11l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⍞"): uuid4().__str__(),
            bstack1l1l11l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⍟"): bstack1111ll11ll_opy_().isoformat() + bstack1l1l11l_opy_ (u"ࠬࡠࠧ⍠"),
            bstack1l1l11l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⍡"): bstack1l1l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ⍢"),
            bstack1l1l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ⍣"): bstack1l1l11l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭⍤"),
            bstack1l1l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭⍥"): bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭⍦")
        }
        _111l1111l1_opy_[item.nodeid + bstack1l1l11l_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ⍧")] = bstack111l111l11_opy_
        bstack1lll1ll11l11_opy_(item, bstack111l111l11_opy_, bstack1l1l11l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⍨"))
    except Exception as err:
        print(bstack1l1l11l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭⍩"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack1lllll111l11_opy_(fixturedef.argname):
        store[bstack1l1l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ⍪")] = request.node
    elif bstack1lllll11l111_opy_(fixturedef.argname):
        store[bstack1l1l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ⍫")] = request.node
    if not bstack1l1111ll1l_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.SETUP_FIXTURE, bstack1ll1lll111l_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.SETUP_FIXTURE, bstack1ll1lll111l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.SETUP_FIXTURE, bstack1ll1lll111l_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.SETUP_FIXTURE, bstack1ll1lll111l_opy_.POST, fixturedef, request, outcome)
        return # skip all existing operations
    try:
        fixture = {
            bstack1l1l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨ⍬"): fixturedef.argname,
            bstack1l1l11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⍭"): bstack111l1ll1l1l_opy_(outcome),
            bstack1l1l11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⍮"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l1l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ⍯")]
        if not _111l1111l1_opy_.get(current_test_item.nodeid, None):
            _111l1111l1_opy_[current_test_item.nodeid] = {bstack1l1l11l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ⍰"): []}
        _111l1111l1_opy_[current_test_item.nodeid][bstack1l1l11l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ⍱")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1l11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ⍲"), str(err))
if bstack1ll111l11l_opy_() and bstack1l1111ll1l_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.STEP, bstack1ll1lll111l_opy_.PRE, request, step)
            return
        try:
            _111l1111l1_opy_[request.node.nodeid][bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭⍳")].bstack1ll11ll1ll_opy_(id(step))
        except Exception as err:
            print(bstack1l1l11l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩ⍴"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.STEP, bstack1ll1lll111l_opy_.POST, request, step, exception)
            return
        try:
            _111l1111l1_opy_[request.node.nodeid][bstack1l1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⍵")].bstack111ll11l1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1l11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ⍶"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.STEP, bstack1ll1lll111l_opy_.POST, request, step)
            return
        try:
            bstack111l1llll1_opy_: bstack111ll111l1_opy_ = _111l1111l1_opy_[request.node.nodeid][bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ⍷")]
            bstack111l1llll1_opy_.bstack111ll11l1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1l11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ⍸"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll1l1l1lll_opy_
        try:
            if not bstack1l1111ll1l_opy_.on() or bstack1lll1l1l1lll_opy_ != bstack1l1l11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭⍹"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.TEST, bstack1ll1lll111l_opy_.PRE, request, feature, scenario)
                return
            driver = bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ⍺"), None)
            if not _111l1111l1_opy_.get(request.node.nodeid, None):
                _111l1111l1_opy_[request.node.nodeid] = {}
            bstack111l1llll1_opy_ = bstack111ll111l1_opy_.bstack11ll11ll1l1_opy_(
                scenario, feature, request.node,
                name=bstack1lllll111111_opy_(request.node, scenario),
                started_at=bstack11l1lllll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1l11l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭⍻"),
                tags=bstack1lllll111lll_opy_(feature, scenario),
                bstack111l1ll111_opy_=bstack1l1111ll1l_opy_.bstack111lll1111_opy_(driver) if driver and driver.session_id else {}
            )
            _111l1111l1_opy_[request.node.nodeid][bstack1l1l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ⍼")] = bstack111l1llll1_opy_
            bstack1lll1l1l1111_opy_(bstack111l1llll1_opy_.uuid)
            bstack1l1111ll1l_opy_.bstack111ll11lll_opy_(bstack1l1l11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⍽"), bstack111l1llll1_opy_)
        except Exception as err:
            print(bstack1l1l11l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ⍾"), str(err))
def bstack1lll1ll111ll_opy_(bstack111ll11ll1_opy_):
    if bstack111ll11ll1_opy_ in store[bstack1l1l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ⍿")]:
        store[bstack1l1l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭⎀")].remove(bstack111ll11ll1_opy_)
def bstack1lll1l1l1111_opy_(test_uuid):
    store[bstack1l1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⎁")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1l1111ll1l_opy_.bstack1llll1111l1l_opy_
def bstack1lll1l1ll1ll_opy_(item, call, report):
    logger.debug(bstack1l1l11l_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡶࡹ࠭⎂"))
    global bstack1lll1l1l1lll_opy_
    bstack1l111lll1_opy_ = bstack11l1lllll_opy_()
    if hasattr(report, bstack1l1l11l_opy_ (u"ࠬࡹࡴࡰࡲࠪ⎃")):
        bstack1l111lll1_opy_ = bstack111ll11l1ll_opy_(report.stop)
    elif hasattr(report, bstack1l1l11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬ⎄")):
        bstack1l111lll1_opy_ = bstack111ll11l1ll_opy_(report.start)
    try:
        if getattr(report, bstack1l1l11l_opy_ (u"ࠧࡸࡪࡨࡲࠬ⎅"), bstack1l1l11l_opy_ (u"ࠨࠩ⎆")) == bstack1l1l11l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⎇"):
            logger.debug(bstack1l1l11l_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ⎈").format(getattr(report, bstack1l1l11l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ⎉"), bstack1l1l11l_opy_ (u"ࠬ࠭⎊")).__str__(), bstack1lll1l1l1lll_opy_))
            if bstack1lll1l1l1lll_opy_ == bstack1l1l11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⎋"):
                _111l1111l1_opy_[item.nodeid][bstack1l1l11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⎌")] = bstack1l111lll1_opy_
                bstack1lll1l1l11l1_opy_(item, _111l1111l1_opy_[item.nodeid], bstack1l1l11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⎍"), report, call)
                store[bstack1l1l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⎎")] = None
            elif bstack1lll1l1l1lll_opy_ == bstack1l1l11l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢ⎏"):
                bstack111l1llll1_opy_ = _111l1111l1_opy_[item.nodeid][bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⎐")]
                bstack111l1llll1_opy_.set(hooks=_111l1111l1_opy_[item.nodeid].get(bstack1l1l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⎑"), []))
                exception, bstack111l1lll11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111l1lll11_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l1l11l_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬ⎒"), bstack1l1l11l_opy_ (u"ࠧࠨ⎓"))]
                bstack111l1llll1_opy_.stop(time=bstack1l111lll1_opy_, result=Result(result=getattr(report, bstack1l1l11l_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ⎔"), bstack1l1l11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⎕")), exception=exception, bstack111l1lll11_opy_=bstack111l1lll11_opy_))
                bstack1l1111ll1l_opy_.bstack111ll11lll_opy_(bstack1l1l11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⎖"), _111l1111l1_opy_[item.nodeid][bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⎗")])
        elif getattr(report, bstack1l1l11l_opy_ (u"ࠬࡽࡨࡦࡰࠪ⎘"), bstack1l1l11l_opy_ (u"࠭ࠧ⎙")) in [bstack1l1l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⎚"), bstack1l1l11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⎛")]:
            logger.debug(bstack1l1l11l_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀࠫ⎜").format(getattr(report, bstack1l1l11l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⎝"), bstack1l1l11l_opy_ (u"ࠫࠬ⎞")).__str__(), bstack1lll1l1l1lll_opy_))
            bstack111ll1llll_opy_ = item.nodeid + bstack1l1l11l_opy_ (u"ࠬ࠳ࠧ⎟") + getattr(report, bstack1l1l11l_opy_ (u"࠭ࡷࡩࡧࡱࠫ⎠"), bstack1l1l11l_opy_ (u"ࠧࠨ⎡"))
            if getattr(report, bstack1l1l11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⎢"), False):
                hook_type = bstack1l1l11l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⎣") if getattr(report, bstack1l1l11l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⎤"), bstack1l1l11l_opy_ (u"ࠫࠬ⎥")) == bstack1l1l11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⎦") else bstack1l1l11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⎧")
                _111l1111l1_opy_[bstack111ll1llll_opy_] = {
                    bstack1l1l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⎨"): uuid4().__str__(),
                    bstack1l1l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⎩"): bstack1l111lll1_opy_,
                    bstack1l1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⎪"): hook_type
                }
            _111l1111l1_opy_[bstack111ll1llll_opy_][bstack1l1l11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⎫")] = bstack1l111lll1_opy_
            bstack1lll1ll111ll_opy_(_111l1111l1_opy_[bstack111ll1llll_opy_][bstack1l1l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⎬")])
            bstack1lll1ll11l11_opy_(item, _111l1111l1_opy_[bstack111ll1llll_opy_], bstack1l1l11l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⎭"), report, call)
            if getattr(report, bstack1l1l11l_opy_ (u"࠭ࡷࡩࡧࡱࠫ⎮"), bstack1l1l11l_opy_ (u"ࠧࠨ⎯")) == bstack1l1l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⎰"):
                if getattr(report, bstack1l1l11l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ⎱"), bstack1l1l11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⎲")) == bstack1l1l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⎳"):
                    bstack111l111l11_opy_ = {
                        bstack1l1l11l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⎴"): uuid4().__str__(),
                        bstack1l1l11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⎵"): bstack11l1lllll_opy_(),
                        bstack1l1l11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⎶"): bstack11l1lllll_opy_()
                    }
                    _111l1111l1_opy_[item.nodeid] = {**_111l1111l1_opy_[item.nodeid], **bstack111l111l11_opy_}
                    bstack1lll1l1l11l1_opy_(item, _111l1111l1_opy_[item.nodeid], bstack1l1l11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⎷"))
                    bstack1lll1l1l11l1_opy_(item, _111l1111l1_opy_[item.nodeid], bstack1l1l11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⎸"), report, call)
    except Exception as err:
        print(bstack1l1l11l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨ⎹"), str(err))
def bstack1lll1l11l1ll_opy_(test, bstack111l111l11_opy_, result=None, call=None, bstack1l1l1l11ll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111l1llll1_opy_ = {
        bstack1l1l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⎺"): bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⎻")],
        bstack1l1l11l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⎼"): bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࠬ⎽"),
        bstack1l1l11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭⎾"): test.name,
        bstack1l1l11l_opy_ (u"ࠩࡥࡳࡩࡿࠧ⎿"): {
            bstack1l1l11l_opy_ (u"ࠪࡰࡦࡴࡧࠨ⏀"): bstack1l1l11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⏁"),
            bstack1l1l11l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⏂"): inspect.getsource(test.obj)
        },
        bstack1l1l11l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⏃"): test.name,
        bstack1l1l11l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭⏄"): test.name,
        bstack1l1l11l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ⏅"): bstack11l11l1l1l_opy_.bstack1111l1l11l_opy_(test),
        bstack1l1l11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ⏆"): file_path,
        bstack1l1l11l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ⏇"): file_path,
        bstack1l1l11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⏈"): bstack1l1l11l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⏉"),
        bstack1l1l11l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ⏊"): file_path,
        bstack1l1l11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⏋"): bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⏌")],
        bstack1l1l11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⏍"): bstack1l1l11l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⏎"),
        bstack1l1l11l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ⏏"): {
            bstack1l1l11l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ⏐"): test.nodeid
        },
        bstack1l1l11l_opy_ (u"࠭ࡴࡢࡩࡶࠫ⏑"): bstack111ll1111ll_opy_(test.own_markers)
    }
    if bstack1l1l1l11ll_opy_ in [bstack1l1l11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ⏒"), bstack1l1l11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⏓")]:
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠩࡰࡩࡹࡧࠧ⏔")] = {
            bstack1l1l11l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ⏕"): bstack111l111l11_opy_.get(bstack1l1l11l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭⏖"), [])
        }
    if bstack1l1l1l11ll_opy_ == bstack1l1l11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭⏗"):
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⏘")] = bstack1l1l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ⏙")
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ⏚")] = bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⏛")]
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⏜")] = bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⏝")]
    if result:
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⏞")] = result.outcome
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ⏟")] = result.duration * 1000
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⏠")] = bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⏡")]
        if result.failed:
            bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⏢")] = bstack1l1111ll1l_opy_.bstack1llllll1ll1_opy_(call.excinfo.typename)
            bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ⏣")] = bstack1l1111ll1l_opy_.bstack1llll1111lll_opy_(call.excinfo, result)
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⏤")] = bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⏥")]
    if outcome:
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⏦")] = bstack111l1ll1l1l_opy_(outcome)
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨ⏧")] = 0
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭⏨")] = bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⏩")]
        if bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⏪")] == bstack1l1l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⏫"):
            bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ⏬")] = bstack1l1l11l_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ⏭")  # bstack1lll1l1l1l11_opy_
            bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ⏮")] = [{bstack1l1l11l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⏯"): [bstack1l1l11l_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭⏰")]}]
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⏱")] = bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ⏲")]
    return bstack111l1llll1_opy_
def bstack1lll1l11l11l_opy_(test, bstack111l111l1l_opy_, bstack1l1l1l11ll_opy_, result, call, outcome, bstack1lll1l1lll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⏳")]
    hook_name = bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⏴")]
    hook_data = {
        bstack1l1l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⏵"): bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⏶")],
        bstack1l1l11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ⏷"): bstack1l1l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ⏸"),
        bstack1l1l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⏹"): bstack1l1l11l_opy_ (u"ࠬࢁࡽࠨ⏺").format(bstack1lllll1111l1_opy_(hook_name)),
        bstack1l1l11l_opy_ (u"࠭ࡢࡰࡦࡼࠫ⏻"): {
            bstack1l1l11l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ⏼"): bstack1l1l11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⏽"),
            bstack1l1l11l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ⏾"): None
        },
        bstack1l1l11l_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ⏿"): test.name,
        bstack1l1l11l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ␀"): bstack11l11l1l1l_opy_.bstack1111l1l11l_opy_(test, hook_name),
        bstack1l1l11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ␁"): file_path,
        bstack1l1l11l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ␂"): file_path,
        bstack1l1l11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ␃"): bstack1l1l11l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ␄"),
        bstack1l1l11l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ␅"): file_path,
        bstack1l1l11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ␆"): bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ␇")],
        bstack1l1l11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ␈"): bstack1l1l11l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ␉") if bstack1lll1l1l1lll_opy_ == bstack1l1l11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ␊") else bstack1l1l11l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ␋"),
        bstack1l1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ␌"): hook_type
    }
    bstack1ll11l1111l_opy_ = bstack1111llllll_opy_(_111l1111l1_opy_.get(test.nodeid, None))
    if bstack1ll11l1111l_opy_:
        hook_data[bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ␍")] = bstack1ll11l1111l_opy_
    if result:
        hook_data[bstack1l1l11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ␎")] = result.outcome
        hook_data[bstack1l1l11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭␏")] = result.duration * 1000
        hook_data[bstack1l1l11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ␐")] = bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ␑")]
        if result.failed:
            hook_data[bstack1l1l11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ␒")] = bstack1l1111ll1l_opy_.bstack1llllll1ll1_opy_(call.excinfo.typename)
            hook_data[bstack1l1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ␓")] = bstack1l1111ll1l_opy_.bstack1llll1111lll_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1l11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ␔")] = bstack111l1ll1l1l_opy_(outcome)
        hook_data[bstack1l1l11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ␕")] = 100
        hook_data[bstack1l1l11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ␖")] = bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ␗")]
        if hook_data[bstack1l1l11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ␘")] == bstack1l1l11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ␙"):
            hook_data[bstack1l1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ␚")] = bstack1l1l11l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ␛")  # bstack1lll1l1l1l11_opy_
            hook_data[bstack1l1l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ␜")] = [{bstack1l1l11l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ␝"): [bstack1l1l11l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ␞")]}]
    if bstack1lll1l1lll1l_opy_:
        hook_data[bstack1l1l11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ␟")] = bstack1lll1l1lll1l_opy_.result
        hook_data[bstack1l1l11l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ␠")] = bstack11ll1l1l1l1_opy_(bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭␡")], bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ␢")])
        hook_data[bstack1l1l11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ␣")] = bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ␤")]
        if hook_data[bstack1l1l11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭␥")] == bstack1l1l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ␦"):
            hook_data[bstack1l1l11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ␧")] = bstack1l1111ll1l_opy_.bstack1llllll1ll1_opy_(bstack1lll1l1lll1l_opy_.exception_type)
            hook_data[bstack1l1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ␨")] = [{bstack1l1l11l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭␩"): bstack111ll111111_opy_(bstack1lll1l1lll1l_opy_.exception)}]
    return hook_data
def bstack1lll1l1l11l1_opy_(test, bstack111l111l11_opy_, bstack1l1l1l11ll_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack1l1l11l_opy_ (u"ࠫࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡦࡵࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ␪").format(bstack1l1l1l11ll_opy_))
    bstack111l1llll1_opy_ = bstack1lll1l11l1ll_opy_(test, bstack111l111l11_opy_, result, call, bstack1l1l1l11ll_opy_, outcome)
    driver = getattr(test, bstack1l1l11l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭␫"), None)
    if bstack1l1l1l11ll_opy_ == bstack1l1l11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ␬") and driver:
        bstack111l1llll1_opy_[bstack1l1l11l_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭␭")] = bstack1l1111ll1l_opy_.bstack111lll1111_opy_(driver)
    if bstack1l1l1l11ll_opy_ == bstack1l1l11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ␮"):
        bstack1l1l1l11ll_opy_ = bstack1l1l11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ␯")
    bstack111l11llll_opy_ = {
        bstack1l1l11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ␰"): bstack1l1l1l11ll_opy_,
        bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭␱"): bstack111l1llll1_opy_
    }
    bstack1l1111ll1l_opy_.bstack1ll1l111ll_opy_(bstack111l11llll_opy_)
    if bstack1l1l1l11ll_opy_ == bstack1l1l11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭␲"):
        threading.current_thread().bstackTestMeta = {bstack1l1l11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭␳"): bstack1l1l11l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ␴")}
    elif bstack1l1l1l11ll_opy_ == bstack1l1l11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ␵"):
        threading.current_thread().bstackTestMeta = {bstack1l1l11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ␶"): getattr(result, bstack1l1l11l_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫ␷"), bstack1l1l11l_opy_ (u"ࠫࠬ␸"))}
def bstack1lll1ll11l11_opy_(test, bstack111l111l11_opy_, bstack1l1l1l11ll_opy_, result=None, call=None, outcome=None, bstack1lll1l1lll1l_opy_=None):
    logger.debug(bstack1l1l11l_opy_ (u"ࠬࡹࡥ࡯ࡦࡢ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡩࡱࡲ࡯ࠥࡪࡡࡵࡣ࠯ࠤࡪࡼࡥ࡯ࡶࡗࡽࡵ࡫ࠠ࠮ࠢࡾࢁࠬ␹").format(bstack1l1l1l11ll_opy_))
    hook_data = bstack1lll1l11l11l_opy_(test, bstack111l111l11_opy_, bstack1l1l1l11ll_opy_, result, call, outcome, bstack1lll1l1lll1l_opy_)
    bstack111l11llll_opy_ = {
        bstack1l1l11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ␺"): bstack1l1l1l11ll_opy_,
        bstack1l1l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩ␻"): hook_data
    }
    bstack1l1111ll1l_opy_.bstack1ll1l111ll_opy_(bstack111l11llll_opy_)
def bstack1111llllll_opy_(bstack111l111l11_opy_):
    if not bstack111l111l11_opy_:
        return None
    if bstack111l111l11_opy_.get(bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ␼"), None):
        return getattr(bstack111l111l11_opy_[bstack1l1l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ␽")], bstack1l1l11l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ␾"), None)
    return bstack111l111l11_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩ␿"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.LOG, bstack1ll1lll111l_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_.LOG, bstack1ll1lll111l_opy_.POST, request, caplog)
        return # skip all existing operations
    try:
        if not bstack1l1111ll1l_opy_.on():
            return
        places = [bstack1l1l11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⑀"), bstack1l1l11l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⑁"), bstack1l1l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⑂")]
        logs = []
        for bstack1lll1l11lll1_opy_ in places:
            records = caplog.get_records(bstack1lll1l11lll1_opy_)
            bstack1lll1l1l11ll_opy_ = bstack1l1l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⑃") if bstack1lll1l11lll1_opy_ == bstack1l1l11l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⑄") else bstack1l1l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⑅")
            bstack1lll1l1lllll_opy_ = request.node.nodeid + (bstack1l1l11l_opy_ (u"ࠫࠬ⑆") if bstack1lll1l11lll1_opy_ == bstack1l1l11l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⑇") else bstack1l1l11l_opy_ (u"࠭࠭ࠨ⑈") + bstack1lll1l11lll1_opy_)
            test_uuid = bstack1111llllll_opy_(_111l1111l1_opy_.get(bstack1lll1l1lllll_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack111l1lll111_opy_(record.message):
                    continue
                logs.append({
                    bstack1l1l11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⑉"): bstack111llllllll_opy_(record.created).isoformat() + bstack1l1l11l_opy_ (u"ࠨ࡜ࠪ⑊"),
                    bstack1l1l11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⑋"): record.levelname,
                    bstack1l1l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⑌"): record.message,
                    bstack1lll1l1l11ll_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1l1111ll1l_opy_.bstack11ll11ll11_opy_(logs)
    except Exception as err:
        print(bstack1l1l11l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ⑍"), str(err))
def bstack111llll11_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1111l1lll_opy_
    bstack11l11l1111_opy_ = bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ⑎"), None) and bstack111111l11_opy_(
            threading.current_thread(), bstack1l1l11l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⑏"), None)
    bstack1l111ll1_opy_ = getattr(driver, bstack1l1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ⑐"), None) != None and getattr(driver, bstack1l1l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ⑑"), None) == True
    if sequence == bstack1l1l11l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ⑒") and driver != None:
      if not bstack1111l1lll_opy_ and bstack1l1l11lll11_opy_() and bstack1l1l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⑓") in CONFIG and CONFIG[bstack1l1l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⑔")] == True and bstack1lll111l_opy_.bstack111llll1_opy_(driver_command) and (bstack1l111ll1_opy_ or bstack11l11l1111_opy_) and not bstack111ll11ll_opy_(args):
        try:
          bstack1111l1lll_opy_ = True
          logger.debug(bstack1l1l11l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧ⑕").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l1l11l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫ⑖").format(str(err)))
        bstack1111l1lll_opy_ = False
    if sequence == bstack1l1l11l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭⑗"):
        if driver_command == bstack1l1l11l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ⑘"):
            bstack1l1111ll1l_opy_.bstack11llll1lll_opy_({
                bstack1l1l11l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ⑙"): response[bstack1l1l11l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ⑚")],
                bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⑛"): store[bstack1l1l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ⑜")]
            })
def bstack1l1l1ll11_opy_():
    global bstack1111l11l1_opy_
    bstack11l1l11111_opy_.bstack1ll11lll_opy_()
    logging.shutdown()
    bstack1l1111ll1l_opy_.bstack1111lll1l1_opy_()
    for driver in bstack1111l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1l11ll1l_opy_(*args):
    global bstack1111l11l1_opy_
    bstack1l1111ll1l_opy_.bstack1111lll1l1_opy_()
    for driver in bstack1111l11l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11l1111l_opy_, stage=STAGE.bstack1l1111l11l_opy_, bstack1111l1l11_opy_=bstack1l1l1l1111_opy_)
def bstack1ll1ll111_opy_(self, *args, **kwargs):
    bstack1llll11l_opy_ = bstack111lll1l11_opy_(self, *args, **kwargs)
    bstack11ll11111l_opy_ = getattr(threading.current_thread(), bstack1l1l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧ⑝"), None)
    if bstack11ll11111l_opy_ and bstack11ll11111l_opy_.get(bstack1l1l11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⑞"), bstack1l1l11l_opy_ (u"ࠨࠩ⑟")) == bstack1l1l11l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ①"):
        bstack1l1111ll1l_opy_.bstack11l111l111_opy_(self)
    return bstack1llll11l_opy_
@measure(event_name=EVENTS.bstack1llll1ll11_opy_, stage=STAGE.bstack1ll1ll111l_opy_, bstack1111l1l11_opy_=bstack1l1l1l1111_opy_)
def bstack1lll11l11l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
    if bstack1ll1l111l1_opy_.get_property(bstack1l1l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧ②")):
        return
    bstack1ll1l111l1_opy_.bstack11ll11llll_opy_(bstack1l1l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨ③"), True)
    global bstack1l1lllll_opy_
    global bstack11l11lll1_opy_
    bstack1l1lllll_opy_ = framework_name
    logger.info(bstack1lll111111_opy_.format(bstack1l1lllll_opy_.split(bstack1l1l11l_opy_ (u"ࠬ࠳ࠧ④"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1l11lll11_opy_():
            Service.start = bstack1ll1111l11_opy_
            Service.stop = bstack11ll1l11l_opy_
            webdriver.Remote.get = bstack1l1ll1l1l1_opy_
            webdriver.Remote.__init__ = bstack11l1llll_opy_
            if not isinstance(os.getenv(bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧ⑤")), str):
                return
            WebDriver.quit = bstack1ll11llll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1l1111ll1l_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1ll111_opy_
        bstack11l11lll1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬ⑥")):
        bstack11l11lll1_opy_ = eval(os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭⑦")))
    if not bstack11l11lll1_opy_:
        bstack1llll11lll_opy_(bstack1l1l11l_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦ⑧"), bstack1l1lll11l_opy_)
    if bstack11l1l11l11_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            if hasattr(RemoteConnection, bstack1l1l11l_opy_ (u"ࠪࡣ࡬࡫ࡴࡠࡲࡵࡳࡽࡿ࡟ࡶࡴ࡯ࠫ⑨")) and callable(getattr(RemoteConnection, bstack1l1l11l_opy_ (u"ࠫࡤ࡭ࡥࡵࡡࡳࡶࡴࡾࡹࡠࡷࡵࡰࠬ⑩"))):
                RemoteConnection._get_proxy_url = bstack1l1ll11lll_opy_
            else:
                from selenium.webdriver.remote.client_config import ClientConfig
                ClientConfig.get_proxy_url = bstack1l1ll11lll_opy_
        except Exception as e:
            logger.error(bstack1lll111ll1_opy_.format(str(e)))
    if bstack1l1l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ⑪") in str(framework_name).lower():
        if not bstack1l1l11lll11_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11ll1111ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1lll1l1l_opy_
            Config.getoption = bstack1llllllll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l1lll1l1_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11lll1l11l_opy_, stage=STAGE.bstack1l1111l11l_opy_, bstack1111l1l11_opy_=bstack1l1l1l1111_opy_)
def bstack1ll11llll1_opy_(self):
    global bstack1l1lllll_opy_
    global bstack11llll111_opy_
    global bstack11lllll1ll_opy_
    try:
        if bstack1l1l11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭⑫") in bstack1l1lllll_opy_ and self.session_id != None and bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ⑬"), bstack1l1l11l_opy_ (u"ࠨࠩ⑭")) != bstack1l1l11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⑮"):
            bstack1ll1l1l111_opy_ = bstack1l1l11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⑯") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⑰")
            bstack1ll11l1l1_opy_(logger, True)
            if os.environ.get(bstack1l1l11l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨ⑱"), None):
                self.execute_script(
                    bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ⑲") + json.dumps(
                        os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⑳"))) + bstack1l1l11l_opy_ (u"ࠨࡿࢀࠫ⑴"))
            if self != None:
                bstack1ll1l1ll_opy_(self, bstack1ll1l1l111_opy_, bstack1l1l11l_opy_ (u"ࠩ࠯ࠤࠬ⑵").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1ll11llllll_opy_(bstack1lll111l1ll_opy_):
            item = store.get(bstack1l1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ⑶"), None)
            if item is not None and bstack111111l11_opy_(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⑷"), None):
                bstack11ll111111_opy_.bstack111l11111_opy_(self, bstack1lllllll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l1l11l_opy_ (u"ࠬ࠭⑸")
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢ⑹") + str(e))
    bstack11lllll1ll_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack11lll1l1ll_opy_, stage=STAGE.bstack1l1111l11l_opy_, bstack1111l1l11_opy_=bstack1l1l1l1111_opy_)
def bstack11l1llll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11llll111_opy_
    global bstack1l1l1l1111_opy_
    global bstack11l1l1l11_opy_
    global bstack1l1lllll_opy_
    global bstack111lll1l11_opy_
    global bstack1111l11l1_opy_
    global bstack11ll11l11_opy_
    global bstack1ll111ll1_opy_
    global bstack1lllllll1_opy_
    CONFIG[bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ⑺")] = str(bstack1l1lllll_opy_) + str(__version__)
    command_executor = bstack11l11ll11l_opy_(bstack11ll11l11_opy_, CONFIG)
    logger.debug(bstack111ll111_opy_.format(command_executor))
    proxy = bstack11llll1ll_opy_(CONFIG, proxy)
    bstack1ll1l1111l_opy_ = 0
    try:
        if bstack11l1l1l11_opy_ is True:
            bstack1ll1l1111l_opy_ = int(os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ⑻")))
    except:
        bstack1ll1l1111l_opy_ = 0
    bstack1l111l1l1_opy_ = bstack1ll111l1ll_opy_(CONFIG, bstack1ll1l1111l_opy_)
    logger.debug(bstack11l1llll11_opy_.format(str(bstack1l111l1l1_opy_)))
    bstack1lllllll1_opy_ = CONFIG.get(bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⑼"))[bstack1ll1l1111l_opy_]
    if bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ⑽") in CONFIG and CONFIG[bstack1l1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ⑾")]:
        bstack11l1l1llll_opy_(bstack1l111l1l1_opy_, bstack1ll111ll1_opy_)
    if bstack11ll1lllll_opy_.bstack1ll1lll1l_opy_(CONFIG, bstack1ll1l1111l_opy_) and bstack11ll1lllll_opy_.bstack11ll1l11ll_opy_(bstack1l111l1l1_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1ll11llllll_opy_(bstack1lll111l1ll_opy_):
            bstack11ll1lllll_opy_.set_capabilities(bstack1l111l1l1_opy_, CONFIG)
    if desired_capabilities:
        bstack11ll11ll_opy_ = bstack1l11l1l11l_opy_(desired_capabilities)
        bstack11ll11ll_opy_[bstack1l1l11l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ⑿")] = bstack1ll11ll11l_opy_(CONFIG)
        bstack11l1l1l1l1_opy_ = bstack1ll111l1ll_opy_(bstack11ll11ll_opy_)
        if bstack11l1l1l1l1_opy_:
            bstack1l111l1l1_opy_ = update(bstack11l1l1l1l1_opy_, bstack1l111l1l1_opy_)
        desired_capabilities = None
    if options:
        bstack1111ll1ll_opy_(options, bstack1l111l1l1_opy_)
    if not options:
        options = bstack11l1l11l_opy_(bstack1l111l1l1_opy_)
    if proxy and bstack1l1l1111_opy_() >= version.parse(bstack1l1l11l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭⒀")):
        options.proxy(proxy)
    if options and bstack1l1l1111_opy_() >= version.parse(bstack1l1l11l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭⒁")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1l1111_opy_() < version.parse(bstack1l1l11l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ⒂")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l111l1l1_opy_)
    logger.info(bstack1l11111l1_opy_)
    bstack1llll11111_opy_.end(EVENTS.bstack1llll1ll11_opy_.value, EVENTS.bstack1llll1ll11_opy_.value + bstack1l1l11l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ⒃"),
                               EVENTS.bstack1llll1ll11_opy_.value + bstack1l1l11l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ⒄"), True, None)
    try:
        if bstack1l1l1111_opy_() >= version.parse(bstack1l1l11l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫ⒅")):
            bstack111lll1l11_opy_(self, command_executor=command_executor,
                      options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
        elif bstack1l1l1111_opy_() >= version.parse(bstack1l1l11l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ⒆")):
            bstack111lll1l11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities, options=options,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        elif bstack1l1l1111_opy_() >= version.parse(bstack1l1l11l_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭⒇")):
            bstack111lll1l11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive, file_detector=file_detector)
        else:
            bstack111lll1l11_opy_(self, command_executor=command_executor,
                      desired_capabilities=desired_capabilities,
                      browser_profile=browser_profile, proxy=proxy,
                      keep_alive=keep_alive)
    except Exception as bstack1lll11111l_opy_:
        logger.error(bstack1l1l111l11_opy_.format(bstack1l1l11l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰ࠭⒈"), str(bstack1lll11111l_opy_)))
        raise bstack1lll11111l_opy_
    try:
        bstack111llll1l_opy_ = bstack1l1l11l_opy_ (u"ࠨࠩ⒉")
        if bstack1l1l1111_opy_() >= version.parse(bstack1l1l11l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪ⒊")):
            bstack111llll1l_opy_ = self.caps.get(bstack1l1l11l_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥ⒋"))
        else:
            bstack111llll1l_opy_ = self.capabilities.get(bstack1l1l11l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ⒌"))
        if bstack111llll1l_opy_:
            bstack1ll1ll1l1l_opy_(bstack111llll1l_opy_)
            if bstack1l1l1111_opy_() <= version.parse(bstack1l1l11l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ⒍")):
                self.command_executor._url = bstack1l1l11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ⒎") + bstack11ll11l11_opy_ + bstack1l1l11l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ⒏")
            else:
                self.command_executor._url = bstack1l1l11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ⒐") + bstack111llll1l_opy_ + bstack1l1l11l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ⒑")
            logger.debug(bstack11ll1ll1l_opy_.format(bstack111llll1l_opy_))
        else:
            logger.debug(bstack111l11ll_opy_.format(bstack1l1l11l_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦ⒒")))
    except Exception as e:
        logger.debug(bstack111l11ll_opy_.format(e))
    bstack11llll111_opy_ = self.session_id
    if bstack1l1l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ⒓") in bstack1l1lllll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l1l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ⒔"), None)
        if item:
            bstack1lll1l11l111_opy_ = getattr(item, bstack1l1l11l_opy_ (u"࠭࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࡢࡷࡹࡧࡲࡵࡧࡧࠫ⒕"), False)
            if not getattr(item, bstack1l1l11l_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⒖"), None) and bstack1lll1l11l111_opy_:
                setattr(store[bstack1l1l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⒗")], bstack1l1l11l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⒘"), self)
        bstack11ll11111l_opy_ = getattr(threading.current_thread(), bstack1l1l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ⒙"), None)
        if bstack11ll11111l_opy_ and bstack11ll11111l_opy_.get(bstack1l1l11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⒚"), bstack1l1l11l_opy_ (u"ࠬ࠭⒛")) == bstack1l1l11l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ⒜"):
            bstack1l1111ll1l_opy_.bstack11l111l111_opy_(self)
    bstack1111l11l1_opy_.append(self)
    if bstack1l1l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ⒝") in CONFIG and bstack1l1l11l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭⒞") in CONFIG[bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⒟")][bstack1ll1l1111l_opy_]:
        bstack1l1l1l1111_opy_ = CONFIG[bstack1l1l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⒠")][bstack1ll1l1111l_opy_][bstack1l1l11l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⒡")]
    logger.debug(bstack1l1ll1ll11_opy_.format(bstack11llll111_opy_))
@measure(event_name=EVENTS.bstack1lll1l11_opy_, stage=STAGE.bstack1l1111l11l_opy_, bstack1111l1l11_opy_=bstack1l1l1l1111_opy_)
def bstack1l1ll1l1l1_opy_(self, url):
    global bstack11ll1lll1l_opy_
    global CONFIG
    try:
        bstack11llllllll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11l11lll11_opy_.format(str(err)))
    try:
        bstack11ll1lll1l_opy_(self, url)
    except Exception as e:
        try:
            bstack11ll111ll_opy_ = str(e)
            if any(err_msg in bstack11ll111ll_opy_ for err_msg in bstack1l1l1l111_opy_):
                bstack11llllllll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11l11lll11_opy_.format(str(err)))
        raise e
def bstack1ll11l11l_opy_(item, when):
    global bstack11ll1l1l1_opy_
    try:
        bstack11ll1l1l1_opy_(item, when)
    except Exception as e:
        pass
def bstack11l1lll1l1_opy_(item, call, rep):
    global bstack1llll1l1l_opy_
    global bstack1111l11l1_opy_
    name = bstack1l1l11l_opy_ (u"ࠬ࠭⒢")
    try:
        if rep.when == bstack1l1l11l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⒣"):
            bstack11llll111_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack1l1l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⒤"))
            try:
                if (str(skipSessionName).lower() != bstack1l1l11l_opy_ (u"ࠨࡶࡵࡹࡪ࠭⒥")):
                    name = str(rep.nodeid)
                    bstack1l1l1ll1_opy_ = bstack1l1ll111_opy_(bstack1l1l11l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⒦"), name, bstack1l1l11l_opy_ (u"ࠪࠫ⒧"), bstack1l1l11l_opy_ (u"ࠫࠬ⒨"), bstack1l1l11l_opy_ (u"ࠬ࠭⒩"), bstack1l1l11l_opy_ (u"࠭ࠧ⒪"))
                    os.environ[bstack1l1l11l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⒫")] = name
                    for driver in bstack1111l11l1_opy_:
                        if bstack11llll111_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l1ll1_opy_)
            except Exception as e:
                logger.debug(bstack1l1l11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ⒬").format(str(e)))
            try:
                bstack111lll1ll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1l11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⒭"):
                    status = bstack1l1l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⒮") if rep.outcome.lower() == bstack1l1l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⒯") else bstack1l1l11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⒰")
                    reason = bstack1l1l11l_opy_ (u"࠭ࠧ⒱")
                    if status == bstack1l1l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⒲"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1l11l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭⒳") if status == bstack1l1l11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⒴") else bstack1l1l11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⒵")
                    data = name + bstack1l1l11l_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭Ⓐ") if status == bstack1l1l11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬⒷ") else name + bstack1l1l11l_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩⒸ") + reason
                    bstack1l11llllll_opy_ = bstack1l1ll111_opy_(bstack1l1l11l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩⒹ"), bstack1l1l11l_opy_ (u"ࠨࠩⒺ"), bstack1l1l11l_opy_ (u"ࠩࠪⒻ"), bstack1l1l11l_opy_ (u"ࠪࠫⒼ"), level, data)
                    for driver in bstack1111l11l1_opy_:
                        if bstack11llll111_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11llllll_opy_)
            except Exception as e:
                logger.debug(bstack1l1l11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨⒽ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩⒾ").format(str(e)))
    bstack1llll1l1l_opy_(item, call, rep)
notset = Notset()
def bstack1llllllll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11lll1111_opy_
    if str(name).lower() == bstack1l1l11l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭Ⓙ"):
        return bstack1l1l11l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨⓀ")
    else:
        return bstack11lll1111_opy_(self, name, default, skip)
def bstack1l1ll11lll_opy_(self):
    global CONFIG
    global bstack1l1lll1l1_opy_
    try:
        proxy = bstack1l1l11l11l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1l11l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭Ⓛ")):
                proxies = bstack111ll1ll_opy_(proxy, bstack11l11ll11l_opy_())
                if len(proxies) > 0:
                    protocol, bstack11111111l_opy_ = proxies.popitem()
                    if bstack1l1l11l_opy_ (u"ࠤ࠽࠳࠴ࠨⓂ") in bstack11111111l_opy_:
                        return bstack11111111l_opy_
                    else:
                        return bstack1l1l11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦⓃ") + bstack11111111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1l11l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣⓄ").format(str(e)))
    return bstack1l1lll1l1_opy_(self)
def bstack11l1l11l11_opy_():
    return (bstack1l1l11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨⓅ") in CONFIG or bstack1l1l11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪⓆ") in CONFIG) and bstack1ll1ll1l_opy_() and bstack1l1l1111_opy_() >= version.parse(
        bstack11111lll1_opy_)
def bstack1l111llll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1l1l1111_opy_
    global bstack11l1l1l11_opy_
    global bstack1l1lllll_opy_
    CONFIG[bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩⓇ")] = str(bstack1l1lllll_opy_) + str(__version__)
    bstack1ll1l1111l_opy_ = 0
    try:
        if bstack11l1l1l11_opy_ is True:
            bstack1ll1l1111l_opy_ = int(os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨⓈ")))
    except:
        bstack1ll1l1111l_opy_ = 0
    CONFIG[bstack1l1l11l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣⓉ")] = True
    bstack1l111l1l1_opy_ = bstack1ll111l1ll_opy_(CONFIG, bstack1ll1l1111l_opy_)
    logger.debug(bstack11l1llll11_opy_.format(str(bstack1l111l1l1_opy_)))
    if CONFIG.get(bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧⓊ")):
        bstack11l1l1llll_opy_(bstack1l111l1l1_opy_, bstack1ll111ll1_opy_)
    if bstack1l1l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧⓋ") in CONFIG and bstack1l1l11l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪⓌ") in CONFIG[bstack1l1l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩⓍ")][bstack1ll1l1111l_opy_]:
        bstack1l1l1l1111_opy_ = CONFIG[bstack1l1l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⓎ")][bstack1ll1l1111l_opy_][bstack1l1l11l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ⓩ")]
    import urllib
    import json
    if bstack1l1l11l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ⓐ") in CONFIG and str(CONFIG[bstack1l1l11l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧⓑ")]).lower() != bstack1l1l11l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪⓒ"):
        bstack1l1lllll11_opy_ = bstack111lll1l1l_opy_()
        bstack11111ll1_opy_ = bstack1l1lllll11_opy_ + urllib.parse.quote(json.dumps(bstack1l111l1l1_opy_))
    else:
        bstack11111ll1_opy_ = bstack1l1l11l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧⓓ") + urllib.parse.quote(json.dumps(bstack1l111l1l1_opy_))
    browser = self.connect(bstack11111ll1_opy_)
    return browser
def bstack11l11l1ll_opy_():
    global bstack11l11lll1_opy_
    global bstack1l1lllll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11l1l1lll_opy_
        if not bstack1l1l11lll11_opy_():
            global bstack11l11111_opy_
            if not bstack11l11111_opy_:
                from bstack_utils.helper import bstack1l1l111ll_opy_, bstack1l11l1l11_opy_
                bstack11l11111_opy_ = bstack1l1l111ll_opy_()
                bstack1l11l1l11_opy_(bstack1l1lllll_opy_)
            BrowserType.connect = bstack11l1l1lll_opy_
            return
        BrowserType.launch = bstack1l111llll_opy_
        bstack11l11lll1_opy_ = True
    except Exception as e:
        pass
def bstack1lll1ll11l1l_opy_():
    global CONFIG
    global bstack1ll1l11ll_opy_
    global bstack11ll11l11_opy_
    global bstack1ll111ll1_opy_
    global bstack11l1l1l11_opy_
    global bstack1l11ll11l_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬⓔ")))
    bstack1ll1l11ll_opy_ = eval(os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨⓕ")))
    bstack11ll11l11_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨⓖ"))
    bstack1lll111l1_opy_(CONFIG, bstack1ll1l11ll_opy_)
    bstack1l11ll11l_opy_ = bstack11l1l11111_opy_.configure_logger(CONFIG, bstack1l11ll11l_opy_)
    if cli.bstack1ll1l11111_opy_():
        bstack111l1l111_opy_.invoke(bstack11l11l1l_opy_.CONNECT, bstack1ll1llll1l_opy_())
        cli_context.platform_index = int(os.environ.get(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩⓗ"), bstack1l1l11l_opy_ (u"ࠪ࠴ࠬⓘ")))
        cli.bstack1ll1ll1ll1l_opy_(cli_context.platform_index)
        cli.bstack1ll1ll1l1ll_opy_(bstack11l11ll11l_opy_(bstack11ll11l11_opy_, CONFIG), cli_context.platform_index, bstack11l1l11l_opy_)
        cli.bstack1ll1lllll1l_opy_()
        logger.debug(bstack1l1l11l_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥⓙ") + str(cli_context.platform_index) + bstack1l1l11l_opy_ (u"ࠧࠨⓚ"))
        return # skip all existing operations
    global bstack111lll1l11_opy_
    global bstack11lllll1ll_opy_
    global bstack11lll111l_opy_
    global bstack11l1l11lll_opy_
    global bstack1llll11ll1_opy_
    global bstack11l1lll1l_opy_
    global bstack1111111ll_opy_
    global bstack11ll1lll1l_opy_
    global bstack1l1lll1l1_opy_
    global bstack11lll1111_opy_
    global bstack11ll1l1l1_opy_
    global bstack1llll1l1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack111lll1l11_opy_ = webdriver.Remote.__init__
        bstack11lllll1ll_opy_ = WebDriver.quit
        bstack1111111ll_opy_ = WebDriver.close
        bstack11ll1lll1l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1l11l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩⓛ") in CONFIG or bstack1l1l11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫⓜ") in CONFIG) and bstack1ll1ll1l_opy_():
        if bstack1l1l1111_opy_() < version.parse(bstack11111lll1_opy_):
            logger.error(bstack1ll1111l_opy_.format(bstack1l1l1111_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                if hasattr(RemoteConnection, bstack1l1l11l_opy_ (u"ࠨࡡࡪࡩࡹࡥࡰࡳࡱࡻࡽࡤࡻࡲ࡭ࠩⓝ")) and callable(getattr(RemoteConnection, bstack1l1l11l_opy_ (u"ࠩࡢ࡫ࡪࡺ࡟ࡱࡴࡲࡼࡾࡥࡵࡳ࡮ࠪⓞ"))):
                    bstack1l1lll1l1_opy_ = RemoteConnection._get_proxy_url
                else:
                    from selenium.webdriver.remote.client_config import ClientConfig
                    bstack1l1lll1l1_opy_ = ClientConfig.get_proxy_url
            except Exception as e:
                logger.error(bstack1lll111ll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11lll1111_opy_ = Config.getoption
        from _pytest import runner
        bstack11ll1l1l1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11l11ll1ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1llll1l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫⓟ"))
    bstack1ll111ll1_opy_ = CONFIG.get(bstack1l1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨⓠ"), {}).get(bstack1l1l11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧⓡ"))
    bstack11l1l1l11_opy_ = True
    bstack1lll11l11l_opy_(bstack1lll1ll111_opy_)
if (bstack111ll1l1111_opy_()):
    bstack1lll1ll11l1l_opy_()
@error_handler(class_method=False)
def bstack1lll1l11llll_opy_(hook_name, event, bstack11lllllll11_opy_=None):
    if hook_name not in [bstack1l1l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧⓢ"), bstack1l1l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫⓣ"), bstack1l1l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧⓤ"), bstack1l1l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫⓥ"), bstack1l1l11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨⓦ"), bstack1l1l11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬⓧ"), bstack1l1l11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫⓨ"), bstack1l1l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨⓩ")]:
        return
    node = store[bstack1l1l11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ⓪")]
    if hook_name in [bstack1l1l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧ⓫"), bstack1l1l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫ⓬")]:
        node = store[bstack1l1l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩ⓭")]
    elif hook_name in [bstack1l1l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩ⓮"), bstack1l1l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭⓯")]:
        node = store[bstack1l1l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫ⓰")]
    hook_type = bstack1lllll1111ll_opy_(hook_name)
    if event == bstack1l1l11l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ⓱"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_[hook_type], bstack1ll1lll111l_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111l111l1l_opy_ = {
            bstack1l1l11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭⓲"): uuid,
            bstack1l1l11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⓳"): bstack11l1lllll_opy_(),
            bstack1l1l11l_opy_ (u"ࠪࡸࡾࡶࡥࠨ⓴"): bstack1l1l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ⓵"),
            bstack1l1l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ⓶"): hook_type,
            bstack1l1l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ⓷"): hook_name
        }
        store[bstack1l1l11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ⓸")].append(uuid)
        bstack1lll1ll11111_opy_ = node.nodeid
        if hook_type == bstack1l1l11l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭⓹"):
            if not _111l1111l1_opy_.get(bstack1lll1ll11111_opy_, None):
                _111l1111l1_opy_[bstack1lll1ll11111_opy_] = {bstack1l1l11l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ⓺"): []}
            _111l1111l1_opy_[bstack1lll1ll11111_opy_][bstack1l1l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ⓻")].append(bstack111l111l1l_opy_[bstack1l1l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⓼")])
        _111l1111l1_opy_[bstack1lll1ll11111_opy_ + bstack1l1l11l_opy_ (u"ࠬ࠳ࠧ⓽") + hook_name] = bstack111l111l1l_opy_
        bstack1lll1ll11l11_opy_(node, bstack111l111l1l_opy_, bstack1l1l11l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⓾"))
    elif event == bstack1l1l11l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭⓿"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll1lll1ll_opy_[hook_type], bstack1ll1lll111l_opy_.POST, node, None, bstack11lllllll11_opy_)
            return
        bstack111ll1llll_opy_ = node.nodeid + bstack1l1l11l_opy_ (u"ࠨ࠯ࠪ─") + hook_name
        _111l1111l1_opy_[bstack111ll1llll_opy_][bstack1l1l11l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ━")] = bstack11l1lllll_opy_()
        bstack1lll1ll111ll_opy_(_111l1111l1_opy_[bstack111ll1llll_opy_][bstack1l1l11l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ│")])
        bstack1lll1ll11l11_opy_(node, _111l1111l1_opy_[bstack111ll1llll_opy_], bstack1l1l11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭┃"), bstack1lll1l1lll1l_opy_=bstack11lllllll11_opy_)
def bstack1lll1ll111l1_opy_():
    global bstack1lll1l1l1lll_opy_
    if bstack1ll111l11l_opy_():
        bstack1lll1l1l1lll_opy_ = bstack1l1l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩ┄")
    else:
        bstack1lll1l1l1lll_opy_ = bstack1l1l11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭┅")
@bstack1l1111ll1l_opy_.bstack1llll1111l1l_opy_
def bstack1lll1l1l1l1l_opy_():
    bstack1lll1ll111l1_opy_()
    if cli.is_running():
        try:
            bstack111l11l111l_opy_(bstack1lll1l11llll_opy_)
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣ┆").format(e))
        return
    if bstack1ll1ll1l_opy_():
        bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
        bstack1l1l11l_opy_ (u"ࠨࠩࠪࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡉࡳࡷࠦࡰࡱࡲࠣࡁࠥ࠷ࠬࠡ࡯ࡲࡨࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡧࡦࡶࡶࠤࡺࡹࡥࡥࠢࡩࡳࡷࠦࡡ࠲࠳ࡼࠤࡨࡵ࡭࡮ࡣࡱࡨࡸ࠳ࡷࡳࡣࡳࡴ࡮ࡴࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡴࡵࡶࠠ࠿ࠢ࠴࠰ࠥࡳ࡯ࡥࡡࡨࡼࡪࡩࡵࡵࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡥࡩࡨࡧࡵࡴࡧࠣ࡭ࡹࠦࡩࡴࠢࡳࡥࡹࡩࡨࡦࡦࠣ࡭ࡳࠦࡡࠡࡦ࡬ࡪ࡫࡫ࡲࡦࡰࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࠥ࡯ࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡔࡩࡷࡶࠤࡼ࡫ࠠ࡯ࡧࡨࡨࠥࡺ࡯ࠡࡷࡶࡩ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳࡐࡢࡶࡦ࡬࠭ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡩࡣࡱࡨࡱ࡫ࡲࠪࠢࡩࡳࡷࠦࡰࡱࡲࠣࡂࠥ࠷ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠩࠪࠫ┇")
        if bstack1ll1l111l1_opy_.get_property(bstack1l1l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭┈")):
            if CONFIG.get(bstack1l1l11l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ┉")) is not None and int(CONFIG[bstack1l1l11l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ┊")]) > 1:
                bstack111lll1lll_opy_(bstack111llll11_opy_)
            return
        bstack111lll1lll_opy_(bstack111llll11_opy_)
    try:
        bstack111l11l111l_opy_(bstack1lll1l11llll_opy_)
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ┋").format(e))
bstack1lll1l1l1l1l_opy_()
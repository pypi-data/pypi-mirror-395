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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack11l1l11111_opy_ import get_logger
logger = get_logger(__name__)
bstack1lllll1l11l1_opy_: Dict[str, float] = {}
bstack1lllll1l1lll_opy_: List = []
bstack1lllll1l1111_opy_ = 5
bstack1lll1111l_opy_ = os.path.join(os.getcwd(), bstack1l1l11l_opy_ (u"ࠨ࡮ࡲ࡫ࠬ‷"), bstack1l1l11l_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬ‸"))
logging.getLogger(bstack1l1l11l_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠬ‹")).setLevel(logging.WARNING)
lock = FileLock(bstack1lll1111l_opy_+bstack1l1l11l_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥ›"))
class bstack1lllll1ll111_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack1lllll1l1l1l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack1lllll1l1l1l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1l11l_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࠨ※")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1ll111l_opy_:
    global bstack1lllll1l11l1_opy_
    @staticmethod
    def bstack1l1llll111l_opy_(key: str):
        bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_.bstack11l1lll11ll_opy_(key)
        bstack1lll1ll111l_opy_.mark(bstack1ll11l1lll1_opy_+bstack1l1l11l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ‼"))
        return bstack1ll11l1lll1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack1lllll1l11l1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥ‽").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1ll111l_opy_.mark(end)
            bstack1lll1ll111l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧ‾").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack1lllll1l11l1_opy_ or end not in bstack1lllll1l11l1_opy_:
                logger.debug(bstack1l1l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠠࡰࡴࠣࡩࡳࡪࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠦ‿").format(start,end))
                return
            duration: float = bstack1lllll1l11l1_opy_[end] - bstack1lllll1l11l1_opy_[start]
            bstack1lllll1l1l11_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨ⁀"), bstack1l1l11l_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ⁁")).lower() == bstack1l1l11l_opy_ (u"ࠧࡺࡲࡶࡧࠥ⁂")
            bstack1lllll1l11ll_opy_: bstack1lllll1ll111_opy_ = bstack1lllll1ll111_opy_(duration, label, bstack1lllll1l11l1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l1l11l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨ⁃"), 0), command, test_name, hook_type, bstack1lllll1l1l11_opy_)
            del bstack1lllll1l11l1_opy_[start]
            del bstack1lllll1l11l1_opy_[end]
            bstack1lll1ll111l_opy_.bstack1lllll1l1ll1_opy_(bstack1lllll1l11ll_opy_)
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡥࡢࡵࡸࡶ࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥ⁄").format(e))
    @staticmethod
    def bstack1lllll1l1ll1_opy_(bstack1lllll1l11ll_opy_):
        os.makedirs(os.path.dirname(bstack1lll1111l_opy_)) if not os.path.exists(os.path.dirname(bstack1lll1111l_opy_)) else None
        bstack1lll1ll111l_opy_.bstack1lllll1l111l_opy_()
        try:
            with lock:
                with open(bstack1lll1111l_opy_, bstack1l1l11l_opy_ (u"ࠣࡴ࠮ࠦ⁅"), encoding=bstack1l1l11l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ⁆")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack1lllll1l11ll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack1lllll1ll11l_opy_:
            logger.debug(bstack1l1l11l_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠤࢀࢃࠢ⁇").format(bstack1lllll1ll11l_opy_))
            with lock:
                with open(bstack1lll1111l_opy_, bstack1l1l11l_opy_ (u"ࠦࡼࠨ⁈"), encoding=bstack1l1l11l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ⁉")) as file:
                    data = [bstack1lllll1l11ll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡡࡱࡲࡨࡲࡩࠦࡻࡾࠤ⁊").format(str(e)))
        finally:
            if os.path.exists(bstack1lll1111l_opy_+bstack1l1l11l_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ⁋")):
                os.remove(bstack1lll1111l_opy_+bstack1l1l11l_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ⁌"))
    @staticmethod
    def bstack1lllll1l111l_opy_():
        attempt = 0
        while (attempt < bstack1lllll1l1111_opy_):
            attempt += 1
            if os.path.exists(bstack1lll1111l_opy_+bstack1l1l11l_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ⁍")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11l1lll11ll_opy_(label: str) -> str:
        try:
            return bstack1l1l11l_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤ⁎").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ⁏").format(e))
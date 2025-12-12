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
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
from unittest import result
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1111111l_opy_, bstack1l111111l1_opy_, bstack11lll1ll1l_opy_,
                                    bstack11l1l11l1ll_opy_, bstack11l1l1111ll_opy_, bstack11l11llll1l_opy_, bstack11l11ll11ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11ll11l11l_opy_, bstack1lll111ll1_opy_
from bstack_utils.proxy import bstack11l111ll11_opy_, bstack1l1l11l11l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack11l1l11111_opy_
from bstack_utils.bstack1l1llll11_opy_ import bstack1l1ll1l11l_opy_
from browserstack_sdk._version import __version__
bstack1ll1l111l1_opy_ = Config.bstack11l111l11l_opy_()
logger = bstack11l1l11111_opy_.get_logger(__name__, bstack11l1l11111_opy_.bstack1lll11l1l1l_opy_())
def bstack11l1lll1ll1_opy_(config):
    return config[bstack1l1l11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᯥ")]
def bstack11ll11111l1_opy_(config):
    return config[bstack1l1l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽ᯦ࠬ")]
def bstack1ll111l111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111ll11lll1_opy_(obj):
    values = []
    bstack111lll1l11l_opy_ = re.compile(bstack1l1l11l_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢᯧ"), re.I)
    for key in obj.keys():
        if bstack111lll1l11l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1l11111_opy_(config):
    tags = []
    tags.extend(bstack111ll11lll1_opy_(os.environ))
    tags.extend(bstack111ll11lll1_opy_(config))
    return tags
def bstack111ll1111ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111ll1l11ll_opy_(bstack111ll11l11l_opy_):
    if not bstack111ll11l11l_opy_:
        return bstack1l1l11l_opy_ (u"ࠫࠬᯨ")
    return bstack1l1l11l_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨᯩ").format(bstack111ll11l11l_opy_.name, bstack111ll11l11l_opy_.email)
def bstack11ll111l1l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111lll1ll1l_opy_ = repo.common_dir
        info = {
            bstack1l1l11l_opy_ (u"ࠨࡳࡩࡣࠥᯪ"): repo.head.commit.hexsha,
            bstack1l1l11l_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥᯫ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1l11l_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣᯬ"): repo.active_branch.name,
            bstack1l1l11l_opy_ (u"ࠤࡷࡥ࡬ࠨᯭ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᯮ"): bstack111ll1l11ll_opy_(repo.head.commit.committer),
            bstack1l1l11l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᯯ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1l11l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᯰ"): bstack111ll1l11ll_opy_(repo.head.commit.author),
            bstack1l1l11l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᯱ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1l11l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥ᯲ࠣ"): repo.head.commit.message,
            bstack1l1l11l_opy_ (u"ࠣࡴࡲࡳࡹࠨ᯳"): repo.git.rev_parse(bstack1l1l11l_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦ᯴")),
            bstack1l1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦ᯵"): bstack111lll1ll1l_opy_,
            bstack1l1l11l_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢ᯶"): subprocess.check_output([bstack1l1l11l_opy_ (u"ࠧ࡭ࡩࡵࠤ᯷"), bstack1l1l11l_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤ᯸"), bstack1l1l11l_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥ᯹")]).strip().decode(
                bstack1l1l11l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᯺")),
            bstack1l1l11l_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦ᯻"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ᯼"): repo.git.rev_list(
                bstack1l1l11l_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦ᯽").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111ll1ll111_opy_ = []
        for remote in remotes:
            bstack111l1ll1ll1_opy_ = {
                bstack1l1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᯾"): remote.name,
                bstack1l1l11l_opy_ (u"ࠨࡵࡳ࡮ࠥ᯿"): remote.url,
            }
            bstack111ll1ll111_opy_.append(bstack111l1ll1ll1_opy_)
        bstack11l111111l1_opy_ = {
            bstack1l1l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᰀ"): bstack1l1l11l_opy_ (u"ࠣࡩ࡬ࡸࠧᰁ"),
            **info,
            bstack1l1l11l_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᰂ"): bstack111ll1ll111_opy_
        }
        bstack11l111111l1_opy_ = bstack111l1lll1ll_opy_(bstack11l111111l1_opy_)
        return bstack11l111111l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1l11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᰃ").format(err))
        return {}
def bstack111llll1lll_opy_(bstack111ll1lllll_opy_=None):
    bstack1l1l11l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡴࡲࡨࡧ࡮࡬ࡩࡤࡣ࡯ࡰࡾࠦࡦࡰࡴࡰࡥࡹࡺࡥࡥࠢࡩࡳࡷࠦࡁࡊࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡻࡳࡦࠢࡦࡥࡸ࡫ࡳࠡࡨࡲࡶࠥ࡫ࡡࡤࡪࠣࡪࡴࡲࡤࡦࡴࠣ࡭ࡳࠦࡴࡩࡧࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡦࡰ࡮ࡧࡩࡷࡹࠠࠩ࡮࡬ࡷࡹ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡔ࡯࡯ࡧ࠽ࠤࡒࡵ࡮ࡰ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩ࠮ࠣࡹࡸ࡫ࡳࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡡ࡯ࡴ࠰ࡪࡩࡹࡩࡷࡥࠪࠬࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡋ࡭ࡱࡶࡼࠤࡱ࡯ࡳࡵࠢ࡞ࡡ࠿ࠦࡍࡶ࡮ࡷ࡭࠲ࡸࡥࡱࡱࠣࡥࡵࡶࡲࡰࡣࡦ࡬ࠥࡽࡩࡵࡪࠣࡲࡴࠦࡳࡰࡷࡵࡧࡪࡹࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡧࡧ࠰ࠥࡸࡥࡵࡷࡵࡲࡸ࡛ࠦ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡴࡦࡺࡨࡴ࠼ࠣࡑࡺࡲࡴࡪ࠯ࡵࡩࡵࡵࠠࡢࡲࡳࡶࡴࡧࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡴࡲࡨࡧ࡮࡬ࡩࡤࠢࡩࡳࡱࡪࡥࡳࡵࠣࡸࡴࠦࡡ࡯ࡣ࡯ࡽࡿ࡫ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠ࡭࡫ࡶࡸ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡥ࡫ࡦࡸࡸ࠲ࠠࡦࡣࡦ࡬ࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡨࡲࡶࠥࡧࠠࡧࡱ࡯ࡨࡪࡸ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᰄ")
    if bstack111ll1lllll_opy_ is None:
        bstack111ll1lllll_opy_ = [os.getcwd()]
    elif isinstance(bstack111ll1lllll_opy_, list) and len(bstack111ll1lllll_opy_) == 0:
        return []
    results = []
    for folder in bstack111ll1lllll_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1l1l11l_opy_ (u"ࠧࡌ࡯࡭ࡦࡨࡶࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠥᰅ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l1l11l_opy_ (u"ࠨࡰࡳࡋࡧࠦᰆ"): bstack1l1l11l_opy_ (u"ࠢࠣᰇ"),
                bstack1l1l11l_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᰈ"): [],
                bstack1l1l11l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᰉ"): [],
                bstack1l1l11l_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥᰊ"): bstack1l1l11l_opy_ (u"ࠦࠧᰋ"),
                bstack1l1l11l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨᰌ"): [],
                bstack1l1l11l_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢᰍ"): bstack1l1l11l_opy_ (u"ࠢࠣᰎ"),
                bstack1l1l11l_opy_ (u"ࠣࡲࡵࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠣᰏ"): bstack1l1l11l_opy_ (u"ࠤࠥᰐ"),
                bstack1l1l11l_opy_ (u"ࠥࡴࡷࡘࡡࡸࡆ࡬ࡪ࡫ࠨᰑ"): bstack1l1l11l_opy_ (u"ࠦࠧᰒ")
            }
            bstack111lllll1l1_opy_ = repo.active_branch.name
            bstack111ll11llll_opy_ = repo.head.commit
            result[bstack1l1l11l_opy_ (u"ࠧࡶࡲࡊࡦࠥᰓ")] = bstack111ll11llll_opy_.hexsha
            bstack111llll111l_opy_ = _111lll1111l_opy_(repo)
            logger.debug(bstack1l1l11l_opy_ (u"ࠨࡂࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡫ࡵࡲࠡࡥࡲࡱࡵࡧࡲࡪࡵࡲࡲ࠿ࠦࠢᰔ") + str(bstack111llll111l_opy_) + bstack1l1l11l_opy_ (u"ࠢࠣᰕ"))
            if bstack111llll111l_opy_:
                try:
                    bstack111lll1ll11_opy_ = repo.git.diff(bstack1l1l11l_opy_ (u"ࠣ࠯࠰ࡲࡦࡳࡥ࠮ࡱࡱࡰࡾࠨᰖ"), bstack1lll1l111l1_opy_ (u"ࠤࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾ࠰࠱࠲ࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃࠢᰗ")).split(bstack1l1l11l_opy_ (u"ࠪࡠࡳ࠭ᰘ"))
                    logger.debug(bstack1l1l11l_opy_ (u"ࠦࡈ࡮ࡡ࡯ࡩࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤࡧ࡫ࡴࡸࡧࡨࡲࠥࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠥࡧ࡮ࡥࠢࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠿ࠦࠢᰙ") + str(bstack111lll1ll11_opy_) + bstack1l1l11l_opy_ (u"ࠧࠨᰚ"))
                    result[bstack1l1l11l_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᰛ")] = [f.strip() for f in bstack111lll1ll11_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1lll1l111l1_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯ࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀࠦᰜ")))
                except Exception:
                    logger.debug(bstack1l1l11l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡬࡫ࡴࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡨࡵࡳࡲࠦࡢࡳࡣࡱࡧ࡭ࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠱ࠤࡋࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦࡲࡦࡥࡨࡲࡹࠦࡣࡰ࡯ࡰ࡭ࡹࡹ࠮ࠣᰝ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l1l11l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᰞ")] = _111ll1lll1l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l1l11l_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᰟ")] = _111ll1lll1l_opy_(commits[:5])
            bstack111llll1l11_opy_ = set()
            bstack111ll111l11_opy_ = []
            for commit in commits:
                logger.debug(bstack1l1l11l_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡥࡲࡱࡲ࡯ࡴ࠻ࠢࠥᰠ") + str(commit.message) + bstack1l1l11l_opy_ (u"ࠧࠨᰡ"))
                bstack111lll1l111_opy_ = commit.author.name if commit.author else bstack1l1l11l_opy_ (u"ࠨࡕ࡯࡭ࡱࡳࡼࡴࠢᰢ")
                bstack111llll1l11_opy_.add(bstack111lll1l111_opy_)
                bstack111ll111l11_opy_.append({
                    bstack1l1l11l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣᰣ"): commit.message.strip(),
                    bstack1l1l11l_opy_ (u"ࠣࡷࡶࡩࡷࠨᰤ"): bstack111lll1l111_opy_
                })
            result[bstack1l1l11l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᰥ")] = list(bstack111llll1l11_opy_)
            result[bstack1l1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦᰦ")] = bstack111ll111l11_opy_
            result[bstack1l1l11l_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦᰧ")] = bstack111ll11llll_opy_.committed_datetime.strftime(bstack1l1l11l_opy_ (u"࡙ࠧࠫ࠮ࠧࡰ࠱ࠪࡪࠢᰨ"))
            if (not result[bstack1l1l11l_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢᰩ")] or result[bstack1l1l11l_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᰪ")].strip() == bstack1l1l11l_opy_ (u"ࠣࠤᰫ")) and bstack111ll11llll_opy_.message:
                bstack111llll11ll_opy_ = bstack111ll11llll_opy_.message.strip().splitlines()
                result[bstack1l1l11l_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᰬ")] = bstack111llll11ll_opy_[0] if bstack111llll11ll_opy_ else bstack1l1l11l_opy_ (u"ࠥࠦᰭ")
                if len(bstack111llll11ll_opy_) > 2:
                    result[bstack1l1l11l_opy_ (u"ࠦࡵࡸࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦᰮ")] = bstack1l1l11l_opy_ (u"ࠬࡢ࡮ࠨᰯ").join(bstack111llll11ll_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1l1l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤ࠭࡬࡯࡭ࡦࡨࡶ࠿ࠦࡻࡾࠫ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧᰰ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _111ll11ll1l_opy_(result)
    ]
    return filtered_results
def _111ll11ll1l_opy_(result):
    bstack1l1l11l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡉࡧ࡯ࡴࡪࡸࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡧࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡵࡸࡰࡹࠦࡩࡴࠢࡹࡥࡱ࡯ࡤࠡࠪࡱࡳࡳ࠳ࡥ࡮ࡲࡷࡽࠥ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠤࡦࡴࡤࠡࡣࡸࡸ࡭ࡵࡲࡴࠫ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᰱ")
    return (
        isinstance(result.get(bstack1l1l11l_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᰲ"), None), list)
        and len(result[bstack1l1l11l_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᰳ")]) > 0
        and isinstance(result.get(bstack1l1l11l_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᰴ"), None), list)
        and len(result[bstack1l1l11l_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧᰵ")]) > 0
    )
def _111lll1111l_opy_(repo):
    bstack1l1l11l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡚ࠥࡲࡺࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶ࡫ࡩࠥࡨࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡶࡪࡶ࡯ࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢ࡫ࡥࡷࡪࡣࡰࡦࡨࡨࠥࡴࡡ࡮ࡧࡶࠤࡦࡴࡤࠡࡹࡲࡶࡰࠦࡷࡪࡶ࡫ࠤࡦࡲ࡬ࠡࡘࡆࡗࠥࡶࡲࡰࡸ࡬ࡨࡪࡸࡳ࠯ࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡩ࡫ࡦࡢࡷ࡯ࡸࠥࡨࡲࡢࡰࡦ࡬ࠥ࡯ࡦࠡࡲࡲࡷࡸ࡯ࡢ࡭ࡧ࠯ࠤࡪࡲࡳࡦࠢࡑࡳࡳ࡫࠮ࠋࠢࠣࠤࠥࠨࠢࠣᰶ")
    try:
        try:
            origin = repo.remotes.origin
            bstack111ll111lll_opy_ = origin.refs[bstack1l1l11l_opy_ (u"࠭ࡈࡆࡃࡇ᰷ࠫ")]
            target = bstack111ll111lll_opy_.reference.name
            if target.startswith(bstack1l1l11l_opy_ (u"ࠧࡰࡴ࡬࡫࡮ࡴ࠯ࠨ᰸")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1l1l11l_opy_ (u"ࠨࡱࡵ࡭࡬࡯࡮࠰ࠩ᰹")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _111ll1lll1l_opy_(commits):
    bstack1l1l11l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡊࡩࡹࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡤࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡧࡴࡲࡱࠥࡧࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࡴ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ᰺")
    bstack111lll1ll11_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111lll1l1l1_opy_ in diff:
                        if bstack111lll1l1l1_opy_.a_path:
                            bstack111lll1ll11_opy_.add(bstack111lll1l1l1_opy_.a_path)
                        if bstack111lll1l1l1_opy_.b_path:
                            bstack111lll1ll11_opy_.add(bstack111lll1l1l1_opy_.b_path)
    except Exception:
        pass
    return list(bstack111lll1ll11_opy_)
def bstack111l1lll1ll_opy_(bstack11l111111l1_opy_):
    bstack111ll11l1l1_opy_ = bstack111llll11l1_opy_(bstack11l111111l1_opy_)
    if bstack111ll11l1l1_opy_ and bstack111ll11l1l1_opy_ > bstack11l1l11l1ll_opy_:
        bstack111ll11111l_opy_ = bstack111ll11l1l1_opy_ - bstack11l1l11l1ll_opy_
        bstack111l1ll11l1_opy_ = bstack111ll1l11l1_opy_(bstack11l111111l1_opy_[bstack1l1l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦ᰻")], bstack111ll11111l_opy_)
        bstack11l111111l1_opy_[bstack1l1l11l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ᰼")] = bstack111l1ll11l1_opy_
        logger.info(bstack1l1l11l_opy_ (u"࡚ࠧࡨࡦࠢࡦࡳࡲࡳࡩࡵࠢ࡫ࡥࡸࠦࡢࡦࡧࡱࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪ࠮ࠡࡕ࡬ࡾࡪࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࠢࡤࡪࡹ࡫ࡲࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡽࢀࠤࡐࡈࠢ᰽")
                    .format(bstack111llll11l1_opy_(bstack11l111111l1_opy_) / 1024))
    return bstack11l111111l1_opy_
def bstack111llll11l1_opy_(bstack11ll11l1ll_opy_):
    try:
        if bstack11ll11l1ll_opy_:
            bstack111lll1l1ll_opy_ = json.dumps(bstack11ll11l1ll_opy_)
            bstack111ll1l1ll1_opy_ = sys.getsizeof(bstack111lll1l1ll_opy_)
            return bstack111ll1l1ll1_opy_
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"ࠨࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥࡩࡡ࡭ࡥࡸࡰࡦࡺࡩ࡯ࡩࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࡏ࡙ࡏࡏࠢࡲࡦ࡯࡫ࡣࡵ࠼ࠣࡿࢂࠨ᰾").format(e))
    return -1
def bstack111ll1l11l1_opy_(field, bstack111l1ll1111_opy_):
    try:
        bstack111l1l1lll1_opy_ = len(bytes(bstack11l1l1111ll_opy_, bstack1l1l11l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᰿")))
        bstack111l1l11ll1_opy_ = bytes(field, bstack1l1l11l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᱀"))
        bstack111ll1l1l11_opy_ = len(bstack111l1l11ll1_opy_)
        bstack111ll11l111_opy_ = ceil(bstack111ll1l1l11_opy_ - bstack111l1ll1111_opy_ - bstack111l1l1lll1_opy_)
        if bstack111ll11l111_opy_ > 0:
            bstack111ll1ll1ll_opy_ = bstack111l1l11ll1_opy_[:bstack111ll11l111_opy_].decode(bstack1l1l11l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᱁"), errors=bstack1l1l11l_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࠪ᱂")) + bstack11l1l1111ll_opy_
            return bstack111ll1ll1ll_opy_
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡲ࡬ࠦࡦࡪࡧ࡯ࡨ࠱ࠦ࡮ࡰࡶ࡫࡭ࡳ࡭ࠠࡸࡣࡶࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪࠠࡩࡧࡵࡩ࠿ࠦࡻࡾࠤ᱃").format(e))
    return field
def bstack1lll11ll11_opy_():
    env = os.environ
    if (bstack1l1l11l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥ᱄") in env and len(env[bstack1l1l11l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦ᱅")]) > 0) or (
            bstack1l1l11l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨ᱆") in env and len(env[bstack1l1l11l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢ᱇")]) > 0):
        return {
            bstack1l1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᱈"): bstack1l1l11l_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦ᱉"),
            bstack1l1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᱊"): env.get(bstack1l1l11l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᱋")),
            bstack1l1l11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᱌"): env.get(bstack1l1l11l_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤᱍ")),
            bstack1l1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᱎ"): env.get(bstack1l1l11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᱏ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠥࡇࡎࠨ᱐")) == bstack1l1l11l_opy_ (u"ࠦࡹࡸࡵࡦࠤ᱑") and bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢ᱒"))):
        return {
            bstack1l1l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᱓"): bstack1l1l11l_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤ᱔"),
            bstack1l1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᱕"): env.get(bstack1l1l11l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᱖")),
            bstack1l1l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᱗"): env.get(bstack1l1l11l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣ᱘")),
            bstack1l1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᱙"): env.get(bstack1l1l11l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤᱚ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠢࡄࡋࠥᱛ")) == bstack1l1l11l_opy_ (u"ࠣࡶࡵࡹࡪࠨᱜ") and bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤᱝ"))):
        return {
            bstack1l1l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᱞ"): bstack1l1l11l_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢᱟ"),
            bstack1l1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᱠ"): env.get(bstack1l1l11l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨᱡ")),
            bstack1l1l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᱢ"): env.get(bstack1l1l11l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᱣ")),
            bstack1l1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᱤ"): env.get(bstack1l1l11l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᱥ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠦࡈࡏࠢᱦ")) == bstack1l1l11l_opy_ (u"ࠧࡺࡲࡶࡧࠥᱧ") and env.get(bstack1l1l11l_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋࠢᱨ")) == bstack1l1l11l_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤᱩ"):
        return {
            bstack1l1l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᱪ"): bstack1l1l11l_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦᱫ"),
            bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᱬ"): None,
            bstack1l1l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᱭ"): None,
            bstack1l1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᱮ"): None
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤᱯ")) and env.get(bstack1l1l11l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥᱰ")):
        return {
            bstack1l1l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᱱ"): bstack1l1l11l_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧᱲ"),
            bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᱳ"): env.get(bstack1l1l11l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤᱴ")),
            bstack1l1l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᱵ"): None,
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᱶ"): env.get(bstack1l1l11l_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᱷ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠣࡅࡌࠦᱸ")) == bstack1l1l11l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᱹ") and bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤᱺ"))):
        return {
            bstack1l1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᱻ"): bstack1l1l11l_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦᱼ"),
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᱽ"): env.get(bstack1l1l11l_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥ᱾")),
            bstack1l1l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᱿"): None,
            bstack1l1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᲀ"): env.get(bstack1l1l11l_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᲁ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠦࡈࡏࠢᲂ")) == bstack1l1l11l_opy_ (u"ࠧࡺࡲࡶࡧࠥᲃ") and bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤᲄ"))):
        return {
            bstack1l1l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᲅ"): bstack1l1l11l_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦᲆ"),
            bstack1l1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᲇ"): env.get(bstack1l1l11l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤᲈ")),
            bstack1l1l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᲉ"): env.get(bstack1l1l11l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᲊ")),
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᲋"): env.get(bstack1l1l11l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ᲌"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠣࡅࡌࠦ᲍")) == bstack1l1l11l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᲎") and bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨ᲏"))):
        return {
            bstack1l1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᲐ"): bstack1l1l11l_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧᲑ"),
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᲒ"): env.get(bstack1l1l11l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦᲓ")),
            bstack1l1l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᲔ"): env.get(bstack1l1l11l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᲕ")),
            bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᲖ"): env.get(bstack1l1l11l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢᲗ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠧࡉࡉࠣᲘ")) == bstack1l1l11l_opy_ (u"ࠨࡴࡳࡷࡨࠦᲙ") and bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥᲚ"))):
        return {
            bstack1l1l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᲛ"): bstack1l1l11l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧᲜ"),
            bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᲝ"): env.get(bstack1l1l11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᲞ")),
            bstack1l1l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᲟ"): env.get(bstack1l1l11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣᲠ")) or env.get(bstack1l1l11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥᲡ")),
            bstack1l1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᲢ"): env.get(bstack1l1l11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᲣ"))
        }
    if bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᲤ"))):
        return {
            bstack1l1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᲥ"): bstack1l1l11l_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧᲦ"),
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᲧ"): bstack1l1l11l_opy_ (u"ࠢࡼࡿࡾࢁࠧᲨ").format(env.get(bstack1l1l11l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᲩ")), env.get(bstack1l1l11l_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩᲪ"))),
            bstack1l1l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᲫ"): env.get(bstack1l1l11l_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥᲬ")),
            bstack1l1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᲭ"): env.get(bstack1l1l11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᲮ"))
        }
    if bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤᲯ"))):
        return {
            bstack1l1l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᲰ"): bstack1l1l11l_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦᲱ"),
            bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᲲ"): bstack1l1l11l_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥᲳ").format(env.get(bstack1l1l11l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫᲴ")), env.get(bstack1l1l11l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧᲵ")), env.get(bstack1l1l11l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨᲶ")), env.get(bstack1l1l11l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬᲷ"))),
            bstack1l1l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᲸ"): env.get(bstack1l1l11l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᲹ")),
            bstack1l1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᲺ"): env.get(bstack1l1l11l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᲻"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢ᲼")) and env.get(bstack1l1l11l_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤᲽ")):
        return {
            bstack1l1l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᲾ"): bstack1l1l11l_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦᲿ"),
            bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᳀"): bstack1l1l11l_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢ᳁").format(env.get(bstack1l1l11l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨ᳂")), env.get(bstack1l1l11l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫ᳃")), env.get(bstack1l1l11l_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧ᳄"))),
            bstack1l1l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᳅"): env.get(bstack1l1l11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤ᳆")),
            bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᳇"): env.get(bstack1l1l11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦ᳈"))
        }
    if any([env.get(bstack1l1l11l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᳉")), env.get(bstack1l1l11l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧ᳊")), env.get(bstack1l1l11l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ᳋"))]):
        return {
            bstack1l1l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᳌"): bstack1l1l11l_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤ᳍"),
            bstack1l1l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᳎"): env.get(bstack1l1l11l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᳏")),
            bstack1l1l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᳐"): env.get(bstack1l1l11l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ᳑")),
            bstack1l1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᳒"): env.get(bstack1l1l11l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ᳓"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸ᳔ࠢ")):
        return {
            bstack1l1l11l_opy_ (u"ࠥࡲࡦࡳࡥ᳕ࠣ"): bstack1l1l11l_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲ᳖ࠦ"),
            bstack1l1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬᳗ࠣ"): env.get(bstack1l1l11l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬᳘ࠣ")),
            bstack1l1l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᳙"): env.get(bstack1l1l11l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢ᳚")),
            bstack1l1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᳛"): env.get(bstack1l1l11l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲ᳜ࠣ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖ᳝ࠧ")) or env.get(bstack1l1l11l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊ᳞ࠢ")):
        return {
            bstack1l1l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᳟ࠦ"): bstack1l1l11l_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣ᳠"),
            bstack1l1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᳡"): env.get(bstack1l1l11l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᳢")),
            bstack1l1l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩ᳣ࠧ"): bstack1l1l11l_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨ᳤ࠦ") if env.get(bstack1l1l11l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊ᳥ࠢ")) else None,
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶ᳦ࠧ"): env.get(bstack1l1l11l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘ᳧ࠧ"))
        }
    if any([env.get(bstack1l1l11l_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ᳨")), env.get(bstack1l1l11l_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᳩ")), env.get(bstack1l1l11l_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᳪ"))]):
        return {
            bstack1l1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᳫ"): bstack1l1l11l_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦᳬ"),
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᳭"): None,
            bstack1l1l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᳮ"): env.get(bstack1l1l11l_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧᳯ")),
            bstack1l1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᳰ"): env.get(bstack1l1l11l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᳱ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢᳲ")):
        return {
            bstack1l1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᳳ"): bstack1l1l11l_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤ᳴"),
            bstack1l1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᳵ"): env.get(bstack1l1l11l_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᳶ")),
            bstack1l1l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᳷"): bstack1l1l11l_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦ᳸").format(env.get(bstack1l1l11l_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧ᳹"))) if env.get(bstack1l1l11l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣᳺ")) else None,
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᳻"): env.get(bstack1l1l11l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᳼"))
        }
    if bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤ᳽"))):
        return {
            bstack1l1l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᳾"): bstack1l1l11l_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦ᳿"),
            bstack1l1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᴀ"): env.get(bstack1l1l11l_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤᴁ")),
            bstack1l1l11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᴂ"): env.get(bstack1l1l11l_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥᴃ")),
            bstack1l1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᴄ"): env.get(bstack1l1l11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᴅ"))
        }
    if bstack1llll111_opy_(env.get(bstack1l1l11l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖࠦᴆ"))):
        return {
            bstack1l1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᴇ"): bstack1l1l11l_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨᴈ"),
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᴉ"): bstack1l1l11l_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽࠣᴊ").format(env.get(bstack1l1l11l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬᴋ")), env.get(bstack1l1l11l_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭ᴌ")), env.get(bstack1l1l11l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠪᴍ"))),
            bstack1l1l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᴎ"): env.get(bstack1l1l11l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝ࠢᴏ")),
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᴐ"): env.get(bstack1l1l11l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢᴑ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠣࡅࡌࠦᴒ")) == bstack1l1l11l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᴓ") and env.get(bstack1l1l11l_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎࠥᴔ")) == bstack1l1l11l_opy_ (u"ࠦ࠶ࠨᴕ"):
        return {
            bstack1l1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᴖ"): bstack1l1l11l_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨᴗ"),
            bstack1l1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᴘ"): bstack1l1l11l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀࠦᴙ").format(env.get(bstack1l1l11l_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭ᴚ"))),
            bstack1l1l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᴛ"): None,
            bstack1l1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᴜ"): None,
        }
    if env.get(bstack1l1l11l_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣᴝ")):
        return {
            bstack1l1l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᴞ"): bstack1l1l11l_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤᴟ"),
            bstack1l1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᴠ"): None,
            bstack1l1l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᴡ"): env.get(bstack1l1l11l_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦᴢ")),
            bstack1l1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᴣ"): env.get(bstack1l1l11l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᴤ"))
        }
    if any([env.get(bstack1l1l11l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤᴥ")), env.get(bstack1l1l11l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢᴦ")), env.get(bstack1l1l11l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨᴧ")), env.get(bstack1l1l11l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥᴨ"))]):
        return {
            bstack1l1l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᴩ"): bstack1l1l11l_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢᴪ"),
            bstack1l1l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᴫ"): None,
            bstack1l1l11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᴬ"): env.get(bstack1l1l11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᴭ")) or None,
            bstack1l1l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᴮ"): env.get(bstack1l1l11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᴯ"), 0)
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᴰ")):
        return {
            bstack1l1l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᴱ"): bstack1l1l11l_opy_ (u"ࠧࡍ࡯ࡄࡆࠥᴲ"),
            bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᴳ"): None,
            bstack1l1l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᴴ"): env.get(bstack1l1l11l_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᴵ")),
            bstack1l1l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᴶ"): env.get(bstack1l1l11l_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤᴷ"))
        }
    if env.get(bstack1l1l11l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᴸ")):
        return {
            bstack1l1l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᴹ"): bstack1l1l11l_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤᴺ"),
            bstack1l1l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᴻ"): env.get(bstack1l1l11l_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᴼ")),
            bstack1l1l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᴽ"): env.get(bstack1l1l11l_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᴾ")),
            bstack1l1l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᴿ"): env.get(bstack1l1l11l_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᵀ"))
        }
    return {bstack1l1l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᵁ"): None}
def get_host_info():
    return {
        bstack1l1l11l_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤᵂ"): platform.node(),
        bstack1l1l11l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥᵃ"): platform.system(),
        bstack1l1l11l_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᵄ"): platform.machine(),
        bstack1l1l11l_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᵅ"): platform.version(),
        bstack1l1l11l_opy_ (u"ࠦࡦࡸࡣࡩࠤᵆ"): platform.architecture()[0]
    }
def bstack1ll1ll1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111llllll11_opy_():
    if bstack1ll1l111l1_opy_.get_property(bstack1l1l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ᵇ")):
        return bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᵈ")
    return bstack1l1l11l_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭ᵉ")
def bstack111l1l111l1_opy_(driver):
    info = {
        bstack1l1l11l_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᵊ"): driver.capabilities,
        bstack1l1l11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ᵋ"): driver.session_id,
        bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᵌ"): driver.capabilities.get(bstack1l1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᵍ"), None),
        bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᵎ"): driver.capabilities.get(bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᵏ"), None),
        bstack1l1l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᵐ"): driver.capabilities.get(bstack1l1l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᵑ"), None),
        bstack1l1l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᵒ"):driver.capabilities.get(bstack1l1l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᵓ"), None),
    }
    if bstack111llllll11_opy_() == bstack1l1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᵔ"):
        if bstack1ll1ll1111_opy_():
            info[bstack1l1l11l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᵕ")] = bstack1l1l11l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᵖ")
        elif driver.capabilities.get(bstack1l1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᵗ"), {}).get(bstack1l1l11l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᵘ"), False):
            info[bstack1l1l11l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᵙ")] = bstack1l1l11l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᵚ")
        else:
            info[bstack1l1l11l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᵛ")] = bstack1l1l11l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᵜ")
    return info
def bstack1ll1ll1111_opy_():
    if bstack1ll1l111l1_opy_.get_property(bstack1l1l11l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᵝ")):
        return True
    if bstack1llll111_opy_(os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᵞ"), None)):
        return True
    return False
def bstack11l1l1l111_opy_(bstack111ll11ll11_opy_, url, data, config):
    headers = config.get(bstack1l1l11l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᵟ"), None)
    proxies = bstack11l111ll11_opy_(config, url)
    auth = config.get(bstack1l1l11l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᵠ"), None)
    response = requests.request(
            bstack111ll11ll11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1lll11_opy_(bstack111ll1111_opy_, size):
    bstack1l1l1ll11l_opy_ = []
    while len(bstack111ll1111_opy_) > size:
        bstack111111ll_opy_ = bstack111ll1111_opy_[:size]
        bstack1l1l1ll11l_opy_.append(bstack111111ll_opy_)
        bstack111ll1111_opy_ = bstack111ll1111_opy_[size:]
    bstack1l1l1ll11l_opy_.append(bstack111ll1111_opy_)
    return bstack1l1l1ll11l_opy_
def bstack11l11111l1l_opy_(message, bstack111ll1111l1_opy_=False):
    os.write(1, bytes(message, bstack1l1l11l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᵡ")))
    os.write(1, bytes(bstack1l1l11l_opy_ (u"ࠫࡡࡴࠧᵢ"), bstack1l1l11l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᵣ")))
    if bstack111ll1111l1_opy_:
        with open(bstack1l1l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬᵤ") + os.environ[bstack1l1l11l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᵥ")] + bstack1l1l11l_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭ᵦ"), bstack1l1l11l_opy_ (u"ࠩࡤࠫᵧ")) as f:
            f.write(message + bstack1l1l11l_opy_ (u"ࠪࡠࡳ࠭ᵨ"))
def bstack1l1l11lll11_opy_():
    return os.environ[bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᵩ")].lower() == bstack1l1l11l_opy_ (u"ࠬࡺࡲࡶࡧࠪᵪ")
def bstack11l1lllll_opy_():
    return bstack1111ll11ll_opy_().replace(tzinfo=None).isoformat() + bstack1l1l11l_opy_ (u"࡚࠭ࠨᵫ")
def bstack11ll1l1l1l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1l11l_opy_ (u"࡛ࠧࠩᵬ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1l11l_opy_ (u"ࠨ࡜ࠪᵭ")))).total_seconds() * 1000
def bstack111ll11l1ll_opy_(timestamp):
    return bstack111llllllll_opy_(timestamp).isoformat() + bstack1l1l11l_opy_ (u"ࠩ࡝ࠫᵮ")
def bstack111lll11lll_opy_(bstack111l1l11l11_opy_):
    date_format = bstack1l1l11l_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨᵯ")
    bstack111ll1l1l1l_opy_ = datetime.datetime.strptime(bstack111l1l11l11_opy_, date_format)
    return bstack111ll1l1l1l_opy_.isoformat() + bstack1l1l11l_opy_ (u"ࠫ࡟࠭ᵰ")
def bstack111l1ll1l1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᵱ")
    else:
        return bstack1l1l11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᵲ")
def bstack1llll111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1l11l_opy_ (u"ࠧࡵࡴࡸࡩࠬᵳ")
def bstack11l11111l11_opy_(val):
    return val.__str__().lower() == bstack1l1l11l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᵴ")
def error_handler(bstack111lll111l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111lll111l1_opy_ as e:
                print(bstack1l1l11l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤᵵ").format(func.__name__, bstack111lll111l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1111l1ll_opy_(bstack111l1l1l1ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l1l1l1ll_opy_(cls, *args, **kwargs)
            except bstack111lll111l1_opy_ as e:
                print(bstack1l1l11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᵶ").format(bstack111l1l1l1ll_opy_.__name__, bstack111lll111l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1111l1ll_opy_
    else:
        return decorator
def bstack1lll11lll1_opy_(bstack11111l1ll1_opy_):
    if os.getenv(bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᵷ")) is not None:
        return bstack1llll111_opy_(os.getenv(bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᵸ")))
    if bstack1l1l11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᵹ") in bstack11111l1ll1_opy_ and bstack11l11111l11_opy_(bstack11111l1ll1_opy_[bstack1l1l11l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᵺ")]):
        return False
    if bstack1l1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᵻ") in bstack11111l1ll1_opy_ and bstack11l11111l11_opy_(bstack11111l1ll1_opy_[bstack1l1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᵼ")]):
        return False
    return True
def bstack1ll111l11l_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1111111l_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥᵽ"), None)
        return bstack11l1111111l_opy_ is None or bstack11l1111111l_opy_ == bstack1l1l11l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᵾ")
    except Exception as e:
        return False
def bstack11l11ll11l_opy_(hub_url, CONFIG):
    if bstack1l1l1111_opy_() <= version.parse(bstack1l1l11l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬᵿ")):
        if hub_url:
            return bstack1l1l11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᶀ") + hub_url + bstack1l1l11l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦᶁ")
        return bstack1l111111l1_opy_
    if hub_url:
        return bstack1l1l11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᶂ") + hub_url + bstack1l1l11l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥᶃ")
    return bstack11lll1ll1l_opy_
def bstack111ll1l1111_opy_():
    return isinstance(os.getenv(bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩᶄ")), str)
def bstack11lllllll_opy_(url):
    return urlparse(url).hostname
def bstack111l1lll_opy_(hostname):
    for bstack11l11l111_opy_ in bstack1111111l_opy_:
        regex = re.compile(bstack11l11l111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11ll11l1l1l_opy_(bstack111l1lll1l1_opy_, file_name, logger):
    bstack11l1l1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l1l11l_opy_ (u"ࠫࢃ࠭ᶅ")), bstack111l1lll1l1_opy_)
    try:
        if not os.path.exists(bstack11l1l1lll1_opy_):
            os.makedirs(bstack11l1l1lll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1l11l_opy_ (u"ࠬࢄࠧᶆ")), bstack111l1lll1l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1l11l_opy_ (u"࠭ࡷࠨᶇ")):
                pass
            with open(file_path, bstack1l1l11l_opy_ (u"ࠢࡸ࠭ࠥᶈ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11ll11l11l_opy_.format(str(e)))
def bstack11ll11l11ll_opy_(file_name, key, value, logger):
    file_path = bstack11ll11l1l1l_opy_(bstack1l1l11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᶉ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll1ll1_opy_ = json.load(open(file_path, bstack1l1l11l_opy_ (u"ࠩࡵࡦࠬᶊ")))
        else:
            bstack1lll1ll1_opy_ = {}
        bstack1lll1ll1_opy_[key] = value
        with open(file_path, bstack1l1l11l_opy_ (u"ࠥࡻ࠰ࠨᶋ")) as outfile:
            json.dump(bstack1lll1ll1_opy_, outfile)
def bstack11111l1l1_opy_(file_name, logger):
    file_path = bstack11ll11l1l1l_opy_(bstack1l1l11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᶌ"), file_name, logger)
    bstack1lll1ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1l11l_opy_ (u"ࠬࡸࠧᶍ")) as bstack1ll11l11l1_opy_:
            bstack1lll1ll1_opy_ = json.load(bstack1ll11l11l1_opy_)
    return bstack1lll1ll1_opy_
def bstack1l11ll111l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪᶎ") + file_path + bstack1l1l11l_opy_ (u"ࠧࠡࠩᶏ") + str(e))
def bstack1l1l1111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1l11l_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥᶐ")
def bstack1ll11ll11l_opy_(config):
    if bstack1l1l11l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᶑ") in config:
        del (config[bstack1l1l11l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᶒ")])
        return False
    if bstack1l1l1111_opy_() < version.parse(bstack1l1l11l_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪᶓ")):
        return False
    if bstack1l1l1111_opy_() >= version.parse(bstack1l1l11l_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫᶔ")):
        return True
    if bstack1l1l11l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᶕ") in config and config[bstack1l1l11l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᶖ")] is False:
        return False
    else:
        return True
def bstack1l111ll111_opy_(args_list, bstack111llllll1l_opy_):
    index = -1
    for value in bstack111llllll1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l1llll11l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l1llll11l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111l1lll11_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111l1lll11_opy_ = bstack111l1lll11_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1l11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᶗ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᶘ"), exception=exception)
    def bstack1llllll1ll1_opy_(self):
        if self.result != bstack1l1l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᶙ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1l11l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᶚ") in self.exception_type:
            return bstack1l1l11l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᶛ")
        return bstack1l1l11l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᶜ")
    def bstack11ll1l1l111_opy_(self):
        if self.result != bstack1l1l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᶝ"):
            return None
        if self.bstack111l1lll11_opy_:
            return self.bstack111l1lll11_opy_
        return bstack111ll111111_opy_(self.exception)
def bstack111ll111111_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l1lll111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111111l11_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1l11l1l_opy_(config, logger):
    try:
        import playwright
        bstack111ll1lll11_opy_ = playwright.__file__
        bstack111llll1111_opy_ = os.path.split(bstack111ll1lll11_opy_)
        bstack111llll1ll1_opy_ = bstack111llll1111_opy_[0] + bstack1l1l11l_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫᶞ")
        os.environ[bstack1l1l11l_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬᶟ")] = bstack1l1l11l11l_opy_(config)
        with open(bstack111llll1ll1_opy_, bstack1l1l11l_opy_ (u"ࠪࡶࠬᶠ")) as f:
            bstack11lllllll1_opy_ = f.read()
            bstack111ll1l1lll_opy_ = bstack1l1l11l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪᶡ")
            bstack111ll111ll1_opy_ = bstack11lllllll1_opy_.find(bstack111ll1l1lll_opy_)
            if bstack111ll111ll1_opy_ == -1:
              process = subprocess.Popen(bstack1l1l11l_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤᶢ"), shell=True, cwd=bstack111llll1111_opy_[0])
              process.wait()
              bstack111l1llllll_opy_ = bstack1l1l11l_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭ᶣ")
              bstack11l11111111_opy_ = bstack1l1l11l_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦᶤ")
              bstack111lll11111_opy_ = bstack11lllllll1_opy_.replace(bstack111l1llllll_opy_, bstack11l11111111_opy_)
              with open(bstack111llll1ll1_opy_, bstack1l1l11l_opy_ (u"ࠨࡹࠪᶥ")) as f:
                f.write(bstack111lll11111_opy_)
    except Exception as e:
        logger.error(bstack1lll111ll1_opy_.format(str(e)))
def bstack1lll1lll_opy_():
  try:
    bstack111lllllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᶦ"))
    bstack111lll1lll1_opy_ = []
    if os.path.exists(bstack111lllllll1_opy_):
      with open(bstack111lllllll1_opy_) as f:
        bstack111lll1lll1_opy_ = json.load(f)
      os.remove(bstack111lllllll1_opy_)
    return bstack111lll1lll1_opy_
  except:
    pass
  return []
def bstack1ll1ll1l1l_opy_(bstack111llll1l_opy_):
  try:
    bstack111lll1lll1_opy_ = []
    bstack111lllllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪᶧ"))
    if os.path.exists(bstack111lllllll1_opy_):
      with open(bstack111lllllll1_opy_) as f:
        bstack111lll1lll1_opy_ = json.load(f)
    bstack111lll1lll1_opy_.append(bstack111llll1l_opy_)
    with open(bstack111lllllll1_opy_, bstack1l1l11l_opy_ (u"ࠫࡼ࠭ᶨ")) as f:
        json.dump(bstack111lll1lll1_opy_, f)
  except:
    pass
def bstack1ll11l1l1_opy_(logger, bstack111l1l1l11l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1l11l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᶩ"), bstack1l1l11l_opy_ (u"࠭ࠧᶪ"))
    if test_name == bstack1l1l11l_opy_ (u"ࠧࠨᶫ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧᶬ"), bstack1l1l11l_opy_ (u"ࠩࠪᶭ"))
    bstack111lll111ll_opy_ = bstack1l1l11l_opy_ (u"ࠪ࠰ࠥ࠭ᶮ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111l1l1l11l_opy_:
        bstack1ll1l1111l_opy_ = os.environ.get(bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᶯ"), bstack1l1l11l_opy_ (u"ࠬ࠶ࠧᶰ"))
        bstack1lll1l1l1_opy_ = {bstack1l1l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᶱ"): test_name, bstack1l1l11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᶲ"): bstack111lll111ll_opy_, bstack1l1l11l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᶳ"): bstack1ll1l1111l_opy_}
        bstack111lllll11l_opy_ = []
        bstack111l1l1111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᶴ"))
        if os.path.exists(bstack111l1l1111l_opy_):
            with open(bstack111l1l1111l_opy_) as f:
                bstack111lllll11l_opy_ = json.load(f)
        bstack111lllll11l_opy_.append(bstack1lll1l1l1_opy_)
        with open(bstack111l1l1111l_opy_, bstack1l1l11l_opy_ (u"ࠪࡻࠬᶵ")) as f:
            json.dump(bstack111lllll11l_opy_, f)
    else:
        bstack1lll1l1l1_opy_ = {bstack1l1l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᶶ"): test_name, bstack1l1l11l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᶷ"): bstack111lll111ll_opy_, bstack1l1l11l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᶸ"): str(multiprocessing.current_process().name)}
        if bstack1l1l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫᶹ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1lll1l1l1_opy_)
  except Exception as e:
      logger.warn(bstack1l1l11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧᶺ").format(e))
def bstack11111111_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1l11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬᶻ"))
    try:
      bstack111l1llll11_opy_ = []
      bstack1lll1l1l1_opy_ = {bstack1l1l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨᶼ"): test_name, bstack1l1l11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᶽ"): error_message, bstack1l1l11l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᶾ"): index}
      bstack111lll1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᶿ"))
      if os.path.exists(bstack111lll1llll_opy_):
          with open(bstack111lll1llll_opy_) as f:
              bstack111l1llll11_opy_ = json.load(f)
      bstack111l1llll11_opy_.append(bstack1lll1l1l1_opy_)
      with open(bstack111lll1llll_opy_, bstack1l1l11l_opy_ (u"ࠧࡸࠩ᷀")) as f:
          json.dump(bstack111l1llll11_opy_, f)
    except Exception as e:
      logger.warn(bstack1l1l11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ᷁").format(e))
    return
  bstack111l1llll11_opy_ = []
  bstack1lll1l1l1_opy_ = {bstack1l1l11l_opy_ (u"ࠩࡱࡥࡲ࡫᷂ࠧ"): test_name, bstack1l1l11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᷃"): error_message, bstack1l1l11l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ᷄"): index}
  bstack111lll1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭᷅"))
  lock_file = bstack111lll1llll_opy_ + bstack1l1l11l_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬ᷆")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111lll1llll_opy_):
          with open(bstack111lll1llll_opy_, bstack1l1l11l_opy_ (u"ࠧࡳࠩ᷇")) as f:
              content = f.read().strip()
              if content:
                  bstack111l1llll11_opy_ = json.load(open(bstack111lll1llll_opy_))
      bstack111l1llll11_opy_.append(bstack1lll1l1l1_opy_)
      with open(bstack111lll1llll_opy_, bstack1l1l11l_opy_ (u"ࠨࡹࠪ᷈")) as f:
          json.dump(bstack111l1llll11_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1l11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡦࡪ࡮ࡨࠤࡱࡵࡣ࡬࡫ࡱ࡫࠿ࠦࡻࡾࠤ᷉").format(e))
def bstack11l1l1111l_opy_(bstack1ll11lll1_opy_, name, logger):
  try:
    bstack1lll1l1l1_opy_ = {bstack1l1l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨ᷊"): name, bstack1l1l11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᷋"): bstack1ll11lll1_opy_, bstack1l1l11l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ᷌"): str(threading.current_thread()._name)}
    return bstack1lll1l1l1_opy_
  except Exception as e:
    logger.warn(bstack1l1l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ᷍").format(e))
  return
def bstack111lll11ll1_opy_():
    return platform.system() == bstack1l1l11l_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨ᷎")
def bstack1111llll_opy_(bstack111lll11l1l_opy_, config, logger):
    bstack111l1ll111l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111lll11l1l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃ᷏ࠢ").format(e))
    return bstack111l1ll111l_opy_
def bstack11l1111lll1_opy_(bstack111l1llll1l_opy_, bstack11l111111ll_opy_):
    bstack11l1111l111_opy_ = version.parse(bstack111l1llll1l_opy_)
    bstack111l1ll1l11_opy_ = version.parse(bstack11l111111ll_opy_)
    if bstack11l1111l111_opy_ > bstack111l1ll1l11_opy_:
        return 1
    elif bstack11l1111l111_opy_ < bstack111l1ll1l11_opy_:
        return -1
    else:
        return 0
def bstack1111ll11ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111llllllll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111l1l1l1l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1lllllll_opy_(options, framework, config, bstack11l11l11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1l11l_opy_ (u"ࠩࡪࡩࡹ᷐࠭"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1llll111_opy_ = caps.get(bstack1l1l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᷑"))
    bstack11l1111ll1l_opy_ = True
    bstack1lll1ll11_opy_ = os.environ[bstack1l1l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᷒")]
    bstack1ll1111l11l_opy_ = config.get(bstack1l1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᷓ"), False)
    if bstack1ll1111l11l_opy_:
        bstack1lll1l1l1ll_opy_ = config.get(bstack1l1l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᷔ"), {})
        bstack1lll1l1l1ll_opy_[bstack1l1l11l_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᷕ")] = os.getenv(bstack1l1l11l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᷖ"))
        bstack11ll111lll1_opy_ = json.loads(os.getenv(bstack1l1l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᷗ"), bstack1l1l11l_opy_ (u"ࠪࡿࢂ࠭ᷘ"))).get(bstack1l1l11l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᷙ"))
    if bstack11l11111l11_opy_(caps.get(bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫᷚ"))) or bstack11l11111l11_opy_(caps.get(bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭ᷛ"))):
        bstack11l1111ll1l_opy_ = False
    if bstack1ll11ll11l_opy_({bstack1l1l11l_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢᷜ"): bstack11l1111ll1l_opy_}):
        bstack1l1llll111_opy_ = bstack1l1llll111_opy_ or {}
        bstack1l1llll111_opy_[bstack1l1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᷝ")] = bstack111l1l1l1l1_opy_(framework)
        bstack1l1llll111_opy_[bstack1l1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᷞ")] = bstack1l1l11lll11_opy_()
        bstack1l1llll111_opy_[bstack1l1l11l_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᷟ")] = bstack1lll1ll11_opy_
        bstack1l1llll111_opy_[bstack1l1l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᷠ")] = bstack11l11l11_opy_
        if bstack1ll1111l11l_opy_:
            bstack1l1llll111_opy_[bstack1l1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᷡ")] = bstack1ll1111l11l_opy_
            bstack1l1llll111_opy_[bstack1l1l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᷢ")] = bstack1lll1l1l1ll_opy_
            bstack1l1llll111_opy_[bstack1l1l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᷣ")][bstack1l1l11l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᷤ")] = bstack11ll111lll1_opy_
        if getattr(options, bstack1l1l11l_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᷥ"), None):
            options.set_capability(bstack1l1l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᷦ"), bstack1l1llll111_opy_)
        else:
            options[bstack1l1l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᷧ")] = bstack1l1llll111_opy_
    else:
        if getattr(options, bstack1l1l11l_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ᷨ"), None):
            options.set_capability(bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᷩ"), bstack111l1l1l1l1_opy_(framework))
            options.set_capability(bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᷪ"), bstack1l1l11lll11_opy_())
            options.set_capability(bstack1l1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᷫ"), bstack1lll1ll11_opy_)
            options.set_capability(bstack1l1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᷬ"), bstack11l11l11_opy_)
            if bstack1ll1111l11l_opy_:
                options.set_capability(bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᷭ"), bstack1ll1111l11l_opy_)
                options.set_capability(bstack1l1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᷮ"), bstack1lll1l1l1ll_opy_)
                options.set_capability(bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᷯ"), bstack11ll111lll1_opy_)
        else:
            options[bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᷰ")] = bstack111l1l1l1l1_opy_(framework)
            options[bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᷱ")] = bstack1l1l11lll11_opy_()
            options[bstack1l1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᷲ")] = bstack1lll1ll11_opy_
            options[bstack1l1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᷳ")] = bstack11l11l11_opy_
            if bstack1ll1111l11l_opy_:
                options[bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᷴ")] = bstack1ll1111l11l_opy_
                options[bstack1l1l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᷵")] = bstack1lll1l1l1ll_opy_
                options[bstack1l1l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᷶")][bstack1l1l11l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ᷷ࠧ")] = bstack11ll111lll1_opy_
    return options
def bstack111lll11l11_opy_(bstack111lllll111_opy_, framework):
    bstack11l11l11_opy_ = bstack1ll1l111l1_opy_.get_property(bstack1l1l11l_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ᷸"))
    if bstack111lllll111_opy_ and len(bstack111lllll111_opy_.split(bstack1l1l11l_opy_ (u"ࠨࡥࡤࡴࡸࡃ᷹ࠧ"))) > 1:
        ws_url = bstack111lllll111_opy_.split(bstack1l1l11l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᷺"))[0]
        if bstack1l1l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭᷻") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1111l1l1_opy_ = json.loads(urllib.parse.unquote(bstack111lllll111_opy_.split(bstack1l1l11l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᷼"))[1]))
            bstack11l1111l1l1_opy_ = bstack11l1111l1l1_opy_ or {}
            bstack1lll1ll11_opy_ = os.environ[bstack1l1l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆ᷽ࠪ")]
            bstack11l1111l1l1_opy_[bstack1l1l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᷾")] = str(framework) + str(__version__)
            bstack11l1111l1l1_opy_[bstack1l1l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᷿")] = bstack1l1l11lll11_opy_()
            bstack11l1111l1l1_opy_[bstack1l1l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪḀ")] = bstack1lll1ll11_opy_
            bstack11l1111l1l1_opy_[bstack1l1l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪḁ")] = bstack11l11l11_opy_
            bstack111lllll111_opy_ = bstack111lllll111_opy_.split(bstack1l1l11l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩḂ"))[0] + bstack1l1l11l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪḃ") + urllib.parse.quote(json.dumps(bstack11l1111l1l1_opy_))
    return bstack111lllll111_opy_
def bstack1l1l111ll_opy_():
    global bstack11l11111_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l11111_opy_ = BrowserType.connect
    return bstack11l11111_opy_
def bstack1l11l1l11_opy_(framework_name):
    global bstack1l1lllll_opy_
    bstack1l1lllll_opy_ = framework_name
    return framework_name
def bstack11l1l1lll_opy_(self, *args, **kwargs):
    global bstack11l11111_opy_
    try:
        global bstack1l1lllll_opy_
        if bstack1l1l11l_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩḄ") in kwargs:
            kwargs[bstack1l1l11l_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪḅ")] = bstack111lll11l11_opy_(
                kwargs.get(bstack1l1l11l_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫḆ"), None),
                bstack1l1lllll_opy_
            )
    except Exception as e:
        logger.error(bstack1l1l11l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣḇ").format(str(e)))
    return bstack11l11111_opy_(self, *args, **kwargs)
def bstack11l1111l11l_opy_(bstack111ll1ll1l1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l111ll11_opy_(bstack111ll1ll1l1_opy_, bstack1l1l11l_opy_ (u"ࠤࠥḈ"))
        if proxies and proxies.get(bstack1l1l11l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤḉ")):
            parsed_url = urlparse(proxies.get(bstack1l1l11l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥḊ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1l11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨḋ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1l11l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩḌ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1l11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪḍ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1l11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫḎ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1ll1l111l_opy_(bstack111ll1ll1l1_opy_):
    bstack111l1l11l1l_opy_ = {
        bstack11l11ll11ll_opy_[bstack111ll1ll11l_opy_]: bstack111ll1ll1l1_opy_[bstack111ll1ll11l_opy_]
        for bstack111ll1ll11l_opy_ in bstack111ll1ll1l1_opy_
        if bstack111ll1ll11l_opy_ in bstack11l11ll11ll_opy_
    }
    bstack111l1l11l1l_opy_[bstack1l1l11l_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤḏ")] = bstack11l1111l11l_opy_(bstack111ll1ll1l1_opy_, bstack1ll1l111l1_opy_.get_property(bstack1l1l11l_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥḐ")))
    bstack111l1l1ll11_opy_ = [element.lower() for element in bstack11l11llll1l_opy_]
    bstack111llll1l1l_opy_(bstack111l1l11l1l_opy_, bstack111l1l1ll11_opy_)
    return bstack111l1l11l1l_opy_
def bstack111llll1l1l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1l11l_opy_ (u"ࠦ࠯࠰ࠪࠫࠤḑ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111llll1l1l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111llll1l1l_opy_(item, keys)
def bstack1l1l1l111ll_opy_():
    bstack111l1ll1lll_opy_ = [os.environ.get(bstack1l1l11l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘࠢḒ")), os.path.join(os.path.expanduser(bstack1l1l11l_opy_ (u"ࠨࡾࠣḓ")), bstack1l1l11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧḔ")), os.path.join(bstack1l1l11l_opy_ (u"ࠨ࠱ࡷࡱࡵ࠭ḕ"), bstack1l1l11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩḖ"))]
    for path in bstack111l1ll1lll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1l11l_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥḗ") + str(path) + bstack1l1l11l_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢḘ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1l11l_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤḙ") + str(path) + bstack1l1l11l_opy_ (u"ࠨࠧࠣḚ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1l11l_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢḛ") + str(path) + bstack1l1l11l_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨḜ"))
            else:
                logger.debug(bstack1l1l11l_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦḝ") + str(path) + bstack1l1l11l_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢḞ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1l11l_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤḟ") + str(path) + bstack1l1l11l_opy_ (u"ࠧ࠭࠮ࠣḠ"))
            return path
        except Exception as e:
            logger.debug(bstack1l1l11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦḡ") + str(e) + bstack1l1l11l_opy_ (u"ࠢࠣḢ"))
    logger.debug(bstack1l1l11l_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧḣ"))
    return None
@measure(event_name=EVENTS.bstack11l11l1ll11_opy_, stage=STAGE.bstack1l1111l11l_opy_)
def bstack1lll111111l_opy_(binary_path, bstack1ll1l1l1l1l_opy_, bs_config):
    logger.debug(bstack1l1l11l_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣḤ").format(binary_path))
    bstack111l1lll11l_opy_ = bstack1l1l11l_opy_ (u"ࠪࠫḥ")
    bstack111lllll1ll_opy_ = {
        bstack1l1l11l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩḦ"): __version__,
        bstack1l1l11l_opy_ (u"ࠧࡵࡳࠣḧ"): platform.system(),
        bstack1l1l11l_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮ࠢḨ"): platform.machine(),
        bstack1l1l11l_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧḩ"): bstack1l1l11l_opy_ (u"ࠨ࠲ࠪḪ"),
        bstack1l1l11l_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣḫ"): bstack1l1l11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪḬ")
    }
    bstack111l1l1l111_opy_(bstack111lllll1ll_opy_)
    try:
        if binary_path:
            if bstack111lll11ll1_opy_():
                bstack111lllll1ll_opy_[bstack1l1l11l_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩḭ")] = subprocess.check_output([binary_path, bstack1l1l11l_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨḮ")]).strip().decode(bstack1l1l11l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬḯ"))
            else:
                bstack111lllll1ll_opy_[bstack1l1l11l_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬḰ")] = subprocess.check_output([binary_path, bstack1l1l11l_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤḱ")], stderr=subprocess.DEVNULL).strip().decode(bstack1l1l11l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨḲ"))
        response = requests.request(
            bstack1l1l11l_opy_ (u"ࠪࡋࡊ࡚ࠧḳ"),
            url=bstack1l1ll1l11l_opy_(bstack11l11llll11_opy_),
            headers=None,
            auth=(bs_config[bstack1l1l11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ḵ")], bs_config[bstack1l1l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨḵ")]),
            json=None,
            params=bstack111lllll1ll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1l11l_opy_ (u"࠭ࡵࡳ࡮ࠪḶ") in data.keys() and bstack1l1l11l_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ḷ") in data.keys():
            logger.debug(bstack1l1l11l_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤḸ").format(bstack111lllll1ll_opy_[bstack1l1l11l_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧḹ")]))
            if bstack1l1l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭Ḻ") in os.environ:
                logger.debug(bstack1l1l11l_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡣࡶࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠠࡪࡵࠣࡷࡪࡺࠢḻ"))
                data[bstack1l1l11l_opy_ (u"ࠬࡻࡲ࡭ࠩḼ")] = os.environ[bstack1l1l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩḽ")]
            bstack111l1l1llll_opy_ = bstack111l1l111ll_opy_(data[bstack1l1l11l_opy_ (u"ࠧࡶࡴ࡯ࠫḾ")], bstack1ll1l1l1l1l_opy_)
            bstack111l1lll11l_opy_ = os.path.join(bstack1ll1l1l1l1l_opy_, bstack111l1l1llll_opy_)
            os.chmod(bstack111l1lll11l_opy_, 0o777) # bstack111l1lllll1_opy_ permission
            return bstack111l1lll11l_opy_
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡳ࡫ࡷࠡࡕࡇࡏࠥࢁࡽࠣḿ").format(e))
    return binary_path
def bstack111l1l1l111_opy_(bstack111lllll1ll_opy_):
    try:
        if bstack1l1l11l_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨṀ") not in bstack111lllll1ll_opy_[bstack1l1l11l_opy_ (u"ࠪࡳࡸ࠭ṁ")].lower():
            return
        if os.path.exists(bstack1l1l11l_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨṂ")):
            with open(bstack1l1l11l_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢṃ"), bstack1l1l11l_opy_ (u"ࠨࡲࠣṄ")) as f:
                bstack111l1l1ll1l_opy_ = {}
                for line in f:
                    if bstack1l1l11l_opy_ (u"ࠢ࠾ࠤṅ") in line:
                        key, value = line.rstrip().split(bstack1l1l11l_opy_ (u"ࠣ࠿ࠥṆ"), 1)
                        bstack111l1l1ll1l_opy_[key] = value.strip(bstack1l1l11l_opy_ (u"ࠩࠥࡠࠬ࠭ṇ"))
                bstack111lllll1ll_opy_[bstack1l1l11l_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪṈ")] = bstack111l1l1ll1l_opy_.get(bstack1l1l11l_opy_ (u"ࠦࡎࡊࠢṉ"), bstack1l1l11l_opy_ (u"ࠧࠨṊ"))
        elif os.path.exists(bstack1l1l11l_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡦࡲࡰࡪࡰࡨ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧṋ")):
            bstack111lllll1ll_opy_[bstack1l1l11l_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧṌ")] = bstack1l1l11l_opy_ (u"ࠨࡣ࡯ࡴ࡮ࡴࡥࠨṍ")
    except Exception as e:
        logger.debug(bstack1l1l11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡧ࡭ࡸࡺࡲࡰࠢࡲࡪࠥࡲࡩ࡯ࡷࡻࠦṎ") + e)
@measure(event_name=EVENTS.bstack11l11l11ll1_opy_, stage=STAGE.bstack1l1111l11l_opy_)
def bstack111l1l111ll_opy_(bstack11l1111ll11_opy_, bstack111l1ll11ll_opy_):
    logger.debug(bstack1l1l11l_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧṏ") + str(bstack11l1111ll11_opy_) + bstack1l1l11l_opy_ (u"ࠦࠧṐ"))
    zip_path = os.path.join(bstack111l1ll11ll_opy_, bstack1l1l11l_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦṑ"))
    bstack111l1l1llll_opy_ = bstack1l1l11l_opy_ (u"࠭ࠧṒ")
    with requests.get(bstack11l1111ll11_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1l11l_opy_ (u"ࠢࡸࡤࠥṓ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1l11l_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥṔ"))
    with zipfile.ZipFile(zip_path, bstack1l1l11l_opy_ (u"ࠩࡵࠫṕ")) as zip_ref:
        bstack11l11111lll_opy_ = zip_ref.namelist()
        if len(bstack11l11111lll_opy_) > 0:
            bstack111l1l1llll_opy_ = bstack11l11111lll_opy_[0] # bstack11l11111ll1_opy_ bstack11l1l11111l_opy_ will be bstack111ll1llll1_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111l1ll11ll_opy_)
        logger.debug(bstack1l1l11l_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤṖ") + str(bstack111l1ll11ll_opy_) + bstack1l1l11l_opy_ (u"ࠦࠬࠨṗ"))
    os.remove(zip_path)
    return bstack111l1l1llll_opy_
def get_cli_dir():
    bstack111l1l11lll_opy_ = bstack1l1l1l111ll_opy_()
    if bstack111l1l11lll_opy_:
        bstack1ll1l1l1l1l_opy_ = os.path.join(bstack111l1l11lll_opy_, bstack1l1l11l_opy_ (u"ࠧࡩ࡬ࡪࠤṘ"))
        if not os.path.exists(bstack1ll1l1l1l1l_opy_):
            os.makedirs(bstack1ll1l1l1l1l_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l1l1l1l_opy_
    else:
        raise FileNotFoundError(bstack1l1l11l_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤṙ"))
def bstack1ll1l1l1ll1_opy_(bstack1ll1l1l1l1l_opy_):
    bstack1l1l11l_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦṚ")
    bstack111ll111l1l_opy_ = [
        os.path.join(bstack1ll1l1l1l1l_opy_, f)
        for f in os.listdir(bstack1ll1l1l1l1l_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l1l1l1l_opy_, f)) and f.startswith(bstack1l1l11l_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤṛ"))
    ]
    if len(bstack111ll111l1l_opy_) > 0:
        return max(bstack111ll111l1l_opy_, key=os.path.getmtime) # get bstack111ll1l111l_opy_ binary
    return bstack1l1l11l_opy_ (u"ࠤࠥṜ")
def bstack11l1ll1l1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll111ll1ll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll111ll1ll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111l11l11_opy_(data, keys, default=None):
    bstack1l1l11l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡦ࡬ࡥ࡭ࡻࠣ࡫ࡪࡺࠠࡢࠢࡱࡩࡸࡺࡥࡥࠢࡹࡥࡱࡻࡥࠡࡨࡵࡳࡲࠦࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩࡧࡴࡢ࠼ࠣࡘ࡭࡫ࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸࠥࡺ࡯ࠡࡶࡵࡥࡻ࡫ࡲࡴࡧ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡ࡭ࡨࡽࡸࡀࠠࡂࠢ࡯࡭ࡸࡺࠠࡰࡨࠣ࡯ࡪࡿࡳ࠰࡫ࡱࡨ࡮ࡩࡥࡴࠢࡵࡩࡵࡸࡥࡴࡧࡱࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡨࡪࡦࡻ࡬ࡵ࠼࡚ࠣࡦࡲࡵࡦࠢࡷࡳࠥࡸࡥࡵࡷࡵࡲࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡶࡪࡺࡵࡳࡰ࠽ࠤ࡙࡮ࡥࠡࡸࡤࡰࡺ࡫ࠠࡢࡶࠣࡸ࡭࡫ࠠ࡯ࡧࡶࡸࡪࡪࠠࡱࡣࡷ࡬࠱ࠦ࡯ࡳࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠰ࠍࠤࠥࠦࠠࠣࠤࠥṝ")
    if not data:
        return default
    current = data
    try:
        for key in keys:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int):
                current = current[key]
            else:
                return default
        return current
    except (KeyError, IndexError, TypeError):
        return default
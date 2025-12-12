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
bstack1l1l11l_opy_ (u"ࠤࠥࠦࠏࡖࡹࡵࡧࡶࡸࠥࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡩࡧ࡯ࡴࡪࡸࠠࡶࡵ࡬ࡲ࡬ࠦࡤࡪࡴࡨࡧࡹࠦࡰࡺࡶࡨࡷࡹࠦࡨࡰࡱ࡮ࡷ࠳ࠐࠢࠣࠤၜ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack11111llll1_opy_(bstack1111l1111l_opy_=None, bstack1111l11111_opy_=None):
    bstack1l1l11l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡇࡴࡲ࡬ࡦࡥࡷࠤࡵࡿࡴࡦࡵࡷࠤࡹ࡫ࡳࡵࡵࠣࡹࡸ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠩࡶࠤ࡮ࡴࡴࡦࡴࡱࡥࡱࠦࡁࡑࡋࡶ࠲ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡢࡴࡪࡷࠥ࠮࡬ࡪࡵࡷ࠰ࠥࡵࡰࡵ࡫ࡲࡲࡦࡲࠩ࠻ࠢࡆࡳࡲࡶ࡬ࡦࡶࡨࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡶࡹࡵࡧࡶࡸࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡ࡫ࡱࡧࡱࡻࡤࡪࡰࡪࠤࡵࡧࡴࡩࡵࠣࡥࡳࡪࠠࡧ࡮ࡤ࡫ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡕࡣ࡮ࡩࡸࠦࡰࡳࡧࡦࡩࡩ࡫࡮ࡤࡧࠣࡳࡻ࡫ࡲࠡࡶࡨࡷࡹࡥࡰࡢࡶ࡫ࡷࠥ࡯ࡦࠡࡤࡲࡸ࡭ࠦࡡࡳࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤࡶࡡࡵࡪࡶࠤ࠭ࡲࡩࡴࡶࠣࡳࡷࠦࡳࡵࡴ࠯ࠤࡴࡶࡴࡪࡱࡱࡥࡱ࠯࠺ࠡࡖࡨࡷࡹࠦࡦࡪ࡮ࡨࠬࡸ࠯࠯ࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠫ࡭ࡪࡹࠩࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥ࡬ࡲࡰ࡯࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡉࡡ࡯ࠢࡥࡩࠥࡧࠠࡴ࡫ࡱ࡫ࡱ࡫ࠠࡱࡣࡷ࡬ࠥࡹࡴࡳ࡫ࡱ࡫ࠥࡵࡲࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡳࡥࡹ࡮ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡍ࡬ࡴ࡯ࡳࡧࡧࠤ࡮࡬ࠠࡵࡧࡶࡸࡤࡧࡲࡨࡵࠣ࡭ࡸࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤ࠯ࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡷࡪࡶ࡫ࠤࡰ࡫ࡹࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡷࡺࡩࡣࡦࡵࡶࠤ࠭ࡨ࡯ࡰ࡮ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡨࡵࡵ࡯ࡶࠣࠬ࡮ࡴࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡱࡳࡩ࡫ࡩࡥࡵࠣࠬࡱ࡯ࡳࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠠࠩ࡮࡬ࡷࡹ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡦࡴࡵࡳࡷࠦࠨࡴࡶࡵ࠭ࠏࠦࠠࠡࠢࠥࠦࠧၝ")
    try:
        bstack1111l1l111_opy_ = os.getenv(bstack1l1l11l_opy_ (u"ࠦࡕ࡟ࡔࡆࡕࡗࡣࡈ࡛ࡒࡓࡇࡑࡘࡤ࡚ࡅࡔࡖࠥၞ")) is not None
        if bstack1111l1111l_opy_ is not None:
            args = list(bstack1111l1111l_opy_)
        elif bstack1111l11111_opy_ is not None:
            if isinstance(bstack1111l11111_opy_, str):
                args = [bstack1111l11111_opy_]
            elif isinstance(bstack1111l11111_opy_, list):
                args = list(bstack1111l11111_opy_)
            else:
                args = [bstack1l1l11l_opy_ (u"ࠧ࠴ࠢၟ")]
        else:
            args = [bstack1l1l11l_opy_ (u"ࠨ࠮ࠣၠ")]
        if bstack1111l1l111_opy_:
            return _1111l11ll1_opy_(args)
        bstack1111l11l11_opy_ = args + [
            bstack1l1l11l_opy_ (u"ࠢ࠮࠯ࡦࡳࡱࡲࡥࡤࡶ࠰ࡳࡳࡲࡹࠣၡ"),
            bstack1l1l11l_opy_ (u"ࠣ࠯࠰ࡵࡺ࡯ࡥࡵࠤၢ")
        ]
        class bstack11111lllll_opy_:
            bstack1l1l11l_opy_ (u"ࠤࠥࠦࡕࡿࡴࡦࡵࡷࠤࡵࡲࡵࡨ࡫ࡱࠤࡹ࡮ࡡࡵࠢࡦࡥࡵࡺࡵࡳࡧࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠠࡵࡧࡶࡸࠥ࡯ࡴࡦ࡯ࡶ࠲ࠧࠨࠢၣ")
            def __init__(self):
                self.bstack1111l111ll_opy_ = []
                self.test_files = set()
                self.bstack1111l11lll_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1l1l11l_opy_ (u"ࠥࠦࠧࡎ࡯ࡰ࡭ࠣࡧࡦࡲ࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡩࡴࠢࡩ࡭ࡳ࡯ࡳࡩࡧࡧ࠲ࠧࠨࠢၤ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1111l111ll_opy_.append(nodeid)
                        if bstack1l1l11l_opy_ (u"ࠦ࠿ࡀࠢၥ") in nodeid:
                            file_path = nodeid.split(bstack1l1l11l_opy_ (u"ࠧࡀ࠺ࠣၦ"), 1)[0]
                            if file_path.endswith(bstack1l1l11l_opy_ (u"࠭࠮ࡱࡻࠪၧ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1111l11lll_opy_ = str(e)
        collector = bstack11111lllll_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1111l11l11_opy_, plugins=[collector])
        if collector.bstack1111l11lll_opy_:
            return {bstack1l1l11l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣၨ"): False, bstack1l1l11l_opy_ (u"ࠣࡥࡲࡹࡳࡺࠢၩ"): 0, bstack1l1l11l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࡵࠥၪ"): [], bstack1l1l11l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡹࠢၫ"): [], bstack1l1l11l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥၬ"): bstack1l1l11l_opy_ (u"ࠧࡉ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧၭ").format(collector.bstack1111l11lll_opy_)}
        return {
            bstack1l1l11l_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢၮ"): True,
            bstack1l1l11l_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨၯ"): len(collector.bstack1111l111ll_opy_),
            bstack1l1l11l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤၰ"): collector.bstack1111l111ll_opy_,
            bstack1l1l11l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨၱ"): sorted(collector.test_files),
            bstack1l1l11l_opy_ (u"ࠥࡩࡽ࡯ࡴࡠࡥࡲࡨࡪࠨၲ"): exit_code
        }
    except Exception as e:
        return {bstack1l1l11l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧၳ"): False, bstack1l1l11l_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦၴ"): 0, bstack1l1l11l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢၵ"): [], bstack1l1l11l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦၶ"): [], bstack1l1l11l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢၷ"): bstack1l1l11l_opy_ (u"ࠤࡘࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠽ࠤࢀࢃࠢၸ").format(e)}
def _1111l11ll1_opy_(args):
    bstack1l1l11l_opy_ (u"ࠥࠦࠧࡏࡳࡰ࡮ࡤࡸࡪࡪࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡪࡾࡥࡤࡷࡷࡩࡩࠦࡩ࡯ࠢࡤࠤࡸ࡫ࡰࡢࡴࡤࡸࡪࠦࡐࡺࡶ࡫ࡳࡳࠦࡰࡳࡱࡦࡩࡸࡹࠠࡵࡱࠣࡥࡻࡵࡩࡥࠢࡱࡩࡸࡺࡥࡥࠢࡳࡽࡹ࡫ࡳࡵࠢ࡬ࡷࡸࡻࡥࡴ࠰ࠥࠦࠧၹ")
    bstack11111lll1l_opy_ = [sys.executable, bstack1l1l11l_opy_ (u"ࠦ࠲ࡳࠢၺ"), bstack1l1l11l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧၻ"), bstack1l1l11l_opy_ (u"ࠨ࠭࠮ࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡲࡲࡱࡿࠢၼ"), bstack1l1l11l_opy_ (u"ࠢ࠮࠯ࡴࡹ࡮࡫ࡴࠣၽ")]
    bstack1111l11l1l_opy_ = [a for a in args if a not in (bstack1l1l11l_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤၾ"), bstack1l1l11l_opy_ (u"ࠤ࠰࠱ࡶࡻࡩࡦࡶࠥၿ"), bstack1l1l11l_opy_ (u"ࠥ࠱ࡶࠨႀ"))]
    cmd = bstack11111lll1l_opy_ + bstack1111l11l1l_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1111l111ll_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1l1l11l_opy_ (u"ࠦࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠣႁ") in line.lower():
                continue
            if bstack1l1l11l_opy_ (u"ࠧࡀ࠺ࠣႂ") in line:
                bstack1111l111ll_opy_.append(line)
                file_path = line.split(bstack1l1l11l_opy_ (u"ࠨ࠺࠻ࠤႃ"), 1)[0]
                if file_path.endswith(bstack1l1l11l_opy_ (u"ࠧ࠯ࡲࡼࠫႄ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1l1l11l_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤႅ"): success,
            bstack1l1l11l_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣႆ"): len(bstack1111l111ll_opy_),
            bstack1l1l11l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦႇ"): bstack1111l111ll_opy_,
            bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣႈ"): sorted(test_files),
            bstack1l1l11l_opy_ (u"ࠧ࡫ࡸࡪࡶࡢࡧࡴࡪࡥࠣႉ"): proc.returncode,
            bstack1l1l11l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧႊ"): None if success else bstack1l1l11l_opy_ (u"ࠢࡔࡷࡥࡴࡷࡵࡣࡦࡵࡶࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࠪࡨࡼ࡮ࡺࠠࡼࡿࠬࠦႋ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1l1l11l_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤႌ"): False, bstack1l1l11l_opy_ (u"ࠤࡦࡳࡺࡴࡴႍࠣ"): 0, bstack1l1l11l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦႎ"): [], bstack1l1l11l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣႏ"): [], bstack1l1l11l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ႐"): bstack1l1l11l_opy_ (u"ࠨࡓࡶࡤࡳࡶࡴࡩࡥࡴࡵࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ႑").format(e)}
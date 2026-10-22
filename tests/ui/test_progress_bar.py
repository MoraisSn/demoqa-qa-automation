"""Para a barra antes de 25%, retoma até 100% e reinicia."""

import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from pages.progress_bar_page import ProgressBarPage
from tests.ui.browser import chrome_browser


def test_progress_bar_stops_completes_and_resets():
    with chrome_browser("progress_bar") as driver:
        page = ProgressBarPage(driver)
        page.open_from_home()
        assert page.value() == 0
        page.start_or_stop()
        page.wait_for_at_least(10)
        page.start_or_stop()
        stopped_at = page.value()
        assert 0 < stopped_at < 25, f"Barra parou em {stopped_at}%"
        time.sleep(0.35)
        assert page.value() == stopped_at, "A barra continuou avançando após Stop"
        page.start_or_stop()
        page.wait_for_100()
        assert page.value() == 100
        page.reset()
        assert page.value() == 0


if __name__ == "__main__":
    test_progress_bar_stops_completes_and_resets()
    print("Progress Bar: sucesso.")

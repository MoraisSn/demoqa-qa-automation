"""Valida a abertura e o fechamento da nova janela."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from pages.browser_windows_page import BrowserWindowsPage
from tests.ui.browser import chrome_browser

def test_new_window_shows_sample_message():
    
    with chrome_browser("browser_windows") as driver:
        page = BrowserWindowsPage(driver)
        page.open_from_home()
        original_handle = page.open_new_window()
        try:
            assert len(driver.window_handles) == 2
            assert page.sample_page_message() == "This is a sample page"
        finally:
            page.close_new_window_and_return(original_handle)
        assert driver.current_window_handle == original_handle
        assert len(driver.window_handles) == 1


if __name__ == "__main__":
    test_new_window_shows_sample_message()
    print("Browser Windows: sucesso.")


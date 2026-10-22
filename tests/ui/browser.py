"""Abre o navegador e guarda uma captura quando um cenário falha."""

from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from selenium import webdriver

@contextmanager
def chrome_browser(scenario: str):
    browser = webdriver.Chrome()
    browser.set_window_size(1440, 1000)
    try:
        yield browser
    except Exception:
        output = Path(__file__).resolve().parents[2] / "reports" / "screenshots"
        output.mkdir(parents=True, exist_ok=True)
        path = output / f"{scenario}_{datetime.now():%Y%m%d_%H%M%S}.png"
        browser.save_screenshot(str(path))
        print(f"Screenshot da falha: {path}", flush=True)
        raise
    finally:
        browser.quit()


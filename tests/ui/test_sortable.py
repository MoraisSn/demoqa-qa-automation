"""Desordena e recoloca a lista em ordem crescente por drag and drop."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from pages.sortable_page import SortablePage
from tests.ui.browser import chrome_browser


def test_sortable_ascending_with_drag_and_drop():
    expected = ["One", "Two", "Three", "Four", "Five", "Six"]
    with chrome_browser("sortable") as driver:
        page = SortablePage(driver)
        page.open_from_home()
        assert sorted(page.order()) == sorted(expected)
        page.move_before("Six", "One")
        assert page.order() != expected
        page.sort_ascending(expected)
        assert page.order() == expected


if __name__ == "__main__":
    test_sortable_ascending_with_drag_and_drop()
    print("Sortable: sucesso.")

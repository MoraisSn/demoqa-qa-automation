"""Cria, edita e exclui o mesmo registro em Web Tables."""

import sys
from pathlib import Path
from uuid import uuid4

root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from pages.web_tables_page import TableRecord, WebTablesPage
from tests.ui.browser import chrome_browser


def test_create_edit_delete_record():
    email = f"qa_{uuid4().hex[:12]}@example.com"
    record = TableRecord("Natalia", "Silva", email, 27, 4500, "QA")
    updated = TableRecord("Natalia", "Costa", email, 28, 5200, "Automation")

    with chrome_browser("web_tables") as driver:
        page = WebTablesPage(driver)
        page.open_from_home()
        page.add_record(record)
        assert page.record_values(email) == ["Natalia", "Silva", "27", email, "4500", "QA"]
        page.edit_record(email, updated)
        assert page.record_values(email) == ["Natalia", "Costa", "28", email, "5200", "Automation"]
        page.delete_record(email)
        assert page.record_is_absent(email)


if __name__ == "__main__":
    test_create_edit_delete_record()
    print("Web Tables: sucesso.")

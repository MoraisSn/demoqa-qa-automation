"""Preenche todo o Practice Form e confere o popup final."""

import secrets
import sys
from datetime import date
from pathlib import Path
from uuid import uuid4

root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from pages.practice_form_page import PracticeFormPage
from tests.ui.browser import chrome_browser


def test_practice_form():
    state, city = secrets.choice([
        ("NCR", "Delhi"), ("Haryana", "Karnal"),
        ("Uttar Pradesh", "Agra"), ("Rajasthan", "Jaipur"),
    ])
    student = {
        "first_name": secrets.choice(["Natalia", "Ana", "Julia"]),
        "last_name": secrets.choice(["Silva", "Costa", "Oliveira"]),
        "email": f"qa_{uuid4().hex[:12]}@example.com",
        "gender": secrets.choice(["Male", "Female", "Other"]),
        "mobile": "9" + "".join(str(secrets.randbelow(10)) for _ in range(9)),
        "birth_date": date(secrets.randbelow(16) + 1990, secrets.randbelow(12) + 1, secrets.randbelow(28) + 1),
        "subject": secrets.choice(["Maths", "Physics", "English"]),
        "hobby": secrets.choice(["Sports", "Reading", "Music"]),
        "picture": root / "tests" / "fixtures" / "natalia teste.txt",
        "address": f"Rua Teste, {secrets.randbelow(900) + 100}",
        "state": state,
        "city": city,
    }
    assert student["picture"].is_file()

    with chrome_browser("practice_form") as driver:
        page = PracticeFormPage(driver)
        page.open_from_home()
        page.fill(student)
        page.submit()
        summary = page.summary()
        assert summary["Student Name"] == f"{student['first_name']} {student['last_name']}"
        assert summary["Student Email"] == student["email"]
        assert summary["Gender"] == student["gender"]
        assert summary["Mobile"] == student["mobile"]
        assert summary["Date of Birth"] == student["birth_date"].strftime("%d %B,%Y")
        assert summary["Subjects"] == student["subject"]
        assert summary["Hobbies"] == student["hobby"]
        assert summary["Picture"] == student["picture"].name
        assert summary["Address"] == student["address"]
        assert summary["State and City"] == f"{student['state']} {student['city']}"
        page.close_summary()


if __name__ == "__main__":
    test_practice_form()
    print("Practice Form: sucesso.")

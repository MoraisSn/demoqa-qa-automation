"""Passos do bônus BDD para Web Tables."""

from uuid import uuid4

from behave import given, then, when

from pages.web_tables_page import TableRecord, WebTablesPage

@given("que estou na página Web Tables")
def open_web_tables(context):
    context.page = WebTablesPage(context.driver)
    context.page.open_from_home()

@when("crio 12 registros diferentes")
def create_records(context):
    context.records = []
    run_id = uuid4().hex[:8]

    for number in range(1, 13):
        record = TableRecord(
            first_name=f"Teste{number}",
            last_name="QA",
            email=f"qa_{run_id}_{number}@example.com",
            age=20 + number,
            salary=3000 + number,
            department="QA",
        )
        context.page.add_record(record)
        context.records.append(record)

@then("encontro os 12 registros na tabela")
def check_records(context):
    for record in context.records:
        assert context.page.record_values(record.email) == [
            record.first_name, record.last_name, str(record.age),
            record.email, str(record.salary), record.department,
        ]


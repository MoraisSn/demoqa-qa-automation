"""Cadastro, edição, busca e exclusão de registros em Web Tables."""

from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage


@dataclass(frozen=True)
class TableRecord:
    """Dados de um registro da Web Tables."""

    first_name: str
    last_name: str
    email: str
    age: int
    salary: int
    department: str


class WebTablesPage:
    """Cadastra, consulta, edita e exclui registros da tabela."""

    def __init__(self, driver) -> None:
        """Guarda o navegador e configura a espera dos elementos."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.add_button = (By.ID, "addNewRecordButton")
        self.form_fields = (
            (By.ID, "firstName"),
            (By.ID, "lastName"),
            (By.ID, "userEmail"),
            (By.ID, "age"),
            (By.ID, "salary"),
            (By.ID, "department"),
        )
        self.submit_button = (By.ID, "submit")
        self.user_form = (By.ID, "userForm")
        self.search_box = (By.ID, "searchBox")
        self.row_xpath = "//tbody/tr[td[normalize-space()='{email}']]"
        self.table_cell = (By.TAG_NAME, "td")
        self.edit_button = (By.CSS_SELECTOR, "[title='Edit']")
        self.delete_button = (By.CSS_SELECTOR, "[title='Delete']")

    def open_from_home(self) -> None:
        """Abre Web Tables pela página inicial."""
        HomePage(self.driver).open_section("Elements", "Web Tables")
        self.wait.until(EC.element_to_be_clickable(self.add_button))

    def _fill_form(self, record: TableRecord) -> None:
        """Preenche e envia o formulário de registro."""
        values = (
            record.first_name, record.last_name, record.email,
            str(record.age), str(record.salary), record.department,
        )
        for locator, value in zip(self.form_fields, values):
            field = self.wait.until(EC.visibility_of_element_located(locator))
            field.clear()
            field.send_keys(value)
        self.driver.find_element(*self.submit_button).click()
        self.wait.until(EC.invisibility_of_element_located(self.user_form))

    def add_record(self, record: TableRecord) -> None:
        """Adiciona um registro à tabela."""
        self.wait.until(EC.element_to_be_clickable(self.add_button)).click()
        self._fill_form(record)

    def search(self, email: str) -> None:
        """Filtra a tabela pelo e-mail informado."""
        field = self.wait.until(EC.visibility_of_element_located(self.search_box))
        field.clear()
        field.send_keys(email)

    def _row(self, email: str):
        """Localiza a linha do e-mail informado."""
        return self.wait.until(EC.presence_of_element_located((
            By.XPATH, self.row_xpath.format(email=email),
        )))

    def record_values(self, email: str) -> list[str]:
        """Devolve os valores do registro encontrado."""
        self.search(email)
        return [cell.text for cell in self._row(email).find_elements(*self.table_cell)[:6]]

    def edit_record(self, email: str, updated: TableRecord) -> None:
        """Edita o registro identificado pelo e-mail."""
        self.search(email)
        self._row(email).find_element(*self.edit_button).click()
        self._fill_form(updated)

    def delete_record(self, email: str) -> None:
        """Exclui o registro identificado pelo e-mail."""
        self.search(email)
        self._row(email).find_element(*self.delete_button).click()
        self.wait.until(lambda driver: not driver.find_elements(
            By.XPATH, self.row_xpath.format(email=email),
        ))

    def record_is_absent(self, email: str) -> bool:
        """Verifica se o registro não aparece na tabela."""
        self.search(email)
        return not self.driver.find_elements(
            By.XPATH, self.row_xpath.format(email=email),
        )


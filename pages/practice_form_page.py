"""Interações com o formulário de cadastro de estudante."""

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage


class PracticeFormPage:
    """Preenche o Practice Form e consulta o resultado enviado."""

    def __init__(self, driver) -> None:
        """Guarda o navegador e configura a espera dos elementos."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.first_name = (By.ID, "firstName")
        self.last_name = (By.ID, "lastName")
        self.email = (By.ID, "userEmail")
        self.gender_label = "label[for='gender-radio-{gender_id}']"
        self.mobile = (By.ID, "userNumber")
        self.birth_date = (By.ID, "dateOfBirthInput")
        self.birth_month = (By.CLASS_NAME, "react-datepicker__month-select")
        self.birth_year = (By.CLASS_NAME, "react-datepicker__year-select")
        self.birth_day_xpath = (
            "//div[contains(@class,'react-datepicker__day') "
            "and not(contains(@class,'outside-month')) "
            "and normalize-space()='{day}']"
        )
        self.subject = (By.ID, "subjectsInput")
        self.hobby_label = "label[for='hobbies-checkbox-{hobby_id}']"
        self.picture = (By.ID, "uploadPicture")
        self.address = (By.ID, "currentAddress")
        self.state = (By.ID, "react-select-3-input")
        self.city = (By.ID, "react-select-4-input")
        self.option_xpath = "//div[@role='option' and normalize-space()='{value}']"
        self.submit_button = (By.ID, "submit")
        self.modal_title = (By.ID, "example-modal-sizes-title-lg")
        self.modal_rows = (By.CSS_SELECTOR, ".modal-content tbody tr")
        self.modal_cell = (By.TAG_NAME, "td")
        self.modal_container = (By.CSS_SELECTOR, ".modal.show")

    def open_from_home(self) -> None:
        """Abre o Practice Form pela página inicial."""
        HomePage(self.driver).open_section("Forms", "Practice Form")
        self.wait.until(EC.visibility_of_element_located(self.first_name))

    def _fill(self, locator: tuple[str, str], value: str) -> None:
        """Limpa um campo e digita o valor recebido."""
        field = self.driver.find_element(*locator)
        field.clear()
        field.send_keys(value)

    def _choose_option(self, locator: tuple[str, str], value: str) -> None:
        """Seleciona uma opção em um campo com sugestões."""
        field = self.driver.find_element(*locator)
        field.send_keys(value)
        self.wait.until(EC.visibility_of_element_located((
            By.XPATH, self.option_xpath.format(value=value),
        )))
        field.send_keys(Keys.ENTER)

    def fill(self, student: dict) -> None:
        """Preenche todos os campos com os dados do estudante."""
        self._fill(self.first_name, student["first_name"])
        self._fill(self.last_name, student["last_name"])
        self._fill(self.email, student["email"])
        gender_id = {"Male": 1, "Female": 2, "Other": 3}[student["gender"]]
        self.driver.find_element(By.CSS_SELECTOR, self.gender_label.format(gender_id=gender_id)).click()
        self._fill(self.mobile, student["mobile"])

        self.driver.find_element(*self.birth_date).click()
        Select(self.driver.find_element(*self.birth_month)).select_by_index(student["birth_date"].month - 1)
        Select(self.driver.find_element(*self.birth_year)).select_by_visible_text(str(student["birth_date"].year))
        self.driver.find_element(By.XPATH, self.birth_day_xpath.format(day=student["birth_date"].day)).click()

        self._choose_option(self.subject, student["subject"])
        hobby_id = {"Sports": 1, "Reading": 2, "Music": 3}[student["hobby"]]
        self.driver.find_element(By.CSS_SELECTOR, self.hobby_label.format(hobby_id=hobby_id)).click()
        self.driver.find_element(*self.picture).send_keys(str(student["picture"].resolve()))
        self._fill(self.address, student["address"])
        self._choose_option(self.state, student["state"])
        self._choose_option(self.city, student["city"])

    def submit(self) -> None:
        """Envia o formulário."""
        button = self.driver.find_element(*self.submit_button)
        button.send_keys(Keys.ENTER)

    def summary(self) -> dict[str, str]:
        """Lê os campos exibidos no modal de confirmação."""
        self.wait.until(EC.visibility_of_element_located(self.modal_title))
        rows = self.driver.find_elements(*self.modal_rows)
        return {row.find_elements(*self.modal_cell)[0].text: row.find_elements(*self.modal_cell)[1].text for row in rows}

    def close_summary(self) -> None:
        """Fecha o modal clicando fora da caixa de conteúdo."""
        modal = self.wait.until(EC.visibility_of_element_located(self.modal_container))
        ActionChains(self.driver).move_to_element(modal).move_by_offset(
            -modal.size["width"] // 2 + 20, 0
        ).click().perform()
        self.wait.until(EC.invisibility_of_element_located(self.modal_title))


"""Controles e leitura do valor da barra de progresso."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage


class ProgressBarPage:
    """Controla a barra de progresso e consulta seu valor."""

    def __init__(self, driver) -> None:
        """Guarda o navegador e configura a espera da barra."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 20, poll_frequency=0.05)
        self.progress_container = (By.ID, "progressBar")
        self.progress_value = (By.CSS_SELECTOR, "#progressBar [role='progressbar']")
        self.start_stop_button = (By.ID, "startStopButton")
        self.reset_button = (By.ID, "resetButton")

    def open_from_home(self) -> None:
        """Abre Progress Bar pela página inicial."""
        HomePage(self.driver).open_section("Widgets", "Progress Bar")
        self.wait.until(EC.visibility_of_element_located(self.progress_container))

    def value(self) -> int:
        """Lê a porcentagem atual da barra."""
        bar = self.driver.find_element(*self.progress_value)
        return int(bar.get_attribute("aria-valuenow"))

    def start_or_stop(self) -> None:
        """Inicia ou pausa a barra pelo botão da página."""
        self.wait.until(EC.element_to_be_clickable(self.start_stop_button)).click()

    def wait_for_at_least(self, value: int) -> int:
        """Espera a barra atingir ao menos a porcentagem indicada."""
        self.wait.until(lambda driver: self.value() >= value)
        return self.value()

    def wait_for_100(self) -> None:
        """Espera a barra chegar a 100%."""
        self.wait.until(lambda driver: self.value() == 100)

    def reset(self) -> None:
        """Reinicia a barra e espera o valor voltar a zero."""
        self.wait.until(EC.element_to_be_clickable(self.reset_button)).click()
        self.wait.until(lambda driver: self.value() == 0)


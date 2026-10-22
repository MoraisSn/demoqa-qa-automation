from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage


class BrowserWindowsPage:
    """Controla a nova janela aberta pelo Browser Windows."""

    def __init__(self, driver, timeout: int = 15) -> None:
        """Guarda o navegador e define o tempo de espera."""
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.new_window_button = (By.ID, "windowButton")
        self.sample_message = (By.ID, "sampleHeading")

    def open_from_home(self) -> None:
        """Abre Browser Windows pela página inicial."""
        HomePage(self.driver).open_section("Alerts, Frame & Windows", "Browser Windows")

    def open_new_window(self) -> str:
        """Abre a nova janela e devolve o identificador da original."""
        original_handle  = self.driver.current_window_handle
        previous_handles = set(self.driver.window_handles)
        
        self.wait.until(EC.element_to_be_clickable(self.new_window_button)).click()
        self.wait.until(EC.new_window_is_opened(list(previous_handles)))
        new_handles = set(self.driver.window_handles) - previous_handles
        
        if len(new_handles) != 1:
            raise RuntimeError("Era esperada exatamente uma nova janela")
        self.driver.switch_to.window(new_handles.pop())
        return original_handle

    def sample_page_message(self) -> str:
        """Lê a mensagem exibida na nova janela."""
        return self.wait.until(EC.visibility_of_element_located(self.sample_message)).text

    def close_new_window_and_return(self, original_handle: str) -> None:
        """Fecha a nova janela e volta para a original."""
        self.driver.close()
        self.driver.switch_to.window(original_handle)


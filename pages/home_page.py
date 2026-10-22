"""Navegação a partir da página inicial do DemoQA."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HomePage:
    """Navega da página inicial para uma opção do menu."""

    URL = "https://demoqa.com/"

    def __init__(self, driver) -> None:
        """Guarda o navegador e configura a espera dos elementos."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.card_xpath = "//div[contains(concat(' ', normalize-space(@class), ' '), ' card ')][.//h5[normalize-space()='{category}']]"
        self.menu_item_xpath = "//span[normalize-space()='{item}']"

    def open_section(self, category: str, item: str) -> None:
        """Abre o item indicado dentro da categoria."""
        self.driver.get(self.URL)
        card = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, self.card_xpath.format(category=category),
        )))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
        card.click()
        link = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, self.menu_item_xpath.format(item=item),
        )))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        self.driver.execute_script("arguments[0].click();", link)
        self.wait.until(EC.url_changes(self.URL))
        self.driver.execute_script("window.scrollTo(0, 0);")


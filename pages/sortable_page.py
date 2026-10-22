"""Leitura e drag and drop dos itens da lista Sortable."""

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage


class SortablePage:
    """Lê e altera a ordem dos itens da lista Sortable."""

    def __init__(self, driver) -> None:
        """Guarda o navegador e configura a espera dos itens."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.items = (By.CSS_SELECTOR, "#demo-tabpane-list .list-group-item")

    def open_from_home(self) -> None:
        """Abre Sortable pela página inicial."""
        HomePage(self.driver).open_section("Interactions", "Sortable")
        self.wait.until(EC.visibility_of_element_located(self.items))

    def order(self) -> list[str]:
        """Devolve os itens na ordem exibida na página."""
        return [item.text for item in self.driver.find_elements(*self.items)]

    def move_before(self, label: str, next_label: str) -> None:
        """Arrasta um item para antes de outro."""
        items = self.driver.find_elements(*self.items)
        names = [item.text for item in items]
        source_index = names.index(label)
        target_index = names.index(next_label)
        if source_index < target_index:
            return

        drag = ActionChains(self.driver).click_and_hold(items[source_index]).pause(0.3)
        for item in reversed(items[target_index:source_index]):
            drag.move_to_element(item).pause(0.2)
        drag.release().perform()

        self.wait.until(lambda driver: self.order().index(label) < self.order().index(next_label))

    def sort_ascending(self, expected: list[str]) -> None:
        """Reorganiza os itens conforme a ordem esperada."""
        for index, label in enumerate(expected):
            current = self.order()
            if current[index] != label:
                self.move_before(label, current[index])


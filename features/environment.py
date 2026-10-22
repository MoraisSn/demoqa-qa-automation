"""Abre e fecha o Chrome para cada cenário BDD."""

import sys
from pathlib import Path

from selenium import webdriver

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def before_scenario(context, scenario):
    context.driver = webdriver.Chrome()
    context.driver.set_window_size(1440, 1000)

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()

import selenium.webdriver.chrome.options
import selenium.webdriver.common.by
import selenium.webdriver.support.expected_conditions
import selenium.webdriver.support.ui
import selenium.webdriver.support
import os
import pandas
import tqdm
import json
import multiprocessing
import time
import bs4

class Browser:

    def __init__(
        self, 
        display: bool
    ) -> None:
        self.display = display
        return
    
    def openClient(self) -> bool:
        option = selenium.webdriver.chrome.options.Options()
        option.add_argument(
            "--disable-blink-features=AutomationControlled"
        )
        option.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        option.add_argument("--disable-notifications")
        option.add_argument("user-agent=Chromium")
        if(not self.display):
            option.add_argument("--headless")
            pass
        client = selenium.webdriver.Chrome(options=option)
        self.client = client
        return(True)

    def visitPage(self, link: str) -> bool:
        self.client.get(link)
        return(True)

    def closeClient(self) -> bool:
        self.client.quit()
        return(True)
    
    def saveScreen(self, path: str) -> bool:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.client.save_screenshot(path)
        return(True)    

    rule = selenium.webdriver.common.by.By
    event = selenium.webdriver.support.ui.WebDriverWait
    condition = selenium.webdriver.support.expected_conditions
    selection = selenium.webdriver.support.ui.Select
    pass
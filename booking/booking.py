from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import booking.constants as const

class Booking(webdriver.Chrome): # extends webdriver.Chrome
    def __init__(self, isExit = False):
        self.isExit = isExit

        options = Options()
        options.add_experimental_option("detach", True)

        super(Booking, self).__init__(options=options) # initialize instance webdriver.Chrome

        self.implicitly_wait(10)

    def __exit__(self, exc_type, exc, traceback):
        if self.isExit:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

        try: 
            self.find_element(By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info."]').click() # click dismiss sign in
        except: 
            print("okay")

    def change_currency(self, currency):
        currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        select_currency_element = self.find_elements(By.CLASS_NAME, "ea1163d21f")

        for item in select_currency_element:
            if currency in item.text:
                item.click()
                break
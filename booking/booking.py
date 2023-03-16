from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from prettytable import PrettyTable

import booking.constants as const
from booking.booking_report import BookingReport

class Booking(webdriver.Chrome): # extends webdriver.Chrome
    def __init__(self, isExit = False):
        self.isExit = isExit

        options = Options()
        options.add_experimental_option("detach", True)

        super(Booking, self).__init__(options=options) # initialize instance webdriver.Chrome

        self.implicitly_wait(10)
        self.maximize_window()

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
    
    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.CSS_SELECTOR, 'input[name="ss"]')
        search_field.clear()
        search_field.send_keys(place_to_go)

        time.sleep(2)
        first_search = self.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/form/div[1]/div[1]/div/div/div[2]/ul/li[1]')
        first_search.click()
    
    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]')
        check_in_element.click()

        check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
        check_out_element.click()

    def select_adults(self, count):
        selection_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]/button[1]')
            decrease_adults_element.click() # decrease quantity for adult
            
            adults_value_element = self.find_element(By.ID, "group_adults")
            adults_value = adults_value_element.get_attribute('value') # Should give back the adults count

            if int(adults_value) == 1:
                break
        
        increase_button_element = self.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]/button[2]')
        
        for _ in range(count -1): # 0 -> count - 1 time
            increase_button_element.click()
    
    def click_search(self):
        search_element = self.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/form/div[1]/div[4]/button')
        search_element.click()

    def get_quantity_paging(self):
        return self.find_element(By.CSS_SELECTOR, 'ol.a8b500abde li:last-child button').get_attribute('innerHTML').strip()

    def report_results(self):
        hotel_cards = self.find_element(By.CLASS_NAME, 'd4924c9e74')
        total_paging = int(self.get_quantity_paging())

        result = []
        for pag in range(total_paging):
            if(not pag == 0):
                next_page_element = self.find_element(By.CSS_SELECTOR, f"ol.a8b500abde li button[aria-label~='{pag+1}']")
                next_page_element.click()
                time.sleep(6)
                hotel_cards = self.find_element(By.CLASS_NAME, 'd4924c9e74')

            report = BookingReport(hotel_cards)
            result += report.pull_deal_card_attributes()

            del report

        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(result)

        print(table)



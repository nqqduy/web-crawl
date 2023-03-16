from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
# The specific data that we need from each one of the deal boxes

class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_cards = self.pull_deal_cards() # contain all hotel card in one page
        
    def pull_deal_cards(self):
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
    
    def pull_deal_card_attributes(self) -> str:
        collection = []

        for deal_card in self.deal_cards:
            hotel_name = deal_card.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute("innerHTML").strip()
            hotel_price = deal_card.find_element(By.CSS_SELECTOR, 'div[data-testid="availability-rate-information"]').find_element(By.CLASS_NAME, 'fcab3ed991').get_attribute("innerHTML").strip()
            hotel_price = hotel_price.split(";")[1]

            try: 
                hotel_core = deal_card.find_element(By.CLASS_NAME, 'd10a6220b4').get_attribute("innerHTML").strip()
            except:
                hotel_core = "not found"

            collection.append([hotel_name, hotel_price, hotel_core])

        return collection
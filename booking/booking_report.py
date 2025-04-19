# This file is going to include method that will parse
# the specific data that we need from each one of the deal boxes.
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingReport:
    def __init__(self, boxes_section_element: list[WebElement]):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        collection = []
        len = 0
        for box_element in self.boxes_section_element:
            len += 1
            hotel_name = box_element.find_element(
            By.CSS_SELECTOR,
            f'div[data-testid="title"]'
            ).get_attribute('innerHTML').strip()

            # Need to use the try except as some element don't have review score.
            try:
                review_score = WebDriverWait(box_element, 1).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div[data-testid="review-score"]')
                    )
                ).get_attribute('textContent').strip().split()[1]

            except Exception as e:
                review_score = "N/A"

            price = box_element.find_element(
                By.CSS_SELECTOR,
                f'span[data-testid="price-and-discounted-price"]'
            ).get_attribute('textContent').strip()


            collection.append([len, hotel_name, review_score, price])
        return collection


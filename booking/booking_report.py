# This file is going to include method that will parse
# the specific data that we need from each one of the deal boxes.
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class BookingReport:
    def __init__(self, boxes_section_element: list[WebElement]):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        collection = []
        for box_element in self.boxes_section_element:

            hotel_name = box_element.find_element(
            By.CSS_SELECTOR,
            f'div[data-testid="title"]'
            ).get_attribute('innerHTML').strip()

            review_score = box_element.find_element(
                By.CSS_SELECTOR,
                "div.a3b8729ab1.d86cee9b25"
            ).get_attribute('textContent').strip().split()[-1]

            collection.append([hotel_name, review_score])
        # print(collection)
        return collection


# This file is going to include method that will parse
# the specific data that we need from each one of the deal boxes.
from selenium.webdriver.common.by import By


class BookingReport:
    def __init__(self, boxes_section_element):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            By.CSS_SELECTOR,
            f'div[aria-label="Property"]'
        )
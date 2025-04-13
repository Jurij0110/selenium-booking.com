from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_star_rating(self, star_elements: list[int]):
        try:
            dismiss_button = self.driver.find_element(
                By.XPATH,
                "//button[@aria-label='Dismiss sign-in info.']"
            )
            self.driver.execute_script("arguments[0].click();", dismiss_button)
            print("Dismissed the sign-in popup")
            time.sleep(1)
        except NoSuchElementException:
            print("No sign-in popup found, proceeding...")

        for star_element in star_elements:
            star_element_component = self.driver.find_element(
                By.XPATH,
                # "//label[.//div[contains(text(), '2 stars')]]"
                # "//input[contains(@aria-label, '4 stars')]"
                f"//input[contains(@aria-label, '{star_element} stars')]"
            )
            star_element_component.click()
            time.sleep(2)
            print("Selected the star rating")


    def sort_price_lowest(self):
        sorters_dropdown = self.driver.find_element(
            By.CSS_SELECTOR,
            f'button[data-testid="sorters-dropdown-trigger"'
        )
        sorters_dropdown.click()

        lowest_first = self.driver.find_element(
            By.CSS_SELECTOR,
            f'button[aria-label="Price (lowest first)"]'
        )
        lowest_first.click()
        print("Successfully sorted price lowest")

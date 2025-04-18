import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport


class Booking(webdriver.Chrome):
    def __init__(self, teardown=False):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.teardown = teardown
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(3)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            print("Quitting ")
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        try:
            # Step 1: Dismiss popup if present
            try:
                dismiss_button = self.find_element(
                    By.XPATH,
                    "//button[@aria-label='Dismiss sign-in info.']"
                )
                self.execute_script("arguments[0].click();", dismiss_button)
                print("Dismissed the sign-in popup")
                time.sleep(1)
            except NoSuchElementException:
                print("No sign-in popup found, proceeding...")

            # Step 2: Open the currency picker
            currency_element = self.find_element(
                By.CSS_SELECTOR,
                'button[data-testid="header-currency-picker-trigger"]'
            )

            self.execute_script("arguments[0].click();", currency_element)
            print("Opened currency picker")
            time.sleep(1)  # Wait for dropdown to appear

            # Step 3: Find and click the currency option
            try:
                selected_currency = self.find_element(
                    By.XPATH,
                    f"//button[.//div[contains(@class, 'CurrencyPicker_currency') and text()='{currency}']]"
                )

                # Get and print text
                button_text = self.execute_script("return arguments[0].innerText;", selected_currency)
                print("Button text:", button_text)

                selected_currency.click()

                # Pause to observe the result
                # time.sleep(2)


            except NoSuchElementException:
                print("No currency selected, proceeding...")

        except Exception as e:
            print("Error:", e)

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(
            By.ID,
            ":rh:"
        )
        search_field.clear()
        search_field.send_keys(place_to_go)
        time.sleep(2)
        first_result = self.find_element(
            By.CSS_SELECTOR,
            'li[id="autocomplete-result-0"]'
        )
        first_result.click()

    def select_dates(self, checkin_date, checkout_date):
        checkin_element = self.find_element(
            By.CSS_SELECTOR,
            f'span[data-date="{checkin_date}"]'
        )
        checkout_element = self.find_element(
            By.CSS_SELECTOR,
            f'span[data-date="{checkout_date}"]'
        )
        checkin_element.click()
        checkout_element.click()

    def select_adults(self, number_adults=1):
        adults_element = self.find_element(
            By.CSS_SELECTOR,
            f'button[data-testid="occupancy-config"]'
        )
        adults_element.click()

        adults_button_decrease = self.find_element(
            By.CSS_SELECTOR,
            f'button[class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 bb803d8689 e91c91fa93"]'
        )

        adults_value_element = self.find_element(
            By.ID,
            "group_adults"
        )

        number = int(adults_value_element.get_attribute("aria-valuenow"))
        print("The current number of adults is", number)

        # Change the default value to the lowest before increasing.
        while number > 1:
            adults_button_decrease.click()
            number = number - 1

        adults_button_increase = self.find_element(
            By.CSS_SELECTOR,
            f'button[class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 bb803d8689 f4d78af12a"]'
        )
        while number < number_adults:
            adults_button_increase.click()
            number = number + 1

        travel_with_pets = self.find_element(
            By.ID,
            "pets"
        )
        is_checked = travel_with_pets.get_attribute("aria-checked") == "true"
        print(f"Pets checkbox is currently: {'checked' if is_checked else 'unchecked'}")
        if not is_checked:
            label = self.find_element(By.XPATH, "//label[@for='pets']")
            self.execute_script("arguments[0].scrollIntoView(true);", label)
            time.sleep(0.5)
            self.execute_script("arguments[0].click();", label)
            # travel_with_pets.click()
            print("Clicked to enable pets checkbox")
        else:
            print("Pets checkbox is already enabled")

        search_button = WebDriverWait(self, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        f'button[class="a83ed08757 c21c56c305 bf0537ecb5 ab98298258 a2abacf76b af7297d90d c213355c26 b9fd3c6b3c"]'))
        )
        search_button.click()

    def submit(self):
        submit_button = self.find_element(
            By.CSS_SELECTOR,
            f'button[type="submit"]'
        )
        submit_button.click()


    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(star_elements=[2,3,4])

        filtration.sort_price_lowest()

    def report_results(self):

        hotel_box = self.find_elements(
            By.CSS_SELECTOR,
            f'div[aria-label="Property"]'
        )
        report = BookingReport(hotel_box)

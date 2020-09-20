import time
from selenium.webdriver.common.keys import Keys
from amazon_config import (
    get_chrome_web_driver,
    get_web_driver_options,
    set_browser_as_incognito,
    set_automation_as_head_less,
    set_ignore_certificate_error,
    DIRECTORY,
    NAME,
    CURRENCY,
    MIN_PRICE,
    MAX_PRICE,
    FILTERS,
    BASE_URL,
)


class GenerateReport:
    def __init__(self):
        pass


class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        """
        Init all needed variables and mehtods for the API to work
        """
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        # TODO:: change the filter so it is a function that finds the elements on the page and click on them
        # For now this is empty because o don't want to do it the way the turoial is doing it
        self.price_filter = ''

    def run(self):
        """
        Main method for the script

        :return: None
        """
        # Print to the terminal
        print("Starting script...")
        print(f"Looking for {self.search_term} prodcuts...")
        links = self.get_products_links()
        # do stuff

        return None

    def get_products_links(self):
        self.driver.get(self.base_url)


if __name__ == '__main__':
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = amazon.run()

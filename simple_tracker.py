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
        # Open url
        self.driver.get(self.base_url)
        # find the search bar by ID
        amazon_search_box = self.driver.find_element_by_id(
            'twotabsearchtextbox')
        # type in the search bar the {search_term}
        amazon_search_box.send_keys(self.search_term)
        # press enter
        amazon_search_box.send_keys(Keys.ENTER)
        # give the page time to load
        time.sleep(2)
        # TODO:: implement the filtering for price rnage and type

        # this xpath will match the whole table of results, each result is an element of that table
        results_list = self.driver.find_elements_by_xpath(
            "//div[@class='s-main-slot s-result-list s-search-results sg-row']")
        items_links = []
        try:
            # match all the search results elements by xpath
            search_results = results_list[0].find_elements_by_xpath(
                "//div/div[1]/div/div/div[1]/h2/a")
            # collect the links from href
            items_links = [link.get_attribute('href')
                           for link in search_results]
            return items_links
        except Exception as e:
            print("Did not find products, got the below error:")
            print(e)
        return items_links


if __name__ == '__main__':
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = amazon.run()

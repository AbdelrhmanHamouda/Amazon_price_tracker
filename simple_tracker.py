import time
import re
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

        # a check to make sure links var is not empty
        if not links:
            print("'links' are empty, stopping the script")
            return
        print(f"got {len(links)} links to product...")
        print("Getting products info...")

        products = self.get_products_info(links)

        return None

    def get_products_info(self, links):
        """
        Method to get information about the found products

        :param: links       - list of links to products
        :return: products   - list of products and its info
        """
        # get all uniq ids "asin"
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products

    def get_single_product_info(self, asin):
        """
        Method to collect product information based on asin

        :param: asin - product id
        :return:  <to update>
        """
        print(f"Product ID: {asin} - getting info...")
        product_short_url = self.shorten_link(asin)
        # test it works
        self.driver.get(f'{product_short_url}')
        time.sleep(2)

        # Get product info
        title = self.get_title(product_short_url)
        seller = self.get_seller(product_short_url)
        price = self.get_price(product_short_url)

        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_seller(self, product_short_url):
        pass

    def get_title(self, product_short_url):
        """
        Method to locate the product title.

        :param:     product_short_url - url for the product
        :return:    title - string, product title.
        """
        try:
            title = self.driver.find_element_by_id('productTitle').text
            return title
        except:
            return f"Could not get title for {product_short_url}"

    def get_price(self, product_short_url):
        """
        Method to locate the product title.

        :param:     product_short_url - url for the product
        :return:    price - string, product title.
        """
        try:
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            return price
        except:
            return f"Could not get price for {product_short_url}"

    def shorten_link(self, asin):
        """
        Method to shorten the link so it is easier to handle

        :param: asin - will be used to shorten the link
        :return: short_link - shortend link for the product
        """
        return self.base_url + 'dp/' + asin

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    def get_asin(self, link):
        """
        Method uses regex to match the asin name from the url

        :param: link - to extract the asin from 
        :return: asin - the asin number as a string 
        """
        # use regex to get the asin
        regex = re.compile('https.*/dp/(\w+)/ref=.*')
        try:
            asin = regex.match(link).group(1)
            return str(asin)
        # handle regex failing because of no match in link
        except AttributeError:
            return ""

    def get_products_links(self):
        """
        Method to collect product links

        :return: items_links - list of links
        """
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

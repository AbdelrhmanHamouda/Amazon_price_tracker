import time
import json
from datetime import datetime
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
    DEPARTMENT,
)


class GenerateReport:
    """
    Class to generate json reports based on the collected data
    """
    # TODO:: Solve issue with report reporting best price is Null

    def __init__(self, file_name, filters, base_link, currency, data):
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        self.currency = currency
        self.data = data
        report = {
            'Title': self.file_name,
            'Date': self.get_now(),
            'Best Item': self.get_best_item(),
            'currency': self.currency,
            'base_link': self.base_link,
            'products': self.data
        }
        print("Creating report...")
        with open(f'{DIRECTORY}/{file_name}.json', 'w') as fh:
            json.dump(report, fh)
        print("Report generation completed.")

    def get_now(self):
        """
        Method to get the current time

        :return: time - with %d/%m/%Y %H:%M:%S format
        """
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def get_best_item(self):
        """
        Method to sort the results and get the best price

        :return: sorted.price[0] or None in case of an exception
        """
        try:
            # The lamda function greps the "price" info for each product
            return sorted(self.data, k=lambda k: k['price'])[0]
        except:
            print("Got a problem while sorting items...")
            return None


class AmazonAPI:
    """
    Class to collect indo about the provided product
    """
    # TODO:: solve issues with currency detection

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

        return products

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
        """
        Method to locate the product seller name.

        :param:     product_short_url - url for the product
        :return:    seller - string, product title.
        """
        try:
            seller = self.driver.find_element_by_id('bylineInfo').text
            return seller
        except:
            return f"Could not get seller for {product_short_url}"

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
        Method to locate the product price.

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

    def apply_filter(self, min_price=0, max_price=999999, DEPARTMENT=''):
        """
        Method to apply the max, min prices and department (if know)

        :param: min_price, int  - min price to apply
        :param: max_price, int  - max price to apply
        :param: department , str    - department to use (not used )

        :return: None
        """
        # find the min price box
        amazon_min_price_box = self.driver.find_element_by_id('low-price')
        # find the max price box
        amazon_max_price_box = self.driver.find_element_by_id('high-price')
        # find go button
        amazon_go_button_for_price = self.driver.find_element_by_xpath(
            '//*[@id="a-autoid-1"]/span/input')
        # add value to the min price box
        amazon_min_price_box.send_keys(int(min_price))
        time.sleep(0.5)
        # add value to the max price box
        amazon_max_price_box.send_keys(int(max_price))
        time.sleep(0.5)
        # press go
        amazon_go_button_for_price.click()

    def get_products_links(self):
        """
        Method to collect product links

        : return: items_links - list of links
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
        # filtering for price rnage and type
        self.apply_filter(MIN_PRICE, MAX_PRICE, DEPARTMENT)

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
    GenerateReport(NAME, FILTERS, BASE_URL, CURRENCY, data)

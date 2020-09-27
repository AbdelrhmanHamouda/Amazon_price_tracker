from selenium import webdriver

DIRECTORY = 'reports'
NAME = "iphone 11"
CURRENCY = "€"
MIN_PRICE = "275"
MAX_PRICE = "650"
DEPARTMENT = ''


FILTERS = {
    'min': MIN_PRICE,
    'max': MAX_PRICE
}

BASE_URL = 'https://www.amazon.com/'


def get_chrome_web_driver(options):
    """
    Functions to get the Chrome webdriver and pass it the options as well

    :param: options - list of options 
    :return: webdriver object
    """
    return webdriver.Chrome("./chromedriver", chrome_options=options)


def get_web_driver_options():
    """
    Functions to get the chrome webdriver options

    :return: webdriver.ChromeOptions
    """
    return webdriver.ChromeOptions()


def set_ignore_certificate_error(options):
    """
    Functions to add the 'ignore certificate errors while run' to the options list

    :param: options list
    """
    options.add_argument('--ignore-certificate-errors')


def set_browser_as_incognito(options):
    """
    Functions to add the 'run chrome in incognito mode' to the options list

    :param: options list
    """
    options.add_argument('--incognito')


def set_automation_as_head_less(options):
    options.add_argument('--headless')

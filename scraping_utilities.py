""" Commonly used functions to scrape or automate. """
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from bs4 import BeautifulSoup


def get_gecko_browser(headless=True):
    """ Get an instance of the Firefox driver """
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    service = FirefoxService(executable_path='geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def get_chrome_browser(headless=True, hide=False, user_agent=False, proxy=False):
    """ Get an instance of the Chrome driver. """
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless")
    if hide:
        options.add_argument('--no-sandbox')
        # options.add_argument('--start-maximized')
        # options.add_argument('--start-fullscreen')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("disable-infobars")

    if proxy:
        # TODO get proxy service
        proxy = ''
        options.add_argument("--proxy-server=%s" % proxy)
    if user_agent:
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    service = ChromeService(executable_path='chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    if hide:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })
    return driver


def request_soup(url: str) -> BeautifulSoup:
    """ Fetch the HTML response from the given URL,
        and return the BeautifulSoup object.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import warnings
from fake_useragent import UserAgent



def initialize_driver():

    path = '/Users/ckelaid/Downloads/chromedriver_win32/chromedriver'


    driver = set_driver_options(path)

    #driver = webdriver.Chrome(path, options=chrome_options)

    return driver



def set_driver_options(path):

    chrome_options = Options()

    # set random user-agent
    #set_userAgent(chrome_options) # Not all random user agents work with Captcha 

    # set headless
    #chrome_options.headless = True

    # Avoid detection
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(path, options=chrome_options)

    set_viewport_size(driver, 1920, 1080)

    # Change the property value of the navigator for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


    # User agent that works with Captcha
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.4103.53 Safari/537.36'})

    # Print user-agent
    #print(driver.execute_script("return navigator.userAgent;"))

    return driver



def set_userAgent(chrome_options):

    ua = UserAgent().random
    #print(ua)
    chrome_options.add_argument(f'user-agent={ua}')
    



def set_viewport_size(driver, width, height):

    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

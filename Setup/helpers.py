# Helper functions

import time 
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import math
import pandas as pd
import warnings
import pickle
import GetSalary
import importlib
import scrape2_2 as scr2
import driver_config as dc
import numpy as np
import scipy.interpolate as si
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
importlib.reload(scr2)
importlib.reload(dc)

# Remove DevTools warning
#chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])



def human_like_mouse(action:ActionChains, startElem):
    # B-spline function
    # Curve base:
    points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]]
    points = np.array(points)

    x = points[:,0]
    y = points[:,1]


    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)

    x_tup = si.splrep(t, x, k=3)
    y_tup = si.splrep(t, y, k=3)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list) # x interpolate values
    y_i = si.splev(ipl_t, y_list) # y interpolate values

    
    start_element = startElem

    action.move_to_element(start_element)
    action.perform()

    c = 5
    i = 0
    for mouse_x, mouse_y in zip(x_i, y_i):
        action.move_by_offset(mouse_x,mouse_y)
        action.perform()
        #print("Move mouse to, %s ,%s" % (mouse_x, mouse_y))   
        i += 1    
        if i == c:
            break




def bypassCaptcha1():

    # Switch to captcha iframe
    iframe = browser.find_elements(By.TAG_NAME,'iframe')[0]
    browser.switch_to.frame(iframe)
    iframe = browser.find_elements(By.TAG_NAME,'iframe')[0]
    browser.switch_to.frame(iframe)
    
    # Captcha check button
    captcha_check = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='recaptcha-anchor']")))
    browser.implicitly_wait(12)
    action =  ActionChains(browser)
    # Simulate human like mouse movements
    human_like_mouse(action, captcha_check)
    captcha_check.click() # Click captcha check


    browser.implicitly_wait(8)
    action =  ActionChains(browser)
    human_like_mouse(action, captcha_check)

    browser.switch_to.default_content()

    print('\nSuccessfuly bypassed Captcha 1!\n')




# Check if we get second captcha check
#  if browser.find_elements(By.TAG_NAME,'iframe')[0].text.startswith('Request unsuccessful.'):

def bypassCaptcha2():

    t = random.randint(8,10)
    browser.implicitly_wait(t)

    iframe2 = browser.find_elements(By.TAG_NAME,"iframe")[0]
    browser.switch_to.frame(iframe2)
    iframe3 = browser.find_elements(By.XPATH,"//iframe[@title='recaptcha challenge expires in two minutes']")[0]
    browser.switch_to.frame(iframe3)
    # Find nearest element to #shadow-root (closed)
    elem = browser.find_element(By.XPATH, '//div[@class="button-holder help-button-holder"]')
    browser.implicitly_wait(10)
    elem.click() # click on it
    browser.switch_to.default_content()

    print('\nSuccessfuly bypassed Captcha 2!\n')  
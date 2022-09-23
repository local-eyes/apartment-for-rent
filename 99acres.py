import datetime
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome("chromedriver", chrome_options=options)
driver.get("https://www.99acres.com/search/property/rent/pratap-nagar-jaipur?city=177&locality=2326&preference=R&area_unit=1&res_com=R")
driver.maximize_window()
time.sleep(5)
cons = driver.find_element_by_css_selector("div[data-label='SEARCH']")
count = 1
flats = []
listings = cons.find_elements_by_class_name("srpTuple__cardWrap.tupleCardWrap")
for elem in listings:
    title = elem.find_element_by_class_name('srpTuple__tupleTitleOverflow').text
    print("\n" + title)
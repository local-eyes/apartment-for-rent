import datetime
import json
import time
from datetime import datetime
from unittest import result
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome("chromedriver", chrome_options=options)
# driver.get("https://housing.com/rent/search-CeP2alkth6ij0szzgf3")
driver.get("https://housing.com/user-profile/properties-contacted")
# driver.maximize_window()
time.sleep(5)
for i in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
driver.execute_script("window.scrollTo(0, 0);")
# results = driver.find_element_by_class_name('results-wrapper.css-19v6osn')
# resListings = results.find_elements_by_tag_name('article')
# for i in range(10):
#     time.sleep(1)
#     print("\n" + "For Listing " + str(i))
#     driver.execute_script("arguments[0].scrollIntoView();", resListings[i])
#     elems = resListings[i].text.split('\n')
#     print(len(elems))
#     for elem in elems:
#         print(elem)
#         print("=============")
#     print("\n\n")

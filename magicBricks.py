import datetime
import json
from flask import Flask, request, session, jsonify
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime
from selenium import webdriver

app = Flask(__name__)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome("chromedriver", chrome_options=options)
driver.get("https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=1,2&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment&Locality=Pratap-Nagar&cityName=Jaipur")
time.sleep(7)
cons = driver.find_elements_by_class_name("mb-srp__list")
count = 0
flats = []
for elem in cons:
    # if count <= 5:
    print(count)
    title = elem.find_element_by_class_name('mb-srp__card--title').text
    description = elem.find_element_by_class_name('mb-srp__card--desc--text').text
    rent = elem.find_element_by_class_name('mb-srp__card__price--amount').text.split('₹')[1]
    postedBy = elem.find_element_by_class_name('mb-srp__card__ads--name').text
    furnishingElem = elem.find_element_by_xpath('.//div[@data-summary="furnishing"]')
    furnishing = furnishingElem.find_element_by_class_name('mb-srp__card__summary--value').text
    bhk = int(title.split('BHK')[0])
    infoChips = []
    opener = elem.find_element_by_class_name('mb-srp__card__summary__action')
    opener.click()
    infoElem = elem.find_elements_by_class_name('mb-srp__card__summary__list--item')
    for chip in infoElem:
        key = chip.find_element_by_class_name('mb-srp__card__summary--label').text
        value = chip.find_element_by_class_name('mb-srp__card__summary--value').text
        infoChips.append({key : value})
    postedOn = elem.find_element_by_class_name('mb-srp__card__photo__fig--post').text
    imgCount = elem.find_element_by_class_name('mb-srp__card__photo__fig--count').text
    dateNow = datetime.now()
    updatedOn = dateNow.strftime("%Y-%m-%d %H:%M:%S")
    imgElem = elem.find_element_by_class_name('mb-srp__card__photo__fig--graphic')
    imgElem.click()
    time.sleep(8)
    imgsElem = driver.find_element_by_class_name("masonryGrid").find_elements_by_tag_name("img")
    imgs = []
    _range = len(imgsElem) if len(imgsElem) < 6 else 6
    for i in range(_range):
        imgs.append(imgsElem[i].get_attribute("src"))
    time.sleep(2)
    driver.find_element_by_class_name("leftArrow").click()
    flatsInfo = {
        'title': title,
        'description': description,
        'rent': rent,
        'imgCount': imgCount,
        'imgs': ",".join(imgs),
        'furnishing': furnishing,
        'postedBy': postedBy,
        'infoChips': infoChips,
        'date': postedOn,
        'area': 'pratap nagar',
        'updatedOn': updatedOn,
        'bhk': bhk,
        'source': 'Magic Brick',
    }
    count += 1
    driver.execute_script("window.stop();");
    time.sleep(2)
    json_object = json.dumps(flatsInfo, indent=4)
 
    # write to json file in append mode
    with open("data.json", "a") as outfile:
        outfile.write(json_object)
        outfile.write(",")

import datetime
import json
from flask import Flask, request, session, jsonify
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome("chromedriver", chrome_options=options)
driver.get("https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=3,1,2&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment&Locality=Pratap-Nagar&cityName=Jaipur")
driver.maximize_window()
time.sleep(5)
cons = driver.find_elements_by_class_name("mb-srp__list")
count = 1
flats = []
for elem in cons:
    print(f"Reading listing number {count}")
    print("Reading Title, Description, Rent and Posted by")
    title = elem.find_element_by_class_name('mb-srp__card--title').text
    description = elem.find_element_by_class_name('mb-srp__card--desc--text').text
    rent = elem.find_element_by_class_name('mb-srp__card__price--amount').text.split('₹')[1]
    postedBy = elem.find_element_by_class_name('mb-srp__card__ads--name').text
    furnishingElem = elem.find_element_by_css_selector('div[data-summary="furnishing"]')
    furnishing = furnishingElem.find_element_by_class_name('mb-srp__card__summary--value').text
    bhk = int(title.split('BHK')[0])
    print(f"{title[:10] + '...'} {description[:10] + '...'} {rent} {postedBy} {furnishing} {bhk} \n")
    infoChips = []
    opener = elem.find_element_by_class_name('mb-srp__card__summary__action')
    print("Reading Chips from all inforamtion buttons")
    opener.click()
    time.sleep(2)
    infoElem = elem.find_elements_by_class_name('mb-srp__card__summary__list--item')
    for i in range(6):
        key = infoElem[i].find_element_by_class_name('mb-srp__card__summary--label').text
        value = infoElem[i].find_element_by_class_name('mb-srp__card__summary--value').text
        print(f"{key} : {value}")
        infoChips.append({key : value})
    postedOn = elem.find_element_by_class_name('mb-srp__card__photo__fig--post').text
    try:
        imgCountElm = elem.find_element_by_class_name('mb-srp__card__photo__fig--count')
    except NoSuchElementException:
        imgCount = 0
    imgCount = imgCountElm.text
    dateNow = datetime.now()
    updatedOn = dateNow.strftime("%Y-%m-%d %H:%M:%S")
    try:
        imgElem = elem.find_element_by_class_name('mb-srp__card__photo__fig--graphic')
    except NoSuchElementException:
        print("No images found. Defaulting to no images")
        imgs = ['https://img.freepik.com/free-vector/houses-concept-illustration_114360-668.jpg']
    imgElem.click()
    time.sleep(8)
    try:
        imgsGrid = driver.find_element_by_class_name("masonryGrid")
    except NoSuchElementException:
        print("Image Modal not opened. Defaulting to no images")
        imgs = ['https://img.freepik.com/free-vector/houses-concept-illustration_114360-668.jpg']
    print("Opening Image Modal...")
    imgsElem = imgsGrid.find_elements_by_tag_name("img")
    imgs = []
    _range = len(imgsElem) if len(imgsElem) < 6 else 6
    print("Found " + str(_range) + " images")
    for i in range(_range):
        imgs.append(imgsElem[i].get_attribute("src"))
    time.sleep(2)
    driver.find_element_by_class_name("leftArrow").click()
    time.sleep(2)
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
    print("Closing Image Modal...")
    time.sleep(2)
    json_object = json.dumps(flatsInfo, indent=4)
 
    # write to json file in append mode
    print("Writing to file...")
    with open("magic_bricks.json", "a") as outfile:
        outfile.write(json_object)
        outfile.write(",")
    print("Done\n\n\n")

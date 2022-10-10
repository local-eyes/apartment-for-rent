import json
import time
from datetime import datetime
from unittest import result
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome("chromedriver", chrome_options=options)
allSearchResults = driver.find_element_by_class_name("results-wrapper.css-19v6osn")
allResults = allSearchResults.find_elements_by_tag_name("article")
print(len(allResults))
time.sleep(5)
for ind, res in enumerate(allResults):
    print(ind)
    driver.execute_script("window.scrollTo(0, {})".format(res.location['y'] - 100))
    rent = res.find_element_by_css_selector("div[data-q='price']").text
    title = res.find_element_by_css_selector("a[data-q='title']").text
    description = res.find_element_by_css_selector("div[data-q='desc']").text
    contactType = 'url'
    titleLink = res.find_element_by_css_selector("a[data-q='title']").get_attribute("href")
    contact = f"housing.com{titleLink}"
    imgs = []
    # if "Request Images" in res.text:
    #     print("IMAGES NOT PRESENT")
    # else:
    #     res.find_element_by_css_selector("div.slider-Wrapper.css-dlu4u9").click()
    #     time.sleep(1)
    #     imgsCarousel = driver.find_element_by_css_selector("div.slider-Wrapper.css-dlu4u9")
    #     imgsElement = imgsCarousel.find_elements_by_tag_name("img")
    #     _range = len(imgsElement) if len(imgsElement) < 6 else 6
    #     for i in range(_range):
    #         imgs.append(imgsElement[i].get_attribute("src"))
    #     time.sleep(3)
    #     closeBtn = driver.find_element_by_css_selector("div[data-q='close-btn']").click()
    res.find_element_by_css_selector("div.more.css-1b6siul").click()
    infoChipsWrapper = res.find_element_by_css_selector("div.css-5f61y5")
    infoChipsElem = infoChipsWrapper.find_elements_by_css_selector("div.css-1wcu9mf")
    infoChips = []
    for info in infoChipsElem:
        key, value = info.text.split("\n")
        if key.lower() == "furnishing":
            furnishing = value.lower()
        infoChips.append(info.text.replace("\n", ": "))

    owner = res.find_element_by_css_selector("div.css-wni7av").text
    agent = res.find_element_by_css_selector("div.contact-bar-subtitle.css-125f5y1").text
    postedBy = f"{agent}: {owner}"
    postedOn = res.find_element_by_css_selector("div.css-18jm55b").text
    bhk = title[:2]
    flatsInfo = {
        'title': title,
        'description': description,
        'rent': rent,
        'contactType': contactType,
        'contact': contact,
        'imgCount': len(imgs),
        'imgs': ",".join(imgs),
        'furnishing': furnishing,
        'postedBy': postedBy,
        'infoChips': ",".join(infoChips),
        'date': postedOn,
        'area': 'pratap nagar',
        'updatedOn': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        'bhk': bhk,
        'source': 'Housing.com',
    }
    print(f"=={bhk}==")
    # json_object = json.dumps(flatsInfo, indent=4) 
    # print("Writing to file...")
    # with open("housing.json", "a") as outfile:
    #     outfile.write(json_object)
    #     outfile.write(",")
    # print("Done\n")
    print("=======================================================\n")
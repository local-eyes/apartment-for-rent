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
driver = webdriver.Edge()
driver.get("https://www.99acres.com/search/property/rent/pratap-nagar-jaipur?city=177&locality=2326&preference=R&area_unit=1&res_com=R")
driver.maximize_window()
time.sleep(5)
cons = driver.find_element_by_css_selector("div[data-label='SEARCH']")
count = 1
flats = []
listings = cons.find_elements_by_css_selector("section[data-hydration-on-demand='true']")
for i in range(10):
    driver.execute_script(f"window.scrollTo(0, {i * 400});")
    print("\n" + listings[i].text + "\n")
    time.sleep(2)
    if i == 5:
        description = listings[i].text.split("\n")[12]
        ownerClass = "f10.Ng100.srpTuple__postedByText.ellipsis"
        postedByClass = "srpTuple__postedByText.list_header_semiBold.Ng100.ellipsis"
    elif i == 6:
        # do not continue the loop
        continue
    else:
        descriptionClass = "srp_tuple_description  "
        description = listings[i].find_element_by_css_selector(f"div[id='{descriptionClass}']").text
        ownerClass = "caption_strong_small"
        postedByClass = "list_header_semiBold"
    print("Scrolling to iteration " + str(i))
    title = listings[i].find_element_by_css_selector("h2[class='srpTuple__tupleTitleOverflow']").text
    rent = listings[i].find_element_by_css_selector(f"td[id='srp_tuple_price']").text.split('/month')[0]
    owner_agent = listings[i].find_element_by_css_selector(f"div.{ownerClass}").text.split('by')[1].strip()
    postedOn = listings[i].find_element_by_css_selector(f"div.{ownerClass}").text.split('by')[0].strip()
    name = listings[i].find_element_by_css_selector(f"div.{postedByClass}").text
    postedBy = f"{owner_agent.capitalize()}: {name}"

    listings[i].click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    furnishingElem = driver.find_element_by_id('FurnishDetails')
    furnishing = furnishingElem.find_element_by_tag_name('h2').text.lower()
    bhk= driver.find_element_by_id('bedWash').find_element_by_tag_name('b').text
    area = "pratap nagar"
    imgCount = driver.find_element_by_id('Overview').find_element_by_tag_name("li").text.split('(')[1][:-1]
    if int(imgCount) > 0:
        driver.find_element_by_id('overviewCarousel').click()
        time.sleep(4)
        imgsElem = driver.find_element_by_id("PhotonFilmStrip").find_elements_by_tag_name("img")
        imgs = []
        _range = len(imgsElem) if len(imgsElem) < 6 else 6
        for i in range(_range):
            imgs.append(imgsElem[i].get_attribute("data-main"))
    else:
        imgs = ['https://img.freepik.com/free-vector/houses-concept-illustration_114360-668.jpg']
    driver.close()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])
    print({
        "title": title,
        "urlList": imgs,
        "furnishing": furnishing,
        "area": area,
        "bhk": bhk,
        "imgCount": imgCount,
        "postedBy": postedBy,
        "rent": rent,
        "source": "99 Acres",
        "date": postedOn,
        "updatedOn": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "infoChips": [],
        "description": description,
    })
    print('\n====================================================\n')
import datetime
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome("chromedriver", chrome_options=options)
driver.get("https://www.99acres.com/search/property/rent/pratap-nagar-jaipur?city=177&locality=2326&preference=R&area_unit=1&res_com=R")
driver.maximize_window()
time.sleep(5)
cons = driver.find_element_by_css_selector("div[data-label='SEARCH']")
count = 1
flats = []
listings = cons.find_elements_by_css_selector("section[data-hydration-on-demand='true']")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(2)
spl = int(input("Enter Special Element index\n"))
feat = int(input("Enter Featured Element index\n"))
rera = int(input("Enter Rera last listing\n"))
for i in range(rera, len(listings)):
    driver.execute_script("arguments[0].scrollIntoView();", listings[i])
    print("\n" + listings[i].text + "\n")
    time.sleep(2)
    if i == spl:
        description = listings[i].text.split("\n")[12]
        ownerClass = "f10.Ng100.srpTuple__postedByText.ellipsis"
        postedByClass = "srpTuple__postedByText.list_header_semiBold.Ng100.ellipsis"
        infoChipsClass = "PremiumPdKeyHighlight__listBlock"
        infoChipsTag = 'li'
    elif i == feat:
        # do not continue the loop
        continue
    else:
        descriptionClass = "srp_tuple_description  "
        description = listings[i].find_element_by_css_selector(f"div[id='{descriptionClass}']").text
        ownerClass = "caption_strong_small"
        postedByClass = "list_header_semiBold"
        infoChipsClass = 'reasonToBuy__pd_hghlgtProp'
        infoChipsTag = 'div'
    print("Scrolling to iteration " + str(i))
    title = listings[i].find_element_by_css_selector("h2[class='srpTuple__tupleTitleOverflow']").text
    # if i == 4:
    #     rent = "22,000"
    # else:
    rent = listings[i].find_element_by_css_selector(f"td[id='srp_tuple_price']").text.split('/month')[0]
    owner_agent = listings[i].find_element_by_css_selector(f"div.{ownerClass}").text.split('by')[1].strip()
    postedOn = listings[i].find_element_by_css_selector(f"div.{ownerClass}").text.split('by')[0].strip()
    name = listings[i].find_element_by_css_selector(f"div.{postedByClass}").text
    postedBy = f"{owner_agent.capitalize()}: {name}"
    contactElem = listings[i].find_element_by_tag_name("button").click()
    isLoggedIn = input("Logged In?")
    if (isLoggedIn == 'y'):
        contactType = "number"
        contact = driver.find_element_by_css_selector('div.component__activeDetails').text
        time.sleep(2)
        driver.find_element_by_css_selector("i[data-label='CLOSE']").click()
        print("CONTACT DETAILS: " + contact + "\n\n")
    else:
        driver.find_element_by_css_selector("i.iconS_Common_24.icon_close.style__close").click()
    time.sleep(2)
    listings[i].click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    furnishing = driver.find_element_by_id('furnishingLabel').text
    if isLoggedIn == 'n':
        contactType = "url"
        contact = driver.current_url
        print("CONTACT DETAILS: " + contact + "\n\n")
    # furnishing = furnishingElem.find_element_by_tag_name('h2').text.lower()
    bhk= driver.find_element_by_id('bedWash').find_element_by_tag_name('b').text
    infoChips = []
    try:
        infoChipsElem = driver.find_element_by_class_name(infoChipsClass).find_elements_by_tag_name(infoChipsTag)
        for chip in infoChipsElem:
            infoChips.append(chip.text)
    except NoSuchElementException:
        pass
    print("Info Chips: " + str(infoChips))
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
    flatsInfo = {
        'title': title,
        'description': description,
        'rent': rent,
        'contactType': contactType,
        'contact': contact,
        'imgCount': imgCount,
        'imgs': ",".join(imgs),
        'furnishing': furnishing,
        'postedBy': postedBy,
        'infoChips': ",".join(infoChips),
        'date': postedOn,
        'area': 'pratap nagar',
        'updatedOn': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        'bhk': bhk,
        'source': '99 Acres',
    }

    json_object = json.dumps(flatsInfo, indent=4) 
    print("Writing to file...")
    with open("99acres.json", "a") as outfile:
        outfile.write(json_object)
        outfile.write(",")
    print("Done\n\n\n")
    print('\n====================================================\n')
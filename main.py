from flask import Flask, request, session, jsonify
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, data')
    return response

@app.route('/')
def index():
    magicBricksRes = magicBricks()
    return jsonify(magicBricksRes)

def magicBricks():
    url = "https://www.magicbricks.com/property-for-rent/residential-real-estate?bedroom=1,2&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Service-Apartment&Locality=Pratap-Nagar&cityName=Jaipur"
    response = requests.get(url)
    flat=[]
    soup = bs(response.content, 'html.parser') 
    titleElem = soup.find_all('h2', attrs={'class':'mb-srp__card--title'})
    descElem = soup.find_all('div', attrs={'class':'mb-srp__card--desc--text'})
    rentElem = soup.find_all('div', attrs={'class':'mb-srp__card__price--amount'})
    imgCountElem = soup.find_all('span', attrs={'class':'mb-srp__card__photo__fig--count'})
    imgElem = soup.find_all('div', attrs={'class':'mb-srp__card__photo__fig'})
    posteeElem = soup.find_all('div', attrs={'class':'mb-srp__card__ads--name'})
    furnishingElem = soup.find_all('div', attrs={'data-summary':'furnishing'})
    infoElem = soup.find_all('div', attrs={'class':'mb-srp__card__summary__list'})
    for ind, elem in enumerate(titleElem):
        title = titleElem[ind].text
        desc = descElem[ind].text
        rent = rentElem[ind].text
        imgCheck = imgElem[ind].text.split('Posted')
        if imgCheck[0] == 'No Image Available' or imgCheck[0] == 'Request Photos':
            continue
        img = imgElem[ind].select('img')[0]['data-src']
        furnishing = furnishingElem[ind].text.split('Furnishing')[1].strip()
        agent_name = posteeElem[ind].text.split(":")
        infoChips = []
        for child in infoElem[ind].children:
            labels = child.findAll('div', attrs={'class':'mb-srp__card__summary--label'})
            values = child.findAll('div', attrs={'class':'mb-srp__card__summary--value'})
            infoChips.append(f"{labels[0].text} : {values[0].text}")
        posteeInfo = {'entity': agent_name[0], 'name': agent_name[1].strip()}
        flat.append({
            'title': title,
            'desc': desc,
            'rent': rent,
            'img': img,
            'furnishing': furnishing,
            'postee':posteeInfo,
            'infoChips': infoChips
        })
    return flat

@app.route('/99-acres')
def _99acres():
    url = "https://www.99acres.com/search/property/rent/pratap-nagar-jaipur?city=177&locality=2326&preference=R&area_unit=1&res_com=R"
    response = requests.get(url)
    flat=[]
    soup = bs(response.content, 'html.parser')
    section = soup.findAll('section', attrs={'data-hydration-on-demand': 'true'})
    for title in section:
        print('\n\n\n')
        print(title.text)
        print('\n\n\n')
    return jsonify(flat)


if __name__ == '__main__':
    app.run(debug=True)
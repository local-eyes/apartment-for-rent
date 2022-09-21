from flask import Flask, request, session, jsonify
from flask_mysqldb import MySQL
from os import urandom
from yaml import load, FullLoader
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

app = Flask(__name__)
mysql = MySQL(app)

# MySQL Configuration
db_keeps = load(open('db.yaml'), Loader=FullLoader)
app.config['MYSQL_HOST'] = db_keeps['mysql_host']
app.config['MYSQL_USER'] = db_keeps['mysql_user']
app.config['MYSQL_PASSWORD'] = db_keeps['mysql_password']
app.config['MYSQL_DB'] = db_keeps['mysql_db']
app.config['SECRET_KEY'] = urandom(24)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, data')
    return response

@app.route('/')
def index():
    available = magic()
    for flat in available:
        title = flat['title']
        if len(flat['desc']) > 100:
            description = flat['desc'][:100] + '...'
        else:
            description = flat['desc']
        imgUrl = flat['img']
        furnishing = flat['furnishing']
        area = "pratap nagar"
        bhkFull = flat['title'].split('BHK')
        bhk = bhkFull[0] + "BHK"
        imgCount = 1
        postedBy = flat['postee']
        rent = flat['rent'].split('₹')[1]
        source = "Magic Bricks"
        date = flat['postedOn'].split(":")[-1].strip()
        dateNow = datetime.now()
        updatedOn = dateNow.strftime("%Y-%m-%d %H:%M:%S")
        infoChips = ", ".join(flat['infoChips'][:6])
        # print("\n", rent, infoChips)
        # db_data.append({
        # "title": title,
        # "description": description,
        # "imgUrl": imgUrl,
        # "furnishing": furnishing,
        # "area": area,
        # "bhk": bhk,
        # "imgCount": imgCount,
        # "postedBy": postedBy,
        # "rent": rent,
        # "source": source,
        # "date": date,
        # "updatedOn": updatedOn,
        # "infoChips": infoChips
        # })
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO listings (title, description, imgUrl, furnishing, area, bhk, imgCount, postedBy, rent, source, date, updatedOn, infoChips) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (title, description, imgUrl, furnishing, area, bhk, imgCount, postedBy, rent, source, date, updatedOn, infoChips))
        mysql.connection.commit()
        cur.close()
    # return jsonify(db_data)
    return "Done"

def magic():
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
        if rentElem[ind].text[0] != "₹":
            rent = "₹" + rentElem[ind].text
        else:
            rent = rentElem[ind].text
        imgCheck = imgElem[ind].text.split('Posted')
        if imgCheck[0] == 'No Image Available' or imgCheck[0] == 'Request Photos':
            continue
        else:
            postedOn = imgCheck[1]
        img = imgElem[ind].select('img')[0]['data-src']
        furnishing = furnishingElem[ind].text.split('Furnishing')[1].strip()
        posteeInfo= posteeElem[ind].text
        infoChips = []
        for child in infoElem[ind].children:
            labels = child.findAll('div', attrs={'class':'mb-srp__card__summary--label'})
            values = child.findAll('div', attrs={'class':'mb-srp__card__summary--value'})
            infoChips.append(f"{labels[0].text} : {values[0].text}")
        flat.append({
            'title': title,
            'desc': desc,
            'rent': rent,
            'img': img,
            'furnishing': furnishing,
            'postee':posteeInfo,
            'infoChips': infoChips,
            'postedOn': postedOn
        })
    return flat

@app.route('/api/v1/available')
def db():
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM listings;")
    if q > 0:
        allApartments = []
        listings = cur.fetchall()
        for _list in listings:
            infoChipsList = _list[13].split(', ')
            allApartments.append({
                "id": _list[0],
                "title": _list[1],
                "description": _list[2],
                "imgUrl": _list[3],
                "furnishing": _list[4],
                "area": _list[5],
                "bhk": _list[6],
                "imgCount": _list[7],
                "postedBy": _list[8],
                "rent": _list[9],
                "source": _list[10],
                "date": _list[11],
                "updatedOn": _list[12],
                "infoChips": infoChipsList
            })
    return jsonify(allApartments)


if __name__ == '__main__':
    app.run(debug=True)
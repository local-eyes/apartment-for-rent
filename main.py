from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from os import urandom
from yaml import load, FullLoader
import json

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

@app.route('/add-data/<provider>')
def index(provider):
    f = open(f'sites/{provider}.json')
    data = json.load(f)
    cur = mysql.connection.cursor()
    for listing in data:
        infochips = listing['infoChips'].split(',')
        title = listing['title']
        description = listing['description']
        rent = listing['rent']
        imgCount = listing['imgCount']
        imgs = listing['imgs']
        furnishing = listing['furnishing']
        postedBy = listing['postedBy']
        infoChips = ", ".join(infochips)
        date = listing['date']
        area = listing['area']
        updatedOn = listing['updatedOn']
        bhk = listing['bhk']
        source = listing['source']
        contactType = listing['contactType']
        contact = listing['contact']

        cur.execute("INSERT INTO listings (title, description, rent, contactType, contact, imgCount, urlList, furnishing, postedBy, infoChips, date, area, updatedOn, bhk, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (title, description, rent, contactType, contact, imgCount, imgs, furnishing, postedBy, infoChips, date, area, updatedOn, bhk, source))
        cur.connection.commit()
    cur.close()
    return "Added to database"

@app.route('/api/v1.7/available')
def db():
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM listings;")
    if q > 0:
        allApartments = []
        listings = cur.fetchall()
        for _list in listings:
            infoChipsList = _list[14].split(', ')
            imgUrlsList = _list[2].split(',')
            allApartments.append({
                "id": _list[0],
                "title": _list[1],
                "description": _list[15],
                "imgUrl": imgUrlsList,
                "furnishing": _list[3],
                "area": _list[4],
                "bhk": _list[5],
                "imgCount": _list[6],
                "postedBy": _list[7],
                "rent": _list[8],
                "contactType": _list[9],
                "contact": _list[10],
                "source": _list[11],
                "date": _list[12],
                "updatedOn": _list[13],
                "infoChips": infoChipsList
            })
    return jsonify(allApartments)

@app.route('/api/filters')
def filters():
    if len(request.args) == 4:
        bhk = request.args.get('bhk')
        furnishings = request.args.get('furnishing').split(',')
        area = request.args.get('area')

        if furnishings[0] != '':
            furnishing = "'" + "', '".join(furnishings) + "'"
        else:
            furnishing = "'semifurnished','furnished','unfurnished'"
        
        priceQuery = request.args.get('price').split("to")
        if len(priceQuery) == 2:
            priceTo = priceQuery[1]
        else:
            priceTo = '100'
        
        if bhk != '':
            queryBhk = f"(bhk IN ({bhk}))"
        else:
            queryBhk = f"(bhk IN (1, 2, 3))"
        queryFurnishing = f"(furnishing IN ({furnishing}))"
        queryPrice = f"(rent <= {priceTo}000)"
        finalQuery = f"SELECT * FROM listings WHERE {queryBhk} AND {queryFurnishing} AND {queryPrice} AND area='{area}';"
        print('\n' + finalQuery + '\n')
        flats = []
        cur = mysql.connection.cursor()
        q = cur.execute(finalQuery)
        if q > 0:
            listings = cur.fetchall()
            for _list in listings:
                infoChipsList = _list[14].split(',')
                imgUrlsList = _list[2].split(',')
                flats.append({
                    "id": _list[0],
                    "title": _list[1],
                    "description": _list[15],
                    "imgUrl": imgUrlsList,
                    "furnishing": _list[3],
                    "area": _list[4],
                    "bhk": _list[5],
                    "imgCount": _list[6],
                    "postedBy": _list[7],
                    "rent": _list[8],
                    "contactType": _list[9],
                    "contact": _list[10],
                    "source": _list[11],
                    "date": _list[12],
                    "updatedOn": _list[13],
                    "infoChips": infoChipsList
                })
        return jsonify(flats)
    else:
        return "Invalid request"

if __name__ == '__main__':
    app.run(debug=True)

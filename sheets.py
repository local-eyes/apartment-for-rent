import gspread
from flask import Flask, request, session, jsonify

app = Flask(__name__)
sa = gspread.service_account(filename='localeyes-95d0d-7dd35becf2f5.json')
sh = sa.open("Flat Hunter Beta Testing Database")
userSheet = sh.worksheet("user")
flatSheet = sh.worksheet("flat")
allData = userSheet.get_all_values()

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, data')
    return response

@app.route('/')
def index():
    return jsonify({'message': 'reponse'})

@app.route('/update-user', methods=['POST'])
def update_user():
    data = request.get_json()
    userId = data['userId']
    updateTab = data['updateTab']
    updateValue = data['updateValue']
    found = False
    for row in allData:
        if userId in row:
            found = True
            workingCell = userSheet.find(userId)
            cellToUpdate = f'{updateTab}{workingCell.row}'
            if updateValue == 'increment':
                print("Increment Detected")
                updateValue = int(userSheet.acell(cellToUpdate).value) + 1
                print("New Value will be: ", updateValue)
            print("Updating Cell ", cellToUpdate, " with value ", updateValue)
            break
    if found:
        userSheet.update_acell(cellToUpdate, updateValue)
        return jsonify({'message': 'success'})
    userSheet.update_acell(cellToUpdate, updateValue)
    print("Done...")
    return jsonify({'message': data})


if __name__ == '__main__':
    app.run(debug=True)
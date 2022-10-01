import gspread
from flask import Flask, request, session, jsonify

app = Flask(__name__)
sa = gspread.service_account(filename='localeyes-95d0d-7dd35becf2f5.json')
sh = sa.open("Flat Hunter Beta Testing Database")

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, data')
    return response

@app.route('/')
def index():
    return jsonify({'message': 'reponse'})

@app.route('/<sheet>/update', methods=['POST'])
def update_user(sheet):
    workSheet = sh.worksheet(sheet)
    data = request.get_json()
    userId = data['userId']
    updateTab = data['updateTab']
    updateValue = data['updateValue']
    workingCell = workSheet.find(userId)
    cellToUpdate = f'{updateTab}{workingCell.row}'
    if updateValue == 'increment':
        print("Increment Detected")
        updateValue = int(workSheet.acell(cellToUpdate).value) + 1
        print("New Value will be: ", updateValue)
    print("Updating Cell ", cellToUpdate, " with value ", updateValue)
    workSheet.update_acell(cellToUpdate, updateValue)
    print("Done...")
    return jsonify({
        'request': 'success',
        'message': 'Your Response has been recorded',
        'insights': {
            'cellToUpdate': cellToUpdate,
            'updatedValue': updateValue,
            'sheet': sheet
            },
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
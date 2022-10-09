import gspread
from math import floor
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
    updateValueOps = data['updateValue']
    operation, updateValue = updateValueOps.split(",[")
    if sheet == 'user':
        workingCell = workSheet.find(userId)
        print(workingCell)
    else:
        first_column = workSheet.range("A1:A{}".format(workSheet.row_count))
        found_cell_list = [found for found in first_column if found.value == userId]
        workingCell = found_cell_list[0]
        print(workingCell)

    cellToUpdate = f'{updateTab}{workingCell.row}'
    if operation == 'increment':
        print("Increment Detected")
        updateValue = int(workSheet.acell(cellToUpdate).value) + floor(float(updateValue))
        print("New Value will be: ", updateValue)
    if operation == 'append':
        print("Append Detected")
        updateValue = updateValue[:-1]
        if workSheet.acell(cellToUpdate).value == '' or workSheet.acell(cellToUpdate).value == None:
            updateValue = updateValue
        else:
            updateValue = str(workSheet.acell(cellToUpdate).value) + ", " + updateValue
        print("New Value will be: ", updateValue)
    if operation == 'overwrite':
        print("Overwrite Detected")
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
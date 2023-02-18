import gspread
from math import floor
from flask import Flask, request, session, jsonify

app = Flask(__name__)
sa = gspread.service_account(filename='localeyes-95d0d-7dd35becf2f5.json')
sh = sa.open("Flat Hunter Beta Testing Database")
progressSheet = sa.open("LocalEyes Growth Stats")

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
    operation, updateValue = updateValueOps.split(",")[:1], updateValueOps.split(",")[1:]
    updateValue = ", ".join(updateValue)
    updateValue = updateValue.replace("[", "").replace("]", "")
    print(operation[0], updateValue)
    if sheet == 'user':
        workingCell = workSheet.find(userId)
        print(workingCell)
    else:
        first_column = workSheet.range("A1:A{}".format(workSheet.row_count))
        found_cell_list = [found for found in first_column if found.value == userId]
        workingCell = found_cell_list[0]

    cellToUpdate = f'{updateTab}{workingCell.row}'
    if operation[0] == 'increment':
        print("Increment Detected")
        updateValue = int(workSheet.acell(cellToUpdate).value) + floor(float(updateValue))
        print("New Value will be: ", updateValue)
    if operation[0] == 'append':
        print("Append Detected")
        if workSheet.acell(cellToUpdate).value == '' or workSheet.acell(cellToUpdate).value == None:
            updateValue = updateValue
        else:
            updateValue = str(workSheet.acell(cellToUpdate).value) + ", " + updateValue
        print("New Value will be: ", updateValue)
    if operation[0] == 'overwrite':
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

@app.route('/update-users', methods=['POST'])
def update_user_tracking():
    # append to the end of the sheet
    workSheet = progressSheet.worksheet("Users Report")
    first_column = workSheet.range("C1:C{}".format(workSheet.row_count))
    found_cell_list = [found for found in first_column if found.value == '']
    workingRow = found_cell_list[0]
    rowToUpdate = workingRow.row
    data = request.get_json()
    for key, value in data.items():
        cellToUpdate = f'{key}{rowToUpdate}'
        workSheet.update_acell(cellToUpdate, value)
    return {
        "message": "Sheet Updated Successfully",
        "status": "OK"
    }


@app.route('/update-content', methods=['POST'])
def update_content():
    # append to the end of the sheet
    workSheet = progressSheet.worksheet("Content Report")
    first_column = workSheet.range("B1:B{}".format(workSheet.row_count))
    found_cell_list = [found for found in first_column if found.value == '']
    workingRow = found_cell_list[0]
    rowToUpdate = workingRow.row
    data = request.get_json()
    for key, value in data.items():
        cellToUpdate = f'{key}{rowToUpdate}'
        workSheet.update_acell(cellToUpdate, value)
    return {
        "message": "Sheet Updated Successfully",
        "status": "OK"
    }


if __name__ == '__main__':
    app.run(debug=True)
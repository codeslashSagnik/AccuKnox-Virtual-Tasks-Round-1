import json
import csv
from flask import Flask, jsonify

app = Flask(__name__)

def make_json(csvFilePath, jsonFilePath):
    data = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            data.append(row)

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        json.dump(data, jsonf, indent=4)

@app.route('/convert', methods=['GET'])
def get_students():
    # Read the JSON file
    with open('data/exams.json', 'r') as json_file:
        data = json.load(json_file)
    # Return the JSON data
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)
    
#python app.py

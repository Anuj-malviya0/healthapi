from flask import Flask, request, jsonify
import csv

app = Flask(__name__)
csv_file = 'healthcare.csv'

def read_csv():
    data = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def write_csv(data):
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    data = read_csv()
    return jsonify(data)

@app.route('/inventory/<item_id>', methods=['GET'])
def get_item(item_id):
    data = read_csv()
    item = next((item for item in data if item["Item ID"] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/inventory/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = read_csv()
    item = next((item for item in data if item["Item ID"] == item_id), None)
    if item:
        updated_data = request.json
        for key, value in updated_data.items():
            if key in item:
                item[key] = value
        write_csv(data)
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

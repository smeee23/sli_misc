from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load JSON data from file
with open('output.json') as f:
    data = json.load(f)  

# Define API endpoint
@app.route('/status/<int:key>', methods=['GET'])
def status(key):
    result = ""
    for validator in data['data']:
        if key == validator["index"]:
            result = validator
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"index": 9999999999999, "slashed": False, "withdrawAddress": "0x0", "loss": "0"})

# Define API endpoint
@app.route('/add/<int:key>', methods=['GET'])
def add(key):
    req_params = ['withdrawAddress']
    params = request.args.keys()
    if not all(param in req_params for param in params):
        return jsonify({"error": "add request not formatted correctly"}), 404

    for validator in data['data']:
        if key == validator["index"]:
            return jsonify({"error": "validator already exists"}), 404
    
    withdrawAddress = request.args.get('withdrawAddress')

    data['data'].append({"index": key, "slashed": False, "withdrawAddress": withdrawAddress, "loss": 0})
    
    with open('output.json', 'w') as outfile:
        json.dump(data, outfile)

    return data

# Define API endpoint
@app.route('/remove/<int:key>', methods=['GET'])
def remove(key):

    new_data = [validator for validator in data["data"] if key != validator["index"]]

    if(new_data == data["data"]):
        return jsonify({"error": "validator does not exist"}), 404
    
    data["data"] = new_data
    with open('output.json', 'w') as outfile:
        json.dump(data, outfile)

    return data

# Define API endpoint
@app.route('/slash/<int:key>', methods=['GET'])
def slash(key):
    params = request.args.keys()
    if not ('loss' in params):
        return jsonify({"error": "slash request not formatted correctly"}), 404

    found = False
    for validator in data['data']:
        if key == validator["index"]:
            validator["slashed"] = True
            validator["loss"] = str(request.args.get('loss'))
            found = True

    if(not found):
        return jsonify({"error": "validator does not exist"}), 404
    
    with open('output.json', 'w') as outfile:
        json.dump(data, outfile)

    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
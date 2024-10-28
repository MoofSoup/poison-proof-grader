from flask import Flask, jsonify, request
from utils import check_if_poisoned

app = Flask(__name__)

@app.route('/is_poisoned', methods=['POST'])
def is_poisoned():
    # if userInput is not in request.json, return 400
    if "userInput" not in request.json:
        return jsonify({'error': 'userInput is required'}), 400

    is_poisoned = check_if_poisoned(request.json["userInput"])

    return jsonify({'is_poisoned': is_poisoned})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000, debug=True)
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/is_poisoned', methods=['POST'])
def is_poisoned():
    return jsonify({'is_poisoned': True})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
from flask import Flask, request, jsonify
from src.api.reports import Reports

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World"

@app.route("/reports/<account_id>", methods=["GET"])
def get_data(account_id):
    payload = request.get_json()
    data = Reports(payload.get("COLUMNS")).get_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) #REVISAR - o que é o debug?

from main import app
import requests
from flask import jsonify


@app.route('/tests/ai')
def test_ai():
    r = requests.get('http://ai:5000/')
    print(r.status_code)
    print(r.json())
    return jsonify(r.json())

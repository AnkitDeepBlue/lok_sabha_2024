import os
from flask import Flask, render_template, jsonify
import json

class Config:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    CANDIDATE_DATA_PATH = os.path.join(PROJECT_ROOT, 'candidate_data.json')
    STATE_DATA_PATH = os.path.join(PROJECT_ROOT, 'data.json')




app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    try:
        with open(app.config['STATE_DATA_PATH']) as f:
            data = json.load(f)
        return render_template('index.html', data=data)
    except FileNotFoundError:
        return "data.json file not found", 404

@app.route('/api/data')
def get_data():
    try:
        with open(app.config['STATE_DATA_PATH']) as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "data.json file not found"}), 404

@app.route('/candidate')
def candidate():
    try:
        with open(app.config['CANDIDATE_DATA_PATH']) as f:
            data = json.load(f)
        return render_template('candidate.html', data=data)
    except FileNotFoundError:
        return "candidate_data.json file not found", 404

@app.route('/api/candidate')
def get_candidate_data():
    try:
        with open(app.config['CANDIDATE_DATA_PATH']) as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "candidate_data.json file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

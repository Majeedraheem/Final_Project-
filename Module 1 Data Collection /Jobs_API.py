import flask
from flask import request, jsonify
import re
import json

# Define the pattern dictionary with raw strings
pattern_dict = {
    'c': r'(c)',
    'c++': r'(c\+\+)',
    'java': r'(java)',
    'c#': r'(c#)',
    'python': r'(python)',
    'scala': r'(scala)',
    'oracle': r'(oracle)',
    'sql server': r'(sql server)',
    'mysql server': r'(mysql server)',
    'postgresql': r'(postgresql)',
    'mongodb': r'(mongodb)',
    'javascript': r'(javascript)',
    'los angeles': r'(los angeles)',
    'new york': r'(new york)',
    'san francisco': r'(san francisco)',
    'washington dc': r'(washington dc)',
    'seattle': r'(seattle)',
    'austin': r'(austin)',
    'detroit': r'(detroit)'
}

def get_data(key, value, current):
    # Convert the value to lowercase for case-insensitive matching
    value = value.lower().strip()
    
    # Check if the value exists in the pattern dictionary
    if value not in pattern_dict:
        print(f"Pattern for '{value}' not found in pattern_dict.")
        return []
    
    pattern = pattern_dict[value]
    results = []

    # Iterate through the data
    for rec in current:
        # Normalize the job field value and check for the pattern
        job_field_value = rec.get(key, '').lower()
        if re.search(pattern, job_field_value):
            results.append(rec)

    return results

app = flask.Flask(__name__)

data = None
with open('jobs.json', encoding='utf-8') as f:
    data = json.load(f)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to Flask JOB search API</h1>'''

@app.route('/data/all', methods=['GET'])
def api_all():
    return jsonify(data)

@app.route('/data', methods=['GET'])
def api_id():
    res = None
    for req in request.args:
        key = None
        value = request.args.get(req, '').strip().lower()

        if req == 'Job Title':
            key = 'Job Title'
        elif req == 'Job Experience Required':
            key = 'Job Experience Required'
        elif req == 'Key Skills':
            key = 'Key Skills'
        elif req == 'Role Category':
            key = 'Role Category'
        elif req == 'Location':
            key = 'Location'
        elif req == 'Functional Area':
            key = 'Functional Area'
        elif req == 'Industry':
            key = 'Industry'
        elif req == 'Role':
            key = 'Role'
        
        if key:
            if res is None:
                res = get_data(key, value, data)
            else:
                res = get_data(key, value, res)

    return jsonify(res) if res is not None else jsonify([])

if __name__ == "__main__":
    app.run(port=50001)

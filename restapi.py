from flask import Flask, jsonify, abort, json, render_template, request, Response
import os
import glob
from jsonschema import validate


app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_maneuver():
    return render_template('index.html')


@app.route('/page1.html', methods=['GET'])
def get_page1():
    return render_template('page1.html')


@app.route('/page2.html', methods=['GET'])
def get_page2():
    return render_template('page2.html')


@app.route('/alertWindow.html', methods=['GET'])
def get_alert():
    return render_template('alertWindow.html')


@app.route('/keywordsPage.html', methods=['GET'])
def get_keywords():
    return render_template('keywordsPage.html')


@app.route('/UI/API/0.1/<int:file_name>/', methods=['GET'])
def get_app(file_name):
    jfile=open(str(file_name)+'.json','r')
    json_file=json.load(jfile)
    response = jsonify(json_file)
    response.status_code = 200
    return response


@app.route('/UI/API/0.1/', methods=['POST'])
def post_app():
    maxim=0
    for filename in glob.glob('*.json'):
        filenr=filename.split('.')[0]
        if is_number(filenr) and int(filenr)>maxim:
            maxim=int(filenr)

    data=request.get_json()

    with open('JSON schema.json','r') as schema:
        schemajson = json.load(schema)
    validate(data,schemajson)

    with open(str(maxim+1) + '.json', 'w') as outfile:
        json.dump(data, outfile,indent=4, separators=(',', ': '))

    response=Response("")
    response.headers['Location']='/UI/API/0.1/'+str(maxim+1)
    response.status_code=201
    return response


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


@app.route('/UI/API/0.1/<int:file_name>/', methods=['DELETE'])
def delete_app(file_name):
    try:
        os.remove(str(file_name) + '.json')
    except OSError:
        abort(404)
    return 'No content', 204


@app.route('/UI/API/0.1/<int:file_name>/applicationName', methods=['GET'])
def get_app_name(file_name):
    jfile = open(str(file_name) + '.json', 'r')
    json_file = json.load(jfile)
    response = jsonify({"applicationName": json_file["application"]})
    response.status_code = 200
    return response


@app.route('/UI/API/0.1/<int:file_name>/components', methods=['GET'])
def get_descriptor_components(file_name):
    jfile = open(str(file_name) + '.json', 'r')
    json_file = json.load(jfile)
    response = jsonify({"components": json_file["components"]})
    response.status_code = 200
    return response


@app.route('/UI/API/0.1/<int:file_name>/components/<int:component_id>', methods=['GET'])
def get_component_id(component_id,file_name):
    jfile = open(str(file_name) + '.json', 'r')
    json_file = json.load(jfile)
    component = [component for component in json_file["components"] if component['id'] == component_id]
    if len(component) == 0:
        abort(404)
    return jsonify({'component': component[0]})


@app.route('/UI/API/0.1/<int:file_name>/components/<string:name>', methods=['GET'])
def get_component_name(name,file_name):
    jfile = open(str(file_name) + '.json', 'r')
    json_file = json.load(jfile)
    component = [component for component in json_file["components"] if component['name'] == name]
    if len(component) == 0:
        abort(404)
    return jsonify({'component': component[0]})


@app.route('/UI/API/0.1/<int:file_name>/IP', methods=['GET'])
def get_app_IP(file_name):
    jfile = open(str(file_name) + '.json', 'r')
    json_file = json.load(jfile)
    response = jsonify({"IP": json_file["IP"]})
    response.status_code = 200
    return response


@app.route('/UI/API/0.1/<int:file_name>/budget', methods=['GET'])
def get_app_budget(file_name):
    jfile = open(str(file_name) + '.json', 'r')
    json_file = json.load(jfile)
    response = jsonify({"budget": json_file["budget"]})
    response.status_code = 200
    return response


@app.route('/UI/API/0.1/<int:file_name>/restrictions', methods=['GET'])
def get_app_restrictions(file_name):
    jfile = open(str(file_name) + '.json', 'r')
    json_file = json.load(jfile)
    response = jsonify({"restrictions": json_file["restrictions"]})
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run(debug=True, port=8080)

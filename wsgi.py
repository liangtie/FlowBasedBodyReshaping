# from flask_json import FlaskJSON, JsonError, json_response, as_json
import json
from flask import Flask, request
from flask import Flask, request, jsonify, send_file

from flask_cors import CORS
from playhouse.shortcuts import model_to_dict

# sudo lsof -i :7565
import base64
import os
from reshaping import ReShaping
import utils


app = Flask(__name__)
CORS(app)


@app.route('/body_shaping', methods=['POST'])
def body_shaping():

   # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

  # Get JSON parameters
    json_params = request.form.get('json')
    if not json_params:
        return jsonify({"error": "No JSON parameters provided"}), 400

    json_data = None

    try:
        json_data = json.loads(json_params)
    except Exception as e:
        return jsonify({"error": "Invalid JSON format"}), 400

    reshape_worker = ReShaping()

    try :
        reshape_worker.reshape_body(file, json_data['degree'], json_data['roi'])
    except Exception as e:
        return jsonify({"error": f'{e}'}), 400

    res_img = reshape_worker.get_out_img_path()

    if res_img == None:
        return jsonify({"error": "supported image format is '.png', '.jpg', '.jpeg','.JPG'"}), 400

    response = send_file(res_img, mimetype=file.mimetype)
    reshape_worker.clear_up_dirs()
    return response

if __name__ == '__main__':
    print("starting srv")
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('0.0.0.0', 7565), app)
    server.serve_forever()

# from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask import Flask, request
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict

# sudo lsof -i :7565
import base64
import os
import utils


app = Flask(__name__)
CORS(app)


@app.route('/is_valid_license', methods=['POST'])
def is_valid_license():

    is_valid =  False
    error = None

    try:
        license =  request.form['license']
        mac =  request.form['mac']

        def do_valid_license(license , usr_mac):
            d =utils.base64_decode(license)

            b = d.split(SPLITTER)
            if len(b) != 2:
                return False , "Invalid license"
            mac , expiration_time = b

            if utils.current_datetime_in_seconds() > int(expiration_time):
                return False , "License expired"

            if mac != usr_mac:
                return False , "License not match"

            return True , None

        is_valid , error= do_valid_license(license ,mac)

    except (KeyError, TypeError, ValueError) as e:
        error = f'{str(e) } ; {error}'

    return {"is_valid" : is_valid , "error" : error}

if __name__ == '__main__':
    from gevent import pywsgi
    print("starting srv")
    server = pywsgi.WSGIServer(('0.0.0.0', 7565), app)
    server.serve_forever()

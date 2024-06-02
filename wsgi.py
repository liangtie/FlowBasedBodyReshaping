import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reshaping import ReShaping

app = Flask(__name__)
CORS(app)

@app.route('/body_shaping', methods=['POST'])
def body_shaping():
    """
    Endpoint to handle body reshaping requests.
    Expects a file upload and JSON parameters containing degree and ROI for reshaping.
    """

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

    # Parse JSON parameters
    try:
        json_data = json.loads(json_params)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400

    # Ensure required JSON parameters are present
    if 'degree' not in json_data or 'roi' not in json_data:
        return jsonify({"error": "Missing required JSON parameters: 'degree' and 'roi'"}), 400

    reshape_worker = ReShaping()

    # Perform reshaping operation
    try:
        reshape_worker.reshape_body(file, json_data['degree'], json_data['roi'])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Get the output image path
    res_img = reshape_worker.get_out_img_path()
    if res_img is None:
        return jsonify({"error": "Supported image formats are '.png', '.jpg', '.jpeg', '.JPG'"}), 400

    # Send the reshaped image file as response
    response = send_file(res_img, mimetype=file.mimetype)
    
    return response

if __name__ == '__main__':
    print("Starting server")
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('0.0.0.0', 7565), app)
    server.serve_forever()

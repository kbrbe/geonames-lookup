from flask import jsonify

def handle_error(message, status_code):
    response = jsonify({"error": message})
    response.status_code = status_code
    return response

from werkzeug.local import LocalProxy
from src.exceptions import ApiException

def get_request_body(request: LocalProxy):
    try:
        request_body = request.get_json()
    except Exception as error:
        raise ApiException(f"Invalid JSON format. Details: {str(error)}", 400)
    
    if request_body is None:
        raise ApiException("Missing JSON in request body", 400)

    return request_body


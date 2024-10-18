from typing import Dict, Any
from datetime import datetime
from src.exceptions import ApiException

def __check_data_format(date_string: str):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def assert_values(function_name: str, payload: Dict[str, Any]):
    endpoint_by_function = { #REVISAR - this is a bit weird. Isnt there a better approach?
        "get_data": "reports",
        "issue_token": "token",
        "get_refresh_token": "authorize"
    }
    values_by_endpoint = {
        "get_data": {
            "columns": list,
            "start_date": str,
            "end_date": str
        },
        "issue_token": {
            "refresh_token": str
        },
        "get_refresh_token": {
            "client_id": str,
            "client_secret": str
        }
    }
    for value, value_type in values_by_endpoint[function_name].items():
        if value not in payload:
            raise ApiException(f"Parameter '{value}' is mandatory for '{endpoint_by_function[function_name]}' endpoint.", 400)
        if not payload[value]:
            raise ApiException(f"Mandatory parameter '{value}' is empty.", 400) #REVISAR - isso pode ser um problema no caso de receber um boolean
        if not isinstance(payload[value], value_type):
            raise ApiException(f"Parameter '{value}' must be of type '{value_type.__name__}'.", 400)
        if "date" in value:
            if not __check_data_format(payload[value]):
                raise ApiException(f"Parameter '{value}' must be in the format 'YYYY-MM-DD'", 400)
            # payload[value] = datetime.strptime(payload[value], "%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 GMT")
    return payload

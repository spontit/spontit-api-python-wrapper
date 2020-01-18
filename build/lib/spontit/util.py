import requests
import json


def put_request(payload):
    """
    A PUT request helper.
    :param payload: The content being PUT
    :return: The content resulting from the PUT request
    """
    r = requests.post("https://www.spontit.com/api", data=payload, json=payload)
    if str(r.status_code) != "200":
        return {
            "Error": "Internal Server Error"
        }
    json_content = json.loads(r.content)
    return json_content

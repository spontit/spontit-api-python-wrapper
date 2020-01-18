import requests
import json


def put_request(payload):
    """

    :param payload:
    :return:
    """
    r = requests.post("https://www.spontit.com/api", data=payload, json=payload)
    print(r.status_code)
    if str(r.status_code) != "200":
        return {
            "Error": "Internal Server Error"
        }
    json_content = json.loads(r.content)
    print(json_content)
    return json_content

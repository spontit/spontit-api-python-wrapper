import requests
import json


def put_request(payload):
    """

    :param payload:
    :return:
    """
    r = requests.post("https://www.spontit.com/api", data=payload, json=payload)
    json_content = json.loads(r.content)
    return json_content

from spontit import util
from enum import Enum
import json


class SpontitResource:
    """
    Use this resource to access your account and related functions.
    """
    class FunctionStrings(Enum):
        """
        An mapping of function to string. For internal use.
        """
        GET_TOPIC_ID_TO_DISPLAY_NAME_MAPPING = "get_topic_id_to_display_name_mapping"
        PUSH = "push"

    def __init__(self, user_id, secret_key):
        """
        Initializes the resource.
        :param user_id: Your user ID.
        :param secret_key: A secret key you generated on spontit.com/secret_keys
        """
        if type(user_id) is not str:
            raise Exception("User ID must be a string.")
        if type(secret_key) is not str:
            raise Exception("Secret key must be a string.")
        self.user_id = user_id
        self.secret_key = secret_key

    def __get_payload_dict(self, method_str):
        """
        Constructs a basic payload dictionary for the method string passed. To be sent with the put request.
        :param method_str: The string representing the method in consideration.
        :return: The payload dictionary
        """
        if type(method_str) is SpontitResource.FunctionStrings:
            method_str = method_str.value
        print(type(method_str))
        assert type(method_str) is str
        return {
            'user_id': self.user_id,
            'secret_key': self.secret_key,
            'method': method_str
        }

    def get_topic_id_to_display_name_mapping(self):
        """
        Sends a put request requesting the topic IDs associated with the user account. You can access the list of topic
        IDs by getting the .keys() of the dictionary returned.
        :return: Returns either a mapping or an error description (with the key "Error")
        """
        return util.put_request(self.__get_payload_dict(self.FunctionStrings.GET_TOPIC_ID_TO_DISPLAY_NAME_MAPPING))

    def push(self,
             call_to_action,
             link=None,
             to_topic_ids=None):
        """
        Use this method to send your own push notification!
        :param call_to_action: The message that you would like to push.
        :param link: [OPTIONAL] A link for content you would like to attach to the push notification
        :param to_topic_ids: [OPTIONAL] A list of topic IDS you would like to push to. If to_topic_ids is not specified,
        then the push notification will be sent to the main channel.
        :return: Returns either a success response or an error description (with the key "Error")
        """
        # Construct the payload.
        payload = self.__get_payload_dict(self.FunctionStrings.PUSH)

        # Type check call_to_action and add to payload.
        if type(call_to_action) is not str:
            raise Exception("Content must be a string.")
        payload["call_to_action"] = call_to_action

        # If link exists, type check and add to payload.
        if link is not None:
            if type(link) is not str:
                raise Exception("URL must be formatted as a string.")
            payload["link"] = link

        # If topic IDs exist, type check and add to payload.
        if to_topic_ids is not None:
            if type(to_topic_ids) is set:
                to_topic_ids = list(to_topic_ids)
            if type(to_topic_ids) is not list:
                raise Exception("The list of topic IDs passed must be a set or a list.")
            payload["to_topic_ids"] = json.dumps(to_topic_ids)
        # Send the put request and return the content.
        return util.put_request(payload)

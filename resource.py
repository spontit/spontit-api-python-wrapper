import util
from enum import Enum


class SpontitResource:
    """

    """
    class FunctionStrings(Enum):
        """

        """
        GET_FOLLOWER_TO_CONTACT_MAPPING = "get_follower_to_contact_mapping"
        GET_FOLLOWER_IDS = "get_follower_ids"
        PUSH = "push"

    def __init__(self, user_id, secret_key):
        """

        :param user_id:
        :param secret_key:
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
            "method": method_str
        }

    def get_follower_ids(self, for_topic_id=None):
        """
        Sends a put request requesting the IDs of the followers for the user ID with which the SpontitResource was
        created. However, if a topic ID is specified, it will instead return the followers for the topic ID for the user
        ID. To get a topic ID, list them using list_topic_ids(...). You can now use these IDs to send personal push
        notifications.
        :param for_topic_id: [OPTIONAL] If specified, the function will return the followers for the topic passed,
        rather than the user account. Keep in mind that Spontit users can follow your topic without following you and
        they can follow you without following your topic (i.e. topic followers are not necessarily a subset of
        your main account's followers).
        :return:
        """
        # Construct the payload for the method.
        payload = self.__get_payload_dict(self.FunctionStrings.GET_FOLLOWER_IDS)

        # If the topic ID exists, type check it and add it to the payload.
        if for_topic_id is not None:
            if for_topic_id is not str:
                raise Exception("Topic ID must be a string.")
            payload["topic"] = for_topic_id

        # Send the put request and return the content.
        return util.put_request(payload)

    def get_topic_id_to_display_name_mapping(self):
        """
        Sends a put request requesting the topic IDs associated with the user account. You can access the list of topic
        IDs by getting the .keys() of the dictionary returned.
        :return:
        """
        return util.put_request(self.__get_payload_dict(self.FunctionStrings.GET_TOPIC_ID_TO_DISPLAY_NAME_MAPPING))

    def push(self,
             call_to_action,
             link=None,
             to_topic_ids=None):
        """

        :param call_to_action:
        :param link: [OPTIONAL]
        :param to_topic_ids: [OPTIONAL]
        :return:
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
            payload["to_topic_ids"] = to_topic_ids

        # Send the put request and return the content.
        return util.put_request(payload)


if __name__ == "__main__":
    spontit_src = SpontitResource("josh-wolff", "secret343")
    ids = spontit_src.get_follower_ids()
    spontit_src.push("Hello", link="https://www.google.com", to_topic_ids=["savethelions"])
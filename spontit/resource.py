import requests
import json
import time


class SpontitResource:
    class Expiration:
        """
        Use an instance of this class to set the expiration time in the push function.
        """

        def __init__(self, days, hours, minutes):
            # noinspection PyBroadException
            try:
                assert type(days) == int
                assert type(hours) == int
                assert type(minutes) == int
            except Exception:
                raise Exception("Days, minutes, and hours must be formatted as an int.")
            self.days = days
            self.hours = hours
            self.minutes = minutes

        def get_time_stamp_from_schedule(self, schedule_time_stamp):
            """
            Generates an epoch timestamp of the desired expiration stamp by adding the input desired lifetime of the
            push notification to the value entered for schedule_time_stamp (an epoch timestamp).
            :param schedule_time_stamp: The scheduled time of the push, or the current time if there is not a scheduled
            time. Epoch timestamp.
            :return: The epoch timestamp of the desired expiration stamp.
            """
            return schedule_time_stamp + self.days * 24 * 60 * 60 + self.hours * 60 * 60 + self.minutes * 60

    ENDPOINTS = {
        "get_channel_categories": "get_channel_categories",
        "create_channel": "create_channel",
        "get_display_name_to_channel_id_mapping": "get_my_topics",
        "push": "push"
    }

    def __init__(self, user_id, secret_key):
        """
        Initializes the Spontit Resource.
        :param user_id: Your userId. You can find this on the Profile tab of the iOS Spontit app or in the top left
        of spontit.com once you log-in.
        :param secret_key: Your secret key. To create a secret key, go to spontit.com/secret_keys. Sign in / sign up
        and then click "Add Key" after being redirected to the page. If the redirect fails after signing in, re-enter
        spontit.com/secret_keys.
        """
        if type(user_id) is not str:
            raise Exception("User ID must be a string.")
        if type(secret_key) is not str:
            raise Exception("Secret key must be a string.")
        self.user_id = user_id
        self.secret_key = secret_key

    def __post_request(self, payload, function_name=None, endpoint=None):
        """
        Makes a POST request.
        :param payload: The payload containing the desired query parameters
        :param function_name: The name of the function that is sending the POST request
        :param endpoint: The desired endpoint
        :return:
        """
        assert function_name is not None or endpoint is not None
        if function_name is not None:
            endpoint = self.ENDPOINTS[function_name]
        url = "https://api.spontit.com/v2/"
        r = requests.post(url + endpoint, data=payload, json=payload)
        json_content = json.loads(r.content)
        return json_content

    def __get_payload_dict(self):
        """
        Constructs a basic payload dictionary for your credentials
        :return: The payload dictionary
        """
        return {
            'secretUser': self.user_id,
            'secretKey': self.secret_key
        }

    def get_channel_categories(self):
        """
        Gets a list of categories that you can use when creating a new channel.
        :return: A list of categories. Each category is a dict with the attributes channelCode and categoryName.
        """
        return self.__post_request(self.__get_payload_dict(), self.get_channel_categories.__name__)

    def create_channel(self, display_name, channel_code=99):
        """
        Creates a new channel. You will then be able to push and invite to this channel separately from your main
        account.
        :param display_name: The display name of the new channel you want to create.
        :param channel_code: The channel code that defines the category of your channel. The default is 99. To get a
        mapping of channel codes to category names, call get_channel_categories.
        :return:
        """
        payload = self.__get_payload_dict()
        assert type(channel_code) is int
        assert type(display_name) is str
        payload["displayName"] = display_name
        payload["channelCode"] = int(channel_code)
        return self.__post_request(payload, self.create_channel.__name__)

    def get_invite_options(self, channel_id=None):
        """
        Gets the invite options for the given channel. Get the channel ID using get_display_name_to_channel_id_mapping.
        :param channel_id: The ID of the channel that you want invite options for
        :return: Invite options; or an error, if there is one
        """
        if channel_id is None:
            channel_id = self.user_id
        assert type(channel_id) is str

        options = {
            "link": "https://spontit.com/" + channel_id
        }

        # Get the number to which to text the referral code.
        current_texting_number_data = self.__post_request(self.__get_payload_dict(),
                                                          endpoint="get_current_texting_number")
        texting_number = None
        if "data" not in current_texting_number_data:
            # Error received
            return current_texting_number_data
        if "number" in current_texting_number_data["data"]:
            texting_number = current_texting_number_data["data"]["number"]
            options["textCodeTo"] = texting_number

        # Get the referral code.
        sub_item_payload = self.__get_payload_dict()
        sub_item_payload["subscription"] = channel_id
        subscription_item = self.__post_request(sub_item_payload, endpoint="get_subscription_item")
        if "data" not in subscription_item:
            # Error received.
            return subscription_item
        if "referralCode" in subscription_item["data"]:
            referral_code = subscription_item["data"]["referralCode"]
            options["referralCode"] = referral_code
            if texting_number is not None:
                options["signUpViaText"] = "Text @" + str(referral_code) + " to " + str(texting_number) + "."

        return {
            "data": {
                "inviteOptions": options
            }
        }

    def get_display_name_to_channel_id_mapping(self):
        """
        Maps human display names to the ID of the channel. When you create a channel, you supply a human-readable
        display name, which creates an ID. You need this ID to push to that channel and get its invite options.
        :return: The mapping; or an error if there is one
        """
        channel_data = self.__post_request(self.__get_payload_dict(), endpoint="get_my_channels")
        if "data" not in channel_data:
            # Error received
            return channel_data
        channel_id_to_display_name_map = {}
        for channel in channel_data["data"]:
            channel_id = channel.get("subscription", None)
            display_name = channel.get("displayName", None)
            if channel_id is not None:
                channel_id_to_display_name_map[display_name] = channel_id
        return {
            "data": channel_id_to_display_name_map
        }

    def push(self,
             call_to_action,
             subtitle=None,
             body=None,
             schedule_time_stamp=None,
             expiration=None,
             link=None,
             should_open_link_in_app=None,
             ios_deep_link=None,
             channel_id=None):
        """
        Sends a push notification.
        :param call_to_action: The primary content of the push notification. Limited to 100 characters. Appears in the
        notification itself.
        :param subtitle: A subtitle to include in the push notification. Does not appear after opening the notification.
        :param body: A body of up to 500 characters to include for when the user opens the push notification. Currently
        only available for iOS.
        :param schedule_time_stamp: Schedule the push notification for a later time. Int, epoch timestamp.
        :param expiration: Length of time for which the notification should exist. Set to Expiration.
        :param link: A link to include in the notification. Appears once the user opens the notification.
        :param should_open_link_in_app: Whether or not to open the attached link within the Spontit app or externally
        in the Safari browser or other app. Set to False when attaching a website to the link attribute that you
        expect to open within an app (e.g. a Tweet that you want to open inside of the Twitter app).
        :param ios_deep_link: A deep link to another iOS app of the format *://*. Only for iOS versions >= v6.0.1.
        :param channel_id: The channel ID of the push notification to send to. Default is your main channel. To get a
        channel ID, call get_display_name_to_channel_id_mapping. To create a channel, call create_channel.
        :return: The result of the call, either with an error or with a result.
        """
        # Construct the payload.
        payload = self.__get_payload_dict()

        # Type check call_to_action and add to payload.
        assert type(call_to_action) == str
        payload["callToAction"] = call_to_action

        # If link exists, type check and add to payload.
        if link is not None:
            assert type(link) == str
            payload["link"] = link

        if should_open_link_in_app is not None:
            assert type(should_open_link_in_app) == bool
            payload["openLinkInApp"] = int(bool(should_open_link_in_app))

        if subtitle is not None:
            assert type(subtitle) == str
            payload["subtitle"] = subtitle

        if body is not None:
            assert type(body) == str
            payload["body"] = body

        if schedule_time_stamp is not None:
            if type(schedule_time_stamp) is not int:
                raise Exception("The schedule time stamp must be formatted as an int. "
                                "You can get an epoch timestamp here: https://www.epochconverter.com/")
            payload["scheduled"] = schedule_time_stamp

        if expiration is not None:
            if type(expiration) is not self.Expiration:
                raise Exception("\"Expiration\" value must be formatted using an instance of the Expiration class "
                                "available via the command \"from spontit import Expiration\".")
            payload["expirationStamp"] = expiration.get_time_stamp_from_schedule(
                schedule_time_stamp if schedule_time_stamp is not None else int(time.time()))

        if ios_deep_link is not None:
            assert type(ios_deep_link) == str
            payload["iOSDeepLink"] = ios_deep_link

        payload["userId"] = self.user_id
        if channel_id is not None:
            assert type(channel_id) == str
            payload["userId"] = channel_id

        return self.__post_request(payload, self.push.__name__)

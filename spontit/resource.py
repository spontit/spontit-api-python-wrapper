import json
import time
from enum import Enum
import requests


class SpontitResource:

    __url = "https://api.spontit.com/v3/"

    class RequestMethod(Enum):
        GET = "GET"
        POST = "POST"
        PATCH = "PATCH"
        DELETE = "DELETE"

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

    def __init__(self, user_id, secret_key):
        """
        Initializes the Spontit Resource.
        :param user_id: Your userId. You can find this on the Profile tab of the iOS Spontit app or
        at spontit.com/profile after signing in
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

    def _get_headers(self):
        """
        Get the headers with the appropriate authentication parameters
        :return: The headers
        """
        return {
            'X-UserId': self.user_id,
            'X-Authorization': self.secret_key
        }

    def _request(self, payload, endpoint, request_method, files=None, headers=None):
        """
        Makes a POST request.
        :param payload: the payload containing the parameters
        :param endpoint: the desired endpoint
        :param request_method: the method (e.g. POST, GET, PATCH, DELETE)
        :param files: files to send. only used when changing a profile image
        :param headers: headers for the request. only specified when changing a profile image
        :return:
        """
        if headers is None:
            headers = self._get_headers()

        if files is None:
            r = requests.request(
                request_method.value,
                url=self.__url + endpoint,
                data=json.dumps(payload),
                headers=headers
            )
        else:
            r = requests.request(
                request_method.value,
                url=self.__url + endpoint,
                data=payload,
                files=files,
                headers=headers
            )
        try:
            json_content = json.loads(r.content)
        except json.decoder.JSONDecodeError:
            return r
        return json_content

    def get_categories(self):
        """
        Gets a list of categories that you can use when creating a new channel.
        :return: a list of categories. each category is a dict with the attributes categoryCode and categoryName.
        """
        return self._request(
            payload={},
            endpoint="categories",
            request_method=self.RequestMethod.GET
        )

    def create_channel(self, channel_name, category_code=99):
        """
        Creates a new channel. You will then be able to push and invite to this channel separately from your main
        account.
        :param channel_name: the name of the new channel you want to create
        :param category_code: the category code that defines the category of your channel. default is 99. to get a
        mapping of channel codes to category names, call get_categories
        :return: the new channel
        """
        assert type(category_code) is int
        assert type(channel_name) is str

        return self._request(
            payload={
                "channelName": channel_name,
                "categoryCode": category_code
            },
            endpoint="channel",
            request_method=self.RequestMethod.POST
        )

    def delete_channel(self, channel_name):
        """
        Deletes a channel with the specified name
        :param channel_name: the name of the channel to delete
        :return: the response of the request
        """
        return self._request(
            payload={
                "channelName": channel_name
            },
            endpoint="channel",
            request_method=self.RequestMethod.DELETE
        )

    def update_channel(self,
                       channel_name,
                       add_all_followers=None,
                       auto_add_future_followers=None,
                       category_code=None):
        """
        Updates the channel.
        :param channel_name: the name of the channel to change
        :param add_all_followers: whether to add all followers from your main channel to this channel
        :param auto_add_future_followers: whether to add all followers to the main channel (your account) to this
        channel as well (so that they follow both channels)
        :param category_code: the category code to change. List available categories with the get_categories function
        :return: the new channel item
        """
        payload = {
            "channelName": channel_name
        }

        if add_all_followers is not None:
            payload['addAllFollowers'] = add_all_followers
        if auto_add_future_followers is not None:
            payload['autoAddFutureFollowers'] = auto_add_future_followers
        if category_code is not None:
            payload['categoryCode'] = category_code

        return self._request(
            payload=payload,
            endpoint="channel",
            request_method=self.RequestMethod.PATCH
        )

    def get_channel(self, channel_name=None):
        """
        If channel_name is not provided, the user's main channel is returned. (This is the default channel that
        you push to if you do not create a channel. This is also known as the main channel.)

        :param channel_name: the name of the channel to retrieve. if None, the main channel (your account channel) will
        be retrieved
        :return: the channel
        """
        payload = dict()
        if channel_name is not None:
            payload = {
                "channelName": channel_name
            }
        return self._request(
            payload=payload,
            endpoint="channel",
            request_method=self.RequestMethod.GET
        )

    def get_channels(self):
        """
        Lists the channels
        :return: Your channels
        """
        return self._request(
            payload={},
            endpoint="channels",
            request_method=self.RequestMethod.GET
        )

    def channel_profile_image_upload(self, image_path, is_png, channel_name=None):
        """
        :param image_path: the path to the image
        :param is_png: whether or not the image is PNG or JPEG
        :param channel_name: the channel name of the channel whose profile image is being changed. if None, the user
        account's profile image will change
        :return: the response from the request
        """

        file_type = "image/jpeg"
        if is_png:
            file_type = "image/png"

        files = {
            'image': ("my_file_name", open(image_path, 'rb'), file_type)
        }

        if channel_name is None:
            payload = dict()
        else:
            payload = {
                "channelName": channel_name
            }

        return self._request(
            payload=payload,
            endpoint="channel/profile_image",
            request_method=self.RequestMethod.POST,
            files=files
        )

    def list_followers(self, channel_name=None):
        # Construct the payload.
        payload = dict()
        if channel_name is not None:
            assert type(channel_name) == str
            payload["channelName"] = channel_name

        # Make the request.
        return self._request(
            payload=payload,
            endpoint="followers",
            request_method=self.RequestMethod.GET
        )

    def push(self,
             message,
             push_title=None,
             ios_subtitle=None,
             body=None,
             push_to_followers=None,
             schedule_time_stamp=None,
             expiration=None,
             link=None,
             should_open_link_in_app=None,
             ios_deep_link=None,
             channel_name=None):
        """
        Sends a push notification.
        :param message: The primary content of the push notification. Limited to 100 characters. Appears in the
        notification itself.
        :param push_title: A title of your push. Limited to 100 characters.
        :param ios_subtitle: A subtitle to include in the push notification. Does not appear after opening the
        notification. Limited to 20 characters.
        :param body: A body of up to 5000 characters to include for when the user opens the push notification. Currently
        only available for iOS.
        :param push_to_followers: The specific followers to send the push to. A list of strings of the userIds
        :param schedule_time_stamp: Schedule the push notification for a later time. Int, epoch timestamp.
        :param expiration: Length of time for which the notification should exist. Set to Expiration.
        :param link: A link to include in the notification. Appears once the user opens the notification.
        :param should_open_link_in_app: Whether or not to open the attached link within the Spontit app or externally
        in the Safari browser or other app. Set to False when attaching a website to the link attribute that you
        expect to open within an app (e.g. a Tweet that you want to open inside of the Twitter app).
        :param ios_deep_link: A deep link to another iOS app of the format *://*. Only for iOS versions >= v6.0.1.
        :param channel_name: The name of your channel
        :return: The result of the call, either with an error or with a result.
        """
        # Construct the payload.
        payload = dict()

        # Type check call_to_action and add to payload.
        assert type(message) == str
        payload["message"] = message

        # If link exists, type check and add to payload.
        if link is not None:
            assert type(link) == str
            payload["link"] = link

        if should_open_link_in_app is not None:
            assert type(should_open_link_in_app) == bool
            payload["openLinkInApp"] = int(bool(should_open_link_in_app))

        if push_title is not None:
            assert type(push_title) == str
            payload["pushTitle"] = push_title

        if ios_subtitle is not None:
            assert type(ios_subtitle) == str
            payload["subtitle"] = ios_subtitle

        if body is not None:
            assert type(body) == str
            payload["body"] = body

        if push_to_followers is not None:
            assert type(push_to_followers) == list or type(push_to_followers) == set
            payload["individualFollowers"] = list(push_to_followers)

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

        if channel_name is not None:
            assert type(channel_name) == str
            payload["channelName"] = channel_name

        return self._request(
            payload=payload,
            endpoint="push",
            request_method=SpontitResource.RequestMethod.POST
        )

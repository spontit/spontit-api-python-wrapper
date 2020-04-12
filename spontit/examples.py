from spontit import SpontitResource
import time


class Examples:
    __resource = None

    def __init__(self, resource):
        """
        Initializes an instance of Examples. You can try the different examples in this class.
        To do so, initialize the class and then call one of the functions.
        :param resource: An instance of SpontitResource
        """
        assert type(resource) == SpontitResource
        self.__resource = resource

    def simple_push_example(self):
        """
        Sends a simple push notification.
        :return: The result of the call to push
        """
        return self.__resource.push("Hello!")

    def scheduled_push(self):
        """
        Schedules a push notification for one hour from the current time.
        :return: The result of the call to push
        """
        # 3600 seconds in one hour
        return self.__resource.push("Hello, in 1 hour",
                                    schedule_time_stamp=int(time.time()) + 3600)

    def immediate_expiration_push(self):
        """
        Sends a push notification and sets the expiration for the current time. Because our expiration function
        polls approximately every 15-30 minutes, the notification will delete within 30 minutes.
        :return: The result of the call to push
        """
        return self.__resource.push("Hello, expire ASAP (within 15 minutes)",
                                    expiration=SpontitResource.Expiration(0, 0, 0))

    def expire_one_hour_after_schedule(self):
        """
        Schedules a push notification for one hour from now, and then expires it one hour later.
        :return: The result of the call to push
        """
        return self.__resource.push("Hello, in 1 hour. Bye in 2.",
                                    schedule_time_stamp=int(time.time()) + 3600,
                                    expiration=SpontitResource.Expiration(days=0, hours=1, minutes=0))

    def rate_limit_example(self):
        """
        Spontit currently only supports sending one push notification per second.
        This function throttles that limit as an example of what you can expect if you exceed that limit.
        :return: The final response of the 10 calls to push.
        """
        response = None
        for _ in range(10):
            response = self.simple_push_example()
            print(response)
        return response

    def subtitle_body_example(self):
        """
        Sends a push notification with a subtitle and a body.
        :return: The result of the call to push
        """
        return self.__resource.push("Hello!",
                                    subtitle="An API Notice",
                                    body="This is a body. You can write up to 500 characters "
                                         "in the body. The body does not show up in the push "
                                         "notification. The body only appears once the user "
                                         "opens the notification with their mobile phone. Currently,"
                                         " the body only shows on iOS devices, but we will change "
                                         "this soon. As a side note, the subtitle only shows on "
                                         "the push notification, but does not show when the user "
                                         "opens the app. Currently, the subtitle is only supported "
                                         "for iOS devices.")

    def post_a_link_ex_1(self):
        """
        Sends a push notification with a link to Jack Dorsey's first tweet. should_open_link_in_app is set to False
        so that the Twitter app opens (rather than opening twitter.com within the Spontit app).
        :return: The result of the call to push
        """
        return self.__resource.push("Jack's first tweet.",
                                    link="https://twitter.com/jack/status/20",
                                    should_open_link_in_app=False,
                                    body="This link does not open within the app. The purpose "
                                         "is that we want the Twitter app to open. If set "
                                         "should_open_link_in_app to True, then the link would "
                                         "open within the Spontit app and the app would not "
                                         "launch.")

    def post_a_link_ex_2(self):
        """
        Sends a push notification with a link to Amazon.com.
        :return: The result of the call to push
        """
        return self.__resource.push("Buy from Amazon.",
                                    link="https://amazon.com")

    def post_a_link_ex_3(self):
        """
        Sends a push notification linking the Spontit review compose window in the App Store. should_open_link_in_app is
        set to False so that the App Store opens.
        :return: The result of the call to push
        """
        return self.__resource.push("Please give Spontit 5 stars!!!",
                                    link="https://itunes.apple.com/app/id1448318683?action=write-review",
                                    should_open_link_in_app=False)

    def post_an_ios_deep_link_ex_1(self):
        """
        Sends a push notification deep linking to Stocks app.
        Only works for iOS Spontit App, >= v6.0.1
        :return: The result of the call to push
        """
        return self.__resource.push("Open the stocks app.",
                                    ios_deep_link="stocks://")

    def post_an_ios_deep_link_ex_2(self):
        """
        Sends a push notification deep linking to the gallery tab of the Shortcuts app.
        Only works for iOS Spontit App, >= v6.0.1
        :return: The result of the call to push
        """
        return self.__resource.push("Open the gallery tab of the Shortcuts app.",
                                    ios_deep_link="shortcuts://gallery")

    def post_an_ios_deep_link_ex_3(self):
        """
        Pushes a notification that deep links to the Spontit review creation window in the App Store.
        :return: The result of the call to push
        """
        return self.__resource.push("Please give Spontit 5 stars!!!",
                                    ios_deep_link="itms-apps://itunes.apple.com/app/id1448318683?action=write-review")

    def create_new_channel(self):
        """
        Creates a new channel
        :return: The new channel
        """
        return self.__resource.create_channel("My First Custom Channel")

    def create_new_channel_with_category(self):
        """
        Creates a new channel with a category code of 0.
        :return: The new channel
        """
        available_categories = self.__resource.get_channel_categories()
        category_code = 0
        if 'data' in available_categories and len(available_categories['data']) > 0:
            category_code = available_categories['data'][0].get('categoryCode', 0)

        new_display_name = "My New Channel"
        return self.__resource.create_channel(new_display_name, category_code)

    def create_new_channel_and_push_to_it(self):
        """
        Creates a new channel and sends a simple push notification to it.
        :return: The result of the push notification
        """
        new_channel_display_name = "Push Push Channel"
        _ = self.__resource.create_channel(new_channel_display_name)

        # The channel might not have been completely initialized just yet. It is generally recommended to create your
        # channels prior to pushing. Sleeping is far less than ideal, and we will work on a better solution to
        # create channels on the fly. If you have any requests, please create an issue in the repo.
        time.sleep(1.0)

        mapping = self.__resource.get_display_name_to_channel_id_mapping()
        if 'data' in mapping:
            channel_id_to_push_to = mapping['data'].get(new_channel_display_name, None)
            if channel_id_to_push_to is not None:
                return self.__resource.push("Hello!",
                                            channel_id=channel_id_to_push_to)
        return {
            "errors": {
                "message": "Channel not found."
            }
        }

    def create_new_channel_and_get_invite_options(self):
        """
        Creates a new channel and gets the invite options.
        :return: The ways to invite someone to the channel, if the channel exists
        """
        new_channel_display_name = "Invite Me Channel"
        _ = self.__resource.create_channel(new_channel_display_name)

        # The channel might not have been completely initialized just yet. It is generally recommended to create your
        # channels prior to pushing. Sleeping is far less than ideal, and we will work on a better solution to
        # create channels on the fly. If you have any requests, please create an issue in the repo.
        time.sleep(1.0)

        mapping = self.__resource.get_display_name_to_channel_id_mapping()
        if 'data' in mapping:
            channel_id_to_invite_to = mapping['data'].get(new_channel_display_name, None)
            if channel_id_to_invite_to is not None:
                return self.__resource.get_invite_options(channel_id_to_invite_to)
        return {
            "errors": {
                "message": "Channel not found."
            }
        }

    def get_invite_options_for_my_main_account(self):
        """
        Gets the invite options for your main channel.
        :return: The response
        """
        return self.__resource.get_invite_options()


if __name__ == "__main__":
    # Try an example...
    spontit_src = SpontitResource("my_username", "my_secret_key")
    example_instance = Examples(spontit_src)
    response = example_instance.simple_push_example()
    print("Simple push example result: " + str(response))

    # ...or get right to pushing!
    response = spontit_src.push("Hello!!!")
    print("Result: " + str(response))

    # To see documentation, run:
    help(SpontitResource)

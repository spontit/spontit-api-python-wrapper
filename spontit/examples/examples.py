from spontit import SpontitResource
import time


class Examples:
    __resource = None

    def __init__(self, resource):
        """
        Initializes an instance of Examples. You can try the different examples in this class.
        To do so, initialize the class and then call one of the functions.
        :param resource: an instance of SpontitResource
        """
        assert type(resource) == SpontitResource
        self.__resource = resource

    def simple_push_example(self):
        """
        Sends a simple push notification.
        :return: the result of the call to push
        """
        response = self.__resource.push("Hello!")
        print(response)
        return response

    def simple_push_to_specific_followers_example(self):
        """
        Sends a push notification to specifically you. You can specify which followers should receive the notification
        as shown below. To list your followers, see the list_followers_example().
        :return:
        """
        followers = [self.__resource.user_id]
        response = self.__resource.push(
            "Hello to myself!",
            body="No one else can see this until I specifically share it with them, by either sharing"
            " the link or tagging them in the comments.",
            push_to_followers=followers
        )
        print(response)
        return response

    def simple_push_to_specific_phone_numbers_and_emails_example(self):
        """
        Sends a push notification to phone numbers and emails. We link the user account to the phone numbers and emails
        defined, and then send a push via Spontit.
        The users linked **do not have to follow your account** to receive the push notification.
        They will have the option to follow you or report you for spam. If you are reported for spam multiple times,
        your account will be restricted.
        :return:
        """
        # TODO- Replace with a real phone number.
        phone_numbers = ["+18005550101"]
        # TODO- Replace with a real email.
        emails = ['fake.email@fake.com']
        response = self.__resource.push(
            "Hello to other users!",
            body="Add any phone numbers or emails to this push. Tell users to sign up on Spontit with the same "
                 "phone number / email as they signed up with using your service. Then you can push directly to them.",
            push_to_phone_numbers=phone_numbers,
            push_to_emails=emails
        )
        print(f"Notification sent to:\nEmails: {str(emails)}\nPhone numbers: {str(phone_numbers)}")
        print(response)
        return response

    def list_followers_example(self):
        """
        Lists all your followers.
        :return:
        """
        response = self.__resource.list_followers()
        print(response)
        return response

    def specific_followers_and_channel_example(self):
        """
        Sends a push notification to a specific user following the channel. The user must be following the channel in
        order to receive it. You can specify which followers should receive the notification as shown below. To list
        your followers, see the list_followers_for_channel_example().
        :return:
        """
        # Create the channel if it is not yet created.
        self.__resource.create_channel("Test channel")
        followers = [self.__resource.user_id]
        response = self.__resource.push(
            f"Hello to {followers[0]}",
            channel_name="Test channel",
            push_to_followers=followers
        )
        print(response)
        return response

    def list_followers_for_channel_example(self):
        """
        Lists all your followers for this particular channel.
        :return:
        """
        self.__resource.create_channel("Test channel")
        response = self.__resource.list_followers(
            channel_name="Test channel"
        )
        print(response)
        return response

    def scheduled_push(self):
        """
        Schedules a push notification for one hour from the current time.
        :return: the result of the call to push
        """
        return self.__resource.push("Hello, in 1 hour",
                                    schedule_time_stamp=int(time.time()) + 3600)

    def immediate_expiration_push(self):
        """
        Sends a push notification and sets the expiration for the current time. Because our expiration function
        polls approximately every 15-30 minutes, the notification will delete within 30 minutes.
        :return: the result of the call to push
        """
        return self.__resource.push("Hello, expire ASAP (within 15 minutes)",
                                    expiration=SpontitResource.Expiration(0, 0, 0))

    def expire_one_hour_after_schedule(self):
        """
        Schedules a push notification for one hour from now, and then expires it one hour later.
        :return: the result of the call to push
        """
        return self.__resource.push("Hello, in 1 hour. Bye in 2.",
                                    schedule_time_stamp=int(time.time()) + 3600,
                                    expiration=SpontitResource.Expiration(days=0, hours=1, minutes=0))

    def subtitle_body_example(self):
        """
        Sends a push notification with a subtitle and a body.
        :return: the result of the call to push
        """
        return self.__resource.push("Hello!",
                                    ios_subtitle="An API Notice",
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
        :return: the result of the call to push
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
        :return: the result of the call to push
        """
        return self.__resource.push("Buy from Amazon.",
                                    link="https://amazon.com")

    def post_a_link_ex_3(self):
        """
        Sends a push notification linking the Spontit review compose window in the App Store. should_open_link_in_app is
        set to False so that the App Store opens.
        :return: the result of the call to push
        """
        return self.__resource.push("Please rate Spontit in the App Store!",
                                    push_title="Spontit Rating Request",
                                    link="https://itunes.apple.com/app/id1448318683?action=write-review",
                                    should_open_link_in_app=False)

    def post_an_ios_deep_link_ex_1(self):
        """
        Sends a push notification deep linking to Stocks app.
        Only works for iOS Spontit App, >= v6.0.1
        :return: the result of the call to push
        """
        return self.__resource.push("Open the stocks app.",
                                    ios_deep_link="stocks://")

    def post_an_ios_deep_link_ex_2(self):
        """
        Sends a push notification deep linking to the gallery tab of the Shortcuts app.
        Only works for iOS Spontit App, >= v6.0.1
        :return: the result of the call to push
        """
        return self.__resource.push("Open the gallery tab of the Shortcuts app.",
                                    ios_deep_link="shortcuts://gallery")

    def post_an_ios_deep_link_ex_3(self):
        """
        Pushes a notification that deep links to the Spontit review creation window in the App Store.
        :return: the result of the call to push
        """
        return self.__resource.push("Please rate Spontit in the App Store!",
                                    push_title="Spontit Rating Request",
                                    ios_deep_link="itms-apps://itunes.apple.com/app/id1448318683?action=write-review")

    def create_new_channel(self):
        """
        Creates a new channel.
        :return: the new channel
        """
        response = self.__resource.create_channel("My First Custom Channel")
        return Examples.__get_channel_from_response(response)

    def create_new_channel_with_category(self):
        """
        Creates a new channel with a category code of 0.
        :return: the new channel
        """
        available_categories = self.__resource.get_categories()
        category_code = 0
        if 'data' in available_categories and len(available_categories['data']) > 0:
            category_code = available_categories['data'][0].get('categoryCode', 0)

        new_display_name = "My New Channel"
        response = self.__resource.create_channel(new_display_name, int(category_code))
        return Examples.__get_channel_from_response(response)

    def create_new_channel_with_profile_image_and_push_to_it(self):
        """
        Creates a new channel, uploads a profile image, and sends a simple push notification to it.
        You should see the profile image in the push notification.

        To change the profile image of your account (main channel), simply call channel_profile_image_upload
        without supplying a channel name.

        :return: the result of the push notification request
        """
        new_channel_display_name = "Profile Image Channel"
        _ = self.__resource.create_channel(new_channel_display_name)

        import os
        cwd = os.getcwd()  # Get the current working directory (cwd)
        print(cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print(files)

        response = self.__resource.channel_profile_image_upload(
            image_path="examples/orange.png",
            is_png=True,
            channel_name=new_channel_display_name
        )
        self.__resource.push(
            "Hello new channel!",
            channel_name=new_channel_display_name
        )
        print("After uploading a profile image, you receive a URL that you can use to confirm the upload succeeded.")
        print("You can also view the result of the push. You should see the channel image in the push, provided you "
              "have good connection.")
        print(response)

    def create_new_channel_and_update_its_settings(self):
        """
        Creates a new channel and sends a simple push notification to it.
        :return: the result of the push notification request
        """
        new_channel_display_name = "Push Push Channel"
        _ = self.__resource.create_channel(new_channel_display_name)
        self.__resource.update_channel(
           new_channel_display_name,
           add_all_followers=True,
           auto_add_future_followers=True,
           category_code=1
        )

    def create_and_then_delete_channel(self):
        """
        Creates a channel and then deletes it.
        :return: the channel (before deletion)
        """
        new_channel_display_name = "Invite Me Channel"
        response = self.__resource.create_channel(new_channel_display_name)
        print("Delete Response:", self.__resource.delete_channel(new_channel_display_name))
        return Examples.__get_channel_from_response(response)

    def create_new_channel_and_get_invite_options(self):
        """
        Creates a new channel and print out the item. Embedded in the channel item are the invite options
        :return: the channel item
        """
        new_channel_display_name = "Invite Me Channel"
        response = self.__resource.create_channel(new_channel_display_name)
        return Examples.__get_channel_from_response(response)

    def get_invite_options_for_my_main_account(self):
        """
        Get the main channel. Embedded in the main channel are the invite options
        :return: the main channel (your account)
        """
        response = self.__resource.get_channel()
        return Examples.__get_channel_from_response(response)

    def list_my_channels(self):
        """
        List all created channels
        :return: the channels
        """
        response = self.__resource.get_channels()
        return Examples.__get_channel_from_response(response)

    @staticmethod
    def __get_channel_from_response(response):
        """
        Print the channel from the responses. This function assumes a response is passed that contains "data". If not,
        it catches the KeyError and prints the error
        :param response: the response received from the Channel endpoint
        :return: either the new channel item or None
        """
        try:
            new_channel = response['data']
            print(new_channel)
            return new_channel
        except KeyError:
            print(response)
            return None

    def do_everything(self):
        """
        Runs every example. Are you ready?
        :return:
        """
        example_functions = [
            self.simple_push_example,
            self.scheduled_push,
            self.immediate_expiration_push,
            self.simple_push_to_specific_followers_example,
            self.simple_push_to_specific_phone_numbers_and_emails_example,
            self.list_followers_example,
            self.list_followers_for_channel_example,
            self.specific_followers_and_channel_example,
            self.expire_one_hour_after_schedule,
            self.subtitle_body_example,
            self.post_a_link_ex_1,
            self.post_a_link_ex_2,
            self.post_an_ios_deep_link_ex_3,
            self.create_new_channel,
            self.create_new_channel_with_category,
            self.create_new_channel_with_profile_image_and_push_to_it,
            self.create_new_channel_and_update_its_settings,
            self.create_and_then_delete_channel,
            self.create_new_channel_and_get_invite_options,
            self.get_invite_options_for_my_main_account,
            self.list_my_channels
        ]

        for func in example_functions:
            # Added time.sleep(1) because of the rate limit. Only one push per second per channel.
            # (e.g. You can have two pushes in the same second if each goes to a different channel.)
            # See rate_limit_example
            print(func.__name__)
            func()
            time.sleep(1)
            print("")


if __name__ == "__main__":
    # Try an example...
    # Get your userId at spontit.com/profile
    # Get your secretKey at spontit.com/secret_keys
    spontit_src = SpontitResource("my_user_id", "my_secret_key")
    example_instance = Examples(spontit_src)

    push_response = example_instance.simple_push_example()
    print("Simple push example result: " + str(push_response))

    # ...or be bold...
    example_instance.do_everything()

    # ...or get right to pushing!
    push_response = spontit_src.push("Hello!!!")
    print("Result: " + str(push_response))

    # To see documentation, run:
    help(SpontitResource)

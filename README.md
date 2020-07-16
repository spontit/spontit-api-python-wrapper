# SPONTIT :vibration_mode:

Check out our complete API documentation at <a href="https://api.spontit.com">api.spontit.com</a>. Our API repository is available <a href="https://github.com/spontit/spontit-api">here</a>.

## Send push notifications without your own app. :punch:
Using the Spontit API and Spontit app/webapp, you can send your own push notifications programmatically to Android, iOS, and Desktop devices. You can send your own in less than 5 minutes. :sunglasses: :trophy: (Without touching Swift, Objective-C, Java, XCode, Android Studio, the App Store approval process... :dizzy_face:).

This repository is the Python wrapper for our API. To see code snippets for several languages, see our documentation <a href="https://api.spontit.com">here</a>.

## TL;DR :running:

**Spontit is 100% free! Please star the repo and rate/review the Spontit app in the App Store as well. Please invite a friend or two to Spontit!**

1) Sign up at <a href="https://www.spontit.com" target="_blank">spontit.com</a> (you might need to click "Take me to the Desktop version"). Note down your username. It should be displayed on your <a href="https://spontit.com/profile" target="_blank">profile</a> once you are signed in.
2) Get a secret key at <a href="https://www.spontit.com/secret_keys" target="_blank">spontit.com/secret_keys</a>. 
3) Get the <a href="https://apps.apple.com/us/app/spontit/id1448318683">iPhone app</a> or <a href="https://play.google.com/store/apps/details?id=xyz.appmaker.nqratw">Android app</a>. Sign in with the same account and allow notifications. See Step 11 to invite others.
4) `pip install spontit --upgrade && pip install requests`
5) `from spontit import SpontitResource`
6) `resource = SpontitResource(my_username, my_secret_key)`
7) `response = resource.push("Hello!")`
8) Run the command `help(SpontitResource)` in Python for complete documentation.
9) Or try an example! Check out the <a href="https://github.com/spontit/spontit-api-python-wrapper/blob/master/spontit/examples/examples.py">examples</a>.
10) You can customize the image of the notification on the website, iPhone app, or via the API by setting the image for the respective channel. See the image example titled `create_new_channel_with_profile_image_and_push_to_it` in the <a href="https://github.com/spontit/spontit-api-python-wrapper/blob/master/spontit/examples/examples.py">examples</a>.
11) To push to others, have them follow the channel to which you will push (e.g. share <a href="https://spontit.com">spontit.com/my_username</a>). You can see available invite options by calling `print(resource.get_channel(...))` and supply the channel name. See the functions titled `create_new_channel_and_get_invite_options` and `get_invite_options_for_my_main_account` in the <a href="https://github.com/spontit/spontit-api-python-wrapper/blob/master/spontit/examples/examples.py">examples</a>.
12) We are constantly working on expanding the functionality of Spontit. We GREATLY appreciate your input - feel free to <a href="https://github.com/spontit/spontit-api-python-wrapper/issues/new" target="_blank">add a feature request</a> on our Github. :smiley:

### Getting Started :white_check_mark:

#### Make an Account

First, go to <a href="https://www.spontit.com" target="_blank">spontit.com</a> or download the <a href="https://itunes.apple.com/us/app/spontit/id1448318683" target="_blank">Spontit app</a>.
Create an account and get your user ID. To see your user ID in the app, tap the "Profile" tab. To see your user ID on the website, look at the top of the screen.

You can change your user ID at any time <a href="https://www.spontit.com/profile" target="_blank">here</a>.

#### Generate a Secret Key

Once you have made an account, generate a secret key <a href="https://spontit.com/secret_keys">here</a>. You might have to re-authenticate.

#### Push Notification UI Anatomy

You can change your user ID and display name at any time <a href="https://www.spontit.com/profile">here</a>.

<p align="center">
    <img src="https://github.com/spontit/spontit-api-python-wrapper/raw/master/images/main_channel_push.png" /> 
</p>

Above we see a push notification sent to the main channel. Here, "Josh Wolff" is the display name of the user. The push message is the displayed text. The image shown is the personal profile picture of the user (see step 10 above). If the user opens the notification, they can open a link attached, if any, among other options (`help(SpontitResource)`). If they have an iPhone, they can like and comment on the notification.

<p align="center">
    <img src="https://github.com/spontit/spontit-api-python-wrapper/raw/master/images/topic_push.png" /> 
</p>

Above we see a push notification to a channel (separate from the main channel). Josh owns this channel, but as you can see, it looks like its own account. "Dem 2020 Polls" is the channel name, the non-bold text is the message, and the image is the image set for the channel (see step 10 above). You can also change the push title with the pushTitle attribute.

#### Note on Our Development Priorities

We prioritize development of the iOS application over the website. If at any time, we describe a feature and it does not seem to be on the website, it might only exist in the iOS application. Please email us at info {at} spontit {dot} io so that we can clarify this to you and other developers. You are more than welcome to <a href="https://github.com/spontit/spontit-api-python-wrapper/issues/new" target="_blank">add a feature request</a>.

# SPONTIT :vibration_mode:
## Send push notifications without your own app. :punch:
Using the Spontit API and Spontit app/webapp, you can send your own push notifications programmatically to Android, iOS, and Desktop devices. You can send your own in less than 5 minutes. :sunglasses: :trophy: (Without touching Swift, Objective-C, Java, XCode, Android Studio, the App Store approval process... :dizzy_face:).


## TL;DR :running:

1) Sign up at <a href="https://www.spontit.com" target="_blank">spontit.com</a> (you might need to click "Take me to the Desktop version."). Note down your username. It should be displayed in the top left of the <a href="https://spontit.com/home">homepage</a>.
2) Get a secret key at <a href="https://www.spontit.com/secret_keys" target="_blank">spontit.com/secret_keys</a>. 
3) Get the iPhone app or Android app. Sign in and allow notifications.
4) `pip install spontit --upgrade && pip install requests`
5) `from spontit import SpontitResource`
6) `resource = SpontitResource(my_username, my_secret_key)`
7) `response = resource.push("Hello!")`
8) Run the command `help(SpontitResource)` in Python for complete documentation.
9) Or try an example! Check out the examples at https://github.com/joshwolff1/spontit_api/blob/master/spontit/examples.py
10) You can customize the image of the notification on the website or iPhone app by setting the image for the respective channel. Sub-channel image customization is currently only supported on the iPhone app. 
11) To push to others, have them follow the channel to which you will push (e.g. share <a href="https://spontit.com">spontit.com/my_username</a>). You can see available invite options by calling `print(resource.get_invite_options())`.
12) We are constantly working on expanding the functionality of Spontit. We GREATLY appreciate your input - feel free to <a href="https://github.com/joshwolff1/spontit_api/issues/new" target="_blank">add a feature request</a> on our Github. :smiley:

### Getting Started :white_check_mark:

#### Make an Account

First, go to <a href="https://www.spontit.com" target="_blank">spontit.com</a> or download the <a href="https://itunes.apple.com/us/app/spontit/id1448318683" target="_blank">Spontit app</a>.
Create an account and get your user ID. To see your user ID in the app, tap the "Profile" tab. To see your user ID on the website, look at the top of the screen.

You can change your user ID at any time <a href="https://www.spontit.com/change_names" target="_blank">here</a>.

#### Generate a Secret Key

Once you have made an account, generate a secret key <a href="https://spontit.com/secret_keys">here</a>. You might have to re-authenticate.

#### Push Notification UI Anatomy

You can change your user ID and display name at any time <a href="https://www.spontit.com/change_names">here</a>.

<p align="center">
    <img src="https://github.com/joshwolff1/spontit_api/raw/master/images/main_channel_push.png" /> 
</p>

Above we see a push notification sent to the main channel. Here, "Josh Wolff" is the first and last name of the user. The call to action is the displayed text. The image shown is the personal profile picture of the user. (You can change your profile image on the homepage of the website or on the iPhone app in the sidebar.) If the user opens the notification, they can open a link attached, if any, among other options (`help(SpontitResource)`). If they have an iPhone, they can forward the notification and share it through several other mediums.

<p align="center">
    <img src="https://github.com/joshwolff1/spontit_api/raw/master/images/topic_push.png" /> 
</p>

Above we see a push notification to a channel (separate from the main channel). Josh owns this channel, but as you can see, it looks like its own account. "Dem 2020 Polls" is the display name, the non-bold text is the call to action, and the image is the image set for the channel. Currently, we only support setting images for sub-channels on the iOS app. To set an image, go to the "Create" tab, select the desired channel, and click the camera icon.

### Limitations

#### Rate Limits

Each channel (including the main channel) has an individual rate limit of 1 push per second. For example, you can push to your main channel and two other channels in the same second, but you cannot push 3 times to one channel in the same second.

If you exceed the rate limit, we will specify this in the response returned for the call to push.

#### Note on Our Development Priorities

We prioritize development of the iOS application over the website. If at any time, we describe a feature and it does not seem to be on the website, it might only exist in the iOS application. Please email us at info {at} spontit {dot} io so that we can clarify this to you and other developers. You are more than welcome to <a href="https://github.com/joshwolff1/spontit_api/issues/new" target="_blank">add a feature request</a>.

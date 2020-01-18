# SPONTIT
## Send push notifications without your own app.
Traditionally, only applications on the iOS platform can send push notifications. Using the Spontit API and Spontit app/webapp, you can send your own push notifications programmatically to Android, iOS, and Desktop devices (without touching Swift, Objective-C, Java, XCode, Android Studio, the App Store approval process...).


## TL;DR

1) Sign up at <a href="https://www.spontit.com">spontit.com</a> (you might need to click "Take me to the Desktop version."). Note down your username. It should be displayed in the top right.
2) Get a secret key at <a href="https://www.spontit.com/secret_keys">spontit.com/secret_keys<a>. 
3) Get the iPhone app or Android app. Sign in and allow notifications.
4) `pip install spontit`
5) `from spontit import SpontitResource`
6) `resource = SpontitResource(my_username, my_secret_key)`
7) `response = resource.push("Hello!")`
8) You can customize the image of this notification on the website or iPhone app. You can push web content and can push to different topics (topic = subchannel). To push to others, have them follow your respective account (e.g. at <a href="https://spontit.com">spontit.com/my_username</a>) and/or topic. Currently, we only support topic creation on the iPhone app.
9) We are constantly working on expanding the functionality of Spontit. We GREATLY appreciate your input - feel free to <a href="https://github.com/joshwolff1/spontit_api/issues/new">add a feature request</a> on our Github.

### About

#### What are topics?
Every user, by definition, is a main channel. Each user can create a topic.

Topics are designed to act separately from your main channel. Users can follow
topics without following your main channel. Users can follow your main channel without following your topics.

For example, my account user ID might be "elon_musk," but I might want to push about new SpaceX developments. I could
push to the topic "spacex" and only those who follow the "spacex" topic would get pushed. 

When you create a topic, you only need to specify the display name. We create a topic ID from this display name. You
then use this ID to programmatically push to the topic. To get the 

A notification pushed to a topic has a separate appearance than one pushed to a root account (see "Push Notification UI Anatomy").

#### Creating Topics

Currently, creating topics is only supported through the GUI on the iOS <a href="https://itunes.apple.com/us/app/spontit/id1448318683">Spontit app</a>. We intend to expand this functionality to the website and the API.

Once you make a topic, you are NOT able to change its display name. This will likely NOT change for quite some time. Please keep this in mind when creating topics.


### Getting Started

For complete documentation listing the functions available, please see <a>here</a>.

#### Make an Account
First, go to <a href="https://www.spontit.com">spontit.com</a> or download the <a href="https://itunes.apple.com/us/app/spontit/id1448318683">Spontit app</a>.
Create an account and get your user ID. To see your user ID in the app, tap on the hamburger button. To see your user ID on the website, look at the top of the screen.

You can change your user ID at any time <a href="https://www.spontit.com/change_names">here</a>.

#### Generate a Secret Key
Once you have made an account, generate a secret key <a href="https://spontit.com/secret_key">here</a>. You might have to re-authenticate.

#### Push Notification UI Anatomy
You can change your user ID, first name, and last name at any time <a href="https://www.spontit.com/change_names">here</a>.

#### Send Your First Push Notification

The Spontit API currently only supports Python 3.7.

`pip install spontit`

Construct the resource with your credentials.

`import spontit`

`spontit_resource = spontit.SpontitResource("my_user_id", "my_secret_key")`

Push the notification to your main account. To specify a topic, specify a topic ID.

`response = spontit_resource.push("My First Push Notification")`

The below code will send a push notification to the topic "mytopic," but it will not send a push notification to the main account.

`response = spontit_resource.push("My First Push Notification", to_topic_ids=["mytopic"])`

To create a topic, see "Creating Topics" above. To get a mapping of topic IDs to display names, do the following:

`response = spontit_resource.get_topic_id_to_display_name_mapping()` 

#### Specify Content on Your Website

To specify specific content on your website, do the following:

`response = spontit_resource.push("My First Push Notification", link="https://www.mywebsite.com", to_topic_ids=["mytopic"])`

#### Send to a Push Notification to Specific Users

You can send a push notification to specific users by specifying their Spontit user IDs as such:

`response = spontit_resource.push("My First Push Notification", to_user_ids=["sandra, new_user1212, jose_c"])`

NOTE: Spontit is designed for virality. Every push notification can go out-of-network and be seen by other users if the receiving user(s) shares it.

#### Map User IDs to Your Own Database

You might be asking, "If I know the Spontit user IDs, what good is that?" You might want to send custom notifications to those
who already have accounts on your platform. If a Spontit user allows you access to their basic contact information (first name, last name, user ID, email, phone number), 
then you can map this using `spontit_resource.get_follower_to_contact_mapping()` or map it for a specific topic using `spontit_resource.get_follower_to_contact_mapping(for_topic_id="mytopic")`.

This will return a mapping of each user ID that follows your or the specified topic to their contact information, provided they specifically give you access to this mapping. If they do not, the `None` type will appear in place of their contact information.

You always have access to their first and last name, as this is public on Spontit. However, the default first and last name for many users is "Anonymous Stork" or "Anonymous Lemur." They must specifically change this or initially provide their first and last name by signing in with Google/Email.


### Limitations

#### Rate Limits
For each combination of topic and userId, you can only push once per second.

For example, you can send to your main account and a separate topic in the same second. You cannot push to the same topic (to everyone who follows the topic) in the same second.

However, you can push separately to three specific users that follow the same topic in the same second.

Effectively, the limit is one push per second per account-topic combination (e.g. combinations could be Everyone-mytopic, Everyone-YourMainAccount, {"user1, user2, user3"}-spacextopic, {"user1, user2, user3"}-YourMainAccount).

If you exceed the rate limit, we will specify this in the response returned.

#### Development Prioritization
We prioritize development of the iOS application over the website. If at any time, we describe a feature and it does 
not seem to be on the website, it might only exist in the iOS application. Please email us at info {at} spontit {dot} io 
so that we can clarify this to you and other developers.
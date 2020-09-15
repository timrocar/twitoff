""" Retrieve Tweets, embeddings, and persist in the DB."""
from os import getenv
import basilica
import tweepy
from .models import DB, Tweet, User

TWITTER_USERS = ['elonmusk', 'neiltyson', 'shroud',
                 'dpatil', 'nasa', 'chrisalbon', 'naval', 'austen',
                 'karpathy', 'championsleague', 'duncantrussell',
                 'fridaysailer', 'IAM_SHAKESPEARE']

#TODO don't checl this in , Use Environrment variables
TWITTER_AUTH = tweepy.OAuthHandler(
    getenv('TWITTER_API_KEY'), #API key
    getenv('TWITTER_API_KEY_SECRET') # API secret key
)
TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection(getenv('BASILICA_KEY'))


def add_or_update_user(username):
    """Add or update a user and their tweets, error if not a twitter user"""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        # We want as many recent non-retweet/reply status as we can get
        #200 is a Twitter API Limit, we'll usually see less due to exclusions
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id
        )
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300],
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error Processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()

def add_users(users=TWITTER_USERS):
    """ Add/Update a list of users."""
    for user in users:
        add_or_update_user(user)


def update_all_users():
    """Update_all existing users."""
    for user in User.query.all():
        add_or_update_user(user.name)
import os
import tweepy

consumer_key = os.environ.get("twitter_key")
consumer_secret = os.environ.get("twitter_secret")
access_token = os.environ.get("twitter_token")
access_token_secret = os.environ.get("twitter_token_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

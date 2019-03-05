import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from textblob import TextBlob

import json
import os


consumer_key = "KhCkUlnoLlyFcK5ohfVHmTVRf"
consumer_secret = "dyUX8Sr3UCQlVLfMLMAlu0hPYW7aHXqXFMOIQIJigIZyacYMlJ"
access_token = "1126016910-y8COolRkm2chkcEGWoYV1eVlxyyvoH8ZjHZAOXM"
access_token_secret = "Sx7FjmXgHtSAs3I4nJ4rpGZQxktbXM4x0O8p8S3QtPZeb"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse


class MyListener(StreamListener):

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.limit = 10

    def on_data(self, data):
        try:
            with open('tweets.csv', 'a') as f:
                decoded= json.loads(data)
                if decoded['place'] and not decoded['text'].startswith('RT') and not decoded['in_reply_to_status_id']:

                    f.write("\"" + decoded['text'] + "\" , " + "\"" + str((TextBlob(decoded['text'])).sentiment.polarity) + "\", " + "\"" + 'Place: ' + decoded['place']['full_name']+ "\", " + "\"" + ' User location: ' + decoded['user']['location'] + "\", " + "\"" + ' Followers: ' +str( decoded['user']['followers_count']) + "\"" + os.linesep)
                    self.counter += 1
                if self.counter < self.limit:
                    return True
                else:
                    twitter_stream.disconnect()
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True


# Set the hashtag to be searched
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['and'], languages=['en'])

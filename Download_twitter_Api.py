from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from dotenv import load_dotenv
import os
import json

import db_queries

load_dotenv()


consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_secret = os.getenv('ACCESS_SECRET')


class StdOutListener(StreamListener):

    def on_data(self, data):
        with open('data/tweetdata.txt','a') as tf:
            tf.write(data)
        data = json.loads(data)
        db_queries.check_user(data['user']['id'], data['place']['bounding_box']['coordinates'])
        db_queries.insert_tweet_with_details(data['user']['id'], data['id'])
        print(json.dumps(data))
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    stream = Stream(auth, l)
    stream.filter(languages=["en"], locations = [68.7,8.4,97.25,37.6])#track=['depression', 'anxiety', 'mental health', 'suicide', 'stress', 'sad', 'kill'])
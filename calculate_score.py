import tweepy
from dotenv import load_dotenv
import os
import json

import db_queries
import depression_sentiment_analysis
import create_email

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
api = tweepy.API(auth)

THRESHOLD_SCORE = -0.6


def get_tweets_of_user(user_id, recent_tweet_id):
    tweets_status = api.user_timeline(user_id=user_id, since_id=recent_tweet_id)
    tweets_json = []
    for tweet_status in tweets_status:
        tweets_json.append(json.dumps(tweet_status._json))
    return tweets_json


def calc_score(user_id):
    user_details = db_queries.get_most_recent_tweet_of_user(user_id)
    tweets = get_tweets_of_user(user_id, user_details[0])
    if len(tweets) == 0:
        return
    print(type(tweets[0]))
    curr_count = user_details[1]
    curr_score = user_details[2]
    depressive_tweets_id = []
    new_most_recent_id = user_details[0]
    new_score = 0
    new_count = 0
    for tweet in tweets:
        new_count += 1
        tweet = json.loads(tweet)
        #print(tweet.id)
        if tweet['id'] > new_most_recent_id:
            new_most_recent_id = tweet['id']
        if depression_sentiment_analysis.get_score_of_tweet(tweet['text']) == 1:
            new_score += 1
            depressive_tweets_id.append(tweet['id_str'])
    new_score = (curr_count * curr_score + new_score * new_count) / (new_count + curr_count)
    curr_score = new_score
    curr_count += new_count
    if curr_score >= THRESHOLD_SCORE:
        print(str(depressive_tweets_id))
        create_email.send_email(user_id,depressive_tweets_id)
    db_queries.update_user_details(user_id,new_most_recent_id,curr_count,curr_score)


if __name__ == '__main__':
    '''depression_sentiment_analysis.initial_run()
    user_ids = db_queries.get_user_id_for_calc()
    print(user_ids)
    for user_id_o in user_ids:
        calc_score(user_id_o[0])'''

depression_sentiment_analysis.initial_run()
calc_score(1291438713575104513)
#get_tweets_of_user(44196397,1377567762919292938)

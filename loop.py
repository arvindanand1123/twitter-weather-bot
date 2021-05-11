import os
import random
import json
from pathlib import Path
import csv
import tweepy
import logging
import time
import config
from dotenv import load_dotenv
import requests


load_dotenv('t.env')
print("Get credentials")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

print("Authenticate")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

l = 'https://fwdyykezdk.execute-api.us-east-1.amazonaws.com/api/tweet'

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        uname = tweet.user.screen_name
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.screen_name}")
            api.update_status(
                status=('@' + uname + " To use Weather Bot, just tweet @ us, use a phrase like 'What's the weather like in <LOCATION>'.  It doesn't matter how you ask for the weather, as long as you do so discernibly and include the location."),
                in_reply_to_status_id=tweet.id,
            )
        else:
            try:
                payload = {"query":tweet.text.lower(), "uname": tweet.user.screen_name ,"id":tweet.id}
                header = {'Content-Type': 'application/json'}
                r = requests.post(l, json=payload, headers=header)
                logger.info(("Payload return", r.json()))
            except:
                api.update_status(
                status=('@' + uname + " Seems like the query was not understood, please try asking about the weather. Try tweeting 'help' or 'support'."),
                    in_reply_to_status_id=tweet.id,
                    )
    return new_since_id


def main():
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "support"], since_id)
        logger.info("Waiting...")
        time.sleep(5)

if __name__ == "__main__":
    main()
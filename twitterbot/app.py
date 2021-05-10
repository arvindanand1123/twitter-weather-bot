from chalice import Chalice
from dotenv import load_dotenv
import os
import random
import json
from pathlib import Path
import tweepy
import csv
from wit import Wit
import requests
from chalice import BadRequestError
from chalice import ChaliceViewError


app = Chalice(app_name='twitterbot')
load_dotenv('chalicelib/.env')
print("Get credentials")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
wit_token = os.getenv("WIT")
weather_token = os.getenv("OWEATHER")

print("Authenticate")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def raise_exception(msg, bad_tag=0):
    if(bad_tag):
        raise BadRequestError(msg)
    else:
        raise ChaliceViewError(msg)

@app.route('/tweet', methods=['POST'])
def tweet():
    body = app.current_request.json_body
    txt = body['query']
    tweet_id = body['id']
    client = Wit(wit_token)
    try:
        wit_resp = client.message(txt)
        resp = wit_resp['intents'][0]['name']
        if(resp == 'wit$get_weather'):
            loc = (wit_resp['entities']['wit$location:location'][0]['resolved']['values'][0]['name'])
            openweather_url = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s' % (loc,weather_token)
            r = requests.get(openweather_url)
            desc = r.json()['weather'][0]['description']
            t = desc + ' today in ' + loc
            api.update_status(
                status=t,
                in_reply_to_status_id=tweet_id,
            )
            return {'weather': t}
    except:
        raise_exception('Seems like the query was not understood, please try asking about the weather',1)

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


def raise_exception(msg, bad_tag=0):
    if(bad_tag):
        raise BadRequestError(msg)
    else:
        raise ChaliceViewError(msg)

@app.route('/tweet', methods=['POST'])
def tweet():
    body = app.current_request.json_body
    txt = body['query']
    client = Wit(wit_token)
    try:
        wit_resp = client.message(txt)
        resp = wit_resp['intents'][0]['name']
        if(resp == 'wit$get_weather'):
            loc = (wit_resp['entities']['wit$location:location'][0]['resolved']['values'][0]['name'])
            openweather_url = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s' % (loc,weather_token)
            r = requests.get(openweather_url)
            desc = r.json()['weather'][0]['description']
            return {'weather': desc + ' today in ' + loc}
    except:
        raise_exception('Seems like the query was not understood, please try asking about the weather',1)


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

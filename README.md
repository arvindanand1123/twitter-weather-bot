# twitter-weather-bot

![image](https://user-images.githubusercontent.com/15079290/117753249-27027900-b1e6-11eb-9412-fb3e0d12af34.png)

# Summary
Hi, welcome to the Twitter Weather Bot GitHub. This is a very advanced Twitter bot that does a simple task: tell you the weather. It's simple to use! You just ask it for the weather and give it some location information. Weather Bot monitors it's feed for mentions and uses NLP + OpenWeather to read your tweet, parse location, and fetch weather information. The coolest feature is the NLP; you don't need a specific pattern/phrase; just ask for the weather!

# Technical Details
This bot is made possible with three key APIs: Twitter Dev API, Wit.ai, and OpenWeatherMap API. First the Twitter API allows for Weather Bot to read tweets and post replies on its feed. Wit.ai is a NLP-based parsing API that understands intent and keywords. I use Wit to, first, understand if you're asking for the weather and, second, to parse out what location you're interested in. Based on the location, the OpenWeatherMap API can be queried via a get request, with location in the header. Backend wise, Weather Bot is running on AWS. There are two main components to the backend system: the Chalice based NLP + Weather engine and the EC2 feed monitoring script. The Chalice portion calls the various external APIs and replies, to the requested user. The EC2 component runs a python script (loop.py) using `nohup`. Its main job is to check for new mentions every five-seconds. The reason for the five second interval is to prevent any, potential, bad actors from overwhelming the system.

# How to Use Weather Bot
First, you need a Twitter account. Then, you need to tweet `@ds3002_weather` with a message like 'What's the weather like in San Diego?' or 'Tell me the weather in DC.' If you need help while using the bot, try tweeting 'help' or 'support' to `@ds3002_weather`.

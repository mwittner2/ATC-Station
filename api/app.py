from flask import Flask
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import json
import os
import time, threading
import tweepy
import emoji
import unicodedata
import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('punkt')

consumer_key = "kEaMOwaPFjdwXelB8rwMXh1Yg"
consumer_secret = "2AKsg0BwxI1bDErlQDUgmNVDvOwzx98htaiYKGXeZzoHv71Jy6"

access_token = "839692039-VulkCGE4QZRZlKYQtDuNjRWgJnxsCdeSfqaPuObs"
access_token_secret = "08AltS6hMTj5Y7sDh2cSLZCrtuqfEYQJ5LTqEI2N4FLN0"

def getSentiment(tweet):
    sid = SentimentIntensityAnalyzer()
    sent = 0.0
    count = 0
    sentList = nltk.tokenize.sent_tokenize(tweet)

    # Go through each sentence in tweet
    for sentence in sentList:
        count += 1
        ss = sid.polarity_scores(sentence)
        sent += ss['compound']  # Tally up the overall sentiment

    if count != 0:
        sent = float(sent / count)
        
    return sent


class listener(StreamListener):
	def __init__(self):
		super().__init__()
		self.counter = 0 
	# def on_status(self, status):
	# 	print(status)
	# def on_data(self, data):
	# 	print(data)
	def on_data(self, data):
		
		data = str(emoji.demojize(data))
		
		decoded = json.loads(str(data))
		# if 'place' in decoded and decoded['place'] is not None:
			# loc = decoded['place']['bounding_box']['coordinates'][0][0]
			
		tweet = str(emoji.demojize(decoded['text']).encode("unicode_escape"))
		tweet = tweet[1:]
		tweet = tweet.strip("\n")
		tweet = tweet.strip("\.")

		tweet = tweet.replace("\n",". ")
		tweet = tweet.replace("\\'","'")
		tweet = tweet.replace("\\","")
		tweet = tweet.replace("\\\.",".")
		tweet = tweet.replace("\"", "'")
		tweet = tweet.replace("\\n",". ")
		tweet = tweet.replace ("\\,", "")
		tweet = tweet.replace(",", "")
		print(tweet)
		sid = SentimentIntensityAnalyzer()
		print(getSentiment(tweet))
		print()
	

		sendJson = '{ "' + str(datetime.datetime.now()) + '": "' + tweet + '" }'

		
	# 		tweetLower = tweet.lower()
	# 		if(company in tweetLower or ticker_symbol in tweetLower):
	# 			companyTweets.write('{"tweet": "' + tweet +'", "coordinates": ' + str(loc) + '}\n')
	# 			companyTweets.flush()
	def on_error(self, status):
		print (status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

myStreamListener = listener()
myStream = Stream(auth = api.auth, listener=myStreamListener)



app = Flask(__name__)

data = []
DATAFOLDER = "data/"


def update_json():
    files = os.listdir(DATAFOLDER)
    for name in files:
        if "history" in name:
            f = open(DATAFOLDER + "" + name, "r")
            x = f.read()
            f.close()
            y = json.loads(x)
            if y not in data:
                data.append(y)

    threading.Timer(10, update_json).start()


@app.route("/")
def index():
    return "Invalid API endpoint"


@app.route("/api/get_flights")
def get_flights():

    return json.dumps(data)


if __name__ == "__main__":
    update_json()
    app.run(port=1337)

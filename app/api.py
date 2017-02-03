from datetime import datetime
import oauth, tweepy, sys, locale, threading
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import requests

def factory(name):
	if name == 'twitter':
		return TwitterAPI()
	return None;

class TwitterAPI():
	def read(self, name, count=10, fromTime=None, toTime=None):
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		api = tweepy.API(auth)
		public_tweets = api.user_timeline(screen_name=name)
		for tweet in public_tweets:
			print tweet.text.encode('utf8')
		return [{'create': datetime.utcnow()}];

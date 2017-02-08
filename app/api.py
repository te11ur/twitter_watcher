from datetime import datetime
import oauth, tweepy, sys, locale, threading
import requests, json, re

def factory(api, params):
	if api == 'twitter':
		return TwitterAPI(params)
	return None;

class TwitterAPI():
	consumer_key = ''
	consumer_secret = ''
	access_token = ''
	access_token_secret = ''
	
	def __init__(self, params):
		data = json.loads(params)
		self.consumer_key = data['consumer_key']
		self.consumer_secret = data['consumer_secret']
		self.access_token = data['access_token']
		self.access_token_secret = data['access_token_secret']
		
	def read(self, params):
		result = []
		filter = json.loads(params)
		try:
			auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
			auth.set_access_token(self.access_token, self.access_token_secret)
			api = tweepy.API(auth)
			for status in tweepy.Cursor(api.user_timeline, **filter).items(200):
				result.append((status.id_str.encode('utf8'), {'create': status.created_at, 'text_raw': json.dumps(status.entities).encode('utf8'), 'text': self.strip_tags(status.text.encode('utf8'))}))
		except tweepy.error.TweepError as e:
			print 'Connection error'

		return result
		
	def strip_tags(self, value):
		"""Returns the given HTML with all tags stripped."""
		return re.sub(r'<[^>]*?>', '', value)

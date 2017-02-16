from datetime import datetime
import oauth, tweepy, sys, locale, threading
import requests, json, re

def factory(api, params, timeout):
	if api == 'twitter':
		return TwitterAPI(params, timeout)
	return None;

class TwitterAPI():
	consumer_key = ''
	consumer_secret = ''
	access_token = ''
	access_token_secret = ''
	timeout = 0
	
	def __init__(self, params, timeout=60):
		try:
			data = json.loads(params)
		except ValueError as e:	
			data = {}

		self.consumer_key = data.get('consumer_key')
		self.consumer_secret = data.get('consumer_secret')
		self.access_token = data.get('access_token')
		self.access_token_secret = data.get('access_token_secret')
		self.timeout = timeout
		
	def read(self, key, params):
		result = []
		try:
			filter = json.loads(params)
		except ValueError as e:	
			filter = {}

		if key is not None:
			filter["since_id"] = key
		try:
			auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
			auth.set_access_token(self.access_token, self.access_token_secret)
			api = tweepy.API(auth, timeout=self.timeout)
			for status in tweepy.Cursor(api.user_timeline, **filter).items(1000):
				result.append((status.id_str.encode('utf8'), {'create': status.created_at, 'text_raw': json.dumps(status.entities).encode('utf8'), 'text': status.text.encode('utf8')}))
		except tweepy.error.TweepError as e:
			print 'Connection error'

		return result
		
	def strip_tags(self, value):
		"""Returns the given HTML with all tags stripped."""
		return re.sub(r'<[^>]*?>', '', value)

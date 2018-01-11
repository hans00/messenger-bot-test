import requests

MESSAGE_API_URL = ''
PROFILE_API_URL = 'https://graph.facebook.com/v2.6/me/messenger_profile?access_token='

class Bot(object):
	"""Facebook Messenger Bot"""
	def __init__(self, token):
		self.token = token

	def profile_row(self, payload):
		response = requests.post(
			PROFILE_API_URL+token,
			json=payload
		)
		return response.json()

	def sent_row(self, payload):
		response = requests.post(
			MESSAGE_API_URL+token,
			json=payload
		)
		return response.json()
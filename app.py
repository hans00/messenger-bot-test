import os
import logging
import json
from flask import Flask, request
import requests
from pymessenger.bot import Bot

TOKEN = os.environ.get('TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
FB_WEBHOOK_PATH = os.environ.get('FB_WEBHOOK_PATH', '/fbapi')

app = Flask(__name__)
bot = Bot(TOKEN)

if FB_WEBHOOK_PATH != '/':
	@app.route('/')
	def root():
		return 'Hello World!'

@app.route(FB_WEBHOOK_PATH, methods=['GET'])
def fb_webhook_challenge():
	verify_token = request.args.get('hub.verify_token')
	if verify_token == VERIFY_TOKEN:
		return request.args.get('hub.challenge')
	else:
		return ''

@app.route(FB_WEBHOOK_PATH, methods=['POST'])
def fb_receive_message():
	message_entries = json.loads(request.data.decode('utf8'))['entry']
	print(request.data.decode('utf8'))
	for entry in message_entries:
		for message in entry['messaging']:
			recipient_id = message['sender']['id']
			if message.get('message'):
				if message['message'].get('text'):
					# msg = message['message']['text']
					# bot.send_button_message(
					# 	recipient_id,
					# 	"Choose service:",
					# 	[
					# 		dict(type='postback', title="Test 1", payload="1"),
					# 		dict(type='postback', title="Test 2", payload="2"),
					# 		dict(type='postback', title="Test 3", payload="3")
					# 	]
					# )
					bot.send_text_message(recipient_id, "I don't kow what it is.\nPlease select on the below.")
			if message.get('postback'):
				payload = message['postback']['payload']
				if payload == 'start':
					bot.send_text_message(
						recipient_id,
						"Hello, please select."
						)
				else:
					bot.send_text_message(
						recipient_id,
						"Please input your question about "+payload.split('_')[1]
						)
	return ''

def set_profile(payload):
	global TOKEN
	url = 'https://graph.facebook.com/v2.6/me/messenger_profile?access_token='+TOKEN
	response = requests.post(
			url,
			json=payload
		)
	return response.json()

if __name__ == '__main__':
	print(set_profile({
			"greeting": [
				{
					"locale":"default",
					"text": "Hello {{user_full_name}}, may I help you?"
				}
			]
		}))
	print(set_profile({
			"get_started": {"payload": "start"}
		}))
	print(set_profile({
			"persistent_menu":[
				{
					"locale":"default",
					"composer_input_disabled": False,
					"call_to_actions":[
						{
							"title":"Create company",
							"type":"nested",
							"call_to_actions":[
								{
									"title":"Registerition",
									"type":"postback",
									"payload":"CTRATE_REG"
								},
								{
									"title":"LOGO",
									"type":"postback",
									"payload":"CTRATE_LOGO"
								},
								{
									"title":"Copyright",
									"type":"postback",
									"payload":"CTRATE_CR"
								},
								{
									"title":"Knowledge Trade",
									"type":"postback",
									"payload":"CTRATE_KT"
								}
							]
						},
						{
							"title":"Manage company",
							"type":"nested",
							"call_to_actions":[
								{
									"title":"Tax",
									"type":"postback",
									"payload":"MANAGE_TAX"
								}
							]
						},
						{
							"type":"web_url",
							"title":"About Us",
							"url":"https://itsrv.tw/",
							"webview_height_ratio":"full"
						}	
					]
				}
			]
		}))
	app.run(
		host='0.0.0.0',
		debug=True,
		port=int(os.environ.get('PORT', 33507))
	)

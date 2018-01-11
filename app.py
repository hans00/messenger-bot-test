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

@app.route(FB_WEBHOOK_PATH, methods=["GET"])
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
					msg = message['message']['text']
					bot.send_button_message(
						recipient_id,
						"Choose service:",
						[
							dict(type='postback', title="Test 1", payload="1"),
							dict(type='postback', title="Test 2", payload="2"),
							dict(type='postback', title="Test 3", payload="3")
						]
					)
			if message.get('postback'):
				payload = message['postback']['payload']
				bot.send_text_message(
					recipient_id,
					"Test - " + payload
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
					"text": "{{user_full_name}} 安安"
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
							"title":"My Account",
							"type":"nested",
							"call_to_actions":[
								{
									"title":"Pay Bill",
									"type":"postback",
									"payload":"PAYBILL_PAYLOAD"
								},
								{
									"type":"web_url",
									"title":"Web",
									"url":"https://itsrv.tw/",
									"webview_height_ratio":"full"
								}
							]
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

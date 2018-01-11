import os
import logging
import json
from flask import Flask, request
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
			if message.get('message'):
				recipient_id = message['sender']['id']
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
	return ''

if __name__ == '__main__':
	# bot.set_greeting_text("Hi, may I help you?")
	# bot.set_get_started_button_payload("Get Start") 
	app.run(
		host='0.0.0.0',
		debug=True,
		port=int(os.environ.get('PORT', 33507))
	)

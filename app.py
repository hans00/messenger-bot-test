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
				bot.send_text_message(message['sender']['id'], request.data.decode('utf8'))
	return ''

if __name__ == '__main__':
	app.run(
		host='0.0.0.0',
		debug=True,
		port=int(os.environ.get('PORT', 33507))
	)

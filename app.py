import os
import logging
import json
from flask import Flask, request
from pymessenger.bot import Bot

TOKEN = os.environ.get('TOKEN')
CHALLENGE_CODE = os.environ.get('CHALLENGE_CODE')
FB_WEBHOOK_PATH = os.environ.get('FB_WEBHOOK_PATH', '/fbapi')

app = Flask(__name__)
bot = Bot(TOKEN)

if FB_WEBHOOK_PATH != '/':
	@app.route('/')
	def root():
		return 'Hello World!'

@app.route(FB_WEBHOOK_PATH, methods=["GET"])
def fb_webhook():
	verify_token = request.args.get('hub.verify_token')
	if verify_token == CHALLENGE_CODE:
		return request.args.get('hub.challenge')

@app.route(FB_WEBHOOK_PATH, methods=['POST'])
def fb_receive_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        for message in entry['messaging']:
            if message.get('message'):
                print("{sender[id]} says {message[text]}".format(**message))
    return "Hi"

if __name__ == '__main__':
    app.run(
    	host='0.0.0.0',
    	debug=True,
    	port=int(os.environ.get('PORT', 33507))
    )

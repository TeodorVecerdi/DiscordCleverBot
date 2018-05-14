import discord
import asyncio
import json
import requests
import re

TOKEN = 'NDQ1NjUwNDc2NDM2ODE1ODkz.Ddtj7Q.9AmZpLZxE1NnyjUq-R9gXIxntCM'
nick = 'vqgXph15'

client = discord.Client()

def createSession():
	body = {
		'user': 'YNWnSHCuFnDun5iV',
		'key': 'fzcVpXJjZBb3av3dwDAoBSXEY6iX5ulR'
	}
	req = requests.post('https://cleverbot.io/1.0/create', json=body)
	req = json.loads(req.text)
	print("Nick: {}".format(req['nick']))
	return req['nick']

def sendMessage(message):
	body = {
		'user': 'YNWnSHCuFnDun5iV',
		'key': 'fzcVpXJjZBb3av3dwDAoBSXEY6iX5ulR',
		'nick': nick,
		'text': message
	}

	r = requests.post('https://cleverbot.io/1.0/ask', json=body)
	r = json.loads(r.text)
	if r['status'] == 'success':
		return r['response']
	else:
		return r

talking = {}
commands = {}

def cmd_talk(message):
	talking[str(message.author)] = True
	print(talking)
	return 'Started talking to CleverBot. To stop type `cvb stop`'
	
def cmd_stop(message):
	talking[str(message.author)] = False
	print(talking)
	return 'Stopped talking to CleverBot. To talk again type `cvb talk`'

def cmd_help(message):
	return 'All CleverBot commands start with cvb\n`cvb help` - show this message\n`cvb talk` - start talking with CleverBot\n`cvb stop` - stop talking to CleverBot\nNote: After starting talking to CleverBot all messages will be sent to CleverBot. To stop this you must run the `cvb stop` command.'


def init():
	commands['talk'] = cmd_talk
	commands['stop'] = cmd_stop
	commands['help'] = cmd_help


@client.event
async def on_message(message):
	if message.author == client.user or not str(message.channel).startswith("cleverbot"):
		return
	if message.content.startswith('cvb'):
		command = ''
		try:
			command = re.match('cvb (.*[a-zA-Z0-9])', message.content).group(1)
			resp = commands[command](message)
			if resp != '':
				await client.send_message(message.channel, resp)
		except:
			await client.send_message(message.channel, "Command `cvb {}` not found. Try `cvb help` for a list of commands.".format(command))
	else:
		if str(message.author) in talking.keys() and talking[str(message.author)] == True:
			cleverResponse = sendMessage(message.content)
			await client.send_message(message.channel, "{}, {}".format(message.author.mention, cleverResponse))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')
    init()


client.run(TOKEN)
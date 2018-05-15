import discord
import json
import requests
import re

TOKEN = 'NDQ1NjUwNDc2NDM2ODE1ODkz.Ddtj7Q.9AmZpLZxE1NnyjUq-R9gXIxntCM'
nick = 'vqgXph15'


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
profile = {}
client = discord.Client()
# server = client.get_server()
currentBot = 'Cleverbot'
profile['TicTacToe'] = open('tictactoe_profile.png', 'rb').read()
profile['Cleverbot'] = open('cleverbot_profile.png', 'rb').read()

def cmd_switch(message):
	global currentBot
	if currentBot == 'Cleverbot':
		currentBot = 'TicTacToe'
	else:
		currentBot = 'Cleverbot'

	return 'Switched to `{}`. Type `cvb switch` to switch again'

def cmd_talk(message):
	talking[str(message.author)] = True
	print(talking)
	return 'Started talking to Cleverbot. To stop type `cvb stop`'

def cmd_stop(message):
	talking[str(message.author)] = False
	print(talking)
	return 'Stopped talking to Cleverbot. To talk again type `cvb talk`'

def cmd_help(message):
	retMsg = 'All Cleverbot commands start with cvb:\n'
	for command in commands:
		retMsg += '`cvb {}` - {}\n'.format(commands[command]['cmd'], commands[command]['desc'])
	return retMsg

def cmd_info(message):
	return 'Cleverbot is a chatterbot web application that uses an artificial intelligence algorithm to have conversations with humans.'

def init():
	commands['talk'] = {}
	commands['talk']['func'] = cmd_talk
	commands['talk']['cmd'] = 'talk'
	commands['talk']['desc'] = 'start talking with Cleverbot'
	commands['talk']['bot'] = 'Cleverbot'

	commands['stop'] = {}
	commands['stop']['func'] = cmd_stop
	commands['stop']['cmd'] = 'stop'
	commands['stop']['desc'] = 'stop talking to Cleverbot'
	commands['stop']['bot'] = 'Cleverbot'

	commands['help'] = {}
	commands['help']['func'] = cmd_help
	commands['help']['cmd'] = 'help'
	commands['help']['desc'] = 'print this help message'
	commands['help']['bot'] = 'General'

	commands['info'] = {}
	commands['info']['func'] = cmd_info
	commands['info']['cmd'] = 'info'
	commands['info']['desc'] = 'details about Cleverbot'
	commands['info']['bot'] = 'Cleverbot'

	# commands['switch'] = {}
	# commands['switch']['func'] = cmd_switch
	# commands['switch']['cmd'] = 'switch'
	# commands['switch']['desc'] = 'switch between Cleverbot and TicTacToe'
	# commands['switch']['bot'] = 'General'


@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.startswith('cvb'):
		if not str(message.channel).startswith("cleverbot"):
			await client.send_message(message.channel, "Cleverbot can only be used in a text channel named `cleverbot`.")
		else:
			command = ''
			try:
				command = re.match('cvb (.*[a-zA-Z0-9])', message.content).group(1)
				if commands[command]['bot'] == 'General' or commands[command]['bot'] == currentBot:
					resp = commands[command]['func'](message)
					if command == 'switch':
						await client.change_nickname(member=discord.Server.me, nickname=currentBot)
						await client.edit_profile(avatar=profile[currentBot])
				else:
					await client.send_message(message.channel, 'Command `cvb {}` is not available for the current bot. Type `cvb switch` to switch to another bot and try again.')
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
	# print(client.server.id)
	print('------------')
	# print('Server name: {}'.format(server.name))
	init()
	await client.change_presence(game=discord.Game(name='cvb help'))


client.run(TOKEN)

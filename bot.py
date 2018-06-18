import discord
import random
import os
import asyncio
#QuagBot class that inherits discord.Client, the base for the discord bot
class QuagBot(discord.Client):
	
	#Runs when the object is created
	def __init__(self):
		#Runs the init of discord.Client
		super().__init__()
		#Sets the attributes player and voice to None
		self.player = None
		self.voice = None
	
	#Runs when the bot has been connected to discord
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		await self.change_presence(game=discord.Game(name='Bubble Shooter'))
		for server in self.servers:
			if self.is_voice_connected(server):
				print("Found existing voice connection. Joining")
				#Creates a voice client for every server it is connected to
				self.voice = self.voice_client_in()

	#Method is used to join a voice channel. The method is called by on_message.
	async def join_voice(self, message):
		#Gets the voice channel that the message was sent in
		voice_ch = message.author.voice_channel
		if voice_ch is None: #Makes sure that the author is in a voice channel
			await self.send_message(message.channel, 'You are not in a voice channel.')
			print("ERROR: Not in voice chat")
		else:
			#Joins a channel if not in one
			if self.voice is None:
				self.voice = await self.join_voice_channel(voice_ch)
			elif self.voice.channel != voice_ch: #Join correct channel
				await self.leave_voice()
				self.voice = await self.join_voice_channel(voice_ch)
				if self.player != None:
					self.player.stop()
			print("Connecting voice")
			#Returns if the join was successful
			return self.voice is not None

	#Method used for leaving the voice channel
	async def leave_voice(self):
		print(self.voice)
		await self.voice.disconnect()
		print("Disconnecting voice")

	#Runs upon reciving a message
	async def on_message(self, message):
			if message.author == self.user:
				return
			#Do not write message code above this line.
			
			#------------------------
			#-------BIG GAY----------
			#------------------------
			if message.content.startswith('!giveGay'):
				print(message.author.name)
				userFound = False
				newUser = message.content.replace("!giveGay ", "")
				print(newUser)
				f = open('bigGay.txt', 'r+')
				nameString = f.readline()
				if message.author.name == nameString:
					print('user is gay')
					x = message.server.members
					for member in x:
						if member.name == newUser:
							f.seek(0)
							f.truncate()
							f.write(newUser)
							userFound = True
							break
					if not userFound:
						await self.send_message(message.channel, 'No user with the name ' + newUser + ' was found')
					else:
						await self.send_message(message.channel, newUser + ' now has the Big Gay')
				else:
					print('user is not gay')
					await self.send_message(message.channel, 'Sorry, but you are not gay')
				f.close()
				
			elif message.content.startswith('!bigGay'):
				msgStr = ' currently has the Big Gay'
				f = open('bigGay.txt', 'r')
				nameStr = f.readline()
				msgStr = nameStr + msgStr
				await self.send_message(message.channel, msgStr)
				f.close()
				
			#------------------------
			#-----TEXT COMMANDS------
			#------------------------
			elif message.content.startswith('!echo'):
				newstr = message.content.replace("!echo ", "")
				await self.send_message(message.channel, newstr)
				await self.delete_message(message)
				
			elif message.content.startswith('!help'):
				with open('help.txt') as f:
					await self.send_message(message.channel, f.read())
			#------------------------
			#-----VOICE COMMANDS-----
			#------------------------
			elif message.content.startswith('!fix'):
				print('fixing bot.')
				print(self.player.error)
				await self.voice.disconnect()
				self.player.stop()
				self.player = None
				self.voice = None
				
			elif message.content.startswith('!song'):
				if await self.join_voice(message):
					print("Playing audio")
					self.player = self.voice.create_ffmpeg_player('te.m4a')
					self.player.start()
					
			elif message.content.startswith('!bubble'):
				if await self.join_voice(message):
					print("Playing mp3")
					self.player = self.voice.create_ffmpeg_player('bubble.mp3')
					self.player.start()
					
			elif message.content.startswith('!soundcloud'):
				if await self.join_voice(message):
					print("Playing mp3")
					oStr = 'rep.mp3'
					songNum = random.randint(1,5)
					nStr = oStr.replace("rep",str(songNum))
					self.player = self.voice.create_ffmpeg_player(nStr)
					self.player.start()
					
			elif message.content.startswith('!leave'):
				await self.voice.disconnect()
			
bot = QuagBot()
bot.run('ENTER TOKEN HERE')


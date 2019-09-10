'''
discord bot by Greenlord, on test
'''

import asyncio 	#time/date
import json     #work with tables
import logging  #logging stuf
import discord  #com. with discord

bot = discord.Client() #'bot'=client

#Template
template = {"server_id": None,
                    "shop": [ ],
                    "server": {
                        "log_channel_id": None,
                        "welcome_channel_id": None,
                        "mods_role_id": None,
                        "sudo_id": None,
                        "admin_role_id": None,
                        "prefix": "!"}}

invite_link = "https://discordapp.com/oauth2/authorize/?permissions=8&scope=bot&client_id=397461072342417408"

#Logging START
logger = logging.getLogger('dat_bot.logs')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(levelname)s|%(asctime)s|%(name)s:  %(message)s',
                                        datefmt="%d/%m/%Y %H:%M"))
logger.addHandler(handler)
#Logging  END

@bot.event
async def on_ready(): #inicialization succesful
    print("Bot is ready and online!")
    print("Name:", bot.user.name)
    print("ID:", bot.user.id)
    print("---INFO---")
    print("Total members '{}' in '{}' guilds".format(len(list(set(bot.get_all_members())))-1, len(bot.guilds)))
    print("Opened PM's:", len(bot.private_channels))
    logger.debug("Bot is online.")
    game = discord.Game("Under Testing(!help)")
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.event
async def on_resumed(): #in case of fail
    print("Resumed...")
    logger.debug("Back online...")

@bot.event
async def on_guild_join(guild): #when bot join guild
    #console print
    print("---#Bot join new guild!#---")
    print("Name:", guild.name)
    print("ID:", guild.id)
    print("Owner: {0.name}[{0.id}]".format(guild.owner))
    print("Members now:", len(guild.members))
    print("Channels now:", len(guild.channels))
    print("Created at:", guild.created_at)
    print("---------------------------")
    #logging
    logger.info("Bot was invited in '{0.name}'[{0.id}]. Owner-{0.owner.name}".format(guild))
    #---Create server data in json_things/data.json
    with open("json/data.json", "r+") as jsonFile:
        data = json.load(jsonFile)
        data["servers_list"].append(simple_new_server)
        data["servers_list"][len(data["servers_list"])-1]["server_id"] = guild.id
        data["servers_list"][len(data["servers_list"])-1]["server"]["sudo_id"] = guild.owner_id
        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()
        logger.info("Server '{0.name}'[{0.id}] added to 'data.json'!".format(server))

@bot.event
async def on_guild_remove(guild): #when bot left guild
	print("---#Bot left guild!#---")
	print("Name:", guild.name)
	print("ID:", guild.id)
	print("Owner: {0.name}[{0.id}]".format(guild.owner))
	print("Members:", len(guild.members))
	print("Created at:", guild.created_at.strftime('%d/%m/%Y %H:%M'))
	print("-Bot info")
	print("Joined at:", guild.me.joined_at.strftime('%d/%m/%Y %H:%M'))
	print("Roles:", list(set(guild.me.roles)))
	print("-----------------------")
	logger.info("Bot left guild '{0.name}'[{0.id}]. Owner-{1.name}[{1.id}]".format(guild, guild.owner))


@bot.event
async def on_member_join(member):
	guild = member.guild
    
	member_tags = None
	#---create embed message---
	embed = discord.Embed(colour=discord.Colour.gold(), description="***'{}' join this server!***".format(member.name))

	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text="Notification by @GreenLord", icon_url="https://cdn.discordapp.com/app-icons/397461072342417408/80b3d35bd5a974d72a833f25cd7e8e07.png")

	embed.add_field(name="Name", value=member.name, inline=True)
	embed.add_field(name="ID", value=member.id, inline=True)
	embed.add_field(name="Account created at", value=member.created_at.strftime('%d/%m/%Y %H:%M - UTC'))
	embed.add_field(name="Tags", value=member_tags)
	#---end---
	channel = None
	with open("json_things/data.json", "r") as jsonFile:
		data = json.load(jsonFile)
		for x in range(len(data["servers_list"])):
			if int(guild.id) == int(data["servers_list"][x]["server_id"]):
				if data["servers_list"][x]["server"]["welcome_channel_id"] is None:
					logger.info("{0.name} join {1.name}, BUT welcome channel isn't set up!".format(member, guild))
					await guild.owner.send(content="Hello, {0.name}!\nInforming You that your server '{1.name}'[ID:{1.id}] hasn't setup welcome channel yet!\nPlease, configure it!".format(guild.owner, guild))
					return
				else:
					channel = bot.get_channel(int(data["servers_list"][x]["server"]["welcome_channel_id"]))
					if channel is None:
						logger.error("Error occurs while sending welcome message")
					else:
						await channel.send(embed=embed)
						logger.info("{0.name}[{0.id}] successfully joined {1.name} !".format(member, guild))
					return
	jsonFile.close

@bot.event 
async def on_member_remove(member):
	'''Left message'''
	guild = member.guild
    
	member_tags = None
    
	embed = discord.Embed(colour=discord.Colour.dark_gold(), description="***'{}' left the server!***".format(member.name))
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text="Notification by @GreenLord", icon_url="https://cdn.discordapp.com/app-icons/397461072342417408/80b3d35bd5a974d72a833f25cd7e8e07.png")

	embed.add_field(name="Name", value=member.name, inline=True)
	embed.add_field(name="ID", value=member.id, inline=True)
	embed.add_field(name="Account created at", value=member.created_at.strftime('%d/%m/%Y %H:%M - UTC'), inline=True)
	embed.add_field(name="Joined at", value=member.joined_at.strftime('%d/%m/%Y %H:%M - UTC'), inline=True)
	embed.add_field(name="Roles", value=member.roles)
	embed.add_field(name="Tags", value=member_tags)

	channel = None
	with open("json_things/data.json", "r") as jsonFile:
		data = json.load(jsonFile)
		for x in range(len(data["servers_list"])):
			if (int(guild.id) == int(data["servers_list"][x]["server_id"])):
				if data["servers_list"][x]["server"]["welcome_channel_id"] is None:
					await guild.owner.send(content="Hello, {0.name}!\nInforming You that your server '{1.name}'[ID:{1.id}] hasn't setup welcome channel yet!\nPlease, configure it!".format(guild.owner, guild))
					logger.info("{0.name} left {1.name}, BUT welcome channel isn't set up!".format(member, guild))
					return
				else:
					channel = bot.get_channel(int(data["servers_list"][x]["server"]["welcome_channel_id"]))
					await channel.send(embed=embed)
					logger.info("{0.name}[{0.id}] left '{1.name}' server!".format(member, guild))


bot.run("Mzk3NDYxMDcyMzQyNDE3NDA4.DTANYA.Plc3vlVO3b2huY9gUqkizvjDyUg")

import disnake
from disnake.ext import commands
import json
import logging
import asyncio
import os

def setOption(the: str, to: any):
	with open("client_secrets.json", "r") as f:
			data = json.load(f)
			data[the] = to
	with open("client_secrets.json", "w") as f:
			json.dump(data, f, indent=4)

def getOption(thing: str):
	with open("client_secrets.json", "r") as f:
		clientSecrets = json.load(f)
		return clientSecrets.get(thing)

def makeEmbed(header, desc, color: disnake.Color):
    return disnake.Embed(title=header, description=desc, color=color)

#bot = commands.Bot(command_prefix=getOption('prefix'))
bot = commands.Bot(command_prefix=disnake.ext.commands.when_mentioned)
# this event is triggered when the bot is online
@bot.event
async def on_ready():
	print("Bot is online!")


@bot.event
async def on_command_error(ctx, error): 
	print(str(error))

def warnMember(author: str, memberID: int, reason: str):
	"""
	# WarnMember

	A function that warns a member

	## PARAMETERS
	
	### Author

	Who did the warn

	### MemberID

	The Warn Victim

	### Reason

	The Reason for Warning the MemberID
	"""
	with open("warns.json", "r") as f:
		warnsData = json.load(f)
		warnsData[str(memberID)].append([author, reason])
	with open("warns.json", "w") as f:
		json.dump(warnsData, f, indent=4)

def getWarns(memberID: int):
	with open("warns.json", "r") as f:
		data = json.load(f)
		return data.get(str(memberID))

@bot.command()
@commands.has_role("Staff")
async def reload(ctx):
	await ctx.reply("Reloading...")
	print("Reloading!")
	os.system("py Main.py")
@bot.command()
@commands.has_role("Staff")
async def warn(ctx, member: disnake.Member, *, reason):
	warnMember(ctx.author.name, member.id, reason=reason)
	await ctx.reply(f"Successfully warned @{member.name} for '{reason},' they now have **{getWarns(member.id)}** warns.")

@bot.command(aliases = ['warnings', 'warnz'])
async def warns(ctx, member: disnake.Member):
	if getWarns(member.id) == "[]":
		await ctx.reply(f"@{member.name} has `0` warns.")
	else:
	 await ctx.reply(f"@{member.name} has `{getWarns(member.id)}` warns.")


@bot.command(aliases = ["chpr", "changepref"])
@commands.has_role('Staff')
async def changeprefix(ctx, prefix):
	print(f"Prefix Changed from {getOption('prefix')} to {prefix}")
	setOption("prefix", prefix)
	bot.command_prefix = getOption('prefix')
@bot.command()
async def rule(ctx, qnum):
    try:
        with open("bot/rule/"+str(qnum)+".md", "r") as rule:
            await ctx.send(rule.read())
    except FileNotFoundError:
        await ctx.send("That does not seem like a valid rule.")


bot.run(getOption("token"))
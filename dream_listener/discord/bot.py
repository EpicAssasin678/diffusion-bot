import discord
import os # default module

from dotenv import load_dotenv
from discord.ext import commands, tasks



load_dotenv() # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")
    
@bot.slash_command(name = "pingHost", description="Pings host computer at desired port addr")
async def pingHost(ctx):
    
    pass


bot.run(os.getenv('TOKEN')) # run the bot with the token



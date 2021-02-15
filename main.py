from bmv import GBM
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils import stock_parser
load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
CLIENTID = os.getenv('CLIENTID')
TOKEN = os.getenv('DISCORD_TOKEN')

gbm = GBM(USERNAME, PASSWORD, CLIENTID)



description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents, case_insensitive=True)


@bot.event
async def on_ready():
    print('Conectado:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(name='hello')
async def hello(ctx):
    """Rolls a dice in NdN format."""
    response = "hello world!"
    await ctx.send(response)


@bot.command(name='bmv')
async def getstock(ctx, stock: str, **kwargs):
    """Consultar informacion de la bmv."""
    result = stock_parser(gbm.get_symbol(stock))
    await ctx.send(result)


bot.run(TOKEN)

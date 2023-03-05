import discord, flask, os, quart, sys, toml, time, datetime
from quart import render_template
from quart.helpers import make_response
from discord.ext import commands


with open("config.toml", "r") as f:
    config = toml.load(f)

token = os.environ.get('MEETOO_TOKEN')

start_time = time.time()


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=["823188238260633600"])
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command(guild_ids=["823188238260633600"])
async def stop(ctx):
    if ctx.author.guild_permissions.administrator:
        print("Terminating the bot...")
        await ctx.respond("https://media4.giphy.com/media/CC5MVO9Jx4RqMQRfvT/giphy.gif")
        sys.exit("Terminated.")
    else:
        await ctx.respond("https://media.tenor.com/Iv6oKRuAhVEAAAAC/hal9000-im-sorry-dave.gif")
#webserver
app = quart.Quart(__name__)
#The index.
@app.route('/', methods=['GET'])
async def index():
    return await render_template('index.html')

@app.route('/configuration', methods=['GET'])
async def configuration():
    return await render_template('configuration.html')

@app.route('/dashboard', methods=['GET'])
async def dashboard():
    return await render_template('dashboard.html')

@app.route('/plugins', methods=['GET'])
async def plugins():
    return await render_template('plugins.html')

@app.route('/stop', methods=['GET'])
async def stop():
    sys.exit("Web terminated.")



bot.loop.create_task(app.run_task('0.0.0.0', 5000))


bot.run(token)

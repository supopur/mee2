import discord, flask, os, quart, sys, toml, time, datetime
from quart import render_template
from quart.helpers import make_response

with open("config.toml", "r") as f:
    config = toml.load(f)

with open("creds.toml", "r") as f:
    creds = toml.load(f)

start_time = time.time()

bot = discord.Bot()

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
    return "Hello!"
@app.route('/stop', methods=['GET'])
async def stop():
    sys.exit("Web terminated.")

@app.route('/dashboard', methods=["GET"])
async def dashboard():
    commands_called = 10
    uptime_seconds = time.time() - start_time
    uptime = str(datetime.timedelta(seconds=uptime_seconds))
    return await render_template('dashboard.html',commands_called=commands_called, uptime=uptime)

bot.loop.create_task(app.run_task('0.0.0.0', 5000, certfile="certs/certificate.crt", keyfile="certs/private.key"))


bot.run('MTAwNDgwODA4OTgzNDM3MzIzMA.Gy9Nou.CVhTk-fEKyTvRLG-KeZm6wuilK9-eDZsEh4p0U')

import discord, flask, os, quart, sys, toml, time, datetime, logging
from quart import render_template
from quart.helpers import make_response
from discord.ext import commands








with open("config.toml", "r") as f:
    config = toml.load(f)

if config["webserver"]["debug"] == "true":
    logging.basicConfig(filename='latest.log', encoding='utf-8', level=logging.DEBUG)
else:
    logging.basicConfig(filename='latest.log', encoding='utf-8', level=logging.INFO)

logging.getLogger().addHandler(logging.StreamHandler())


def log(level, log):
    if level == "inf":
        logging.info(log)
    elif level == "wrn":
        logging.warning(log)
    elif level == "dbg":
        logging.debug(log)
    elif level == "err":
        logging.error(log)

log("inf", "Logging utility set up.")

try:
    token = os.environ.get('MEETOO_TOKEN')
except:
    log("err", 'Error no token is present type: export MEETOO_TOKEN="[Your token here]" into your terminall NOW!')

if token == "":
    log("err", 'Error no token is present type: export MEETOO_TOKEN="[Your token here]" into your terminall NOW!')

log("dbg", f"Token is: {token}")

start_time = time.time()


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

logging.debug("Loaded the client.")

#Load all the extensions
for x in config["bot"]["cogs"]:
    log("inf", f"Loading {x}...")
    try:
        bot.load_extension(x)
    except Exception as e:
        log("wrn", f"{x} Failed to load skipping... Error: {e}")
log("inf", "Loading all cogs completed.")


@bot.event
async def on_ready():
    log("inf", f"We have logged in as {bot.user}")



@bot.slash_command(guild_ids=["823188238260633600"])
async def stop(ctx):
    if ctx.author.guild_permissions.administrator:
        print("Terminating the bot...")
        try:
            await ctx.respond("https://media4.giphy.com/media/CC5MVO9Jx4RqMQRfvT/giphy.gif")
        except:
            pass
        sys.exit("Terminated.")
    else:
        await ctx.respond("https://media.tenor.com/Iv6oKRuAhVEAAAAC/hal9000-im-sorry-dave.gif")
log("inf", "Loading Quart...")
#webserver
app = quart.Quart(__name__)
log("inf", "Quart loaded.")
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

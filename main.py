import discord, os, sys, toml, time, datetime, logging

from discord.ext import commands








with open("config.toml", "r") as f:
    config = toml.load(f)

if config["webserver"]["debug"] == "true":
    logging.basicConfig(filename='latest.log', encoding='utf-8', level=logging.DEBUG)
else:
    logging.basicConfig(filename='latest.log', encoding='utf-8', level=logging.INFO)

logging.getLogger().addHandler(logging.StreamHandler())
try:
    os.remove("latest.log")
except: pass
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


bot.run(token)

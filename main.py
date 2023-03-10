import discord, os, sys, toml, time, datetime, logging

from discord.ext import commands

with open("config.toml", "r") as f:
    config = toml.load(f)

if config["webserver"]["debug"] == "true":
    logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG)
else:
    logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.INFO)

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


#Api used mainly for plugins so getting uptime, loading, unloading, reloading plugins, getting status of plugins, get plugin info, stopping the bot, getting bot name and tag, getting cpm/commands per minute, get if there is web plugin, if there is web plugin register api, get if plugin supports web and so on..

class API:

    #Returns config.tomls content in a array.
    def get_config(self):
        return self.config
    #Dumps all the toml data from self.config and stores it inside toml.config
    def save_config(self):
        try:
            with open("config.toml", w) as f:
                self.log("inf", "Saving the configuration file...")
                toml.dump(self.config, f)
                self.log("inf", "Config was saved to config.toml")
                #aok
                return 0
        #In case file doesnt exist
        except Exception as e:
            self.log("err", f"Failed to save to config.toml. {e}")
            return 1
    #Connect the main .log file to the api so plugins can log to latest.log w/o risking corrupting the file.
    def log(self, status, log):
        self.logger(str(status), str(log))

    #Get the uptime of the root of the bot
    def uptime(self):
        uptime = time.time() - self.start_time

        return uptime

    #Loads a cog
    def load(self, extension):
        extension = str(extension)
        self.logger("inf", f"Loading {extension}...")


        if extension.startswith("cogs."):
            extension.replace("cogs.", "", 1)

        try:
            self.bot.load_extension(f"cogs.{extension}")
        except Exception as e:
            self.logger("wrn", f"Extension {extension} failed to load due to: {e}")
        else:
            self.logger("dbg", "Changing and saving the config for cogs.")
            self.config["bot"]["cogs"].append(f"cogs.{extension}")
            code = self.save_config()
            if code == 1:
                self.logger("Error while saving to config.toml trying again in 2s...")
                time.sleep(2)
                code = self.save_config()
                if code == 1:
                    self.logger("Error while saving to config.toml. Attempt no. 2 aborting...")
                    return 1
            self.logger("inf", f"Extension {extension} loaded.")

    #Unloads a cog
    def unload(self, extension):
        extension = str(extension)
        self.logger("inf", f"Unloading {extension}...")

        if extension.startswith("cogs."):
            extension.replace("cogs.", "", 1)

        try:
            self.bot.unload_extension(f"cogs.{extension}")
        except Exception as e:
            if e == "ExtensionNotFound":
                self.logger("wrn", f"{extension} could not be found are you sure it exists?")
            elif e == "ExtensionNotLoaded":
                self.logger("wrn", f"{extension} is not loaded skipping..")
            else:
                self.logger("err", f"Unknown error while unloading {extension}. Error: {e}")
        #If nothing has gone wrong then write it to the config and save it to the file
        else:
            self.logger("dbg", "Changing and saving the config for cogs.")
            self.config["bot"]["cogs"].remove(extension)
            code = self.save_config()
            if code == 1:
                self.logger("Error while saving to config.toml trying again in 2s...")
                time.sleep(2)
                code = self.save_config()
                if code == 1:
                    self.logger("Error while saving to config.toml. Attempt no. 2 aborting...")
                    return 1
            self.logger("inf", f"Extension {extension} unloaded.")



    def __init__(self, config, bot, log):
        self.start_time = time.time()
        self.config = config
        self.bot = bot
        self.logger = log

print(type(config["bot"]))

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

if __name__ == "__main__":
    api = API(config, bot, log)
    bot.api = api
    bot.run(token)


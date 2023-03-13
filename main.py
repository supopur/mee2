import discord, os, sys, toml, time, datetime, logging, threading, asyncio

from discord.ext import commands

with open("config.toml", "r") as f:
    config = toml.load(f)

if config["webserver"]["debug"] == "true":
    logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG)
else:
    logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.INFO)

logging.getLogger().addHandler(logging.StreamHandler())
try:
    os.remove("main.log")
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
    #Connect the main .log file to the api so plugins can log to latest.log w/o risking corrupting the file. Absolutly useless as you can do: self.bot.api.logger("inf", "Hello w/o some useless function")
    def log(self, status, log):
        self.logger(str(status), str(log))

    #Get the uptime of the root of the bot
    def uptime(self):
        uptime = time.time() - self.start_time

        return uptime



    def __init__(self, config, bot, log):
        self.start_time = time.time()
        self.config = config
        self.bot = bot
        self.logger = log
        self.guild_ids = config["bot"]["guild_ids"]

#This is the most basic interface CLI wich is basically a comand line that appears when you launch the app it will have commands like stop, help, commands, cogs, load, unload and so on..
class CLI:

    def register_command(self, command, function, description):
        self.api.logger("inf", f"Trying to register {command} into the CLI commands...")

        if command in self.cli_cmds:
            self.api.logger("wrn", f"The command {command} already exists.")
            return 1

        if not callable(function):
            self.api.logger("err", f"Unable to register {command} as the passed function is not callable.")
            return 1
        try:
            command = str(command)
            description = str(description)
        except:
            self.api.logger("err", f"Passed cli name or description is not convertable to string.")
            return 1

        dictionary = {"description": description, "function": function}

        try:
            self.cli_cmds[command] = dictionary
        except:
            return 1
        else:
            self.api.logger("inf", f"CLI Command: {command} registered.")
            return 0

    def remove_command(self, command):
        self.api.logger("inf", f"Trying to remove {command} from the CLI commands...")

        if command in self.cli_cmds:
            self.cli_cmds[command] = None
            self.api.logger("inf", f"Command {command} removed.")
            return 0
        else:
            self.api.logger("wrn", f"Command {command} could not be removed as it doesnt exist.")
            return 1

    def help(self, page=1):
        page_size = 10
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        commands = list(self.cli_cmds.keys())[start_index:end_index]

        if not commands:
            self.api.logger("wrn", "No commands found for this page.")
            return 1

        msg = f"Commands (page {page}):\n"
        for command in commands:
            msg += f"  {command}: {self.cli_cmds[command]['description']}\n"

        self.api.logger("inf", msg)
        return 0

    def handle_input(self, user_input):
        # Split the user input into command and arguments
        parts = user_input.strip().split()
        if not parts:
            return
        command_name = parts[0]
        args = parts[1:]

        # Find the command
        command = self.cli_cmds.get(command_name)
        if not command:
            # Suggest commands based on input
            suggestions = [cmd_name for cmd_name in self.cli_cmds
                           if cmd_name.startswith(command_name)]
            if suggestions:
                self.api.logger("wrn", f"Unknown command '{command_name}'. Did you mean one of these?")
                for suggestion in suggestions:
                    self.api.logger("wrn", f" - {suggestion}")
            else:
                self.api.logger("wrn", f"Unknown command '{command_name}'")
            return

        # Execute the command
        function = command["function"]
        try:
            function(*args)
        except TypeError as e:
            self.api.logger("wrn", f"Invalid arguments: {e}")

    def run(self):
        # Start the CLI loop
        while True:
            try:
                user_input = input(self.prompt)
            except KeyboardInterrupt:
                # Handle CTRL+C
                break
            except EOFError:
                # Handle CTRL+D
                break
            else:
                self.handle_input(user_input)


    #Init of the class where all the values inside self are defined. Takes a loaded api as a arg
    def __init__(self, api):
        self.api = api
        self.cli_cmds = {}
        self.prompt = "mee2> "


@bot.event
async def on_ready():
    log("inf", f"We have logged in as {bot.user}")



@bot.slash_command(guild_ids=config["bot"]["guild_ids"])
async def stop(ctx):
    await ctx.defer()
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
    cli = CLI(api)
    bot.api = api
    #Load all the extensions
    for x in config["bot"]["cogs"]:
        log("inf", f"Loading {x}...")
        try:
            bot.load_extension(x)
        except Exception as e:
            log("wrn", f"Extension {x} failed to load due to: {e}")
        else:
            log("inf", f"{x} Loaded.")
    log("inf", "Loading all cogs completed.")

    # Create a thread to run the CLI
    cli_thread = threading.Thread(target=cli.run)
    cli_thread.start()

    bot.run(token)







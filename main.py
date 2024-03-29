import discord, os, sys, toml, time, datetime, logging, threading, asyncio, readline, importlib

from discord.ext import commands

with open("config.toml", "r") as f:
    config = toml.load(f)

try:
    os.remove("main.log")
except: pass


formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.FileHandler('main.log')
handler.setFormatter(formatter)
logger = logging.getLogger('')
logger.addHandler(handler)
logger.setLevel(logging.INFO)


#logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG)


#logging.getLogger().addHandler(logging.StreamHandler())

def log(level, log):
    if level == "inf":
        logger.info(log)
    elif level == "wrn":
        logger.warning(log)
    elif level == "dbg":
        logger.debug(log)
    elif level == "err":
        logger.error(log)

log("inf", "Logging utility set up.")

try:
    token = os.environ.get('MEETOO_TOKEN')
except:
    log("err", 'Error no token is present type: export MEETOO_TOKEN="[Your token here]" into your terminall NOW!')

if token == "":
    log("err", 'Error no token is present type: export MEETOO_TOKEN="[Your token here]" into your terminall NOW!')

log("dbg", f"Token is: {token}")

start_time = time.time()



bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

logger.debug("Loaded the client.")


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



    def __init__(self, config, bot, log, token):
        self.start_time = time.time()
        self.config = config
        self.bot = bot
        self.logger = log
        self.token = token
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
                print(f"Unknown command '{command_name}'. Did you mean one of these?")
                for suggestion in suggestions:
                    print(f" - {suggestion}")
            else:
                print(f"Unknown command '{command_name}'")
            return

        # Execute the command
        function = command["function"]
        try:
            function(self, *args)
        except TypeError as e:
            print(f"Invalid arguments: {e}")

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
    api = API(config, bot, log, token)
    cli = CLI(api)
    bot.api = api



    #CLI commands:

    #help
    def cli_help(self, page=1):
        page_size = 10
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        commands = list(self.cli_cmds.keys())[start_index:end_index]

        if not commands:
            print("No commands found for this page.")
            return 1

        msg = f"Commands (page {page}):\n"
        for command in commands:
            msg += f"  {command}: {self.cli_cmds[command]['description']}\n"

        print(msg)
        return 0

    cli.register_command("help", cli_help, "Shows this page.")

    #uptime
    def cli_uptime(self):
        uptime = self.api.uptime()
        uptime = str(datetime.timedelta(seconds=uptime)).split(".")[0]
        print(f"The uptime of the bot is {uptime} HH:MM:SS.")

    cli.register_command("uptime", cli_uptime, "Shows the uptime of the bot in seconds.")


    #info
    def cli_info(self):
        print(f"You are running version 0.1.0 - Dev. Created by supopur under the GNUv3 license. Git repo: https://git.nazev.eu:8443/supopur/mee2 Our discord link: https://discord.gg/dVVVSM4z")

    cli.register_command("info", cli_info, "Shows the info about the bot.")

    #shutdown
    def cli_sd(self):
        print("Shutting down the bot. You still must do CTRL+C to exit this terminal!!")
        try:
            sys.exit("Terminated from the cli..")
        except: pass

    cli.register_command("stop", cli_sd, "Terminates the bot.")

    def cli_clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    cli.register_command("clear", cli_clear, "Clears the terminal output")

    #load
    def cli_load(self, cog):
        try:
            cog = str(cog)
        except:
            print("Unable to convert the cog name to string.")
            return 1

        print(f"Trying to load {cog}...")

        try:
            cog_module = importlib.import_module(cog)
            class_name = cog.split(".")[1]
            print(class_name)
            cog_class = getattr(cog_module,class_name)
            cog_instance = cog_class(self.api.bot)
            self.api.bot.add_cog(cog_instance)
        except Exception as e:
            print(f"ERR: Failed to load {cog} becouse: {e}")
        else:
            print(f"Loaded {cog} successfully")

    cli.register_command("load", cli_load, "Loads a cog takes a cog name as a arg example: load cogs.example")

    #unload
    def cli_unload(self, cog):
        try:
            cog = str(cog)
        except:
            print("Unable to convert the cog name to string.")
            return 1
        print(f"Trying to loadd {cog}...")

        try:
            cog = cog.split(".")[1]
            self.api.bot.unload_extension(cog)
        except Exception as e:
            print(f"ERR Unable to unload {cog} due to: {e}")
        else:
            print(f"Loaded {cog} successfully")

    cli.register_command("unload", cli_unload, "Unloads a cog takes a cog name as a arg example: unload cogs.example")

    #start Starts the bot itself.
    def cli_start(self):
        print("Starting the bot...")
        try:
            self.api.bot.run(self.api.token)
        except Exception as e:
            print(e)
            return 1
        else:
            print("Bot started.")
        return 0

    #cli.register_command("start", cli_start, "Starts the bot.")


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

    #uncomment this to enable autostartup
    bot.run(token)

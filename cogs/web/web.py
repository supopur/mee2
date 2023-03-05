import sys
import discord
from discord.ext import commands
import quart
import toml
import logging
from quart import render_template
from quart.helpers import make_response

class WebServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.app = quart.Quart(__name__)

        with open("config.toml", "r") as f:
            config = toml.load(f)

        logging.info("Starting Quart server...")
        bot.loop.create_task(self.app.run_task(config["webserver"]["ip"], config["webserver"]["port"]))

        @self.app.route('/', methods=['GET'])
        async def index():
            return await render_template('index.html')

        @self.app.route('/configuration', methods=['GET'])
        async def configuration():
            return await render_template('configuration.html')

        @self.app.route('/dashboard', methods=['GET'])
        async def dashboard():
            return await render_template('dashboard.html')

        @self.app.route('/plugins', methods=['GET'])
        async def plugins():
            return await render_template('plugins.html')

def setup(bot):
    bot.add_cog(WebServer(bot))


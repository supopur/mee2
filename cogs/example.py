import discord, datetime
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(guild_ids=["823188238260633600"])
    async def hello(self, ctx):
        self.bot.api.logger("inf", "hello from the cog!")
        await ctx.send(f'Hello {ctx.author}')

    @commands.slash_command(guild_ids=["823188238260633600"])
    async def uptime(self, ctx):
        #Extends the 3s limit to reply so we dont get a unknown interation error.
        await ctx.defer()
        #References the api
        api = self.bot.api
        #Logs something using the api
        api.logger("inf", "example.py: Getting uptime...")

        #Gets the seconds of how long the root of the bot is runnig
        uptime = api.uptime()
        #Converts it into a HH:MM:SS format thats more readable. Also the .split makes sure that there are no ms
        uptime = str(datetime.timedelta(seconds=uptime)).split(".")[0]
        #Sends a follow up
        await ctx.followup.send(f"The uptime in H:MM:SS format: {uptime}")

def setup(bot):
    bot.add_cog(Greetings(bot))


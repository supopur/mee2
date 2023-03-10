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
        api = self.bot.api
        api.logger("inf", "example.py: Getting uptime...")
        uptime = api.uptime()
        uptime = str(datetime.timedelta(seconds=uptime)).split(".")[0]
        await ctx.respond(f"The uptime in H:MM:SS format: {uptime}")

def setup(bot):
    bot.add_cog(Greetings(bot))


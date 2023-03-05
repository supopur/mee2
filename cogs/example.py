import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=["823188238260633600"])
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author}')

def setup(bot):
    bot.add_cog(Greetings(bot))


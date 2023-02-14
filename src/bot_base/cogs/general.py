import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from bot_base.helpers import checks


SUCCESS = 0x9C84EF
ERROR = 0xE02B2B


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(
        name="help",
        description="List all currently available commands in this bot"
    )
    @checks.not_blacklisted()
    async def help(self, context: Context) -> None:
        prefix = self.bot.config['prefix']
        embed = discord.Embed(
            title="Help",
            description="List of available commands:",
            color=SUCCESS
        )
        
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition('\n')[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(),
                value=f"```{help_text}```",
                inline=False
            )
        await context.send(embed=embed)
        
    @commands.hybrid_command(
        name="bitcoin",
        description="Fetch the current price of BTC to demonstrate API usage"
    )
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(content_type="application/javascript")
                    embed = discord.Embed(
                        title="Bitcoin Price",
                        description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
                        color=SUCCESS
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There was an error with the API, try again later.",
                        color=ERROR
                    )
                await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))

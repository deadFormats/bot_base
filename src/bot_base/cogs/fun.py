import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from bot_base.helpers import checks


class Choice(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "heads"
        self.stop()
    
    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "tails"
        self.stop()
        
        
        
class RockPaperScissors(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Scissors", description="You choose scissors"),
            discord.SelectOption(label="Rock", description="You choose rock"),
            discord.SelectOption(label="Paper", description="You choose paper")
        ]
        super().__init__(placeholder="Choose...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]
        
        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]
        
        result_embed = discord.Embed()
        result_embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        
        if user_choice_index == bot_choice_index:
            result_embed.description = f"**DRAW**\n\n{interaction.user.name}: {user_choice}\nBoT: {bot_choice}"
            
        else:
            result_embed.description = f"Who fuckin cares I choose {random.choice(['rock', 'paper', 'scissors'])} you lose"
        
        await interaction.response.edit_message(embed=result_embed, content=None, view=None)
        

class RockPaperScissorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RockPaperScissors())
        
        
        
class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(
        name="coinflip",
        description="Make a coin flip"
    )
    @checks.not_blacklisted()
    async def coinflip(self, context:Context) -> None:
        buttons = Choice()
        embed = discord.Embed(
            description="Which way will it land?"
        )
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()
        result = random.choice(['heads', 'tails'])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Easy dubs, as you guessed, it landed on `{result}`"
            )
        else:
            embed = discord.Embed(
                description=f"Wrong, you said {buttons.value}, but it landed on {result}."
            )
        await message.edit(embed=embed, view=None, content=None)
        
        
        
async def setup(bot):
    await bot.add_cog(Fun(bot))

from discord.ext import commands
from discord.ext.commands import Context

from bot_base.helpers import checks


class Template(commands.Cog, name="template"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(
        name="testcommand",
        description="This is a test command that does nothing."
    )
    @checks.not_blacklisted()
    async def testcommand(self, context: Context):
        """
        This is a test command that does nothing.
        
        :param context: The command context.
        """
        await context.send("The command actually worked!")
        
        
async def setup(bot):
    await bot.add_cog(Template(bot))

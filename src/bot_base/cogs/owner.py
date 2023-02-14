import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from bot_base.helpers import checks, db_manager


SUCCESS = 0x9C84EF
ERROR = 0xE02B2B


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown"
    )
    @checks.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot
        
        :param context: The command context
        """
        embed = discord.Embed(
            description="Shutting down, bye! :wave:",
            color=SUCCESS
        )
        await context.send(embed=embed)
        await self.bot.close()
        
    @commands.hybrid_command(
        name="embed",
        description="Say something in an embed"
    )
    @app_commands.describe(message="The text that should be put into an embed.")
    @checks.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        Bot says something in an embed
        
        :param context: The command context
        :param message: The text to embed
        """
        embed = discord.Embed(
            description=message,
            color=SUCCESS
        )
        await context.send(embed=embed)
        
    @commands.hybrid_group(
        name="blacklist",
        description="Get the list of all blacklisted users."
    )
    @checks.is_owner()
    async def blacklist(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="You must specify a subcommand. \n\n**Subcommands:**\n`add` - Add a user to the blacklist\n`remove` - Remove a user from the blacklist.",
                color=ERROR
            )
            await context.send(embed=embed)
            
            
    @blacklist.command(
        base="blacklist",
        name="show",
        description="Shows the list of blacklisted users."
    )
    @checks.is_owner()
    async def blacklist_show(self, context: Context) -> None:
        blacklisted_users = await db_manager.get_blacklisted_users()
        if len(blacklisted_users) == 0:
            embed = discord.Embed(
                description="There are currently no blacklisted users.",
                color=ERROR
            )
            await context.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="Blacklisted Users",
            color=SUCCESS
        )
        users = []
        for bluser in blacklisted_users:
            user = self.bot.get_user(int(bluser.user_id)) or await self.bot.fetch_user(int(bluser.user_id))
            users.append(f"+ {user.mention} ({user}) - Blacklisted <t:{bluser.created_at}>")
        embed.description = "\n".join(users)
        
        await context.send(embed=embed)
        
    @blacklist.command(
        base="blacklist",
        name="add",
        description="Ban a user from using the bot."
    )
    @app_commands.describe(user="The user that you want to blacklist.")
    @checks.is_owner()
    async def blacklist_add(self, context: Context, user: discord.User) -> None:
        user_id = user.id
        if await db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** is already in the blacklist.",
                color=ERROR
            )
            await context.send(embed=embed)
            return
        total = await db_manager.add_user_to_blacklist(user_id)
        embed = discord.Embed(
            description=f"**{user.name}** has been successfully added to the blacklist.",
            color=SUCCESS
        )
        embed.set_footer(
            text=f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} in the blacklist."
        )
        await context.send(embed=embed)
        
    @blacklist.command(
        base="blacklist",
        name="remove",
        description="Remove a user from the blacklist."
    )
    @app_commands.describe(user="The user you want to remove from the blacklist.")
    @checks.is_owner()
    async def blacklist_remove(self, context: Context, user: discord.User) -> None:
        user_id = user.id
        if not await db_manager.is_blacklisted(user_id):
            embed = discord.Embed(
                description=f"**{user.name}** is not in the blacklist.",
                color=ERROR
            )
            await context.send(embed=embed)
            return
        total = await db_manager.remove_user_from_blacklist(user_id)
        
        embed = discord.Embed(
            description=f"**{user.name}** has been successfully removed from the blacklist.",
            color=SUCCESS
        )
        embed.set_footer(
            f"There {'is' if total == 1 else 'are'} now {total} {'user' if total == 1 else 'users'} in the blacklist"
        )
        await context.send(embed=embed)
        
        
        
async def setup(bot):
    await bot.add_cog(Owner(bot))

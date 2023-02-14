import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from bot_base.helpers import checks, db_manager


RED = 0xE02B2B
SUCCESS = 0x9C84EF


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(
        name="kick",
        description="Kick a user out of the server"
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="The user to kick from the server", reason="The reason they're being kicked")
    async def kick(self, context: Context, user: discord.User, *, reason: str = "Not specified") -> None:
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                description="User has administrative permissions",
                color=RED
            )
            await context.send(embed=embed)
            
        else:
            try:
                embed = discord.Embed(
                    description=f"**{member}** was kicked by **{context.author}**!",
                    color=SUCCESS
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{context.author}** from **{context.guild.name}**\nReason: {reason}"
                    )
                except:
                    pass
                await member.kick(reason=reason)
            except:
                embed = discord.Embed(
                    description="An error occurred while trying to kick the user.",
                    color=RED
                )
                await context.send(embed=embed)
                
    @commands.hybrid_command(
        name="ban",
        description="Bans a user from the server"
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="The user that should be banned.", reason="The reason why the user is being banned.")
    async def ban(self, context: Context, user: discord.User, *, reason: str = "Not specified") -> None:
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    description = "User has administrator permissions",
                    color=RED
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"**{member}** was banned by **{context.author}**",
                    color=SUCCESS
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(f"You were banned by **{context.author}** from **{context.guild.name}**.\nReason: {reason}")
                except:
                    pass
                await member.ban(reason=reason)
        except:
            embed = discord.Embed(
                title="Error!",
                description="There was an error while attempting to ban the User",
                color=RED
            )
            await context.send(embed=embed)
            
    @commands.hybrid_group(
        name="warning",
        description="Manage a user's warnings on the server"
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warning(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`add` -  Add a warning to a user.\n`remove` - Remove a warning from a user.\n`list` - List all warnings given to a user.",
                color=RED
            )
            await context.send(embed=embed)
        
    @warning.command(
        name="add",
        description="Adds a warning to a user in the server."
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(user="The user that should be warned.", reason="The reason the user is being warned.")
    async def warning_add(self, context: Context, user: discord.User, *, reason: str = "Not specified") -> None:
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        total = await db_manager.add_warn(user.id, context.guild.id, context.author.id, reason)
        
        embed = discord.Embed(
            description=f"**{member}** was warned by **{context.author}**\n. Total warns for this user: {total}",
            color=SUCCESS
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await context.send(embed=embed)
        try:
            await member.send(f"You were warned by **{context.author}** in **{context.guild.name}**\nReason: {reason}")
        except:
            await context.send(f"{member.mention}, you were warned by **{context.author}**!\nReason: {reason}")
            
    @warning.command(
        name="remove",
        description="Remove a warning from a user"
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    async def warning_remove(self, context: Context):
        await context.send("This command doesn't work")
        
    @warning.command(
        name="list",
        description="List all warnings a user has been given."
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="The user to view the warnings of")
    async def warning_list(self, context: Context, user: discord.User):
        warnings_list = await db_manager.get_warnings(user.id, context.guild.id)
        embed = discord.Embed(
            title=f"Warnings for {user}",
            color=SUCCESS
        )
        description = ""
        if len(warnings_list) == 0:
            description = "This user has no warnings."
        else:
            for warning in warnings_list:
                description += f"+ Warned by <@{warning.moderator_id}>: **{warning.reason}** (<t:{warning.created_at}>) - ID #{warning.id}\n"
        embed.description = description
        
        await context.send(embed=embed)
        
    @commands.hybrid_command(
        name="purge",
        description="Delete messages from the server"
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(amount="The number of messages to delete.")
    async def purge(self, context: Context, amount: int) -> None:
        await context.send("Deleting messages...")
        purged_messages = await context.channel.purge(limit=amount+1)
        embed = discord.Embed(
            description=f"**{context.author}** cleared **{len(purged_messages)-1}** messages.",
            color=SUCCESS
        )
        await context.channel.send(embed=embed)
        
        
async def setup(bot):
    await bot.add_cog(Moderation(bot))

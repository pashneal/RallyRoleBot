from discord.ext import commands, tasks
from discord.utils import get
import discord
import data
import json
import rally_api


def owner_or_permissions(**perms):
    original = commands.has_permissions(**perms).predicate

    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)

    return commands.check(extended_check)


class Role_Gate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_roles.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("We have logged in as {0.user}".format(self.bot))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Command missing arguments")

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

    @commands.command(
        name="set_role_mapping",
        help=" <coin name> <coin amount> <role name> "
        + "Set a mapping between coin and role. Roles will be constantly updated.",
    )
    # @owner_or_permissions(administrator=True)
    async def set_coin_for_role(self, ctx, coin_name, coin_amount: int, role_name):
        if ctx.guild is None:
            return
        data.add_role_coin_mapping(ctx.guild.id, coin_name, coin_amount, role_name)

    @commands.command(
        name="one_time_role_mapping",
        help=" <coin name> <coin amount> <role name>"
        + " Set a mapping to be applied once instantly.",
    )
    async def one_time_role_mapping(self, ctx, coin_name, coin_amount: int, role_name):
        if ctx.guild is None:
            return
        for member in ctx.guild.members:
            await self.grant_deny_role_to_member(
                {
                    data.GUILD_ID_KEY: ctx.guild.id,
                    data.COIN_KIND_KEY: coin_name,
                    data.REQUIRED_BALANCE_KEY: coin_amount,
                    data.ROLE_NAME_KEY: role_name,
                },
                member,
            )
        await ctx.send("Done")

    @commands.command(
        name="set_channel_mapping",
        help=" <coin name> <coin amount> <channel name> "
        + "Set a mapping between coin and channel. Channel membership will be constantly updated.",
    )
    # @owner_or_permissions(administrator=True)
    async def set_coin_for_channel(self, ctx, coin_name, coin_amount: int, role_name):
        if ctx.guild is None:
            return
        data.add_channel_coin_mapping(ctx.guild.id, coin_name, coin_amount, role_name)
        await ctx.send("Done")

    @commands.command(
        name="one_time_channel_mapping",
        help=" <coin name> <coin amount> <channel name>"
        + " Grant/deny access to a channel instantly.",
    )
    async def one_time_channel_mapping(
        self, ctx, coin_name, coin_amount: int, channel_name
    ):
        if ctx.guild is None:
            return
        for member in ctx.guild.members:
            await self.grant_deny_channel_to_member(
                {
                    data.GUILD_ID_KEY: ctx.guild.id,
                    data.COIN_KIND_KEY: coin_name,
                    data.REQUIRED_BALANCE_KEY: coin_amount,
                    data.CHANNEL_NAME_KEY: channel_name,
                },
                member,
            )
        await ctx.send("Done")

    @commands.command(
        name="unset_role_mapping",
        help=" <coin name> <coin amount> <role name> "
        + "Unset a mapping between coin and role",
    )
    # @owner_or_permissions(administrator=True)
    async def unset_coin_for_role(self, ctx, coin_name, coin_amount: int, role_name):
        if ctx.guild is None:
            return
        data.remove_role_mapping(ctx.guild.id, coin_name, coin_amount, role_name)
        await ctx.send("Unset")

    @commands.command(
        name="unset_channel_mapping",
        help=" <coin name> <coin amount> <channel name> "
        + "Unset a mapping between coin and channel",
    )
    # @owner_or_permissions(administrator=True)
    async def unset_coin_for_channel(
        self, ctx, coin_name, coin_amount: int, channel_name
    ):
        if ctx.guild is None:
            return
        data.remove_channel_mapping(ctx.guild.id, coin_name, coin_amount, channel_name)
        await ctx.send("Unset")

    @commands.command(name="get_role_mappings", help="Get role mappings")
    # @owner_or_permissions(administrator=True)
    async def get_role_mappings(self, ctx):
        await ctx.send(
            json.dumps(
                [
                    json.dumps(mapping)
                    for mapping in data.get_role_mappings(ctx.guild.id)
                ]
            )
        )

    @commands.command(name="get_channel_mappings", help="Get channel mappings")
    # @owner_or_permissions(administrator=True)
    async def get_channel_mappings(self, ctx):
        await ctx.send(
            json.dumps(
                [
                    json.dumps(mapping)
                    for mapping in data.get_channel_mappings(ctx.guild.id)
                ]
            )
        )

    @commands.command(name="set_rally_id", help="Set your rally id")
    async def set_rally_id(self, ctx, rally_id):
        data.add_discord_rally_mapping(ctx.author.id, rally_id)
        await ctx.sent("Set")

    async def grant_deny_channel_to_member(self, channel_mapping, member):
        print("Checking channel")
        rally_id = data.get_rally_id(member.id)
        if rally_id is None:
            return
        matched_channels = [
            channel
            for channel in member.guild.channels
            if channel.name == channel_mapping[data.CHANNEL_NAME_KEY]
        ]
        if len(matched_channels) == 0:
            return
        channel_to_assign = matched_channels[0]
        if (
            rally_api.get_balance_of_coin(rally_id, channel_mapping[data.COIN_KIND_KEY])
            > channel_mapping[data.REQUIRED_BALANCE_KEY]
        ):
            if channel_to_assign is not None:
                await channel_to_assign.edit(
                    overwrites={
                        member: discord.PermissionOverwrite(
                            read_messages=True,
                            send_messages=True,
                            read_message_history=True,
                        )
                    }
                )
                print("Assigned channel to member")
        else:
            if channel_to_assign is not None:
                await channel_to_assign.edit(
                    overwrites={
                        member: discord.PermissionOverwrite(
                            read_messages=False,
                            send_messages=False,
                            read_message_history=False,
                        )
                    }
                )
                print("Removed channel to member")

    async def grant_deny_role_to_member(self, role_mapping, member):
        rally_id = data.get_rally_id(member.id)
        if rally_id is None:
            return
        role_to_assign = get(member.guild.roles, name=role_mapping["role"])
        if (
            rally_api.get_balance_of_coin(rally_id, role_mapping[data.COIN_KIND_KEY])
            > role_mapping[data.REQUIRED_BALANCE_KEY]
        ):
            if role_to_assign is not None:
                await member.add_roles(role_to_assign)
                print("Assigned role to member")
        else:
            if role_to_assign in member.roles:
                await member.remove_roles(role_to_assign)
                print("Removed role to member")

    @tasks.loop(seconds=60.0)
    async def update_roles(self):
        print("Updating roles")
        guilds = self.bot.guilds
        for guild in guilds:
            await guild.chunk()
            role_mappings = data.get_role_mappings(guild.id)
            channel_mappings = data.get_channel_mappings(guild.id)
            for member in guild.members:
                rally_id = data.get_rally_id(member.id)
                if rally_id is not None:
                    for role_mapping in role_mappings:
                        await self.grant_deny_role_to_member(role_mapping, member)
                    for channel_mapping in channel_mappings:
                        await self.grant_deny_channel_to_member(channel_mapping, member)

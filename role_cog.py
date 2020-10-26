from discord.ext import commands, tasks
from discord.utils import get
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

    @commands.command(
        name="set_role_mapping", help="Set a mapping between coin and role"
    )
    @owner_or_permissions(administrator=True)
    async def set_coin_for_role(self, ctx, coin_name, coin_amount: int, role_name):
        if ctx.guild is None:
            return
        data.add_role_coin_mapping(ctx.guild.id, coin_name, coin_amount, role_name)

    @commands.command(
        name="unset_role_mapping", help="Unset a mapping between coin and role"
    )
    @owner_or_permissions(administrator=True)
    async def unset_coin_for_role(self, ctx, coin_name, coin_amount: int, role_name):
        if ctx.guild is None:
            return
        data.remove_role_mapping(ctx.guild.id, coin_name, coin_amount, role_name)
        await ctx.send("Unset")

    @commands.command(name="get_role_mapping", help="Get role mappings")
    @owner_or_permissions(administrator=True)
    async def get_role_mappings(self, ctx):
        await ctx.send(
            json.dumps(
                [
                    json.dumps(mapping)
                    for mapping in data.get_role_mappings(ctx.guild.id)
                ]
            )
        )

    @commands.command(name="set_rally_id", help="Set your rally id")
    async def set_rally_id(self, ctx, rally_id):
        data.add_discord_rally_mapping(ctx.author.id, rally_id)
        await ctx.sent("Set")

    @tasks.loop(seconds=3600.0)
    async def update_roles(self):
        print("Updating roles")
        guilds = self.bot.guilds
        for guild in guilds:
            await guild.chunk()
            role_mappings = data.get_role_mappings(guild.id)
            for member in guild.members:
                rally_id = data.get_rally_id(member.id)
                if rally_id is not None:
                    for role_mapping in role_mappings:
                        role_to_assign = get(guild.roles, name=role_mapping["role"])
                        if (
                            rally_api.get_balance_of_coin(
                                rally_id, role_mapping["coinKind"]
                            )
                            > role_mapping["requiredBalance"]
                        ):
                            if role_to_assign is not None:
                                await member.add_roles(role_to_assign)
                                print("Updated role for a member")
                        else:
                            if role_to_assign in member.roles:
                                await member.remove_roles(role_to_assign)

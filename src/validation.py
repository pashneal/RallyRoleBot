from discord.ext import commands


def owner_or_permissions(**perms):
    original = commands.has_permissions(**perms).predicate

    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)

    return commands.check(extended_check)


async def is_valid_role(self, ctx, role_name):
    if get(ctx.guild.roles, name=role_name) is None:
        await ctx.send("Role does not exist on this server. Please create it first.")
        return False
    return True

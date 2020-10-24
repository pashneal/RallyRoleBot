import discord
from discord.ext import commands
import config
import data

config.parse_args()
bot = commands.Bot(command_prefix=config.CONFIG.command_prefix)

def owner_or_permissions(**perms):
    original = commands.has_permissions(**perms).predicate
    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)
    return commands.check(extended_check)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='set_role_mapping', help='Set a mapping between coin and role')
@owner_or_permissions(administrator=True)
async def set_coin_for_role(ctx, coin_name, coin_amount : int, role_name):
    if ctx.guild is None:
        return
    data.add_role_coin_mapping(ctx.guild.id, coin_name, coin_amount, role_name)

@bot.command(name='set_role_mapping', help='Set a mapping between coin and role')
@owner_or_permissions(administrator=True)
async def get_role_mappings(ctx):
    ctx.send(data.get_role_mappings())

@bot.command(name='set_rally_id', help='Set your rally id')
async def set_rally_id(ctx, rally_id):
    data.add_discord_rally_mapping(ctx.author.id, rally_id)

if __name__ == "__main__":
    bot.run(config.CONFIG.secret_token)
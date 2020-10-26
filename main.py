import discord
from discord.ext import tasks, commands
import config
import data
import threading
import role_cog


if __name__ == "__main__":
    config.parse_args()
    data.connect_db()
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    bot = commands.Bot(command_prefix=config.CONFIG.command_prefix, intents=intents)
    bot.add_cog(role_cog.Role_Gate(bot))
    bot.run(config.CONFIG.secret_token)

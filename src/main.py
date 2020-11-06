import discord
from discord.ext import tasks, commands
import config
import data
import threading
import role_cog
import rally_cog
import channel_cog
import update_cog


if __name__ == "__main__":
    config.parse_args()
    data.connect_db()
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    bot = commands.Bot(command_prefix=config.CONFIG.command_prefix, intents=intents)
    bot.add_cog(role_cog.RoleCommands(bot))
    bot.add_cog(channel_cog.ChannelCommands(bot))
    bot.add_cog(rally_cog.RallyCommands(bot))
    bot.add_cog(update_cog.UpdateTask(bot))
    bot.run(config.CONFIG.secret_token)

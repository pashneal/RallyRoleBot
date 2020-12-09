from discord.ext import commands

import errors
import rally_api


class CreatorCoin(commands.Converter):
    """
        Custom converter for easy input validation
        Returns the coin name if valid
        Raises BadArgument error if the Creator Coin does not exist
    """

    async def convert(self, ctx, coin_name):
        valid = rally_api.valid_coin_symbol(coin_name)
        if not valid:
            raise errors.BadArgument("Coin '" + coin_name + "' does not seem to exist.")
        return coin_name


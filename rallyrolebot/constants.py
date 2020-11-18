from discord import Color
# TODO: Place holder for now - can use __init__.py once dependencies such as 
# data.ROLE_MAPPINGS_TABLE and rally_api.BASE_URL have been removed

"""
 Constants useful for data module
"""
ROLE_MAPPINGS_TABLE = "mappings"
CHANNEL_MAPPINGS_TABLE = "channel_mappings"
RALLY_CONNECTIONS_TABLE = "rally_connections"

GUILD_ID_KEY = "guildId"
COIN_KIND_KEY = "coinKind"
REQUIRED_BALANCE_KEY = "requiredBalance"
ROLE_NAME_KEY = "roleName"
CHANNEL_NAME_KEY = "channel"
DISCORD_ID_KEY = "discordId"
RALLY_ID_KEY = "rallyId"

"""
 Constants useful for  rally_api module
"""

COIN_KIND_KEY = "coinKind"
COIN_BALANCE_KEY = "coinBalance"

BASE_URL = "https://api.rally.io/v1"


"""
    Constants useful for update_cog module
"""
UPDATE_WAIT_TIME = 600

"""
    Miscellaneous constants
"""

ERROR_COLOR =  Color(0xFF0000)
SUCCESS_COLOR = Color(0x0000FF)
WARNING_COLOR = Color(0xFFFF00)

import dataset
import config

db = None

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


def connect_db():
    global db
    db = dataset.connect(config.CONFIG.database_connection)


def add_role_coin_mapping(guild_id, coin, required_balance, role):
    global db
    table = db[ROLE_MAPPINGS_TABLE]
    table.insert(
        {
            GUILD_ID_KEY: guild_id,
            COIN_KIND_KEY: coin,
            REQUIRED_BALANCE_KEY: required_balance,
            ROLE_NAME_KEY: role,
        }
    )


def add_channel_coin_mapping(guild_id, coin, required_balance, channel):
    global db
    table = db[CHANNEL_MAPPINGS_TABLE]
    table.insert(
        {
            GUILD_ID_KEY: guild_id,
            COIN_KIND_KEY: coin,
            REQUIRED_BALANCE_KEY: required_balance,
            CHANNEL_NAME_KEY: channel,
        }
    )


def get_role_mappings(guild_id, coin=None, required_balance=None, role=None):
    global db
    table = db[ROLE_MAPPINGS_TABLE]
    filtered_mappings = table.find(guildId=guild_id)
    if coin is not None:
        filtered_mappings = [m for m in filtered_mappings if m[COIN_KIND_KEY] == coin]
    if required_balance is not None:
        filtered_mappings = [
            m for m in filtered_mappings if m[REQUIRED_BALANCE_KEY] == required_balance
        ]
    if role is not None:
        filtered_mappings = [m for m in filtered_mappings if m[ROLE_NAME_KEY] == role]
    return filtered_mappings


def get_channel_mappings(guild_id, coin=None, required_balance=None, channel=None):
    global db
    table = db[CHANNEL_MAPPINGS_TABLE]
    filtered_mappings = table.find(guildId=guild_id)
    if coin is not None:
        filtered_mappings = [m for m in filtered_mappings if m[COIN_KIND_KEY] == coin]
    if required_balance is not None:
        filtered_mappings = [
            m for m in filtered_mappings if m[REQUIRED_BALANCE_KEY] == required_balance
        ]
    if channel is not None:
        filtered_mappings = [
            m for m in filtered_mappings if m[CHANNEL_NAME_KEY] == channel
        ]
    return filtered_mappings


def remove_role_mapping(guild_id, coin, required_balance, role):
    global db
    table = db[ROLE_MAPPINGS_TABLE]
    table.delete(
        guildId=guild_id, coinKind=coin, requiredBalance=required_balance, role=role
    )


def remove_channel_mapping(guild_id, coin, required_balance, channel):
    global db
    table = db[CHANNEL_MAPPINGS_TABLE]
    table.delete(
        guildId=guild_id,
        coinKind=coin,
        requiredBalance=required_balance,
        channel=channel,
    )


def add_discord_rally_mapping(discord_id, rally_id):
    global db
    table = db[RALLY_CONNECTIONS_TABLE]
    table.insert({DISCORD_ID_KEY: discord_id, RALLY_ID_KEY: rally_id})


def get_rally_id(discord_id):
    global db
    table = db[RALLY_CONNECTIONS_TABLE]
    row = table.find_one(discordID=discord_id)
    if row is not None:
        return row[RALLY_ID_KEY]
    return None

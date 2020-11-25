import dataset

import config
from constants import *

from utils.ext import connect_db

"""Functions for managing a dataset SQL database
    # Schemas

    #################### mappings ######################
    guildId
    coinKind
    requiredBalance
    roleName

    #################### channel_mappings ######################
    guildId
    coinKind
    requiredBalance
    channelName

    #################### rally_connections ######################
    discordId
    rallyId
"""


@connect_db
def add_role_coin_mapping(db, guild_id, coin, required_balance, role):
    table = db[ROLE_MAPPINGS_TABLE]
    table.upsert(
        {
            GUILD_ID_KEY: guild_id,
            COIN_KIND_KEY: coin,
            REQUIRED_BALANCE_KEY: required_balance,
            ROLE_NAME_KEY: role,
        },
        [GUILD_ID_KEY, ROLE_NAME_KEY],
    )


@connect_db
def add_channel_coin_mapping(db, guild_id, coin, required_balance, channel):
    table = db[CHANNEL_MAPPINGS_TABLE]
    table.upsert(
        {
            GUILD_ID_KEY: guild_id,
            COIN_KIND_KEY: coin,
            REQUIRED_BALANCE_KEY: required_balance,
            CHANNEL_NAME_KEY: channel,
        },
        [GUILD_ID_KEY, CHANNEL_NAME_KEY],
    )


@connect_db
def get_role_mappings(db, guild_id, coin=None, required_balance=None, role=None):

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


@connect_db
def get_channel_mappings(db, guild_id, coin=None, required_balance=None, channel=None):

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

@connect_db
def remove_role_mapping(db, guild_id, coin, required_balance, role):

    table = db[ROLE_MAPPINGS_TABLE]
    table.delete(
        guildId=guild_id, coinKind=coin, requiredBalance=required_balance, roleName=role
    )


@connect_db
def remove_channel_mapping(db, guild_id, coin, required_balance, channel):

    table = db[CHANNEL_MAPPINGS_TABLE]
    table.delete(
        guildId=guild_id,
        coinKind=coin,
        requiredBalance=required_balance,
        channel=channel,
    )

@connect_db
def add_discord_rally_mapping(db, discord_id, rally_id):
    table = db[RALLY_CONNECTIONS_TABLE]
    table.upsert({DISCORD_ID_KEY: discord_id, RALLY_ID_KEY: rally_id}, [DISCORD_ID_KEY])

@connect_db
def get_rally_id(db, discord_id):

    table = db[RALLY_CONNECTIONS_TABLE]
    row = table.find_one(discordId=discord_id)
    if row is not None:
        return row[RALLY_ID_KEY]
    return None

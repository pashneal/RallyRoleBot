import dataset
import config

db = None


def connect_db():
    global db
    db = dataset.connect(config.CONFIG.database_connection)


def add_role_coin_mapping(guild_id, coin, required_balance, role):
    global db
    table = db["mappings"]
    table.insert(
        {
            "guildId": guild_id,
            "coinKind": coin,
            "requiredBalance": required_balance,
            "role": role,
        }
    )


def get_role_mappings(guild_id, coin=None, required_balance=None, role=None):
    global db
    table = db["mappings"]
    filtered_mappings = table.find(guildId=guild_id)
    if coin is not None:
        filtered_mappings = [m for m in filtered_mappings if m["coinKind"] == coin]
    if required_balance is not None:
        filtered_mappings = [
            m for m in filtered_mappings if m["requiredBalance"] == required_balance
        ]
    if role is not None:
        filtered_mappings = [m for m in filtered_mappings if m["role"] == role]
    return filtered_mappings


def remove_role_mappings(guild_id, coin, required_balance, role):
    global db
    table = db["mappings"]
    table.delete(
        guildId=guild_id, coinKind=coin, requiredBalance=required_balance, role=role
    )


def add_discord_rally_mapping(discord_id, rally_id):
    global db
    table = db["rally_connections"]
    table.insert({"discordId": discord_id, "rallyId": rally_id})


def get_rally_id(discord_id):
    global db
    table = db["rally_connections"]
    row = table.find_one(discordID=discord_id)
    if row is not None:
        return row["rallyId"]
    return None

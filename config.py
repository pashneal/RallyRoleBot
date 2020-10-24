import configargparse

CONFIG = None

arg_parser = configargparse.ArgParser(default_config_files=["config.txt"])

arg_parser.add('-c', '--config', is_config_file=True, help='Config file')

arg_parser.add(
    "-t", "--secret_token", help="Discord bot login token"
)


def parse_args():
    global CONFIG
    CONFIG = arg_parser.parse_args()

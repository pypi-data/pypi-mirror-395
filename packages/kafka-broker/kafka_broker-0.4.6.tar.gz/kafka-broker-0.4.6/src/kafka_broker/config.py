from configparser import ConfigParser
import os
from pathlib import Path

current_dir = Path(__file__).parent.resolve()

BASE_CONFIG = str(Path(current_dir, "base_config.ini"))


def check_config(config: dict) -> dict:
    """Quick check if the config has the required settings."""
    
    general = config.get("general")
    if not general:
        raise AttributeError('"general" needs to be defined')

    cur_loc = general.get("current_location")
    if not cur_loc:
        raise AttributeError('"general:current_location" needs to be defined')
    
    return config


def get_config(filename: str):
    base_config_parser = ConfigParser()
    base_config_parser.read(BASE_CONFIG)
    base_config = dict(base_config_parser._sections)
    
    if not os.path.isfile(filename):
        with open(BASE_CONFIG, 'r') as f:
            new_config = f.read()

        with open(filename, 'w') as f:
            f.write(new_config)

    config_parser = ConfigParser()
    config_parser.read(filename)
    custom_config = dict(config_parser._sections)

    base_config.update(custom_config)
    return check_config(base_config)

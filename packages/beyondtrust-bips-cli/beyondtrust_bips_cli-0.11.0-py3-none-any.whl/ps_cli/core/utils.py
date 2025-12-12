import argparse
import configparser
import uuid


def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def is_valid_uuid(value):
    try:
        _ = uuid.UUID(str(value))
        return True
    except ValueError:
        # If a ValueError is raised, the value is not a valid UUID
        return False


def valid_uuid(value):
    if not is_valid_uuid(value):
        raise argparse.ArgumentTypeError(f"Invalid UUID: {value}")
    return value

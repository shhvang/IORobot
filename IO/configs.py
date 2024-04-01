import os
import configparser
from typing import Union, List

class ConfigurationError(Exception):
    pass

class Configuration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = configparser.ConfigParser()
            cls._instance._config.read("config.ini")
        return cls._instance

    def get_config(self, key: str, fallback: Union[str, List[int]] = None, cast_func = str) -> Union[str, List[int]]:
        value = os.getenv(key)
        if value is not None:
            return cast_func(value)

        if self._instance._config.has_option("kiyo", key):
            return cast_func(self._instance._config.get("kiyo", key))

        if fallback is not None:
            return fallback

        raise ConfigurationError(f"Configuration '{key}' not found.")

def encrypt(value: str) -> str:
    # Placeholder encryption - Replace with a secure encryption method
    return value[::-1]  # Reverse the string as an example

def decrypt(value: str) -> str:
    # Placeholder decryption - Replace with the reverse of your encryption method
    return value[::-1]  # Reverse the string as an example

config = Configuration()

TOKEN: str = config.get_config('TOKEN', cast_func=str)
BASE_URL: str = config.get_config('BASE_URI', fallback='https://api.telegram.org/bot', cast_func=str)
BASE_FILE_URL: str = config.get_config('BASEFILE_URI', fallback='https://api.telegram.org/file/bot', cast_func=str)

DEV_USERS: List[int] = config.get_config('DEV_ID', fallback=[1, 2, 3], cast_func=lambda x: list(map(int, x.split(','))))
SUDO_USERS: List[int] = config.get_config('SUDO_ID', fallback=[1, 2, 3], cast_func=lambda x: list(map(int, x.split(','))))
OWNER_ID: List[int] = config.get_config('OWNER_ID', fallback=[1], cast_func=lambda x: list(map(int, x.split(','))))
WHITELIST_USERS: List[int] = config.get_config('WHITELIST_USERS', fallback=[1], cast_func=lambda x: list(map(int, x.split(','))))
SUPPORT_USERS: List[int] = config.get_config('SUPPORT_USERS', fallback=[1], cast_func=lambda x: list(map(int, x.split(','))))



# Using a default URI for database if config not found
DATABASE_URI: str = config.get_config(
    'DATABASE_URI',
    fallback='postgresql://username:password@hostname/dbname',
    cast_func=str
)

# Encrypt sensitive data before saving to config.ini
ENCRYPTED_TOKEN = encrypt(TOKEN)
ENCRYPTED_DATABASE_URI = encrypt(DATABASE_URI)

config._instance._config.set("kiyo", "TOKEN", ENCRYPTED_TOKEN)
config._instance._config.set("kiyo", "DATABASE_URI", ENCRYPTED_DATABASE_URI)

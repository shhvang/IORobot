import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def get_config(key, fallback=None, cast_func=str):
    value = os.getenv(key)
    if value is not None:
        return cast_func(value)

    if config.has_option("kiyo", key):
        return cast_func(config.get("kiyo", key))

    return fallback

Token = get_config(
    'Token', fallback='7042927041:AAFbS4H_RthM70wng9LhgMxEKS5jo4wXScc', cast_func=str
)
BaseUrl = get_config('BaseUrl', fallback='https://api.telegram.org/bot', cast_func=str)
BaseFileUrl = get_config('BaseFileUrl', fallback='https://api.telegram.org/file/bot', cast_func=str)

DEV_ID = get_config('DEV_ID', fallback=[1, 2, 3], 
                    cast_func=lambda x: list(map(int, x.split(',')))
                    )
SUDO_ID = get_config('SUDO_ID', fallback=[1, 2, 3], cast_func=lambda x: list(map(int, x.split(','))))
OWNER_ID = get_config('OWNER_ID', fallback=[1], cast_func=lambda x: list(map(int, x.split(','))))

DATABASE_URI = get_config(
    'DATABASE_URI', 
    fallback='postgresql://tqfhclle:L-s2F6LSSGl-_ij7Qt24fFUwrMBM0m0n@raja.db.elephantsql.com/tqfhclle', 
    cast_func=str
)

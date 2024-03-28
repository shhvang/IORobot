import pathlib, os, configparser

def isLocalHost():
    return os.path.exists("./localhost.txt")

def get_config(key, fallback=None, cast_func=str):
    config = configparser.ConfigParser()
    config.read("config.ini")
    value = os.getenv(key)
    if value is not None:
        return cast_func(value)

    if config.has_option("kiyo", key):
        return cast_func(config.get("kiyo", key))

    return fallback

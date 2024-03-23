from Main import LOGS
from Main.startup.loader import Loader
import inspect

class Attributes:
    IMPORTED = {}
    MIGRATEABLE = []
    HELPABLE = {}
    STATS = []
    USER_INFO = []
    DATA_IMPORT = []
    DATA_EXPORT = []
    CHAT_SETTINGS = {}
    USER_SETTINGS = {}


def load_all_modules():
    try:
        loaded_modules = Loader('./plugins').import_module(log=True)
    except Exception as e:
        LOGS.error(f"Error loading modules: {e}")
        return

    Attributes.IMPORTED = {
        getattr(m, "__mod_name__", m.__name__.capitalize()): m
        for m in loaded_modules if inspect.ismodule(m)
    }
    
    if len(Attributes.IMPORTED) != len(loaded_modules):
        LOGS.warning("Some loaded items are not modules.")
    
    for attr in ['get_help', '__migrate__', '__stats__', '__user_info__', 
                 '__import_data__', '__export_data__', '__chat_settings__', '__user_settings__']:
        setattr(
            Attributes, attr.upper(), 
            {name.lower(): m for name, m in Attributes.IMPORTED.items() if hasattr(m, attr)}
        )

    LOGS.info(f'Loaded Plugins: {str(loaded_modules)}')

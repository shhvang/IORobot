import time
import asyncio
import logging
import pathlib
import inspect
import traceback
from typing import Optional

from telegram.ext import ApplicationBuilder
from kiyo.lib import Attributes
from kiyo import configs as config
from kiyo.logger import enablelogging, logger
from kiyo.loader import Loader
from kiyo_plugins.external.langhelpers import reload_strings

class rKiyobot:
    def __init__(self, cfg=config, logger=logger, *args, **kwargs):
        self.startTime = time.time()
        self.config = cfg
        self.logger = logger
        self.__version__ = '2.1'
        self.client = ApplicationBuilder() \
            .token(self.config.TOKEN) \
            .base_url(self.config.BASE_URL) \
            .base_file_url(self.config.BASE_FILE_URL) \
            .build() \
        
        enablelogging(level=logging.INFO, color=True)
        self.loop = asyncio.get_event_loop()

    @staticmethod
    def log(
        message: Optional[str] = None,
        level=logging.INFO,
        logger: logging.Logger = logging.getLogger(__module__),
    ) -> Optional[str]:
        logger.log(level, message or traceback.format_exc())
        return message or traceback.format_exc()

    def load_modules(self):
        try:
            module_loader = Loader('./kiyo_plugins/internal/')  # Create a Loader instance
            loaded_modules = module_loader.import_module(log=True)  # Import all modules
        except Exception as e:
            self.log(f"Error loading modules: {e}", level=logging.ERROR)
            return

        Attributes.IMPORTED = {
            getattr(m, "__mod_name__", m.__name__.capitalize()): m
            for m in loaded_modules if inspect.ismodule(m)
        }
        if len(Attributes.IMPORTED) != len(loaded_modules):
            self.log("Some loaded items are not modules.", level=logging.WARNING)

        for attr in ['get_help', '__migrate__', '__stats__', '__user_info__',
                     '__import_data__', '__export_data__', '__chat_settings__', '__user_settings__']:
            setattr(
                Attributes, attr.upper(),
                {name.lower(): m for name, m in Attributes.IMPORTED.items() if hasattr(m, attr)}
            )

    def setup_localization(self):
        """
        Check if localization files are available in the 'locales' directory.
        If not found, use the default language (English) and reload strings.
        """
        locales_dir = pathlib.Path("./kiyo/locales")
    
        if not locales_dir.exists() or not list(locales_dir.glob("*")):
            self.log("Localization files not found!", level=logging.ERROR)
            self.log("Using the default language - English.")
            reload_strings()
        else:
            self.log("Localization setup complete!")    
        
    async def initialize_bot(self):
        try:
            self.log(
                'Starting rKiyo - By Aruoto (t.me/customuser) - https://github.com/Aruoto', level=logging.INFO
            )
            await self.client.initialize()
        except Exception as e:
            self.log(f'You got an error: {e}', level=logging.CRITICAL)
        bot_firstname = self.client.bot.first_name
        self.log(f'Logged in bot as : {bot_firstname}')
        self.setup_localization()
        self.load_modules()
    
    def run_in_loop(self, func):
        self.loop.run_until_complete(func)
        
    def run(self):
        self.run_in_loop(self.initialize_bot())
        self.log('rKiyo Started Using Long Polling.')
        return self.client.run_polling(timeout=15, drop_pending_updates=True)
        

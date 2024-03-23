import time

from . import (
    db,
    application,
    LOGS,
    start_time,
    config,
)

from Main.langs import setup_localization
from Main.startup.helpers import load_all_modules
    
def main():
    setup_localization()
    load_all_modules()
    LOGS.info('[KIYO] Started Using long polling.')
    application.run_polling()

if __name__ == '__main__':
    main()

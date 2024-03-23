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

async def error_handler(update, context):
    """Log the error."""
    LOGS.error(msg="Exception while handling an update:", exc_info=context.error)


def main():
    setup_localization()
    load_all_modules()
    LOGS.info('[KIYO] Started Using long polling.')
    application.add_error_handler(error_handler)
    application.run_polling()

if __name__ == '__main__':
    main()

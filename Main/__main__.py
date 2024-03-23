from . import (
    db,
    application,
    LOGS,
    start_time,
    config,
)
from Main.langs import setup_localization

def main():
    setup_localization()
    LOGS.info('[KIYO] Started Using long polling.')
    application.run_polling()

if __name__ == '__main__':
    main()

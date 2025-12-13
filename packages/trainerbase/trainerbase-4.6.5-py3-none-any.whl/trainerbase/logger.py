import sys
import threading
from logging import ERROR, getLogger
from logging.config import dictConfig

from trainerbase.config import CONFIG_FILE, config


if config.logging is None:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] <%(levelname)s> %(funcName)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }
    using_default_config = True
else:
    logging_config = config.logging
    using_default_config = False

dictConfig(logging_config)
getLogger("comtypes").setLevel(ERROR)

logger = getLogger("TrainerBase")
if using_default_config:
    logger.debug(f"No logging config in {CONFIG_FILE}! Using default one.")


def _exception_hook(*args):
    if len(args) == 3:
        exc_type, exc_value, exc_traceback = args
    else:
        except_hook_args = args[0]
        exc_type = except_hook_args.exc_type
        exc_value = except_hook_args.exc_value
        exc_traceback = except_hook_args.exc_traceback

    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


if config.hook_exceptions:
    sys.excepthook = _exception_hook
    threading.excepthook = _exception_hook

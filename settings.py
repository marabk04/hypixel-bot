import os
import pathlib
import logging
from dotenv import load_dotenv
from logging.config import dictConfig


load_dotenv()



DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
HYPIXEL_API_KEY =  os.getenv("HYPIXEL_API_KEY")
BASE_DIR = pathlib.Path(__file__).parent


CMDS_DIR = BASE_DIR/ "cmds"
COGS_DIR = BASE_DIR/ "cogs"
MODERATION_DIR = COGS_DIR/ "moderation"
FUN_DIR = COGS_DIR/ "fun"
SKYBLOCK_DIR = COGS_DIR/ "Skyblock"
RANDOM_DIR = COGS_DIR/ "random"

LOGGING_CONFIG = {

    "version": 1,
    "disabled_exising_Loggers": False,
    "formatters":{
        "verbose":{
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard":{
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        },
    },

    "handlers":{
        "console":{
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "console2":{
            'level': "WARNING",
            'class': "logging.StreamHandler",
            'formatter': "standard",
        },
        'file':{
            'level': "INFO",
            'class': "logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "w",
            'formatter': "verbose",
        },
    },

    "loggers":{
        "bot":{
            'handlers': ['console'],
            "level": "INFO",
            "propagate": False,
        },
          "discord":{
            'handlers': ['console2', "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


dictConfig(LOGGING_CONFIG)




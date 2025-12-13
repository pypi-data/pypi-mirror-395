import uuid
from dioritorm.core.config_manager import ConfigManager

config = ConfigManager().load()

NAMESPACE = uuid.UUID("511a7e14-0626-44c9-962c-4fc4c3feedbd")
NULLLINK = "00000000-0000-0000-0000-000000000000"

#Database Settings
DATABASE_TYPE = config["db"]["type"]
DATABASE_NAME = config["db"]["name"]
DATABASE_USER = config["db"]["user"]
DATABASE_PWD  = config["db"]["pwd"]
DATABASE_PATH = config["db"]["host"]
'''DATABASE_TYPE = "mysql"
DATABASE_NAME = "sync"
DATABASE_USER = "root"
DATABASE_PWD  = "9944"
DATABASE_PATH = "127.0.0.1"'''

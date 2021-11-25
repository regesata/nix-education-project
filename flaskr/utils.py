"""Additional functions for application"""
import logging
from logging.handlers import RotatingFileHandler



class AppConfig:
    #SQLALCHEMY_DATABASE_URI = "sqlite:///model.db"
    SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://postgres:postgres_password@db_postgres/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "too secret"
    LOGFILE = "logs/main.logs"


MAX_BYTES = 1000000
B_COUNT = 3
INVALID_DATA_JSON = {"error": "Data in user request is not valid"}
INVALID_DATA_STR = "Data in user request is not valid"
LOGGER_NAME = "main_logger"




def get_logger_fact(name):

    logger = logging.getLogger(name)

    handler_c = logging.StreamHandler()
    ch = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - Func: %(funcName)s '
                           '- in: %(lineno)d - %(message)s', "[%d/%b/%Y %H:%M:%S]")
    handler_c.setFormatter(ch)
    handler_f = RotatingFileHandler(AppConfig.LOGFILE, maxBytes=MAX_BYTES, backupCount=3)
    handler_f.setFormatter(ch)
    logger.addHandler(handler_f)
    logger.addHandler(handler_c)
    logger.setLevel(logging.INFO)
    return logger





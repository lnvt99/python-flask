import logging
import sys
# from config import configs
# from datetime import datetime
import os


class Logger:
    """Class handle output log"""

    def __init__(self):
        """Constructor"""
        pass

    def setup_logging(self):
        """Set up logging

        Returns:
            Logger: logger instance
        """
        # Log in Cloudwatch
        logger = logging.getLogger()
        for h in logger.handlers:
            logger.removeHandler(h)

        h = logging.StreamHandler(sys.stdout)
        # use whatever format you want here
        formatter = "%(levelname)s - %(asctime)s - %(message)s - %(funcName)s "
        h.setFormatter(logging.Formatter(formatter))
        logger.addHandler(h)

        # if configs.co.Environment == configs.Environment.STAG:
        #     current_date = datetime.now().date()
        #     date = str(
        #         "{current_date}".format(
        #             current_date=datetime.strftime(current_date, "%Y-%m-%d")
        #         )
        #     )
        #     file_name = "log/data-admin-log" + "-" + date + ".log"
        #     os.makedirs(os.path.dirname(file_name), exist_ok=True)
        #     file_handler = logging.FileHandler(file_name, encoding="utf-8")
        #     file_handler.setLevel(logging.DEBUG)
        #     file_handler.setFormatter(logging.Formatter(formatter))
        #     logger.addHandler(file_handler)

        # logger.setLevel(configs.co.LOG_LEVEL)

        return logger

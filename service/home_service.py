import traceback
import sys
import json

from common.dal import DAL
from config.retcode import RetCode
from common.logger import Logger

def get_data():
    _logger = Logger()
    logger = _logger.setup_logging()
    try:
        # Open DB connection
        dal = DAL(True)

        query = "SELECT * FROM tbl_a"
        data = dal.execute_query(query)

        return data
    except Exception as err:
        tb = sys.exc_info()[2]
        err_message = err.with_traceback(tb)
        logger.error(err_message)
        logger.error(traceback.format_exc())
        # Output Message
        return {
            "code": RetCode.RET_500.value,
            "data": [],
            "message": err_message.args[0],
        }


import json
import sys
import traceback
import os

from common.logger import Logger
from common.ret import Ret
from config.retcode import RetCode


def catchEx(logger: Logger, err: Exception):
    """Catch exception

    Args:
        logger (Logger): Logger
        err (Exception): exception

    Returns:
        Ret: ret result
    """
    tb = sys.exc_info()[2]
    err_message = err.with_traceback(tb)
    logger.error(err_message)
    logger.error(traceback.format_exc())

    return Ret(RetCode.RET_500.value, None, err_message.args[0])


def load_json_file(file_path, encoding="utf-8_sig"):
    """Get json data from file path

    Args:
        file_path ([str]): json file path
        encoding([str]): encoding

    Returns:
        [dict]: data
    """
    cur_path = os.getcwd()
    file_path_temp = f"{cur_path}\\dummy\\{file_path}"
    with open(file_path_temp, "r", encoding=encoding) as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        return data


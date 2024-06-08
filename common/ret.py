from config.retcode import RetCode

class Ret:
    """Result handle response result"""

    def __init__(
        self, code: RetCode = RetCode.RET_200, data: any = None, message: str = ""
    ) -> None:
        """Constructor

        Args:
            code (RetCode, optional): status code. Defaults to RetCode.RET_200.
            data (any, optional): data. Defaults to None.
            message (str, optional): message. Defaults to "".
        """
        self.code = code.value
        self.data = data
        self.message = message

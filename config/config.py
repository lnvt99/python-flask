from enum import Enum, unique


@unique
class RetCode(Enum):
    """Enum api response result"""

    RET_200 = 200
    # Accepted
    RET_202 = 202
    RET_400 = 400
    RET_404 = 404
    RET_500 = 500
    RET_503 = 503

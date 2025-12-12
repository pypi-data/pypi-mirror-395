# This file is generated. Do not modify by hand.
from enum import Enum


class ReplyCode(Enum):
    """
    Named constants for all Zaber Binary protocol reply-only command codes.
    """

    MOVE_TRACKING = 8
    LIMIT_ACTIVE = 9
    MANUAL_MOVE_TRACKING = 10
    MANUAL_MOVE = 11
    SLIP_TRACKING = 12
    UNEXPECTED_POSITION = 13
    ERROR = 255

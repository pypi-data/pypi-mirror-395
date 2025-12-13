"""
Created by Jakub Domaszewicz on 17.12.2023.
"""

from enum import IntEnum

class WearState(IntEnum):
    """
    Wear state of the device.
    """
    PLACED_PROPERLY = 0
    PLACED_UPSIDE_DOWN = 1
    LOOSE = 2
    DETACHED = 3
    UNKNOWN = 4
    UNSETTLED = 5

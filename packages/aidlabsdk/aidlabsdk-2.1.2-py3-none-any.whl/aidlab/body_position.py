"""
Created by Jakub Domaszewicz on 17.12.2023.
"""

from enum import IntEnum

class BodyPosition(IntEnum):
    """
    Enumerates the possible positions of a body when lying on a bed with a device. 
    Each value represents a specific orientation of the body relative to the bed.

    Attributes:
        UNKNOWN (0): The body's position is unknown or not recognized.
        PRONE (1): The body is lying face down on its stomach.
        SUPINE (2): The body is lying face up on its back.
        LEFT_SIDE (3): The body is lying on its left side.
        RIGHT_SIDE (4): The body is lying on its right side.
    """
    UNKNOWN = 0
    PRONE = 1
    SUPINE = 2
    LEFT_SIDE = 3
    RIGHT_SIDE = 4

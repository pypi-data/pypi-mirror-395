"""
Created by Jakub Domaszewicz on 16.03.2024.
"""

from enum import IntEnum

class ActivityType(IntEnum):
    """
    Enumerates the possible types of activities that can be recognized by the device.

    Attributes:
        UNKNOWN (0): The activity is unknown or not recognized.
        AUTOMOTIVE (1): The user is in a vehicle, such as a car, bus, or train.
        WALKING (2): The user is walking.
        RUNNING (4): The user is running.
        CYCLING (8): The user is cycling.
        STILL (16): The user is still, i.e. not moving.
        
    """
    UNKNOWN = 0
    AUTOMOTIVE = 1
    WALKING = 2
    RUNNING = 4
    CYCLING = 8
    STILL = 16

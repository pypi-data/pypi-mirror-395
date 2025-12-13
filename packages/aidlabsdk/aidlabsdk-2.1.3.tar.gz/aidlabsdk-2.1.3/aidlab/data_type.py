"""
Created by Szymon Gesicki on 07.11.2021.
"""

from enum import IntEnum

class DataType(IntEnum):
    """
    Data types that can be received from Aidlab and Aidmed One.
    See the documentation to learn more about each data type.
    """
    ECG = 0
    RESPIRATION = 1
    SKIN_TEMPERATURE = 2
    MOTION = 3
    # BATTERY = 4 # Enabled by default since SDK 1.6.0
    ACTIVITY = 5
    ORIENTATION = 6
    STEPS = 7
    HEART_RATE = 8
    # HEALTH_THERMOMETER = 9 # No longer in use. Use SKIN_TEMPERATURE instead.
    SOUND_VOLUME = 10
    RR = 11
    PRESSURE = 12 # Supported since Firmware 3.0.0. No longer available as characteristic.
    SOUND_FEATURES = 13
    RESPIRATION_RATE = 14
    BODY_POSITION = 15
    EDA = 16
    GPS = 17

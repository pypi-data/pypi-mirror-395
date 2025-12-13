
from typing import List

from .body_position import BodyPosition
from .wear_state import WearState
from .device import Device
from .activity_type import ActivityType

class DeviceDelegate:
    """The DeviceDelegate protocol defines methods that you use to receive events"""
    
    async def did_connect(self, device: Device):
        """Called when a connection to an device was established.
        """

    def did_disconnect(self, device: Device):
        """Called when a connection to an device was lost.
        """

    def did_fail_to_connect(self, device: Device, error: str):
        """Called when a connection to an device failed.
        """

    def did_receive_error(self, device: Device, error: str):
        """Called when an error occurred.
        """

    def did_receive_ecg(self, device: Device, timestamp: int, value: float):
        """Called when a new ECG samples was received.
        """

    def did_receive_respiration(self, device: Device, timestamp: int, value: float):
        """Called when a new respiration samples was received.
        """

    def did_receive_respiration_rate(self, device: Device, timestamp: int, value: int):
        """Called when respiration rate is available.
        """

    def did_receive_battery_level(self, device: Device, state_of_charge: int):
        """If battery monitoring is enabled, this event will notify about Aidlab's
           state of charge. You never want Aidlab to run low on battery, as it can
           lead to it's sudden turn off. Use this event to inform your users about
           Aidlab's low energy.
        """

    def did_receive_skin_temperature(self, device: Device, timestamp: int, value: float):
        """Called when a skin temperature was received.
        """

    def did_receive_accelerometer(self, device: Device, timestamp: int, ax: float, ay: float, az: float):
        """Called when new accelerometer data were received.
        """

    def did_receive_gyroscope(self, device: Device, timestamp: int, gx: float, gy: float, gz: float):
        """Called when new gyroscope data were received.
        """

    def did_receive_magnetometer(self,
                                 device: Device,
                                 timestamp: int, mx: float, my: float, mz: float):
        """Called when new magnetometer data were received.
        """

    def did_receive_orientation(self, device: Device, timestamp: int, roll: float, pitch: float, yaw: float):
        """Called when received orientation, represented in RPY angles.
        """

    def did_receive_body_position(self, device: Device, timestamp: int, body_position: BodyPosition):
        """Called when body position has changed.
        """

    def did_receive_quaternion(self, device: Device, timestamp: int, qw: float, qx: float, qy: float, qz: float):
        """Called when new quaternion data were received.
        """

    def did_receive_activity(self, device: Device, timestamp: int, activity: ActivityType):
        """Called when activity data were received.
        """

    def did_receive_steps(self, device: Device, timestamp: int, steps: int):
        """Called when total steps did change.
        """

    def did_receive_heart_rate(self, device: Device, timestamp: int, heart_rate: int):
        """Called when a heart rate did change.
        """

    def did_receive_rr(self, device: Device, timestamp: int, rr: int):
        """Called when a rr did change.
        """

    def wear_state_did_change(self, device: Device, wear_state: WearState):
        """Called when a significant change of wear state did occur. You can use
           that information to make decisions when to start processing data, or
           display short user guide on how to wear Aidlab in your app.
        """

    def did_receive_pressure(self, device: Device, timestamp: int, value: int):
        """Called when a pressure data were received.
        """

    def pressure_wear_state_did_change(self, device: Device, wear_state: WearState):
        """Called when a significant change of wear state did occur. You can use
        """

    def did_receive_sound_volume(self, device: Device, timestamp: int, sound_volume: int):
        """Called when a sound volume data were received.
        """

    def did_receive_signal_quality(self, device: Device, timestamp: int, value: int):
        """Called when a signal quality data were received.
        """

    def did_receive_eda(self, device: Device, timestamp: int, conductance: float):
        """Called when electrodermal activity data were received.

        Args:
            device: The device that sent the data
            timestamp: Unix timestamp in milliseconds
            conductance: Skin conductance in microSiemens (µS)
        """

    def did_receive_gps(self,
                        device: Device,
                        timestamp: int,
                        latitude: float,
                        longitude: float,
                        altitude: float,
                        speed: float,
                        heading: float,
                        hdop: float):
        """Called when GPS data were received.

        Args:
            device: The device that sent the data
            timestamp: Unix timestamp in milliseconds
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            altitude: Altitude in meters
            speed: Speed in km/h
            heading: Heading/course in degrees
            hdop: Horizontal dilution of precision (accuracy indicator)
        """

    def did_detect_exercise(self, device: Device, exercise: str):
        """Called when exercise is detected.
        """

    def did_receive_payload(self, device: Device, process: str, payload: bytes):
        """Called when a payload was received from a process (raw bytes)."""

    def did_detect_user_event(self, device: Device, timestamp: int):
        """Called when user event is detected.
        """

    # Synchronization callbacks

    def sync_state_did_change(self, device: Device, sync_state: str):
        """
        Called when the synchronization state of the device changes.

        :param device: The device instance.
        :param sync_state: The new synchronization state.
        """

    def did_receive_unsynchronized_size(self,
                                        device: Device,
                                        unsynchronized_size: int,
                                        sync_bytes_per_second: float):
        """
        Called when the size of unsynchronized data is received.

        :param device: The device instance.
        :param unsynchronized_size: The size of the unsynchronized data.
        :param sync_bytes_per_second: Data synchronization speed in bytes per second.
        """

    def did_receive_past_ecg(self, device: Device, timestamp: int, value: float):
        """
        Called when past ECG data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the ECG data.
        :param value: ECG data value.
        """

    def did_receive_past_respiration(self, device: Device, timestamp: int, value: float):
        """
        Called when past respiration data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the respiration data.
        :param value: Respiration data.
        """

    def did_receive_past_respiration_rate(self, device: Device, timestamp: int, value: int):
        """
        Called when past respiration rate data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the respiration rate data.
        :param value: The respiration rate value.
        """

    def did_receive_past_skin_temperature(self, device: Device, timestamp: int, value: float):
        """
        Called when past skin temperature data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the skin temperature data.
        :param value: The skin temperature value in degrees Celsius or Fahrenheit.
        """

    def did_receive_past_accelerometer(self, device: Device, timestamp: int, ax: float, ay: float, az: float):
        """
        Called when past accelerometer data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the accelerometer data.
        :param ax: The X-axis acceleration value.
        :param ay: The Y-axis acceleration value.
        :param az: The Z-axis acceleration value.
        """

    def did_receive_past_gyroscope(self, device: Device, timestamp: int, gx: float, gy: float, gz: float):
        """
        Called when past gyroscope data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the gyroscope data.
        :param gx: The X-axis gyroscope value.
        :param gy: The Y-axis gyroscope value.
        :param gz: The Z-axis gyroscope value.
        """

    def did_receive_past_magnetometer(self, device: Device, timestamp: int, mx: float, my: float, mz: float):
        """
        Called when past magnetometer data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the magnetometer data.
        :param mx: The X-axis magnetometer value.
        :param my: The Y-axis magnetometer value.
        :param mz: The Z-axis magnetometer value.
        """

    def did_receive_past_orientation(self, device: Device, timestamp: int, roll: float, pitch: float, yaw: float):
        """
        Called when past orientation data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the orientation data.
        :param roll: The roll value of the orientation.
        :param pitch: The pitch value of the orientation.
        :param yaw: The yaw value of the orientation.
        """

    def did_receive_past_body_position(self, device: Device, timestamp: int, body_position: str):
        """
        Called when past body position data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the body position data.
        :param body_position: The body position value as a string.
        """

    def did_receive_past_quaternion(self,
                                    device: Device,
                                    timestamp: int,
                                    qw: float, qx: float, qy: float, qz: float):
        """
        Called when past quaternion data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the quaternion data.
        :param qw: The W component of the quaternion.
        :param qx: The X component of the quaternion.
        :param qy: The Y component of the quaternion.
        :param qz: The Z component of the quaternion.
        """

    def did_receive_past_activity(self, device: Device, timestamp: int, activity: str):
        """
        Called when past activity data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the activity data.
        :param activity: The activity value as a string.
        """

    def did_receive_past_steps(self, device: Device, timestamp: int, steps: int):
        """
        Called when past step count data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the step count data.
        :param steps: The number of steps taken.
        """

    def did_receive_past_heart_rate(self, device: Device, timestamp: int, heart_rate: int):
        """
        Called when past heart rate data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the heart rate data.
        :param heart_rate: The heart rate value in beats per minute.
        """

    def did_receive_past_rr(self, device: Device, timestamp: int, rr: int):
        """
        Called when past RR interval data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the RR interval data.
        :param rr: The interval value between consecutive heart beats.
        """

    def did_receive_past_pressure(self, device: Device, timestamp: int, value: int):
        """
        Called when past pressure data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the pressure data.
        :param value: pressure value.
        """

    def did_receive_past_sound_volume(self, device: Device, timestamp: int, sound_volume: int):
        """
        Called when past sound volume data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the sound volume data.
        :param sound_volume: The sound volume level in decibels.
        """

    def did_receive_past_user_event(self, device: Device, timestamp: int):
        """
        Called when a past user event is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp when the user event occurred.
        """

    def did_receive_past_signal_quality(self, device: Device, timestamp: int, value: int):
        """
        Called when past signal quality data is received from the device.

        :param device: The device instance.
        :param timestamp: The timestamp of the signal quality data.
        :param value: The value indicating the quality of the signal.
        """

    def did_receive_past_eda(self,
                             device: Device,
                             timestamp: int,
                             conductance: float):
        """Called when past electrodermal activity data is received.

        Args:
            device: The device that sent the data
            timestamp: Unix timestamp in milliseconds
            conductance: Skin conductance in microSiemens (µS)
        """

    def did_receive_past_gps(self,
                             device: Device,
                             timestamp: int,
                             latitude: float,
                             longitude: float,
                             altitude: float,
                             speed: float,
                             heading: float,
                             hdop: float):
        """Called when past GPS data is received.

        Args:
            device: The device that sent the data
            timestamp: Unix timestamp in milliseconds
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            altitude: Altitude in meters
            speed: Speed in km/h
            heading: Heading/course in degrees
            hdop: Horizontal dilution of precision (accuracy indicator)
        """

"""
Part of the Aidlab Python SDK, providing the core functionality for scanning compatible devices.

To customise logging, configure the standard Python logging system in your
application, for example:

    logging.getLogger("aidlab.aidlab_manager").setLevel(logging.INFO)

Created by Szymon Gesicki on 09.05.2020.
"""

import logging
from bleak import BleakScanner
from .device import Device

logger = logging.getLogger(__name__)


class AidlabManager:
    """
    The central class of the Aidlab SDK for scanning compatible devices.
    """

    async def scan(self, timeout: int = 10) -> list[Device]:
        """
        Scans for compatible devices.

        :param timeout: The time in seconds to scan for devices.
        """

        logger.info("Scanning for devices (timeout: %d seconds)...", timeout)

        devices = await BleakScanner.discover(timeout)

        # Container for compatible MAC addresses
        compatible_devices: list[Device] = []

        for device in devices:
            # Name "Aidlab" is applicable for both Aidlab and Aidmed One
            if (device.name == "Aidlab 2" or device.name == "Aidlab") and device.address:
                compatible_devices.append(Device(device))

        logger.info("Finished scanning. Found %d devices.", len(compatible_devices))

        return compatible_devices

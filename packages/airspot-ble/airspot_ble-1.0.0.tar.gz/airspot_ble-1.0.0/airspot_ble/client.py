"""Airspot BLE client for parsing advertisements."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .const import ADV_DATA_LENGTH, MANUFACTURER_ID

if TYPE_CHECKING:
    from bleak.backends.device import BLEDevice


class AirspotError(Exception):
    """Base exception for Airspot BLE errors."""


@dataclass
class AirspotAdvertisement:
    """
    Airspot advertisement data parser.

    Parses manufacturer-specific data from BLE advertisements.
    Similar to Aranet4Advertisement in aranet4 library.
    """

    device: BLEDevice = None
    co2: int | None = None
    battery_level: int | None = None
    reading_mode: str | None = None
    charging: bool = False
    low_battery: bool = False
    sensor_error: bool = False
    calibration_active: bool = False
    sequence: int | None = None
    rssi: int | None = None

    def __init__(self, device=None, ad_data=None):
        """
        Parse Airspot advertisement data.

        Args:
            device: BLEDevice object from bleak
            ad_data: AdvertisementData object from bleak

        Example:
            >>> from airspot_ble.client import AirspotAdvertisement
            >>> adv = AirspotAdvertisement(device, advertisement_data)
            >>> print(f"CO2: {adv.co2} ppm, Battery: {adv.battery_level}%")
        """
        self.device = device

        if device and ad_data:
            # Check if manufacturer data exists
            has_manufacturer_data = MANUFACTURER_ID in ad_data.manufacturer_data
            self.rssi = getattr(ad_data, "rssi", None)

            if has_manufacturer_data:
                # Extract raw bytes
                raw_bytes = bytearray(ad_data.manufacturer_data[MANUFACTURER_ID])

                # Verify data length (6 bytes expected)
                if len(raw_bytes) < ADV_DATA_LENGTH:
                    # Invalid manufacturer data - too short
                    return

                # Parse CO2 value (bytes 0-1, big-endian)
                self.co2 = (raw_bytes[0] << 8) | raw_bytes[1]

                # Parse battery level (byte 2)
                self.battery_level = raw_bytes[2]

                # Parse flags byte (byte 3)
                flags = raw_bytes[3]

                # Reading mode (bits 0-1)
                reading_modes = ["On-Demand", "Low", "Mid", "High"]
                reading_mode_index = flags & 0x03
                self.reading_mode = (
                    reading_modes[reading_mode_index]
                    if reading_mode_index < len(reading_modes)
                    else None
                )

                # Charging (bit 2)
                self.charging = bool(flags & 0x04)

                # Low battery (bit 3)
                self.low_battery = bool(flags & 0x08)

                # Sensor error (bit 4)
                self.sensor_error = bool(flags & 0x10)

                # Calibration active (bit 5)
                self.calibration_active = bool(flags & 0x20)

                # Parse sequence number (bytes 4-5, big-endian)
                self.sequence = (raw_bytes[4] << 8) | raw_bytes[5]

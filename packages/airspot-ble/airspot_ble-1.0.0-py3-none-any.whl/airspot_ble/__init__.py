"""Python library for interacting with Airspot devices via Bluetooth Low Energy (BLE)."""

from .client import AirspotAdvertisement, AirspotError
from .const import (
    ADV_DATA_LENGTH,
    MANUFACTURER_ID,
    NOTIFY_CHAR_UUID,
    SERVICE_UUID,
    WRITE_CHAR_UUID,
)

__all__ = [
    "AirspotAdvertisement",
    "AirspotError",
    "ADV_DATA_LENGTH",
    "MANUFACTURER_ID",
    "NOTIFY_CHAR_UUID",
    "SERVICE_UUID",
    "WRITE_CHAR_UUID",
]
__version__ = "0.1.0"


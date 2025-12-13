"""Tests for airspot_ble.client module."""

from unittest.mock import MagicMock

import pytest

from airspot_ble.client import AirspotAdvertisement
from airspot_ble.const import (
    ADV_DATA_LENGTH,
    MANUFACTURER_ID,
    SERVICE_UUID,
)


def test_airspot_constants():
    """Test Airspot constants."""
    assert MANUFACTURER_ID == 0xFFFF
    assert SERVICE_UUID == "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
    assert ADV_DATA_LENGTH == 6


def test_airspot_advertisement_empty():
    """Test AirspotAdvertisement with no data."""
    adv = AirspotAdvertisement()
    assert adv.device is None
    assert adv.co2 is None
    assert adv.battery_level is None


def test_airspot_advertisement_parse():
    """Test parsing valid advertisement data."""
    # Mock device
    device = MagicMock()
    device.address = "AA:BB:CC:DD:EE:FF"
    device.name = "Airspot-12345"

    # Mock advertisement data
    ad_data = MagicMock()
    ad_data.manufacturer_data = {
        0xFFFF: bytearray([0x01, 0xC2, 0x50, 0x00, 0x04, 0xD2])  # CO2=450, Battery=80, Flags=0x00, Seq=1234
    }
    ad_data.rssi = -75

    adv = AirspotAdvertisement(device, ad_data)

    assert adv.device == device
    assert adv.co2 == 450  # 0x01C2 = 450
    assert adv.battery_level == 80  # 0x50 = 80
    assert adv.reading_mode == "On-Demand"  # flags & 0x03 = 0
    assert adv.charging is False
    assert adv.low_battery is False
    assert adv.sensor_error is False
    assert adv.calibration_active is False
    assert adv.sequence == 1234  # 0x04D2 = 1234
    assert adv.rssi == -75


def test_airspot_advertisement_flags():
    """Test parsing flags byte."""
    device = MagicMock()
    ad_data = MagicMock()
    
    # Test all flags set: High mode (11), Charging, Low battery, Error, Calibration
    # Flags = 0b00111111 = 0x3F
    ad_data.manufacturer_data = {
        0xFFFF: bytearray([0x04, 0xB0, 0x0F, 0x3F, 0x00, 0x01])  # CO2=1200, Battery=15, Flags=0x3F
    }
    ad_data.rssi = -80

    adv = AirspotAdvertisement(device, ad_data)

    assert adv.reading_mode == "High"  # bits 0-1 = 11
    assert adv.charging is True  # bit 2 = 1
    assert adv.low_battery is True  # bit 3 = 1
    assert adv.sensor_error is True  # bit 4 = 1
    assert adv.calibration_active is True  # bit 5 = 1


def test_airspot_advertisement_short_data():
    """Test handling of too-short manufacturer data."""
    device = MagicMock()
    ad_data = MagicMock()
    ad_data.manufacturer_data = {
        0xFFFF: bytearray([0x01, 0xC2, 0x50])  # Only 3 bytes, need 6
    }

    adv = AirspotAdvertisement(device, ad_data)

    # Should not parse anything if data is too short
    assert adv.co2 is None
    assert adv.battery_level is None


def test_airspot_advertisement_no_manufacturer_data():
    """Test handling of missing manufacturer data."""
    device = MagicMock()
    ad_data = MagicMock()
    ad_data.manufacturer_data = {}  # No Airspot manufacturer data

    adv = AirspotAdvertisement(device, ad_data)

    assert adv.co2 is None
    assert adv.battery_level is None


def test_airspot_advertisement_reading_modes():
    """Test all reading mode values."""
    device = MagicMock()
    ad_data = MagicMock()

    modes = ["On-Demand", "Low", "Mid", "High"]
    
    for mode_index, expected_mode in enumerate(modes):
        flags = mode_index & 0x03  # Only bits 0-1
        ad_data.manufacturer_data = {
            0xFFFF: bytearray([0x01, 0xC2, 0x50, flags, 0x00, 0x01])
        }
        
        adv = AirspotAdvertisement(device, ad_data)
        assert adv.reading_mode == expected_mode


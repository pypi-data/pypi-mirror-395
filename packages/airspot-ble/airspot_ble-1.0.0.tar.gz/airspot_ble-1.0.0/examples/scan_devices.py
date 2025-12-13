#!/usr/bin/env python3
"""Example script to scan for Airspot devices."""

import asyncio

from bleak import BleakScanner

from airspot_ble.client import AirspotAdvertisement


async def scan_for_airspot_devices(duration: int = 10):
    """Scan for Airspot devices and print their data."""
    print(f"Scanning for Airspot devices for {duration} seconds...")
    print("-" * 60)

    scanner = BleakScanner()
    devices = await scanner.discover(timeout=duration)

    found_devices = []

    for device, advertisement_data in devices:
        adv = AirspotAdvertisement(device, advertisement_data)

        if adv.co2 is not None:
            found_devices.append((device, adv))

    if not found_devices:
        print("No Airspot devices found.")
        return

    print(f"\nFound {len(found_devices)} Airspot device(s):\n")

    for device, adv in found_devices:
        print(f"Device: {device.name or 'Unknown'}")
        print(f"  Address: {device.address}")
        print(f"  RSSI: {adv.rssi} dBm")
        print(f"  CO2: {adv.co2} ppm")
        print(f"  Battery: {adv.battery_level}%")
        print(f"  Reading Mode: {adv.reading_mode}")
        print(f"  Charging: {'Yes' if adv.charging else 'No'}")
        print(f"  Low Battery: {'Yes' if adv.low_battery else 'No'}")
        print(f"  Sensor Error: {'Yes' if adv.sensor_error else 'No'}")
        print(f"  Calibration Active: {'Yes' if adv.calibration_active else 'No'}")
        print(f"  Sequence: {adv.sequence}")
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(scan_for_airspot_devices())


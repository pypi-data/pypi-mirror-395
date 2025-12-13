"""Constants for Airspot BLE devices."""

# Manufacturer ID for Airspot devices
# 0xFFFF is used for testing - update to official Bluetooth SIG ID when available
MANUFACTURER_ID = 0xFFFF

# BLE Service UUIDs
SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
WRITE_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
NOTIFY_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# Advertisement data format: 6 bytes
# Bytes 0-1: CO2 value (big-endian, 0-65535 ppm)
# Byte 2: Battery level (0-100%)
# Byte 3: Flags byte
# Bytes 4-5: Sequence number (big-endian, increments)
ADV_DATA_LENGTH = 6


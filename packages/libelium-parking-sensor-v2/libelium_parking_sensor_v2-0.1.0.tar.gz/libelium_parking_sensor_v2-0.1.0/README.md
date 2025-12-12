# Libelium Parking Sensor V2 Decoder

A Python library for decoding Libelium Smart Parking Sensor V2 payloads.

## Installation

```bash
pip install libelium-parking-sensor-v2
```

Or with uv:

```bash
uv add libelium-parking-sensor-v2
```

## Usage

```python
from libelium_parking_sensor_v2 import decode
```

### Supported Input Formats

The decoder accepts three input formats:

#### 1. Raw Bytes

```python
from libelium_parking_sensor_v2 import decode

data = bytes([0x80, 0x0A, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09])
result = decode(data)

print(result.header.status)      # Status.OCCUPIED
print(result.header.sequence)    # 10
print(result.payload)            # b'\x01\x02\x03\x04\x05\x06\x07\x08\x09'
```

#### 2. Hex String

```python
from libelium_parking_sensor_v2 import decode

hex_data = "800a010203040506070809"
result = decode(hex_data)

print(result.header.status)      # Status.OCCUPIED
print(result.header.sequence)    # 10
```

#### 3. Base64 Encoded String

```python
from libelium_parking_sensor_v2 import decode

b64_data = "gAoBAgMEBQYHCAk="
result = decode(b64_data)

print(result.header.status)      # Status.OCCUPIED
print(result.header.sequence)    # 10
```

## Data Structure

The decoder returns a `SensorData` object with the following structure:

```python
SensorData(
    frame_type=FrameType,      # Frame type enum
    header=FrameHeader(
        status=Status,         # VACANT (0) or OCCUPIED (1)
        battery_low=bool,      # True if battery is low
        frame_type=FrameType,  # Frame type enum
        sequence=int           # Sequence number (0-255)
    ),
    payload=bytes              # 9 bytes of payload data
)
```

### Frame Types

| Value | Frame Type |
|-------|------------|
| 0 | INFO |
| 1 | KEEP_ALIVE |
| 2 | CONFIG_UP |
| 3 | CONFIG_DOWN |
| 4 | START_FRAME_1 |
| 5 | START_FRAME_2 |
| 6 | RTC_SYNC |
| 7 | RTC_UPDATE |

### Status Values

| Value | Status |
|-------|--------|
| 0 | VACANT |
| 1 | OCCUPIED |

## Header Byte Format

The first byte of the header encodes multiple fields:

```
Bit 7: Status (0=VACANT, 1=OCCUPIED)
Bit 6: Battery Low (0=OK, 1=Low)
Bits 0-2: Frame Type (0-7)
```

The second byte contains the sequence number (0-255).

## Complete Example

```python
from libelium_parking_sensor_v2 import decode, FrameType, Status

# Decode sensor data
data = bytes([0xC1, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
result = decode(data)

# Check parking status
if result.header.status == Status.OCCUPIED:
    print("Parking spot is occupied")
else:
    print("Parking spot is vacant")

# Check battery status
if result.header.battery_low:
    print("Warning: Battery is low")

# Check frame type
if result.frame_type == FrameType.KEEP_ALIVE:
    print("Received keep-alive frame")

# Get sequence number
print(f"Sequence: {result.header.sequence}")

# Access raw payload
print(f"Payload: {result.payload.hex()}")
```

## Error Handling

The decoder raises `ValueError` for invalid input:

```python
from libelium_parking_sensor_v2 import decode

try:
    # Invalid: data must be exactly 11 bytes
    decode(bytes([0x00, 0x01]))
except ValueError as e:
    print(f"Error: {e}")  # "Invalid data length, expected 11 bytes"
```

## Development

### Running Tests

```bash
uv run pytest tests/ -v
```

## License

MIT

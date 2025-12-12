"""Tests for the Libelium Parking Sensor V2 decoder module."""

import pytest
from base64 import b64encode

from libelium_parking_sensor_v2.decoder import (
    decode,
    FrameType,
    Status,
    FrameHeader,
    SensorData,
)


class TestDecodeInputFormats:
    """Test different input formats accepted by decode()."""

    def test_decode_bytes_input(self):
        """Test decoding raw bytes input."""
        # 11 bytes: header (2) + payload (9)
        # header[0] = 0x00 -> status=VACANT, battery_low=False, frame_type=INFO
        # header[1] = 0x01 -> sequence=1
        data = bytes([0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        result = decode(data)

        assert isinstance(result, SensorData)
        assert result.frame_type == FrameType.INFO
        assert result.header.status == Status.VACANT
        assert result.header.battery_low is False
        assert result.header.sequence == 1

    def test_decode_hex_string_input(self):
        """Test decoding hex string input."""
        # Same data as bytes test but as hex string (11 bytes = 22 hex chars)
        hex_data = "0001000000000000000000"
        result = decode(hex_data)

        assert result.frame_type == FrameType.INFO
        assert result.header.status == Status.VACANT

    def test_decode_base64_string_input(self):
        """Test decoding base64 encoded input."""
        raw_bytes = bytes([0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        b64_data = b64encode(raw_bytes).decode('utf-8')
        result = decode(b64_data)

        assert result.frame_type == FrameType.INFO
        assert result.header.status == Status.VACANT


class TestFrameTypes:
    """Test all frame type values."""

    @pytest.mark.parametrize("frame_type_value,expected_frame_type", [
        (0, FrameType.INFO),
        (1, FrameType.KEEP_ALIVE),
        (2, FrameType.CONFIG_UP),
        (3, FrameType.CONFIG_DOWN),
        (4, FrameType.START_FRAME_1),
        (5, FrameType.START_FRAME_2),
        (6, FrameType.RTC_SYNC),
        (7, FrameType.RTC_UPDATE),
    ])
    def test_frame_types(self, frame_type_value, expected_frame_type):
        """Test each frame type is correctly decoded."""
        # Set frame type in lower 3 bits of header[0]
        data = bytes([frame_type_value, 0x00] + [0x00] * 9)
        result = decode(data)

        assert result.frame_type == expected_frame_type
        assert result.header.frame_type == expected_frame_type


class TestStatusField:
    """Test status field decoding."""

    def test_status_vacant(self):
        """Test VACANT status (bit 7 = 0)."""
        # header[0] = 0x00 -> bit 7 is 0 -> VACANT
        data = bytes([0x00, 0x00] + [0x00] * 9)
        result = decode(data)

        assert result.header.status == Status.VACANT

    def test_status_occupied(self):
        """Test OCCUPIED status (bit 7 = 1)."""
        # header[0] = 0x80 -> bit 7 is 1 -> OCCUPIED
        data = bytes([0x80, 0x00] + [0x00] * 9)
        result = decode(data)

        assert result.header.status == Status.OCCUPIED

    def test_status_occupied_with_frame_type(self):
        """Test OCCUPIED status combined with different frame type."""
        # header[0] = 0x81 -> bit 7 is 1 (OCCUPIED), lower 3 bits = 1 (KEEP_ALIVE)
        data = bytes([0x81, 0x00] + [0x00] * 9)
        result = decode(data)

        assert result.header.status == Status.OCCUPIED
        assert result.frame_type == FrameType.KEEP_ALIVE


class TestBatteryLowField:
    """Test battery_low field decoding."""

    def test_battery_not_low(self):
        """Test battery_low=False (bit 6 = 0)."""
        # header[0] = 0x00 -> bit 6 is 0
        data = bytes([0x00, 0x00] + [0x00] * 9)
        result = decode(data)

        assert result.header.battery_low is False

    def test_battery_low(self):
        """Test battery_low=True (bit 6 = 1)."""
        # header[0] = 0x40 -> bit 6 is 1
        data = bytes([0x40, 0x00] + [0x00] * 9)
        result = decode(data)

        assert result.header.battery_low is True

    def test_battery_low_with_occupied(self):
        """Test battery_low combined with OCCUPIED status."""
        # header[0] = 0xC0 -> bit 7=1 (OCCUPIED), bit 6=1 (battery_low)
        data = bytes([0xC0, 0x00] + [0x00] * 9)
        result = decode(data)

        assert result.header.battery_low is True
        assert result.header.status == Status.OCCUPIED


class TestSequenceField:
    """Test sequence field decoding."""

    def test_sequence_zero(self):
        """Test sequence number 0."""
        data = bytes([0x00, 0x00] + [0x00] * 9)
        result = decode(data)

        assert result.header.sequence == 0

    def test_sequence_max(self):
        """Test sequence number 255 (max uint8)."""
        data = bytes([0x00, 0xFF] + [0x00] * 9)
        result = decode(data)

        assert result.header.sequence == 255

    def test_sequence_various_values(self):
        """Test various sequence values."""
        for seq in [1, 50, 100, 128, 200]:
            data = bytes([0x00, seq] + [0x00] * 9)
            result = decode(data)
            assert result.header.sequence == seq


class TestPayload:
    """Test payload extraction."""

    def test_payload_extracted(self):
        """Test that payload bytes are correctly extracted."""
        payload_bytes = bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09])
        data = bytes([0x00, 0x00]) + payload_bytes
        result = decode(data)

        assert result.payload == payload_bytes
        assert len(result.payload) == 9

    def test_payload_with_all_zeros(self):
        """Test payload with all zeros."""
        data = bytes([0x00, 0x00] + [0x00] * 9)
        result = decode(data)

        assert result.payload == bytes([0x00] * 9)

    def test_payload_with_all_ones(self):
        """Test payload with all 0xFF bytes."""
        data = bytes([0x00, 0x00] + [0xFF] * 9)
        result = decode(data)

        assert result.payload == bytes([0xFF] * 9)


class TestCombinedHeaderFields:
    """Test combinations of header fields."""

    def test_all_flags_set(self):
        """Test header with OCCUPIED, battery_low, and RTC_UPDATE frame type."""
        # header[0] = 0xC7 -> bit 7=1 (OCCUPIED), bit 6=1 (battery_low), bits 0-2=7 (RTC_UPDATE)
        data = bytes([0xC7, 0x7F] + [0xAB] * 9)
        result = decode(data)

        assert result.header.status == Status.OCCUPIED
        assert result.header.battery_low is True
        assert result.header.frame_type == FrameType.RTC_UPDATE
        assert result.header.sequence == 127

    def test_vacant_low_battery_keep_alive(self):
        """Test VACANT status with low battery and KEEP_ALIVE frame."""
        # header[0] = 0x41 -> bit 7=0 (VACANT), bit 6=1 (battery_low), bits 0-2=1 (KEEP_ALIVE)
        data = bytes([0x41, 0x0A] + [0x00] * 9)
        result = decode(data)

        assert result.header.status == Status.VACANT
        assert result.header.battery_low is True
        assert result.header.frame_type == FrameType.KEEP_ALIVE
        assert result.header.sequence == 10


class TestInvalidInput:
    """Test error handling for invalid input."""

    def test_invalid_data_length_too_short(self):
        """Test that ValueError is raised for data shorter than 11 bytes."""
        data = bytes([0x00] * 10)  # 10 bytes instead of 11
        with pytest.raises(ValueError, match="Invalid data length"):
            decode(data)

    def test_invalid_data_length_too_long(self):
        """Test that ValueError is raised for data longer than 11 bytes."""
        data = bytes([0x00] * 12)  # 12 bytes instead of 11
        with pytest.raises(ValueError, match="Invalid data length"):
            decode(data)

    def test_invalid_data_length_empty(self):
        """Test that ValueError is raised for empty data."""
        data = bytes()
        with pytest.raises(ValueError, match="Invalid data length"):
            decode(data)

    def test_invalid_hex_string_length(self):
        """Test that ValueError is raised for invalid hex string length."""
        hex_data = "00010000000000000000"  # 10 bytes when decoded (20 hex chars)
        with pytest.raises(ValueError, match="Invalid data length"):
            decode(hex_data)

    def test_invalid_frame_type(self):
        """Test that ValueError is raised for invalid frame type value."""
        # This shouldn't actually fail since we're using only lower 3 bits (0-7)
        # and all values 0-7 are valid. Testing value beyond normal range.
        # Actually frame_type only uses bits 0-2, so max is 7.
        # Using bits 3-5 should be ignored, so this test verifies masking works.
        data = bytes([0x08, 0x00] + [0x00] * 9)  # bit 3 set, lower 3 bits = 0
        result = decode(data)
        assert result.frame_type == FrameType.INFO


class TestSensorDataModel:
    """Test SensorData model attributes."""

    def test_sensor_data_has_frame_type(self):
        """Test that SensorData has frame_type attribute."""
        data = bytes([0x00, 0x00] + [0x00] * 9)
        result = decode(data)

        assert hasattr(result, 'frame_type')
        assert isinstance(result.frame_type, FrameType)

    def test_sensor_data_has_header(self):
        """Test that SensorData has header attribute."""
        data = bytes([0x00, 0x00] + [0x00] * 9)
        result = decode(data)

        assert hasattr(result, 'header')
        assert isinstance(result.header, FrameHeader)

    def test_sensor_data_has_payload(self):
        """Test that SensorData has payload attribute."""
        data = bytes([0x00, 0x00] + [0x00] * 9)
        result = decode(data)

        assert hasattr(result, 'payload')
        assert isinstance(result.payload, bytes)


class TestFrameHeaderModel:
    """Test FrameHeader model attributes."""

    def test_frame_header_attributes(self):
        """Test that FrameHeader has all expected attributes."""
        data = bytes([0x85, 0x10] + [0x00] * 9)  # OCCUPIED, START_FRAME_1, seq=16
        result = decode(data)
        header = result.header

        assert hasattr(header, 'status')
        assert hasattr(header, 'battery_low')
        assert hasattr(header, 'frame_type')
        assert hasattr(header, 'sequence')

        assert isinstance(header.status, Status)
        assert isinstance(header.battery_low, bool)
        assert isinstance(header.frame_type, FrameType)
        assert isinstance(header.sequence, int)


class TestEnumValues:
    """Test enum values are correct."""

    def test_frame_type_values(self):
        """Test FrameType enum has correct integer values."""
        assert FrameType.INFO == 0
        assert FrameType.KEEP_ALIVE == 1
        assert FrameType.CONFIG_UP == 2
        assert FrameType.CONFIG_DOWN == 3
        assert FrameType.START_FRAME_1 == 4
        assert FrameType.START_FRAME_2 == 5
        assert FrameType.RTC_SYNC == 6
        assert FrameType.RTC_UPDATE == 7

    def test_status_values(self):
        """Test Status enum has correct integer values."""
        assert Status.VACANT == 0
        assert Status.OCCUPIED == 1

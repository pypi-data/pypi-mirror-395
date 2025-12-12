from base64 import b64decode
from enum import IntEnum
from typing import Union

from pydantic import BaseModel


class FrameType(IntEnum):
    INFO = 0
    KEEP_ALIVE = 1
    CONFIG_UP = 2
    CONFIG_DOWN = 3
    START_FRAME_1 = 4
    START_FRAME_2 = 5
    RTC_SYNC = 6
    RTC_UPDATE = 7


class Status(IntEnum):
    VACANT = 0
    OCCUPIED = 1


class FrameHeader(BaseModel):
    status: Status
    battery_low: bool
    frame_type: FrameType
    sequence: int


class FramePayload(BaseModel):
    pass


class SensorData(BaseModel):
    frame_type: FrameType
    header: Union[FrameHeader, None] = None
    payload: bytes


def decode(data: Union[str, bytes]) -> SensorData:
    if isinstance(data, str):
        data = b64decode(data) if data[-1] == '=' else bytes.fromhex(data)

    if len(data) != 11:
        raise ValueError("Invalid data length, expected 11 bytes")

    header = data[:2]
    payload = data[2:]

    try:
        frame_type: FrameType = FrameType(header[0] & 0b00000111)
        status: Status = Status(1 if (header[0] & 0b10000000) else 0)
        battery_low = True if (header[0] & 0b01000000) else False

        return SensorData(
            frame_type=frame_type,
            header=FrameHeader(
                status=status,
                battery_low=battery_low,
                frame_type=frame_type,
                sequence=int(header[1])
            ),
            payload=payload
        )
    except ValueError as e:
        raise ValueError(f"Decoding error: {e}")


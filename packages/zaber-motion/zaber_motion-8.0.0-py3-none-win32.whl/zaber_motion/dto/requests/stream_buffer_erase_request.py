# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass
from typing import Any, Dict
import decimal
import zaber_bson


@dataclass
class StreamBufferEraseRequest:

    interface_id: int = 0

    device: int = 0

    buffer_id: int = 0

    pvt: bool = False

    @staticmethod
    def zero_values() -> 'StreamBufferEraseRequest':
        return StreamBufferEraseRequest(
            interface_id=0,
            device=0,
            buffer_id=0,
            pvt=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamBufferEraseRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamBufferEraseRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': int(self.interface_id),
            'device': int(self.device),
            'bufferId': int(self.buffer_id),
            'pvt': bool(self.pvt),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamBufferEraseRequest':
        return StreamBufferEraseRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            buffer_id=data.get('bufferId'),  # type: ignore
            pvt=data.get('pvt'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.interface_id is None:
            raise ValueError(f'Property "InterfaceId" of "StreamBufferEraseRequest" is None.')

        if not isinstance(self.interface_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "InterfaceId" of "StreamBufferEraseRequest" is not a number.')

        if int(self.interface_id) != self.interface_id:
            raise ValueError(f'Property "InterfaceId" of "StreamBufferEraseRequest" is not integer value.')

        if self.device is None:
            raise ValueError(f'Property "Device" of "StreamBufferEraseRequest" is None.')

        if not isinstance(self.device, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Device" of "StreamBufferEraseRequest" is not a number.')

        if int(self.device) != self.device:
            raise ValueError(f'Property "Device" of "StreamBufferEraseRequest" is not integer value.')

        if self.buffer_id is None:
            raise ValueError(f'Property "BufferId" of "StreamBufferEraseRequest" is None.')

        if not isinstance(self.buffer_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "BufferId" of "StreamBufferEraseRequest" is not a number.')

        if int(self.buffer_id) != self.buffer_id:
            raise ValueError(f'Property "BufferId" of "StreamBufferEraseRequest" is not integer value.')

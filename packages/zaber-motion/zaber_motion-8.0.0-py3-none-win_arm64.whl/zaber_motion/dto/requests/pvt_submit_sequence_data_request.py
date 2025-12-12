# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import Any, Dict
import decimal
import zaber_bson
from ..ascii.pvt_sequence_data import PvtSequenceData


@dataclass
class PvtSubmitSequenceDataRequest:

    interface_id: int = 0

    device: int = 0

    stream_id: int = 0

    sequence_data: PvtSequenceData = field(default_factory=PvtSequenceData.zero_values)

    @staticmethod
    def zero_values() -> 'PvtSubmitSequenceDataRequest':
        return PvtSubmitSequenceDataRequest(
            interface_id=0,
            device=0,
            stream_id=0,
            sequence_data=PvtSequenceData.zero_values(),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtSubmitSequenceDataRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtSubmitSequenceDataRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': int(self.interface_id),
            'device': int(self.device),
            'streamId': int(self.stream_id),
            'sequenceData': self.sequence_data.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtSubmitSequenceDataRequest':
        return PvtSubmitSequenceDataRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            stream_id=data.get('streamId'),  # type: ignore
            sequence_data=PvtSequenceData.from_dict(data.get('sequenceData')),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.interface_id is None:
            raise ValueError(f'Property "InterfaceId" of "PvtSubmitSequenceDataRequest" is None.')

        if not isinstance(self.interface_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "InterfaceId" of "PvtSubmitSequenceDataRequest" is not a number.')

        if int(self.interface_id) != self.interface_id:
            raise ValueError(f'Property "InterfaceId" of "PvtSubmitSequenceDataRequest" is not integer value.')

        if self.device is None:
            raise ValueError(f'Property "Device" of "PvtSubmitSequenceDataRequest" is None.')

        if not isinstance(self.device, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "Device" of "PvtSubmitSequenceDataRequest" is not a number.')

        if int(self.device) != self.device:
            raise ValueError(f'Property "Device" of "PvtSubmitSequenceDataRequest" is not integer value.')

        if self.stream_id is None:
            raise ValueError(f'Property "StreamId" of "PvtSubmitSequenceDataRequest" is None.')

        if not isinstance(self.stream_id, (int, float, decimal.Decimal)):
            raise ValueError(f'Property "StreamId" of "PvtSubmitSequenceDataRequest" is not a number.')

        if int(self.stream_id) != self.stream_id:
            raise ValueError(f'Property "StreamId" of "PvtSubmitSequenceDataRequest" is not integer value.')

        if self.sequence_data is None:
            raise ValueError(f'Property "SequenceData" of "PvtSubmitSequenceDataRequest" is None.')

        if not isinstance(self.sequence_data, PvtSequenceData):
            raise ValueError(f'Property "SequenceData" of "PvtSubmitSequenceDataRequest" is not an instance of "PvtSequenceData".')

        self.sequence_data.validate()

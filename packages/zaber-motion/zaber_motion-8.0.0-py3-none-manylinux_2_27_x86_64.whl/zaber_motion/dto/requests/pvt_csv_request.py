# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import Any, Dict
import zaber_bson
from ..ascii.pvt_sequence_data import PvtSequenceData


@dataclass
class PvtCsvRequest:

    sequence_data: PvtSequenceData = field(default_factory=PvtSequenceData.zero_values)

    path: str = ""

    @staticmethod
    def zero_values() -> 'PvtCsvRequest':
        return PvtCsvRequest(
            sequence_data=PvtSequenceData.zero_values(),
            path="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtCsvRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtCsvRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sequenceData': self.sequence_data.to_dict(),
            'path': str(self.path or ''),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtCsvRequest':
        return PvtCsvRequest(
            sequence_data=PvtSequenceData.from_dict(data.get('sequenceData')),  # type: ignore
            path=data.get('path'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.sequence_data is None:
            raise ValueError(f'Property "SequenceData" of "PvtCsvRequest" is None.')

        if not isinstance(self.sequence_data, PvtSequenceData):
            raise ValueError(f'Property "SequenceData" of "PvtCsvRequest" is not an instance of "PvtSequenceData".')

        self.sequence_data.validate()

        if self.path is not None:
            if not isinstance(self.path, str):
                raise ValueError(f'Property "Path" of "PvtCsvRequest" is not a string.')

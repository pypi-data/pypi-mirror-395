# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from collections.abc import Iterable
import zaber_bson
from ..ascii.pvt_sequence_data import PvtSequenceData


@dataclass
class PvtSaveCsvRequest:

    sequence_data: PvtSequenceData = field(default_factory=PvtSequenceData.zero_values)

    path: str = ""

    dimension_names: Optional[List[str]] = None

    @staticmethod
    def zero_values() -> 'PvtSaveCsvRequest':
        return PvtSaveCsvRequest(
            sequence_data=PvtSequenceData.zero_values(),
            path="",
            dimension_names=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtSaveCsvRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtSaveCsvRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sequenceData': self.sequence_data.to_dict(),
            'path': str(self.path or ''),
            'dimensionNames': [str(item or '') for item in self.dimension_names] if self.dimension_names is not None else [],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtSaveCsvRequest':
        return PvtSaveCsvRequest(
            sequence_data=PvtSequenceData.from_dict(data.get('sequenceData')),  # type: ignore
            path=data.get('path'),  # type: ignore
            dimension_names=data.get('dimensionNames'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.sequence_data is None:
            raise ValueError(f'Property "SequenceData" of "PvtSaveCsvRequest" is None.')

        if not isinstance(self.sequence_data, PvtSequenceData):
            raise ValueError(f'Property "SequenceData" of "PvtSaveCsvRequest" is not an instance of "PvtSequenceData".')

        self.sequence_data.validate()

        if self.path is not None:
            if not isinstance(self.path, str):
                raise ValueError(f'Property "Path" of "PvtSaveCsvRequest" is not a string.')

        if self.dimension_names is not None:
            if not isinstance(self.dimension_names, Iterable):
                raise ValueError('Property "DimensionNames" of "PvtSaveCsvRequest" is not iterable.')

            for i, dimension_names_item in enumerate(self.dimension_names):
                if dimension_names_item is not None:
                    if not isinstance(dimension_names_item, str):
                        raise ValueError(f'Item {i} in property "DimensionNames" of "PvtSaveCsvRequest" is not a string.')

# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass
from typing import Any, Dict, List
from collections.abc import Iterable
import zaber_bson
from .measurement_sequence import MeasurementSequence


@dataclass
class PvtSequenceData:
    """
    Data representing a sequence of pvt points with defined positions, velocities and times.
    """

    positions: List[MeasurementSequence]
    """
    Pvt sequence positions for each axis.
    """

    velocities: List[MeasurementSequence]
    """
    Pvt velocities for each axis.
    """

    times: MeasurementSequence
    """
    Relative times corresponding to points in PVT sequence.
    """

    @staticmethod
    def zero_values() -> 'PvtSequenceData':
        return PvtSequenceData(
            positions=[],
            velocities=[],
            times=MeasurementSequence.zero_values(),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtSequenceData':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtSequenceData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'positions': [item.to_dict() for item in self.positions] if self.positions is not None else [],
            'velocities': [item.to_dict() for item in self.velocities] if self.velocities is not None else [],
            'times': self.times.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtSequenceData':
        return PvtSequenceData(
            positions=[MeasurementSequence.from_dict(item) for item in data.get('positions')],  # type: ignore
            velocities=[MeasurementSequence.from_dict(item) for item in data.get('velocities')],  # type: ignore
            times=MeasurementSequence.from_dict(data.get('times')),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.positions is not None:
            if not isinstance(self.positions, Iterable):
                raise ValueError('Property "Positions" of "PvtSequenceData" is not iterable.')

            for i, positions_item in enumerate(self.positions):
                if positions_item is None:
                    raise ValueError(f'Item {i} in property "Positions" of "PvtSequenceData" is None.')

                if not isinstance(positions_item, MeasurementSequence):
                    raise ValueError(f'Item {i} in property "Positions" of "PvtSequenceData" is not an instance of "MeasurementSequence".')

                positions_item.validate()

        if self.velocities is not None:
            if not isinstance(self.velocities, Iterable):
                raise ValueError('Property "Velocities" of "PvtSequenceData" is not iterable.')

            for i, velocities_item in enumerate(self.velocities):
                if velocities_item is None:
                    raise ValueError(f'Item {i} in property "Velocities" of "PvtSequenceData" is None.')

                if not isinstance(velocities_item, MeasurementSequence):
                    raise ValueError(f'Item {i} in property "Velocities" of "PvtSequenceData" is not an instance of "MeasurementSequence".')

                velocities_item.validate()

        if self.times is None:
            raise ValueError(f'Property "Times" of "PvtSequenceData" is None.')

        if not isinstance(self.times, MeasurementSequence):
            raise ValueError(f'Property "Times" of "PvtSequenceData" is not an instance of "MeasurementSequence".')

        self.times.validate()

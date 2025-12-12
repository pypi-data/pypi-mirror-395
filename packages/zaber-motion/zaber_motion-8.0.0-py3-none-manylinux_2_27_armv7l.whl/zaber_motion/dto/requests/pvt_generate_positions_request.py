# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import Any, Dict, List
from collections.abc import Iterable
import zaber_bson
from ..ascii.measurement_sequence import MeasurementSequence


@dataclass
class PvtGeneratePositionsRequest:

    velocities: List[MeasurementSequence] = field(default_factory=list)

    times: MeasurementSequence = field(default_factory=MeasurementSequence.zero_values)

    times_relative: bool = False

    @staticmethod
    def zero_values() -> 'PvtGeneratePositionsRequest':
        return PvtGeneratePositionsRequest(
            velocities=[],
            times=MeasurementSequence.zero_values(),
            times_relative=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtGeneratePositionsRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtGeneratePositionsRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'velocities': [item.to_dict() for item in self.velocities] if self.velocities is not None else [],
            'times': self.times.to_dict(),
            'timesRelative': bool(self.times_relative),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtGeneratePositionsRequest':
        return PvtGeneratePositionsRequest(
            velocities=[MeasurementSequence.from_dict(item) for item in data.get('velocities')],  # type: ignore
            times=MeasurementSequence.from_dict(data.get('times')),  # type: ignore
            times_relative=data.get('timesRelative'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.velocities is not None:
            if not isinstance(self.velocities, Iterable):
                raise ValueError('Property "Velocities" of "PvtGeneratePositionsRequest" is not iterable.')

            for i, velocities_item in enumerate(self.velocities):
                if velocities_item is None:
                    raise ValueError(f'Item {i} in property "Velocities" of "PvtGeneratePositionsRequest" is None.')

                if not isinstance(velocities_item, MeasurementSequence):
                    raise ValueError(f'Item {i} in property "Velocities" of "PvtGeneratePositionsRequest" is not an instance of "MeasurementSequence".')

                velocities_item.validate()

        if self.times is None:
            raise ValueError(f'Property "Times" of "PvtGeneratePositionsRequest" is None.')

        if not isinstance(self.times, MeasurementSequence):
            raise ValueError(f'Property "Times" of "PvtGeneratePositionsRequest" is not an instance of "MeasurementSequence".')

        self.times.validate()

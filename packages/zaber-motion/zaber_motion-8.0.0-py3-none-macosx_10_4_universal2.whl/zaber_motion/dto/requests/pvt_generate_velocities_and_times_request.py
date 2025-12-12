# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, f-string-without-interpolation, too-many-branches, too-many-statements, unnecessary-pass
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import decimal
from collections.abc import Iterable
import zaber_bson
from ..ascii.measurement_sequence import MeasurementSequence
from ..measurement import Measurement


@dataclass
class PvtGenerateVelocitiesAndTimesRequest:

    positions: List[MeasurementSequence] = field(default_factory=list)

    target_speed: Measurement = field(default_factory=Measurement.zero_values)

    target_acceleration: Measurement = field(default_factory=Measurement.zero_values)

    resample_number: Optional[int] = None

    @staticmethod
    def zero_values() -> 'PvtGenerateVelocitiesAndTimesRequest':
        return PvtGenerateVelocitiesAndTimesRequest(
            positions=[],
            target_speed=Measurement.zero_values(),
            target_acceleration=Measurement.zero_values(),
            resample_number=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtGenerateVelocitiesAndTimesRequest':
        """" Deserialize a binary representation of this class. """
        data = zaber_bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtGenerateVelocitiesAndTimesRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        self.validate()
        return zaber_bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'positions': [item.to_dict() for item in self.positions] if self.positions is not None else [],
            'targetSpeed': self.target_speed.to_dict(),
            'targetAcceleration': self.target_acceleration.to_dict(),
            'resampleNumber': int(self.resample_number) if self.resample_number is not None else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtGenerateVelocitiesAndTimesRequest':
        return PvtGenerateVelocitiesAndTimesRequest(
            positions=[MeasurementSequence.from_dict(item) for item in data.get('positions')],  # type: ignore
            target_speed=Measurement.from_dict(data.get('targetSpeed')),  # type: ignore
            target_acceleration=Measurement.from_dict(data.get('targetAcceleration')),  # type: ignore
            resample_number=data.get('resampleNumber'),  # type: ignore
        )

    def validate(self) -> None:
        """" Validates the properties of the instance. """
        if self.positions is not None:
            if not isinstance(self.positions, Iterable):
                raise ValueError('Property "Positions" of "PvtGenerateVelocitiesAndTimesRequest" is not iterable.')

            for i, positions_item in enumerate(self.positions):
                if positions_item is None:
                    raise ValueError(f'Item {i} in property "Positions" of "PvtGenerateVelocitiesAndTimesRequest" is None.')

                if not isinstance(positions_item, MeasurementSequence):
                    raise ValueError(f'Item {i} in property "Positions" of "PvtGenerateVelocitiesAndTimesRequest" is not an instance of "MeasurementSequence".')

                positions_item.validate()

        if self.target_speed is None:
            raise ValueError(f'Property "TargetSpeed" of "PvtGenerateVelocitiesAndTimesRequest" is None.')

        if not isinstance(self.target_speed, Measurement):
            raise ValueError(f'Property "TargetSpeed" of "PvtGenerateVelocitiesAndTimesRequest" is not an instance of "Measurement".')

        self.target_speed.validate()

        if self.target_acceleration is None:
            raise ValueError(f'Property "TargetAcceleration" of "PvtGenerateVelocitiesAndTimesRequest" is None.')

        if not isinstance(self.target_acceleration, Measurement):
            raise ValueError(f'Property "TargetAcceleration" of "PvtGenerateVelocitiesAndTimesRequest" is not an instance of "Measurement".')

        self.target_acceleration.validate()

        if self.resample_number is not None:
            if not isinstance(self.resample_number, (int, float, decimal.Decimal)):
                raise ValueError(f'Property "ResampleNumber" of "PvtGenerateVelocitiesAndTimesRequest" is not a number.')

            if int(self.resample_number) != self.resample_number:
                raise ValueError(f'Property "ResampleNumber" of "PvtGenerateVelocitiesAndTimesRequest" is not integer value.')

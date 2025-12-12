from sys import float_info
from typing import Optional, Dict, Any
from typing_extensions import Self

from .training_protocols import (TrainingActionProtocol, TrainingPhaseProtocol, PredicateContext,
                                                     class_from_dict, class_to_dict)

_FLOAT_COMPARISON = float_info.epsilon * 2


class TrainingAction(TrainingActionProtocol):
    @property
    def has_progress(self) -> bool:
        return False

    @property
    def is_complete(self) -> bool:
        return True

    def evaluate(self, phase: TrainingPhaseProtocol, context: PredicateContext, is_init: bool) -> bool:
        return False

    def serialize_progress(self) -> Dict[str, Any]:
        return {}

    def deserialize_progress(self, data: Dict[str, Any]) -> None:
        pass

    def _to_dict(self) -> Optional[Dict[str, Any]]:
        return None

    def to_dict(self) -> Dict[str, Any]:
        return class_to_dict(self.__class__.__name__, self.__class__.__module__, self._to_dict())

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]):
        return class_from_dict(data)


class HeadMagnetIntensityAction(TrainingAction):
    def __init__(self, start: float, increment: float, end: float, pellet_delta: int):
        # Parameters
        self.start = start
        self.increment = increment
        self.end = end
        self.pellet_delta = pellet_delta

        # Internal Progress
        self.current_intensity = 0
        self.pellet_start = None

    @property
    def has_progress(self) -> bool:
        return True

    @property
    def is_complete(self) -> bool:
        return abs(self.current_intensity) >= self.end - _FLOAT_COMPARISON

    def evaluate(self, phase: TrainingPhaseProtocol, context: PredicateContext, is_init: bool) -> bool:
        if is_init:
            self.pellet_start = context.progress.pellets_consumed
            self.current_intensity = self.start
            # Override any default phase setting
            context.tunnel_device.update_head_magnet_intensity(self.start)
        else:
            if context.progress is None or context.pellet_device is None:
                return False
            if context.progress.pellets_consumed - self.pellet_start > self.pellet_delta:
                intensity = min(self.end, context.tunnel_device.head_magnet_intensity + self.increment)
                self.pellet_start = context.progress.pellets_consumed
                context.tunnel_device.update_head_magnet_intensity(intensity)

        return False

    def serialize_progress(self) -> Dict[str, Any]:
        return {
            "current_intensity": self.current_intensity,
            "pellet_start": self.pellet_start
        }

    def deserialize_progress(self, data: Dict[str, Any]) -> None:
        self.current_intensity = data["current_intensity"]
        self.pellet_start = data["pellet_start"]

    def _to_dict(self) -> Dict[str, Any]:
        return {
            "start": self.start,
            "increment": self.increment,
            "end": self.end,
            "pellet_delta": self.pellet_delta
        }

    @classmethod
    def from_properties(cls, data: Dict[str, Any]) -> Self:
        start = data["start"]
        increment = data["increment"]
        end = data["end"]
        pellet_delta = data["pellet_delta"]

        return HeadMagnetIntensityAction(start, increment, end, pellet_delta)


class ReachDistanceAction(TrainingAction):
    def __init__(self, increment: float, distance: float, pellet_delta: int):
        # Parameters
        self.increment = increment
        self.distance = distance
        self.pellet_delta = pellet_delta

        # Internal Progress
        self.current_distance = 0
        self.pellet_start = None

    @property
    def has_progress(self) -> bool:
        return True

    @property
    def is_complete(self) -> bool:
        return abs(self.current_distance) >= self.distance - _FLOAT_COMPARISON

    def evaluate(self, phase: TrainingPhaseProtocol, context: PredicateContext, is_init: bool) -> bool:
        if is_init:
            self.pellet_start = context.progress.pellets_consumed
            self.current_distance = 0
        else:
            if context.progress is None or context.pellet_device is None:
                return False
            if context.progress.pellets_consumed - self.pellet_start > self.pellet_delta:
                distance = min(self.distance, context.pellet_device.last_set_position.y + self.increment)
                self.pellet_start = context.progress.pellets_consumed
                context.pellet_device.set_y(distance)

        return False

    def serialize_progress(self) -> Dict[str, Any]:
        return {
            "current_distance": self.current_distance,
            "pellet_start": self.pellet_start
        }

    def deserialize_progress(self, data: Dict[str, Any]) -> None:
        self.current_distance = data["current_distance"]
        self.pellet_start = data["pellet_start"]

    def _to_dict(self) -> Dict[str, Any]:
        return {
            "distance": self.distance,
            "increment": self.increment,
            "pellet_delta": self.pellet_delta
        }

    @classmethod
    def from_properties(cls, data: Dict[str, Any]) -> Self:
        distance = data["distance"]
        increment = data["increment"]
        pellet_delta = data["pellet_delta"]

        return ReachDistanceAction(increment, distance, pellet_delta)

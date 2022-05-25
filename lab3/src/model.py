from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class PlaceType(Enum):
    Warehouse = 'WH'
    TrainStation = 'TS'
    Airport = 'AP'


@dataclass(frozen=True)
class Place:
    ref: int
    town: Town
    type: PlaceType


@dataclass(frozen=True)
class Town:
    ref: int
    name: str
    acronym: str


class Urgency(Enum):
    turbo = auto
    standard = auto
    economy = auto


@dataclass
class Transportation:
    _capacity: int
    _price_per_capacity: float
    time: float

    def sum_cost(self, volume: int) -> float:
        return (volume / self._capacity) * self.time * self._price_per_capacity


class PlaneTransportation(Transportation):
    def __init__(self, time: float):
        super().__init__(300, 100., time)


class TrainTransportation(Transportation):
    def __init__(self, time: float):
        super().__init__(100, 500, time)


class CarTransportation(Transportation):
    def __init__(self, time: float):
        super().__init__(60, 50., time)


@dataclass
class Track:
    transportations: list[Transportation]
    volume: int

    @property
    def cost(self):
        return sum(tr.sum_cost(self.volume) for tr in self.transportations)

    @property
    def time(self):
        return sum(tr.time for tr in self.transportations)


@dataclass(frozen=True)
class Order:
    sender_town: Town
    recipient_town: Town
    volume: int
    urgency: Urgency
    track: Track

    @property
    def cost(self):
        return self.track.cost

    @property
    def time(self):
        return self.track.time

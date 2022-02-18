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
    speed: int
    capacity: int
    price: float
    distance: int

    @property
    def sum_time(self) -> float:
        return self.distance / self.speed

    def sum_cost(self, volume: int) -> float:
        return (volume / self.capacity) * self.sum_time * self.price


class PlaneTransportation(Transportation):
    def __init__(self, distance: int):
        super().__init__(500, 300, 100., distance)


class TrainTransportation(Transportation):
    def __init__(self, distance: int):
        super().__init__(200, 100, 500, distance)


class CarTransportation(Transportation):
    def __init__(self, distance: int):
        super().__init__(100, 60, 50., distance)


@dataclass
class Track:
    transportations: list[Transportation]
    volume: int

    @property
    def cost(self):
        return sum(tr.sum_cost(self.volume) for tr in self.transportations)

    @property
    def time(self):
        return sum(tr.sum_time for tr in self.transportations)


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

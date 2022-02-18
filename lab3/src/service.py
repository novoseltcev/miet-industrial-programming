from __future__ import annotations

from model import *
import adapters


class TrackFactory:
    """Factory for Track from Places"""

    def __init__(self, computer: adapters.AbstractComputer):
        self.distance = computer

    def make(self, places: list[Place], volume: int) -> Track:
        receipt_places = iter(places[:-2])
        delivery_places = iter(places[1:])
        result = []
        for _ in range(len(places) - 1):
            distance = self.distance.direct(
                receipt_from := next(receipt_places),
                next(delivery_places)
            )
            match receipt_from.type:
                case PlaceType.Airport:
                    transportation = PlaneTransportation(distance)
                case PlaceType.TrainStation:
                    transportation = TrainTransportation(distance)
                case PlaceType.Warehouse:
                    transportation = CarTransportation(distance)
                case _:
                    raise ValueError(f'Invalid {1}')
            result.append(transportation)
        return Track(result, volume)


class DeliveryService:
    """Facade for delivery system."""

    def __init__(
            self,
            repository: adapters.AbstractRepository,
            computer: adapters.AbstractComputer,
    ):
        self.places = repository
        self.distance = computer
        self.track_factory = TrackFactory(self.distance)

    def calculate_order(self, start_town: str, finish_town: str, volume: int, urgency: Urgency) -> Order:
        [start_place] = self.places.get(start_town),
        [finish_place] = self.places.get(finish_town),
        track = self.track_factory.make(
            places=self.distance.shortest(start_place, finish_place, urgency),
            volume=volume
        )
        return Order(
            sender_town=start_place.town,
            recipient_town=finish_place.town,
            urgency=urgency,
            volume=volume,
            track=track
        )

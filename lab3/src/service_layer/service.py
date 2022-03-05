from __future__ import annotations

from lab3.src.model import *
import adapters


class TrackFactory:
    """Factory for Track from Places"""

    def __init__(self, computer: adapters.AbstractComputer):
        self.distance = computer

    def make(self, places: list[Place], volume: int) -> Track:
        receipt_places = iter(places[:-1])
        delivery_places = iter(places[1:])
        result = []
        for _ in range(len(places) - 1):
            distance = self.distance.direct(
                receipt_from := next(receipt_places),
                delivery_to := next(delivery_places)
            )
            match receipt_from.type, delivery_to.type:
                case PlaceType.Airport, PlaceType.Airport:
                    transportation = PlaneTransportation(distance)
                case PlaceType.TrainStation, PlaceType.TrainStation:
                    transportation = TrainTransportation(distance)
                case _:
                    transportation = CarTransportation(distance)
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
        [from_town] = self.places.get_by_town(start_town).town,
        [to_town] = self.places.get_by_town(finish_town).town,
        if from_town is None or to_town is None:
            raise ValueError()

        track = self.track_factory.make(
            places=self.distance.faster(from_town, to_town, urgency),
            volume=volume
        )
        return Order(
            sender_town=from_town,
            recipient_town=to_town,
            urgency=urgency,
            volume=volume,
            track=track
        )


service = DeliveryService(adapters.InMemoryRepository(), adapters.LocalComputer())
order = service.calculate_order('Moscow', 'Nizhniy Novgorod', 100, Urgency.turbo)
print(order)
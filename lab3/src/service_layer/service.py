from __future__ import annotations

from lab3.src.model import *
from lab3.src.adapters.repository import *
import computer


class TrackFactory:
    """Factory for Track from Places"""

    def __init__(self, comp: computer.AbstractComputer):
        self.way_computer = comp

    def make(self, places: list[Place], volume: int) -> Track:
        receipt_places = iter(places[:-1])
        delivery_places = iter(places[1:])
        result = []
        for _ in range(len(places) - 1):
            time = self.way_computer.direct(
                receipt_from := next(receipt_places),
                delivery_to := next(delivery_places)
            )
            match receipt_from.type, delivery_to.type:
                case PlaceType.Airport, PlaceType.Airport:
                    transportation = PlaneTransportation(time)
                case PlaceType.TrainStation, PlaceType.TrainStation:
                    transportation = TrainTransportation(time)
                case _:
                    transportation = CarTransportation(time)
            result.append(transportation)
        return Track(result, volume)


class DeliveryService:
    """Facade for delivery system."""

    def __init__(
            self,
            repository: AbstractRepository,
            comp: computer.AbstractComputer,
    ):
        self.places = repository
        self.way_computer = comp
        self.track_factory = TrackFactory(self.way_computer)

    def calculate_order(self, start_town: str, finish_town: str, volume: int, urgency: Urgency) -> Order:
        [from_town] = self.places.get_by_town(start_town).town,
        [to_town] = self.places.get_by_town(finish_town).town,
        if from_town is None or to_town is None:
            raise ValueError()

        track = self.track_factory.make(
            places=self.way_computer.fastest(from_town, to_town, urgency),
            volume=volume
        )
        return Order(
            sender_town=from_town,
            recipient_town=to_town,
            urgency=urgency,
            volume=volume,
            track=track
        )


service = DeliveryService(InMemoryRepository(), computer.LocalComputer())
order = service.calculate_order('Moscow', 'NN', 100, Urgency.turbo)
print(order)
print(order.track)


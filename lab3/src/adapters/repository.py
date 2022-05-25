from abc import ABC, abstractmethod
from typing import Optional

from lab3.src.model import PlaceType, Place, Town
from lab3.src.adapters.storage import PointStorage


class AbstractRepository(ABC):
    @abstractmethod
    def get_by_town(self, name: str) -> Place:
        ...

    @abstractmethod
    def get(self, ref: int) -> Place:
        ...

    @abstractmethod
    def all(self) -> list[Place]:
        ...


class InMemoryRepository(AbstractRepository):
    def __init__(self):
        self.storage = PointStorage()

    def _get_town(self, name: str) -> Town:
        ref, town_data = next((i, data) for i, data in enumerate(self.storage.towns) if name in data)
        return Town(
            ref=ref,
            name=town_data[0],
            acronym=town_data[1]
        )

    def get_by_town(self, name: str) -> Optional[Place]:
        try:
            town = self._get_town(name)
            ref = next(i for i, data in enumerate(self.storage.places)
                       if (town.acronym, PlaceType.Warehouse.value) == data)
            return Place(
                ref=ref,
                town=town,
                type=PlaceType.Warehouse,
            )
        except StopIteration as e:
            print(e)
            return None

    def get(self, ref: int) -> Optional[Place]:
        try:
            if ref < 0:
                raise ValueError(f'Invalid {ref=}')
            data = self.storage.places[ref]
            return Place(
                ref=ref,
                town=self._get_town(data[0]),
                type=PlaceType(data[1]),
            )
        except (StopIteration, IndexError, ValueError):
            return None

    def all(self) -> list[Place]:
        result = []
        for ref, data in enumerate(self.storage.places):
            result.append(
                Place(
                    ref=ref,
                    town=self._get_town(data[0]),
                    type=PlaceType(data[1]),
                )
            )
        return result

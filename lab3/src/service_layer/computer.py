from __future__ import annotations
from abc import ABC, abstractmethod

import numpy as np
import networkx as nx

from lab3.src.adapters import repository
from lab3.src.adapters import storage
from lab3.src.model import Place, Town, PlaceType, Urgency


class DistanceToTimeAdapter(storage.GraphStorage):
    def __init__(self, graph: storage.GraphStorage, repo: repository.AbstractRepository):
        self.graph = graph
        self.places = repo

    def get(self) -> np.matrix:
        pre_result = np.where(self.graph._data == 0, self.INF, self.graph._data)
        length = len(pre_result)
        for i in range(length):
            place_i_type = self.places.get(i).type
            for j in range(length):
                place_j_type = self.places.get(j).type
                match place_i_type, place_j_type:
                    case PlaceType.Airport, PlaceType.Airport:
                        pre_result[i, j] /= 500
                    case PlaceType.Airport, PlaceType.Airport:
                        pre_result[i, j] /= 200
                    case _:
                        pre_result[i, j] /= 100
        return np.matrix(pre_result)


class AbstractComputer(ABC):
    @abstractmethod
    def direct(self, begin: Place, end: Place) -> int:
        ...

    @abstractmethod
    def fastest(self, start: Town, finish: Town, urgency: Urgency) -> list[Place]:
        ...


class LocalComputer(AbstractComputer):
    def __init__(self):
        self.places = repository.InMemoryRepository()
        self.graph = DistanceToTimeAdapter(storage.DistanceStorage(), self.places)
        self.INF = np.inf

    def direct(self, begin: Place, end: Place) -> int:
        return self.graph.get()[begin.ref, end.ref]

    def fastest(self, start: Town, finish: Town, urgency: Urgency) -> list[Place]:
        graph = self.graph.get()
        length = len(graph)
        match urgency:
            case Urgency.standard:
                matrix = np.where(
                    ([place.type == PlaceType.Airport] * length for place in self.places.all()),
                    self.INF, graph)
            case Urgency.economy:
                matrix = np.where(
                    ([place.type == PlaceType.TrainStation] * length for place in self.places.all()),
                    self.INF, graph)
            case _:
                matrix = graph

        repo = repository.InMemoryRepository()
        refs = nx.dijkstra_path(
            nx_matrix := nx.from_numpy_matrix(matrix),
            repo.get_by_town(start.name).ref,
            repo.get_by_town(finish.name).ref,
        )
        print(nx_matrix)
        return list(map(repo.get, refs))

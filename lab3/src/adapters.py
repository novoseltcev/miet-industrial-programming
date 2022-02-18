from abc import ABC, abstractmethod

import numpy as np

from model import Place, Town, PlaceType, Urgency


class Storage:
    places = (
        ('msk', 'AP'),
        ('msk', 'TS'),
        ('msk', 'WH'),
        ('mzh', 'TS'),
        ('mzh', 'WH'),
        ('zvn', 'WH'),
        ('NN', 'AP'),
        ('NN', 'TS'),
        ('NN', 'WH'),
        ('dzr', 'TS'),
        ('dzr', 'WH'),
        ('vlg', 'AP'),
        ('vlg', 'TS'),
        ('vlg', 'WH'),
        ('kam', 'TS'),
        ('kam', 'WH'),
    )

    towns = (
        ('Moscow', 'msk'),
        ('Mozhaisk', 'mzh'),
        ('Zvenigorod', 'zvn'),
        ('Nizhniy Novgorod', 'NN'),
        ('Dzerzhinsk', 'dzr'),
        ('Volgograd', 'vlg'),
        ('Kamishin', 'kam'),
    )

    distances = np.matrix([
        [0, 20, 30, 108, 110, 65, 398, 0, 0, 0, 0, 926, 0, 0, 0, 0],
        [20, 0, 10, 98, 100, 55, 0, 415, 0, 483, 0, 0, 937, 0, 1204, 0],
        [30, 0, 0, 108, 110, 65, 0, 0, 430, 0, 390, 0, 0, 652, 0, 1234],

        [108, 98, 108, 0, 5, 0, 0, 0, 0, 581, 0, 0, 1035, 0, 1302, 0],
        [110, 100, 110, 5, 0, 78, 0, 0, 540, 0, 500, 0, 0, 1062, 0, 1344],

        [65, 55, 65, 0, 78, 0, 0, 0, 495, 0, 455, 0, 0, 1017, 0, 1299],

        [398, 0, 0, 0, 0, 0, 0, 19, 23, 0, 26, 828, 0, 0, 0, 0],
        [0, 415, 0, 0, 0, 0, 19, 0, 4, 32, 0, 0, 840, 0, 919, 0],
        [0, 0, 430, 0, 540, 495, 23, 4, 0, 0, 40, 0, 0, 849, 0, 1010],

        [0, 483, 0, 581, 0, 0, 0, 32, 0, 0, 4, 0, 872, 0, 951, 0],
        [0, 0, 390, 0, 500, 455, 26, 0, 40, 4, 0, 0, 0, 889, 0, 1050],

        [926, 0, 0, 0, 0, 0, 828, 0, 0, 0, 0, 0, 15, 16, 0, 285],
        [0, 937, 0, 1035, 0, 0, 0, 840, 0, 872, 0, 15, 0, 2, 257, 281],
        [0, 0, 952, 0, 1062, 1017, 0, 0, 849, 0, 889, 16, 2, 0, 0, 282],

        [0, 1204, 0, 1302, 0, 0, 0, 919, 0, 951, 0, 0, 257, 0, 0, 2],
        [0, 0, 1234, 0, 1344, 1299, 0, 0, 1010, 0, 1050, 285, 281, 282, 2, 0],
    ])


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, town_name: str) -> Place:
        ...

    @abstractmethod
    def shortest_way(self, start_point, finish_point) -> list[Place]:
        ...


class InMemoryRepository(AbstractRepository):
    def __init__(self):
        self.storage = Storage()

    def _get_town(self, name: str) -> Town:
        ref, town_data = next((i, data) for i, data in enumerate(self.storage.towns) if name in data)
        return Town(
            ref=ref,
            name=town_data[0],
            acronym=town_data[1]
        )

    def get_by_town(self, name: str) -> Place:
        town = self._get_town(name)
        ref = next(
            i for i, data in enumerate(self.storage.places) if town.acronym in data and PlaceType.Warehouse in data)
        return Place(
            ref=ref,
            town=town,
            type=PlaceType.Warehouse,
        )

    def get(self, ref: int) -> Place:
        data = self.storage.places[ref]
        return Place(
            ref=ref,
            town=self._get_town(data[0]),
            type=data[1],
        )

    def shortest_way(self, start_point, finish_point) -> list[Place]:
        pass


class AbstractComputer(ABC):
    @abstractmethod
    def direct(self, begin: Place, end: Place) -> int:
        ...

    @abstractmethod
    def shortest(self, start: Place, finish: Place, urgency: Urgency) -> list[Place]:
        ...


class LocalComputer(AbstractComputer):
    def __init__(self):
        self.storage = Storage()

    def direct(self, begin: Place, end: Place) -> int:
        return self.storage.distances[begin.ref, end.ref]

    def shortest(self, start: Place, finish: Place, urgency: Urgency) -> list[Place]:
        pass


# def matrix_upd(urgency: Urgency) -> np.matrix:
#     src = matrix_dist.copy()
#     match urgency:
#         case Urgency.economy:  # Without trains
#             for i in range(SIZE):
#                 if places[i].find('TS'):
#                     for j in range(SIZE):
#                         src[i, j] = INF
#
#         case Urgency.standard:  # Without airplanes
#             for i in range(SIZE):
#                 if places[i].find('AP'):
#                     for j in range(SIZE):
#                         src[i, j] = INF
#
#         case Urgency.turbo:
#             for i in range(SIZE):
#                 for j in range(SIZE):
#                     if src[i, j] == 0:
#                         src[i, j] = INF
#
#     return src
#
#
#
# def x(d: list, v: list, matrix: np.matrix):
#     min_index = INF
#     _min = INF
#     for i in range(SIZE):
#         if v[i] == 1 and d[i] < _min:
#             _min = d[i]
#             min_index = i
#     if min_index != INF:
#         for i in range(SIZE):
#             if matrix[min_index, i] > 0:
#                 temp = _min + matrix[min_index, i]
#                 if temp < d[i]:
#                     d[i] = temp
#
#         v[min_index] = 0
#     return min_index
#
#
# def optim(cls, matrix: np.matrix, start: int, finish: int) -> np.darray:
#     d = [inf_val := np.inf] * SIZE
#     v = [1] * SIZE
#     d[begin_index := start] = 0
#
#     min_index = cls.x(d, v, matrix)
#     while min_index < inf_val:
#         min_index = cls.x(d, v, matrix)
#
#     weight = d[end := finish]
#     src = list()
#     src.append(end)
#
#     while end != begin_index:
#         for i in range(SIZE):
#             cell = matrix[end, i]
#             if cell != 0:
#                 temp = weight - cell
#                 if temp == d[i]:
#                     weight = temp
#                     end = i
#                     src.append(i + 1)
#
#     return src[::-1]


# def best(cls, start: Town, finish: Town, urgency: Urgency, volume: int) -> Track:
#     builder = TrackBuilder(
#         plane_factory=PlaneTransportationFactory(),
#         train_factory=TrainTransportationFactory(),
#         car_factory=CarTransportationFactory()
#     )
#     towns = PlaceDistance(urgency).shortest(start, finish)
#     return builder.make(towns, volume)
#
#     # match len(path):
#     #     case 1:
#     #         return Track([car_factory.make(*path)], volume)
#     #
#     #     case 3:
#     #         _, delivery_type = points[path[1]].split('_')
#     #         match delivery_type:
#     #             case 'AP':
#     #                 return Track([
#     #                     car_factory.make(*path[:1]),
#     #                     plane_factory.make(*path[1:2]),
#     #                     car_factory.make(*path[2:3]),
#     #                 ], volume)
#     #
#     #             case 'TS':
#     #                 return Track([
#     #                     car_factory.make(*path[:1]),
#     #                     train_factory.make(*path[1:2]),
#     #                     car_factory.make(*path[2:3]),
#     #                 ], volume)
#     #             case _:
#     #                 raise ValueError(f'Invalid {delivery_type=}')
#     #
#     #     case 5:
#     #         delivery_type1 = points[path[1]].split('_')[1]
#     #         delivery_type2 = points[path[1]].split('_')[3]
#     #         match delivery_type1, delivery_type2:
#     #             case 'AP', 'TS':
#     #                 return Track([
#     #                     car_factory.make(*path[:1]),
#     #                     plane_factory.make(*path[1:2]),
#     #                     car_factory.make(*path[2:3]),
#     #                     train_factory.make(*path[3:4]),
#     #                     car_factory.make(*path[4:5]),
#     #                 ], volume)
#     #             case 'TS', 'AP':
#     #                 return Track([
#     #                     car_factory.make(*path[:1]),
#     #                     train_factory.make(*path[1:2]),
#     #                     car_factory.make(*path[2:3]),
#     #                     plane_factory.make(*path[3:4]),
#     #                     car_factory.make(*path[4:5]),
#     #                 ], volume)
#     #
#     #             case _:
#     #                 raise ValueError(f'Invalid {delivery_type1=} and {delivery_type2=}')
#     #     case 7:
#     #         return Track([
#     #             car_factory.make(*path[:1]),
#     #             train_factory.make(*path[1:2]),
#     #             car_factory.make(*path[2:3]),
#     #             plane_factory.make(*path[3:4]),
#     #             car_factory.make(*path[4:5]),
#     #             train_factory.make(*path[5:6]),
#     #             car_factory.make(*path[6:7]),
#     #         ], volume)
#     #     case _:
#     #         raise ValueError(f'Invalid {path=}')
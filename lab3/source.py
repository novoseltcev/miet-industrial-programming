from enum import Enum

import numpy as np

SIZE = 16
INF = np.inf

points = [
    "msk_AP", "msk_TS", "msk_WH", "mzh_TS",
    "mzh_WH", "zvn_WH", "NN_AP", "NN_TS", "NN_WH", "dzr_TS", "dzr_WH",
    "vlg_AP", "vlg_TS", "vlg_WH", "kam_TS", "kam_WH"]

towns = {
    "Moscow": 2,
    "Mozhaisk": 4,
    "Zvenigorod": 5,
    "Nizhniy Novgorod": 8,
    "Dzerzhinsk": 1,
    "Volgograd": 13,
    "Kamishin": 15
}

table = {
    "msk": 0,
    "mzh": 1,
    "zvn": 2,
    "NN": 3,
    "dzr": 4,
    "vlg": 5,
    "kam": 6
}

tableCost = (
    (500, 300, 100.),
    (200, 100, 500.),
    (100, 60, 50.),
    (0, 0, 0.),
    (200, 100, 500.),
    (100, 60, 50.),
    (0, 0, 0.),
    (0, 0, 0.),
    (100, 60, 50.),
    (500, 300, 100.),
    (200, 100, 500.),
    (100, 60, 50.),
    (0, 0, 0.),
    (200, 100, 500.),
    (100, 60, 50.),
    (500, 300, 100.),
    (200, 100, 500.),
    (100, 60, 50.),
    (0, 0, 0.),
    (200, 100, 500.),
    (100, 60, 50.)
)

matrix_dist = np.matrix([
    [0, 20, 30, 108, 110, 65, 398, 0, 0, 0, 0, 926, 0, 0, 0, 0],
    [20, 0, 10, 98, 100, 55, 0, 415, 0, 483, 0, 0, 937, 0, 1204, 0],
    [30, 10, 0, 108, 110, 65, 0, 0, 430, 0, 390, 0, 0, 652, 0, 1234],
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


class Type(Enum):
    turbo = 1
    standard = 2
    economy = 3


class Train:
    _speed: int
    _volume: int
    _price: float
    _distance: int

    def __init__(self, price=200, speed=100, volume=500, distance=0):
        self._price = price
        self._speed = speed
        self._volume = volume
        self._distance = distance

    def sum_cost(self, mass: int, distance: int) -> float:
        return (mass / self._volume) * self.sum_time(distance) * self._price

    def sum_time(self, distance: int) -> float:
        return distance / self._speed

    @property
    def distance(self) -> int:
        return self._distance


class Car:
    _speed: int
    _volume: int
    _price: float
    _distance: int

    def __init__(self, price=100, speed=60, volume=50, distance=0):
        self._price = price
        self._speed = speed
        self._volume = volume
        self._distance = distance

    def sum_cost(self, mass: int, distance: int) -> float:
        return (mass / self._volume) * self.sum_time(distance) * self._price

    def sum_time(self, distance: int) -> float:
        return distance / self._speed

    @property
    def distance(self) -> int:
        return self._distance


class Plane:
    _speed: int
    _volume: int
    _price: float
    _distance: int

    def __init__(self, price=500, speed=300, volume=100, distance=0):
        self._price = price
        self._speed = speed
        self._volume = volume
        self._distance = distance

    def sum_cost(self, mass: int, distance: int) -> float:
        return (mass / self._volume) * self.sum_time(distance) * self._price

    def sum_time(self, distance: int) -> float:
        return distance / self._speed

    @property
    def distance(self) -> int:
        return self._distance


class Track:
    _cost: float = 0
    _time: float = 0
    _volume: int = 0

    def __init__(self, vehicles=None, volume: int = 0):
        self._volume = volume
        if vehicles is not None:
            for vehicle in vehicles:
                self._cost += vehicle.sum_cost(volume, vehicle.distance)
                self._time += vehicle.sum_time(vehicle.distance)

    @property
    def cost(self) -> float:
        return self._cost


class Order:
    _cost: float
    _volume: int
    _start_point: str
    _finish_point: str
    _type: Type
    _track: Track

    def __init__(self, delivery: Type, start_point: str, finish_point: str, volume: int):
        self._type = delivery
        self._start_point = start_point
        self._finish_point = finish_point
        self._volume = volume
        self._track = self.best(start_point, finish_point, delivery, volume)
        self._cost = self._track.cost

    @staticmethod
    def decr(town_name: str) -> int:
        for town, weight in towns:
            if town_name == town:
                return weight
        return -1

    @staticmethod
    def matrix_upd(type: Type) -> np.matrix:
        result = matrix_dist.copy()
        match type:
            case Type.economy:
                for i in range(SIZE):
                    if points[i].find('TS'):
                        for j in range(SIZE):
                            result[i, j] = INF

            case Type.standard:
                for i in range(SIZE):
                    if points[i].find('AP'):
                        for j in range(SIZE):
                            result[i, j] = INF

            case Type.turbo:
                for i in range(SIZE):
                    for j in range(SIZE):
                        if result[i, j] == 0:
                            result[i, j] = INF

        return result

    @staticmethod
    def x(d: list, v: list, matrix: np.matrix):
        min_index = INF
        _min = INF
        for i in range(SIZE):
            if v[i] == 1 and d[i] < _min:
                _min = d[i]
                min_index = i
        if min_index != INF:
            for i in range(SIZE):
                if matrix[min_index, i] > 0:
                    temp = _min + matrix[min_index, i]
                    if temp < d[i]:
                        d[i] = temp

            v[min_index] = 0
        return min_index

    @classmethod
    def optim(cls, matrix: np.matrix, start: int, finish: int) -> np.darray:
        d = [inf_val := np.inf] * SIZE
        v = [1] * SIZE
        d[begin_index := start] = 0

        min_index = cls.x(d, v, matrix)
        while min_index < inf_val:
            min_index = cls.x(d, v, matrix)

        weight = d[end := finish]
        result = list()
        result.append(end)

        while end != begin_index:
            for i in range(SIZE):
                cell = matrix[end, i]
                if cell != 0:
                    temp = weight - cell
                    if temp == d[i]:
                        weight = temp
                        end = i
                        result.append(i + 1)

        return result[::-1]

    @classmethod
    def best(cls, start_point: str, finish_point: str, delivery: Type, volume: int) -> Track:
        start = cls.decr(start_point)
        finish = cls.decr(finish_point)
        matrix = cls.matrix_upd(delivery)
        path = cls.optim(matrix, start, finish)
        match len(path):
            case 1:
                point = points[path[0]].split('_')[0]
                car = Car(
                    *tableCost[table[point] * 3 + 2],
                    matrix_dist[path[0], path[1]]
                )
                return Track(car, volume)

            case 3:
                vehicle_list = []
                point1 = points[path[0]].split('_')[0]
                car1 = Car(
                    *tableCost[table[point1] * 3 + 2],
                    distance=matrix_dist[path[0], path[1]]
                )
                vehicle_list.append(car1)

                point2, delivery_type = points[path[1]].split('_')
                match delivery_type:
                    case 'AP':
                        plane = Plane(
                            *tableCost[table[point2] * 3],
                            matrix_dist[path[1], path[2]]
                        )
                        vehicle_list.append(plane)
                    case 'TS':
                        train = Train(
                            *tableCost[table[point2] * 3 + 1],
                            matrix_dist[path[1], path[2]]
                        )
                        vehicle_list.append(train)
                    case _:
                        raise ValueError(f'Invalid {delivery_type=}')

                point3 = points[path[2]].split('_')[0]
                car2 = Car(
                    *tableCost[table[point3] * 3 + 2],
                    matrix_dist[path[2], path[3]]
                )
                vehicle_list.append(car2)
                return Track(vehicle_list, volume)
            case 5:
                vehicle_list = []
                point1 = points[path[0]].split('_')[0]
                car1 = Car(
                    *tableCost[table[point1] * 3 + 2],
                    matrix_dist[path[0], path[1]]
                )
                vehicle_list.append(car1)

                point2, delivery_type = points[path[1]].split('_')
                match delivery_type:
                    case 'AP':
                        plane1 = Plane(
                            *tableCost[table[point2] * 3],
                            matrix_dist[path[1], path[2]]
                        )
                        vehicle_list.append(plane1)
                    case 'TS':
                        train1 = Train(
                            *tableCost[table[point2] * 3 + 1],
                            matrix_dist[path[1], path[2]]
                        )
                        vehicle_list.append(train1)
                    case _:
                        raise ValueError(f'Invalid {delivery_type=}')

                point3 = points[path[2]].split('_')[0]
                car2 = Car(
                    *tableCost[table[point3] * 3 + 2],
                    matrix_dist[path[2], path[3]]
                )
                vehicle_list.append(car2)

                point4, delivery_type = points[path[3]].split('_')
                match delivery_type:
                    case 'AP':
                        plane2 = Plane(
                            *tableCost[table[point4] * 3],
                            matrix_dist[path[3], path[4]]
                        )
                        vehicle_list.append(plane2)
                    case 'TS':
                        train2 = Train(
                            *tableCost[table[point4] * 3 + 1],
                            matrix_dist[path[3], path[4]]
                        )
                        vehicle_list.append(train2)
                    case _:
                        raise ValueError(f'Invalid {delivery_type=}')

                point5 = points[path[4]].split('_')[0]
                car3 = Car(
                    *tableCost[table[point5] * 3 + 2],
                    matrix_dist[path[4], path[5]]
                )
                vehicle_list.append(car3)
                return Track(vehicle_list, volume)
            case 7:
                point1 = points[path[0]].split('_')[0]
                car1 = Car(
                    *tableCost[table[point1] * 3 + 2],
                    matrix_dist[path[0], path[1]]
                )

                point2 = points[path[1]].split('_')[0]
                train1 = Train(
                    *tableCost[table[point2] * 3 + 1],
                    matrix_dist[path[1], path[2]]
                )

                point3 = points[path[0]].split('_')[0]
                car2 = Car(
                    *tableCost[table[point3] * 3 + 2],
                    matrix_dist[path[2], path[3]]
                )

                point4 = points[path[0]].split('_')[0]
                plane = Plane(
                    *tableCost[table[point4] * 3],
                    matrix_dist[path[3], path[4]]
                )

                point5 = points[path[0]].split('_')[0]
                car3 = Car(
                    *tableCost[table[point5] * 3 + 2],
                    matrix_dist[path[4], path[5]]
                )

                point6 = points[path[1]].split('_')[0]
                train2 = Train(
                    *tableCost[table[point6] * 3 + 1],
                    matrix_dist[path[5], path[6]]
                )

                point7 = points[path[0]].split('_')[0]
                car4 = Car(
                    *tableCost[table[point7] * 3 + 2],
                    matrix_dist[path[6], path[7]]
                )
                return Track([car1, train1, car2, plane, car3, train2, car4], volume)
            case _:
                raise ValueError(f'Invalid {path=}')

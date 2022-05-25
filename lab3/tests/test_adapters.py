from itertools import combinations

import pytest

from lab3.src.adapters import *


@pytest.fixture
def repository():
    return InMemoryRepository()


@pytest.fixture
def computer():
    return LocalComputer()


@pytest.fixture
def moscow_warehouse():
    return Place(2, Town(0, 'Moscow', 'msk'), PlaceType.Warehouse)


towns = (
    Town(0, 'Moscow', 'msk'),
    Town(1, 'Mozhaisk', 'mzh'),
    Town(2, 'Zvenigorod', 'zvn'),
    Town(3, 'Nizhniy Novgorod', 'NN'),
    Town(4, 'Dzerzhinsk', 'dzr'),
    Town(5, 'Volgograd', 'vlg'),
    Town(6, 'Kamishin', 'kam'),
)


def test_repository_get_by_town_success(repository, moscow_warehouse):
    assert repository.get_by_town('Moscow') == moscow_warehouse


def test_repository_get_by_town_none(repository):
    assert repository.get_by_town('Piter') is None


def test_repository_get_success(repository, moscow_warehouse):
    assert repository.get(2) == moscow_warehouse


@pytest.mark.parametrize('ref', [-1, 16])
def test_repository_get_none(repository, ref: int):
    assert repository.get(ref) is None


def test_computer_direct_success(computer, moscow_warehouse):
    assert computer.direct(
        moscow_warehouse,
        Place(0, Town(0, 'Moscow', 'msk'), PlaceType.Airport)
    ) == 0.3


@pytest.mark.parametrize('from_town, to_town', combinations(towns, 2))
def test_computer_shortest_turbo_success(computer, from_town: Town, to_town: Town):
    assert computer.fastest(from_town, to_town, Urgency.turbo) == ...


@pytest.mark.parametrize('from_town, to_town', combinations(towns, 2))
def test_computer_shortest_standard_success(computer, from_town: Town, to_town: Town):
    assert computer.fastest(from_town, to_town, Urgency.standard) == ...


@pytest.mark.parametrize('from_town, to_town', combinations(towns, 2))
def test_computer_shortest_economy_success(computer, from_town: Town, to_town: Town):
    assert computer.fastest(from_town, to_town, Urgency.economy) == ...

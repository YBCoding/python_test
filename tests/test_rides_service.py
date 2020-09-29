from datetime import datetime, timedelta
from typing import List

import pytest

from load_config import RidesConfigLoader
from models import Ride
from rides.exception import RideNotFound
from rides.rides_repository import RidesRepository
from rides.rides_service import RidesService

ridesRepository = RidesRepository()
ridesService = RidesService(ridesRepository, RidesConfigLoader("rides_config.json"))


def test_should_cost_normal_fare(mocker):
    ride_id = 0

    def mock_get_all(self) -> List[Ride]:
        return [
            Ride(0, datetime.fromisoformat('2020-01-01T13:00:00'), 2, timedelta(seconds=600)),
            Ride(1, datetime.fromisoformat('2020-01-01T13:00:00'), 4, timedelta(seconds=1200))
        ]

    mocker.patch(
        # Dataset is in slow.py, but imported to main.py
        'rides.rides_repository.RidesRepository.get_all',
        mock_get_all
    )

    assert ridesService.compute_cost(0) == 1 + 5
    assert ridesService.compute_cost(1) == 1 + 10


def test_should_cost_zero(mocker):
    def mock_get_all(self) -> List[Ride]:
        return [
            Ride(0, datetime.fromisoformat('2020-01-01T13:00:00'), 0, timedelta(seconds=600)),
            Ride(1, datetime.fromisoformat('2020-01-01T13:00:00'), 100, timedelta(seconds=0)),
            Ride(2, datetime.fromisoformat('2020-01-01T13:00:00'), 0, timedelta(seconds=0))
        ]

    mocker.patch(
        # Dataset is in slow.py, but imported to main.py
        'rides.rides_repository.RidesRepository.get_all',
        mock_get_all
    )

    assert ridesService.compute_cost(0) == 0
    assert ridesService.compute_cost(1) == 0
    assert ridesService.compute_cost(2) == 0


def test_should_compute_after_midnight(mocker):
    def mock_get_all(self) -> List[Ride]:
        return [
            Ride(0, datetime.fromisoformat('2020-01-01T23:00:00'), 24, timedelta(seconds=3600)),
            Ride(1, datetime.fromisoformat('2020-01-01T23:00:00'), 48, timedelta(seconds=7200)),
        ]

    mocker.patch(
        # Dataset is in slow.py, but imported to main.py
        'rides.rides_repository.RidesRepository.get_all',
        mock_get_all
    )

    assert ridesService.compute_cost(0) == 121
    assert ridesService.compute_cost(1) == 241


def test_should_compute_overlapping_fare(mocker):
    def mock_get_all(self) -> List[Ride]:
        return [
            Ride(0, datetime.fromisoformat('2020-01-01T23:00:00'), 192, timedelta(seconds=28800)),
        ]

    mocker.patch(
        # Dataset is in slow.py, but imported to main.py
        'rides.rides_repository.RidesRepository.get_all',
        mock_get_all
    )

    assert ridesService.compute_cost(0) == 901.0


def test_should_raise_ride_not_found(mocker):
    with pytest.raises(RideNotFound):
        def mock_get_all(self) -> List[Ride]:
            return [
                Ride(0, datetime.fromisoformat('2020-01-01T23:00:00'), 192, timedelta(seconds=28800)),
            ]

        mocker.patch(
            # Dataset is in slow.py, but imported to main.py
            'rides.rides_repository.RidesRepository.get_all',
            mock_get_all
        )

        assert ridesService.compute_cost(1) == 1

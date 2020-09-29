from datetime import time, datetime, date, timedelta
from itertools import cycle
from typing import List

from load_config import RidesConfigLoader
from models import Ride
from rides.rides_repository import RidesRepository
from utils import pairwise


class RidesService:
    def __init__(self, repository: RidesRepository, config_loader):
        self.__repository = repository
        self.rides_config = config_loader.rides_config

    def get(self, ride_id: int) -> Ride:
        return self.__repository.get(ride_id)

    def get_all(self) -> List[Ride]:
        return self.__repository.get_all()

    def compute_cost(self, ride_id: int):
        ride = self.get(ride_id)
        initial_fare = self.rides_config.initial_fare
        distance_rate_cost = self.rides_config.distance_rate_cost

        if ride.duration.total_seconds() == 0 or ride.distance == 0:
            return 0

        speed = ride.distance / ride.duration.total_seconds()  # distance / sec
        cost = initial_fare
        ride_fares = self.__compute_ride_fares(ride)
        for ride_fare in ride_fares:
            cost = cost + RidesService.__compute_cost_for_slot(speed, ride_fare[0], distance_rate_cost, ride_fare[1])
        return cost

    def __compute_ride_fares(self, ride: Ride):
        slot_fares = self.rides_config.slot_fares
        remaining_duration = ride.duration
        ride_fares = []
        start_time = ride.startTime.time()

        for current_slot_fare, next_slot_fare in cycle(pairwise(slot_fares + [slot_fares[0]])):
            if start_time < next_slot_fare.start or next_slot_fare.start == time(0, 0, 0):
                slot_duration = RidesService.__compute_slot_duration(current_slot_fare, next_slot_fare)
                ride_end_time = (ride.startTime + ride.duration).time()

                is_ride_end_in_slot = current_slot_fare.start <= ride_end_time and remaining_duration <= slot_duration
                if is_ride_end_in_slot:
                    ride_fares.append((remaining_duration, current_slot_fare.fare))
                    remaining_duration = timedelta(0)
                else:
                    slot_fare_end = datetime.combine(date.min, current_slot_fare.start) + slot_duration
                    ride_in_slot_duration = slot_fare_end - datetime.combine(date.min, start_time)
                    remaining_duration = remaining_duration - ride_in_slot_duration
                    ride_fares.append((ride_in_slot_duration, current_slot_fare.fare))
                    start_time = slot_fare_end.time()

                if remaining_duration <= timedelta(0):
                    break

        return ride_fares

    @staticmethod
    def __compute_slot_duration(current_slot_fare, next_slot_fare):
        # handle midnight case by adding a day which allows the following subtraction :
        # 01/01/01 20:00:00 - 02/01/01 00:00:00 = 4h
        if next_slot_fare.start == time(0, 0, 0):
            slot_duration = datetime.combine(date.min + timedelta(days=1),
                                             next_slot_fare.start) - datetime.combine(date.min,
                                                                                      current_slot_fare.start)
        else:
            slot_duration = datetime.combine(date.min, next_slot_fare.start) - datetime.combine(date.min,
                                                                                                current_slot_fare.start)
        return slot_duration

    @staticmethod
    def __compute_cost_for_slot(speed, duration, fare_per_distance, slot_fare):
        return (speed * duration.total_seconds() / fare_per_distance) * slot_fare

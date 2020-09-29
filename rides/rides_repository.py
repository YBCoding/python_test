import json
from typing import List

from models import RideSchema, Ride
from rides.exception import RideNotFound


class RidesRepository:

    def get(self, ride_id: int) -> Ride:
        try:
            ride = next(ride for ride in self.get_all() if ride.id == ride_id)
        except StopIteration:
            raise RideNotFound("Ride {} does not exist".format(ride_id))  # Should be a 400 or 404 (resource not found)
        return ride

    def get_all(self) -> List[Ride]:
        with open('rides_examples.json', 'r') as rides_examples_file:
            return [RideSchema().load(ride) for ride in json.load(rides_examples_file)]

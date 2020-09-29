import json

from models import RidesConfigSchema, RidesConfig
from utils import pairwise


class ConfNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class ConfValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class RidesConfigLoader:
    rides_config: RidesConfig

    def __init__(self, file):
        self.rides_config = self.__load(file)
        self.__validate()

    def __load(self, file):
        if file is None:
            raise ConfNotFound("rides_config.json is not found")
        with open(file, 'r') as rides_config_file:
            rides_config: RidesConfig = RidesConfigSchema().load(json.load(rides_config_file))
            rides_config.slot_fares.sort(key=lambda x: x.start)
            return rides_config

    def __validate(self):
        for slot_fare_current, slot_fare_next in pairwise(self.rides_config.slot_fares):
            if slot_fare_current.start == slot_fare_next.start or slot_fare_current.end > slot_fare_next.start:
                raise ConfValidationError("slot fares are overlapping")

from dataclasses import dataclass, field
from datetime import datetime, timedelta, time
from typing import List

import marshmallow_dataclass


@dataclass
class SlotFareConfig:
    start: time = field(metadata={"required": True})
    end: time = field(metadata={"required": True})
    fare: float = field(metadata={"required": True})


@dataclass
class RidesConfig:
    distance_unit: str = field(metadata={"required": True})
    currency: str = field(metadata={"required": True})
    distance_rate_cost: float = field(metadata={"required": True})
    initial_fare: float = field(metadata={"required": True})
    slot_fares: List[SlotFareConfig] = field(default_factory=list, metadata={"required": True})


@dataclass
class SlotFare:
    start: time
    fare: time


@dataclass
class Ride:
    id: int
    startTime: datetime
    distance: int
    duration: timedelta


RidesConfigSchema = marshmallow_dataclass.class_schema(RidesConfig)
RideSchema = marshmallow_dataclass.class_schema(Ride)

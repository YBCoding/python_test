from flask import Blueprint, jsonify, abort

from load_config import RidesConfigLoader
from models import RideSchema
from rides.exception import RideNotFound
from rides.rides_repository import RidesRepository
from rides.rides_service import RidesService

rides_bp = Blueprint('rides_bp', __name__)

ridesRepository = RidesRepository()
ridesService = RidesService(ridesRepository, RidesConfigLoader("rides_config.json"))


@rides_bp.route('/', methods=['GET'])
def get_all():
    rides = ridesService.get_all()
    return RideSchema().dumps(rides, many=True)


@rides_bp.route('/<int:ride_id>/cost', methods=['GET'])
def get_ride_cost(ride_id: int):
    try:
        return jsonify(ridesService.compute_cost(ride_id))
    except RideNotFound as err:
        abort(404, err)

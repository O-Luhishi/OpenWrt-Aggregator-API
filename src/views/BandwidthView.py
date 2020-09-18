from flask import request, g, Blueprint, json, Response
from ..models.BandwidthModel import BandwidthModel, BandwidthSchema
from ..shared.Bandwidth import Bandwidth

bandwidth_api = Blueprint('bandwidth_api', __name__)
bandwidth_schema = BandwidthSchema()


@bandwidth_api.route('/get_live_info', methods=['GET'])
def get_live_bandwidth_info():
    """
    Get Live Bandwidth Test
    """
    speed = Bandwidth()
    result = speed.get_bandwidth_info()
    data = bandwidth_schema.load(result)
    post = BandwidthModel(data)
    post.save()
    data = bandwidth_schema.dump(post)
    return return_response(data, 200)


@bandwidth_api.route('/get_all', methods=['GET'])
def get_all_bandwidth_tests():
    """
    Get All Bandwidth Tests From DB
    """
    result = BandwidthModel.get_all_bandwidth_tests()
    if not result:
        return return_response({'error': 'No Bandwidth Tests Found'}, 404)
    ser_result = bandwidth_schema.dump(result, many=True)
    return return_response(ser_result, 200)


@bandwidth_api.route('/get_info', methods=['GET'])
def get_bandwidth_info():
    """
    Get Latest Bandwidth Tests From DB
    """
    result = BandwidthModel.get_latest_bandwidth_tests()
    if not result:
        return return_response({'error': 'No Bandwidth Tests Found'}, 404)
    ser_result = bandwidth_schema.dump(result)
    return return_response(ser_result, 200)


def return_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

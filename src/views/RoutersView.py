from flask import request, json, Response, Blueprint
from marshmallow import ValidationError
from ..models.RouterModel import RouterModel, RouterSchema
from ..shared.VaultAPIClient import VaultAPIClient

router_api = Blueprint('routers', __name__)
router_schema = RouterSchema()


@router_api.route('/add/<router_ip>', methods=['GET'])
def add_router(router_ip):
    """
    Scan Devices On A Network & Store Them In DB
    """
    # Validates Whether Router Exists By Performing Health Check
    vault = VaultAPIClient(router_ip)
    response, status_code = vault.perform_health_check()
    if status_code == 404:
        return return_response(dict(Router_Add_Failure=response), status_code)
    router_data = dict(ip_address=router_ip, status=True)
    # If Router Passes Health Check Append To Database
    try:
        data = router_schema.load(router_data)
        ip_in_db = RouterModel.get_router_id_by_ip(router_ip)
        if ip_in_db:
            return return_response({'Router-Add-Failure': 'IP-Already-Exists'}, 400)
        post = RouterModel(data)
        post.save()
    # Throw Exception If Duplication Occurs And Slips Through The Sanitation Above
    except ValidationError as err:
        return return_response(err.messages, 400)
    return return_response({'Router-Add': 'Success'}, 201)


@router_api.route('/get_all', methods=['GET'])
def get_all_routers():
    """
    Get All Routers
    """
    result = RouterModel.get_all_routers()
    if not result:
        return return_response({'error': 'No Routers Found'}, 404)
    ser_result = router_schema.dump(result, many=True)
    return return_response(ser_result, 200)


@router_api.route('/get_router_by/id/<router_id>', methods=['GET'])
def get_router_by_id(router_id):
    """
    Get All Routers
    """
    result = RouterModel.get_router_by_id(router_id)
    if not result:
        return return_response({'error': 'No Routers Found'}, 404)
    ser_result = router_schema.dump(result)
    return return_response(ser_result, 200)


@router_api.route('/get_router_by/ip/<router_ip>', methods=['GET'])
def get_router_by_ip(router_ip):
    """
    Get All Routers
    """
    result = RouterModel.get_router_by_ip(router_ip)
    if not result:
        return return_response({'error': 'No Routers Found'}, 404)
    ser_result = router_schema.dump(result)
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

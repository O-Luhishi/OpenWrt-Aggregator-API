# TODO: Create Error Handling For IP's That Don't Exist When PortScanning

from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.PortScanModel import PortScanModel, PortScanSchema
from ..models.DevicesModel import DeviceModel, DeviceSchema
from ..shared.VaultAPIClient import VaultAPIClient


portscan_api = Blueprint('portscan_api', __name__)
portscan_schema = PortScanSchema()


@portscan_api.route('/scan/<device_ip>', methods=['GET'])
# @Auth.auth_required
def portscan(device_ip):
    """
    Create PortScan Function
    """
    vault = VaultAPIClient("192.168.8.1")
    portscan_results = vault.perform_port_scan(device_ip)
    device_id = int(str(DeviceModel.get_device_by_ip(device_ip)))
    results = {"device_id": device_id, "results": str(portscan_results)}
    data = portscan_schema.load(results)
    post = PortScanModel(data)
    post.save()
    data = portscan_schema.dump(post)
    return return_response(data, 201)


@portscan_api.route('/get_all', methods=['GET'])
def get_all_portscan_results():
    """
    Get All PortScan Results
    """
    result = PortScanModel.get_all_portscans()
    if not result:
        return return_response({'error': 'No PortScans Not Found'}, 404)
    ser_result = portscan_schema.dump(result, many=True)
    return return_response(ser_result, 200)


@portscan_api.route('/get_by_scan_id/<int:scan_id>', methods=['GET'])
def get_portscan_result_by_scan_id(scan_id):
    """
    Get PortScan Results By Scan ID
    """
    result = PortScanModel.get_portscan_by_scan_id(scan_id)
    if not result:
        return return_response({'error': 'PortScan Not Found'}, 404)
    ser_result = portscan_schema.dump(result)
    return return_response(ser_result, 200)


@portscan_api.route('/get_by_device_id/<int:device_id>', methods=['GET'])
def get_portscan_result_by_device_id(device_id):
    """
    Get PortScan Results By Device ID
    """
    result = PortScanModel.get_portscan_by_device_id(device_id)
    if not result:
        return return_response({'error': 'PortScan Not Found'}, 404)
    ser_result = portscan_schema.dump(result, many=True)
    return return_response(ser_result, 200)


@portscan_api.route('/get_by_device_ip/<device_ip>', methods=['GET'])
def get_portscan_result_by_ip_address(device_ip):
    """
    Get PortScan Results By Device IP Address
    """
    try:
        device_id = int(str(DeviceModel.get_device_by_ip(device_ip)))
    except ValueError:
        return return_response({'Error': 'IP Address Not Found'}, 404)
    result = PortScanModel.get_portscan_by_device_id(device_id)
    if not result:
        return return_response({'error': 'PortScan Not Found'}, 404)
    ser_result = portscan_schema.dump(result, many=True)
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

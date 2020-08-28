# TODO: Create Error Handling For IP's That Don't Exist When PortScanning Or Fetching Results
# TODO: Create Get_Portscan_Results Function By ID/IP

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
    device_id = int(str(DeviceModel.get_device_id_by_ip(device_ip)))
    results = {"device_id": device_id, "results": str(portscan_results)}
    data = portscan_schema.load(results)
    post = PortScanModel(data)
    post.save()
    data = portscan_schema.dump(post)
    return return_response(data, 201)


def return_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

from flask import request, json, Response, Blueprint
from marshmallow import ValidationError
from ..models.DevicesModel import DeviceModel, DeviceSchema
from ..shared.Authentication import Auth
from ..shared.VaultAPIClient import VaultAPIClient

device_api = Blueprint('devices', __name__)
device_schema = DeviceSchema()


# TODO: Update Vault-API With Dict Keys

@device_api.route('/scan', methods=['GET'])
# @Auth.auth_required -- TBD
def scan():
    """
    Create Device Function
    """
    vault = VaultAPIClient("192.168.8.1")
    devices = vault.perform_network_map().json()
    for device in range(len(devices['Clients'])):
        js = devices['Clients'][device]
        try:
            data = device_schema.load(js)
            ip_in_db = DeviceModel.get_device_by_ip(data.get('ip_address'))
            if ip_in_db:
                continue
            device = DeviceModel(data)
            device.save()
        except ValidationError as err:
                return custom_response(err.messages, 400)
    # JWT Config
    # ser_data = device_schema.dump(device).data
    # token = Auth.generate_token(ser_data.get('id'))
    # return custom_response({'jwt_token': token}, 201)

    return custom_response({'Network-Scan': 'Success'}, 201)


@device_api.route('/getalldevices', methods=['GET'])
def get_all_devices():
    devices = DeviceModel.get_all_devices()
    ser_devices = device_schema.dump(devices, many=True)
    return custom_response(ser_devices, 200)


@device_api.route('/get_device_by/id/<int:device_id>', methods=['GET'])
def get_device_by_id(device_id):
    """
    Get a single device by ID
    """
    device = DeviceModel.get_one_device(device_id)
    if not device:
        return custom_response({'error': 'Device not found'}, 404)
    ser_device = device_schema.dump(device)
    return custom_response(ser_device, 200)


@device_api.route('/get_device_by/ip/<device_ip>', methods=['GET'])
def get_device_by_ip(device_ip):
    """
    Get a single device by IP
    """
    device = DeviceModel.get_device_by_ip(device_ip)
    if not device:
        return custom_response({'error': 'Device not found'}, 404)

    ser_device = device_schema.dump(device)
    return custom_response(ser_device, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


# @device_api.route('/login', methods=['POST'])
# def login():
#     req_data = request.get_json()
#
#     data, error = device_schema.load(req_data, partial=True)
#
#     if error:
#         return custom_response(error, 400)
#
#     if not data.get('email') or not data.get('password'):
#         return custom_response({'error': 'you need email and password to sign in'}, 400)
#
#     user = DeviceModel.get_user_by_email(data.get('email'))
#
#     if not user:
#         return custom_response({'error': 'invalid credentials'}, 400)
#
#     if not user.check_hash(data.get('password')):
#         return custom_response({'error': 'invalid credentials'}, 400)
#
#     ser_data = device_schema.dump(user).data
#
#     token = Auth.generate_token(ser_data.get('id'))
#
#     return custom_response({'jwt_token': token}, 200)

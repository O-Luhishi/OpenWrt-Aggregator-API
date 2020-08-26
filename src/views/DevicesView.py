from flask import request, json, Response, Blueprint
from ..models.DevicesModel import DeviceModel, DeviceSchema
from ..shared.Authentication import Auth
from ..shared.VaultAPIClient import VaultAPIClient

device_api = Blueprint('devices', __name__)
device_schema = DeviceSchema()


# TODO: Update Vault-API With Dict Keys
# TODO  Add Error Handling For Creating New Devices & Duplicates In DB
# TODO  Add Function To Read 1 Device Details From IP or ID

@device_api.route('/append', methods=['GET'])
def create():
    """
    Create Device Function
    """
    x = VaultAPIClient("192.168.8.1")
    req_data = x.perform_network_map().json()
    for x in range(len(req_data['Clients'])):
        js = {"name": req_data['Clients'][x]['Hostname'],
              "mac_address": req_data['Clients'][x]['MAC'],
              "ip_address": req_data['Clients'][x]['IP'],
              "status": True}
        data = device_schema.load(js)

        # if error:
        #     return custom_response(error, 400)

        # check if device already exist in the db
        # ip_in_db = DeviceModel.get_device_by_ip(data.get('ip_address'))
        # if ip_in_db:
        #     message = {'error': 'Device already exist, please supply ip address'}
        #     return custom_response(message, 400)

        device = DeviceModel(data)
        device.save()

    # JWT Config
    # ser_data = device_schema.dump(device).data
    # token = Auth.generate_token(ser_data.get('id'))
    # return custom_response({'jwt_token': token}, 201)

    return custom_response({'Devices-Added': 'Success'}, 201)


@device_api.route('/getalldevices', methods=['GET'])
# @Auth.auth_required
def get_all_devices():
    devices = DeviceModel.get_all_devices()
    ser_devices = device_schema.dump(devices, many=True)
    return custom_response(ser_devices, 200)


@device_api.route('/<int:device_id>', methods=['GET'])
# @Auth.auth_required
def get_a_user(device_id):
    """
    Get a single user
    """
    device = DeviceModel.get_one_device(device_id)
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

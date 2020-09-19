from flask import Flask

from .config import app_config
from .models import db

from .views.DevicesView import device_api as device_blueprint
from .views.PortScanView import portscan_api as portscan_blueprint
from .views.BandwidthView import bandwidth_api as bandwidth_blueprint
from .views.RoutersView import router_api as router_blueprint


def create_app(env_name):
    """
    Create app
    """

    # app initialisation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    db.init_app(app)

    app.register_blueprint(device_blueprint, url_prefix='/api/v1/devices')
    app.register_blueprint(portscan_blueprint, url_prefix='/api/v1/portscan')
    app.register_blueprint(bandwidth_blueprint, url_prefix='/api/v1/bandwidth')
    app.register_blueprint(router_blueprint, url_prefix='/api/v1/routers')

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return dict(Vault_Processor_Healthcheck="Healthy")

    return app

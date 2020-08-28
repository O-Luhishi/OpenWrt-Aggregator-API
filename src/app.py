from flask import Flask

from .config import app_config
from .models import db

from .views.DevicesView import device_api as device_blueprint
from .views.PortScanView import portscan_api as portscan_blueprint


def create_app(env_name):
    """
    Create app
    """

    # app initialisation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    db.init_app(app)

    app.register_blueprint(device_blueprint, url_prefix='/api/v1/devices')  # add this line
    app.register_blueprint(portscan_blueprint, url_prefix='/api/v1/portscan')  # add this line

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return 'Congratulations! Your first endpoint is working'

    return app

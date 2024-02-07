import os
import configparser
import logging.config
from flask import Flask
from flask_cors import CORS
from OpenSSL import SSL
from api.restx import api
from flask import Blueprint
from api.geo3bcn import ns as geo3bcn_namespace
from api.epos import ns as epos_namespace

REQUIRED_CONFIG_FIELDS = {
    'paths': ['volcano', 'type', 'incoming', 'temp', 'version', 'trash', 'crt', 'key'],
    'webserver': ['host', 'port'],
    'flask': ['SERVER_NAME', 'DEBUG', 'SWAGGER_UI_DOC_EXPANSION', 'RESTX_VALIDATE',
              'RESTX_MASK_SWAGGER', 'RESTX_ERROR_404_HELP']
}


def initialize_app(flask_app, log, config_file_path):
    """
    Initializes the Flask application with configurations, logging, and API namespaces.

    :param flask_app: Instance of the Flask app
    """
    set_config(flask_app, log, config_file_path)
    # Registering API namespaces
    api.add_namespace(geo3bcn_namespace)
    api.add_namespace(epos_namespace)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    flask_app.register_blueprint(blueprint)


def set_config(flask_app, log, config_file_path):
    """
    Reads the configuration from the config.ini file and sets it to the Flask application.

    :param flask_app: Instance of the Flask app
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)
    for section in REQUIRED_CONFIG_FIELDS:
        flask_app.config[section] = {}
        for option in REQUIRED_CONFIG_FIELDS[section]:
            try:
                value = config.get(section, option)
                flask_app.config[section][option] = value if section != 'flask' else flask_app.config[option]
            except configparser.NoOptionError:
                log.error(f"ERROR, {section} {option} not set, check your config.ini.")

    flask_app.config['paths']['current'] = os.path.dirname(os.path.abspath(__file__)) + '/'


def create_app(log, config_file_path):
    # Configurable parameters

    # SSL Context setup
    context = SSL.Context(SSL.SSLv23_METHOD)
    app = Flask(__name__)
    # CORS(app)
    initialize_app(app, log, config_file_path)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8080"]}})
    return app


def create_log():
    # Configuración de logging
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './logging.conf'))
    logging.config.fileConfig(logging_conf_path)
    log = logging.getLogger(__name__)
    return log

import logging
from flask_restx import Api

# Configure logging for the current module.
log = logging.getLogger(__name__)

# Description of the API. It can be more detailed to provide a better understanding of the purpose and capabilities of the API.
description = 'API for Volcanbox, a volcanic risk prevention platform. Provides access and functionalities for the web applications of Volcanbox.'

# Initialize the API instance with version, title, and description.
api = Api(version='1.0', title='Volcanbox Rest API', description=description)


# Decorator to globally handle errors in the API.
@api.errorhandler
def default_error_handler(e):
    """
    Default error handler.
    Gets triggered when an exception is not caught and handled by a custom error handler.

    Args:
        e (Exception): The unhandled exception that was caught.

    Returns:
        Tuple: An error response in JSON format and the HTTP status code 500.
    """
    message = 'An unhandled exception occurred.'
    # Log the exception along with a message. This is useful for debugging and error logging.
    log.exception(message)

    # TODO: Consider returning a more descriptive error response or a custom HTTP status code if needed.
    # The commented condition (config['FLASK_DEBUG']) can be used to return more detailed error messages in debug mode.
    # if not config['FLASK_DEBUG']:
    return {'message': message}, 500

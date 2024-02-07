import os
from __init__ import create_app, create_log


def main():
    """
    Main function to start the Flask application.
    """
    config_file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'config.ini'))
    log = create_log()
    app = create_app(log, config_file_path)

    cer = app.config['paths']['crt']
    key = app.config['paths']['key']
    context = (cer, key)

    log.info(
        f'>>>>> Starting development server at http://{app.config["webserver"]["host"]}:{app.config["webserver"]["port"]}/api/ <<<<<')
    app.run(host=app.config['webserver']['host'])  # Consider using host and port from config
    # app.run(host=app.config['webserver']['host'], port=app.config['webserver']['port'], ssl_context=context, debug=app.config['flask']['FLASK_DEBUG'])


if __name__ == "__main__":
    main()

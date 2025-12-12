import os

from flask import Flask

from qr_payment_cz.web_app.web_server_app import WebServerApp


def main():
    static_folder = os.path.join(os.path.dirname(__file__), "resources/static")
    templates_folder = os.path.join(os.path.dirname(__file__), "resources/templates")
    flask_app = Flask(__name__, static_folder=static_folder, template_folder=templates_folder)
    server_app = WebServerApp(flask_app)
    flask_app.run(host=server_app.app_args.host, port=server_app.app_args.port)


if __name__ == "__main__":
    main()

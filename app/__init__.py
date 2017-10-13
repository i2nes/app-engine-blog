from flask import Flask


def create_app(config_name):

    app = Flask(__name__)
    app.config.update(config_name)

    from .main import app as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    return app

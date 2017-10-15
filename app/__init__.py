from flask import Flask


def create_app(config_name):

    app = Flask(__name__)
    app.config.update(config_name)

    from .main import app as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .editor import app as editor_blueprint
    app.register_blueprint(editor_blueprint, url_prefix='/editor')

    return app

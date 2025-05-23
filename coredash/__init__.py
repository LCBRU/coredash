from flask import Flask
from coredash.model.security import User
from .ui import blueprint as ui_blueprint
from .config import Config
from .admin import init_admin
from lbrc_flask import init_lbrc_flask, ReverseProxied
from lbrc_flask.security import init_security, Role
from lbrc_flask.celery import init_celery


def create_app(config=Config):
    app = Flask(__name__)
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    app.config.from_object(config)

    TITLE = 'coredash'

    with app.app_context():
        init_lbrc_flask(app, TITLE)

        init_security(app, user_class=User, role_class=Role)
        init_admin(app, TITLE)
        init_celery(app, TITLE)

    app.register_blueprint(ui_blueprint)

    return app

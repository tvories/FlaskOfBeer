from flask import Flask
from flask_bootstrap import Bootstrap
from config import config, Config
from flask_moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    celery.conf.update(app.config)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .sensors import sensors as sensors_blueprint
    app.register_blueprint(sensors_blueprint)
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app

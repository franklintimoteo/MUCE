import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
boostrap = Bootstrap()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # initialize configs
    db.init_app(app)
    boostrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

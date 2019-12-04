import os
from flask import Flask
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail

db = SQLAlchemy()
boostrap = Bootstrap()
mail = Mail()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # configure your email
    app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_SENDER'] = os.environ.get('MAIL_SENDER')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['DDNS'] = os.environ.get('DDNS')
    ###################

    # initialize configs
    db.init_app(app)
    boostrap.init_app(app)
    mail.init_app(app)

    app.cli.add_command(init_db_command)

    from .main import main as main_blueprint
    from .main import error_bp
    app.register_blueprint(main_blueprint)
    app.register_blueprint(error_bp)

    return app


def init_db():
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize database tables"""
    init_db()
    click.echo("Database created!")

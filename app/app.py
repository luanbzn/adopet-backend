import os
from .blueprints.tutor import tutor_blueprint
from .extensions import db
from flask import Flask
from dotenv import load_dotenv


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PWD")}@{os.getenv("POSTGRES_SERVER")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DATABASE")}'
    db.init_app(app)
    app.register_blueprint(tutor_blueprint)
    return app

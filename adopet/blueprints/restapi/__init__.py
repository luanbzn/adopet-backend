from flask import Blueprint
from flask_restx import Api
from .resources import TutorResource, TutorResourceItem, ns

bp = Blueprint('restapi', __name__, url_prefix = '/api/v1')
api = Api(
    bp, version='1.0', title='Adopet Backend API', 
    description='Backend API developed for the Alura Challenge 6.'
)
api.add_namespace(ns)


def init_app(app):
    app.register_blueprint(bp)
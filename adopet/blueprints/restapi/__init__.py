from flask import Blueprint
from flask_restful import Api
from .resources import CaretakerResource, CaretakerResourceItem

bp = Blueprint('restapi', __name__, url_prefix = '/api/v1')
api = Api(bp)
api.add_resource(CaretakerResource, '/caretaker/', '/caretaker')
api.add_resource(CaretakerResourceItem, '/caretaker/<id>')

def init_app(app):
    app.register_blueprint(bp)
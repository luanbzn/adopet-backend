from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib import sqla

from adopet.extensions.database import db, Caretaker

admin = Admin()

def init_app(app):
    admin.name = app.config.TITLE
    admin.init_app(app)
    admin.add_view(sqla.ModelView(Caretaker, db.session))

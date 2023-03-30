import datetime
from flask import abort, jsonify, request
from flask_restful import Resource

from adopet.extensions.database import db, Caretaker


class CaretakerResource(Resource):
    def get(self):
        try:
            caretakers = Caretaker.query.all()
            return jsonify(
                {'caretakers':[caretaker.to_dict() for caretaker in caretakers]}
            )
        except Exception as e:
            return f'{e}', 204
        
    def post(self):
        try:
            new_caretaker = Caretaker(
                name = request.form['name'],
                email = request.form['email'],
                password = request.form['password']
            )
            now = datetime.datetime.now()
            new_caretaker.created_at = now
            new_caretaker.updated_at = now 
            db.session.add(new_caretaker)
            db.session.commit()
            return {'message': 'Caretaker successfully created.'}, 201
        except Exception as e:
            db.session.rollback()
            return abort(400, f"{e}")


class CaretakerResourceItem(Resource):
    def get(self, id:int):
        try:
            caretaker = Caretaker.query.filter_by(id=id).first()
            return jsonify(caretaker.to_dict())
        except Exception as e:
            return f'{e}', 204
    
    def delete(self, id:int):
        caretaker = Caretaker.query.filter_by(id=id).first() or abort(204)
        if not caretaker.deleted_at:
            now = datetime.datetime.now()
            caretaker.updated_at = now
            caretaker.deleted_at = now
            db.session.commit()
            return {'message': 'Caretaker successfully deleted.'}, 204
        return abort(400, "This caretaker isn't active.")
    
    def put(self, id:int):
        caretaker = Caretaker.query.filter_by(id=id).first() or abort(204)
        fields_in_form = {k: v for (k, v) in request.form.items() if v != ""}
        caretaker_keys = Caretaker.__mapper__.column_attrs.keys()
        for k, v in fields_in_form.items():
            if k in caretaker_keys:
                setattr(caretaker, k, v)
            elif k == 'password':
                caretaker.password = v
            else:
                return abort(400, "There are missing keys in the form.")
        caretaker.updated_at = datetime.datetime.now()
        db.session.commit()
        return {'message': 'Caretaker successfully updated.'}, 204


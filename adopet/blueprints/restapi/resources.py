import datetime
from flask import abort, jsonify
from flask_restx import Resource, Namespace, fields

from adopet.extensions.database import db, Tutor

ns = Namespace('Tutor', description="Operations with tutor")
new_tutor_model = ns.model('TutorModel', {
    'name': fields.String(required=True, description='The name of the tutor'),
    'email': fields.String(required=True, description='The email address of the tutor'),
    'password': fields.String(required=True, description='The password of the tutor'),
    'phone': fields.String(required=False, description='The phone number of the tutor'),
    'city': fields.String(required=False, description='The city of the tutor'),
    'photo': fields.String(required=False, description='An URL path to the profile photo of the tutor')
})


def process_payload(payload:dict, tutor:object) -> object:
    """Process a payload and set each key value to the appropriate key value in the tutor object."""
    fields_in_form = {k: v for (k, v) in payload if v != ""}
    tutor_keys = Tutor.__mapper__.column_attrs.keys()
    for k, v in fields_in_form.items():
        if k in tutor_keys:
            setattr(tutor, k, v)
        elif k == 'password':
            tutor.password = v
        else:
            raise Exception(f'The key {k} does not exist.')
    return tutor


@ns.route('/')
class TutorResource(Resource):
    def get(self):
        '''Return all tutors.'''
        try:
            tutors = Tutor.query.all()
            return jsonify(
                {'tutors':[tutor.to_dict() for tutor in tutors]}
            )
        except Exception as e:
            return e, 400

    @ns.expect(new_tutor_model)
    @ns.response(201, 'Tutor successfully created.')
    @ns.response(400, 'Bad request.')
    def post(self):
        """Create a new tutor."""
        try:
            new_tutor = process_payload(payload=ns.payload.items(), tutor=Tutor())
            now = datetime.datetime.now()
            new_tutor.created_at = now
            new_tutor.updated_at = now
            db.session.add(new_tutor)
            db.session.commit()
            return 'Tutor successfully created.', 201
        except Exception as e:
            db.session.rollback()
            return abort(400, f"{e}")

@ns.route('/<int:id>')
@ns.param('id', 'The tutor identifier.')
@ns.response(404, 'Tutor not found.')
class TutorResourceItem(Resource):
    def get(self, id:int):
        """Return a tutor based on the specified identifier."""
        tutor = Tutor.query.filter_by(id=id).first() or abort(404 ,'Tutor not found.')
        return jsonify(tutor.to_dict())
    
    
    @ns.response(204, 'Tutor successfully deleted.')
    @ns.response(400, "The tutor isn't active.")
    def delete(self, id:int):
        """Delete a tutor based on the specified identifier."""
        tutor = Tutor.query.filter_by(id=id).first() or abort(404, 'Tutor not found.')
        if not tutor.deleted_at:
            now = datetime.datetime.now()
            tutor.updated_at = now
            tutor.deleted_at = now
            db.session.commit()
            return 'Tutor successfully deleted.', 204
        return abort(400, "This tutor isn't active.")


    @ns.response(204, 'Tutor successfully updated.')
    @ns.response(400, 'Bad request.')
    @ns.expect(new_tutor_model)
    def put(self, id:int):
        """Update a tutor based on the specified identifier."""
        try:
            tutor = Tutor.query.filter_by(id=id).first() or abort(404, 'Tutor not found.')
            tutor = process_payload(payload=ns.payload.items(), tutor=tutor)
            tutor.updated_at = datetime.datetime.now()
            db.session.commit()
            return 'Tutor successfully updated.', 204
        except Exception as e:
            db.session.rollback()
            return abort(400, f"{e}")

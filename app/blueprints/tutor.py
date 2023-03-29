import datetime
import json
from ..extensions import db
from flask import Blueprint, jsonify, redirect, url_for, abort, request
from ..models.tutor import Tutor

tutor_blueprint = Blueprint('tutor', __name__, template_folder='blueprints')

@tutor_blueprint.route('/tutores')
def get_all_tutores():
    try:
        tutores = Tutor.query.all()
        return jsonify([tutor.serialize() for tutor in tutores]), 200
    except:
        abort(400)


@tutor_blueprint.route('/tutores/<int:id>')
def get_tutor(id):
    try:
        tutor = Tutor.query.get(id)
        return jsonify([tutor.serialize()]), 200
    except:
        abort(400)


@tutor_blueprint.route('/tutores/delete/<int:id>', methods=['POST'])
def delete_tutor(id):
    try:
        tutor = Tutor.query.get(id)
        if not tutor.deleted_at:
            tutor.deleted_at = datetime.datetime.now()
            tutor.updated_at = datetime.datetime.now()
            db.session.commit()
            return redirect(url_for('tutor.get_all_tutores')), 200
        else:
            return abort(400)
    except:
        db.session.rollback()
        return abort(400)


@tutor_blueprint.route('/tutores/update/<int:id>', methods=['POST'])
def update_tutor(id):
    try:
        tutor = Tutor.query.get(id)
        fields_in_form = {k: v for (k, v) in request.form.items() if v != ""}
        tutor_keys = Tutor.__mapper__.column_attrs.keys()
        for k, v in fields_in_form.items():
            if k in tutor_keys:
                setattr(tutor, k, v)
            elif k == 'senha':
                tutor.senha = v
            else:
                return abort(400)
        tutor.updated_at = datetime.datetime.now()
        db.session.commit()
        return redirect(url_for('tutor.get_tutor', id=tutor.id)), 200
    except:
        db.session.rollback()
        return abort(400)


@tutor_blueprint.route('/tutores/add', methods=['GET', 'POST'])
def add_tutor():
    if request.method == 'POST':
        new_tutor = Tutor(
            nome=request.form['nome'],
            email=request.form['email'],
            senha=request.form['senha']
        )
        try:
            db.session.add(new_tutor)
            db.session.commit()
            return redirect(url_for('tutor.get_tutor', id=new_tutor.id)), 200
        except:
            db.session.rollback()
            return abort(400)

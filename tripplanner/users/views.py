from flask import Blueprint, request, jsonify, g, abort

from tripplanner import db, basic_auth
from tripplanner.auth.decorators import allow_superuser_and_owner, allow_superusers_only
from tripplanner.errors.validation import ValidationError
from tripplanner.users.models import User

user_app = Blueprint('user', __name__)


@user_app.route('/users/', methods=['POST'])
def register_user():
    user = None
    try:
        user = User.create_from_json(request.get_json())
    except ValidationError:
        abort(400)

    if user:
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id, 'username': user.username}), 201


@user_app.route('/users/<int:_id>/', methods=['GET'])
@allow_superuser_and_owner
def get_user(_id):
    user = User.query.get(_id)
    if not user:
        abort(400)

    return jsonify({'username': user.username})


@user_app.route('/users/<int:_id>/', methods=['PUT'])
@allow_superuser_and_owner
def update_user(_id):
    try:
        user = User.query.get(_id)
        user.update_from_dict(request.get_json())
        db.session.add(user)
        db.session.commit()
    except ValidationError as err:
        return jsonify({'error': [f'Error validating input data: {err.get_error_message()}']}), 400
    except:
        db.session.rollback()
        return jsonify({'error': ['There was a problem updating the user']}), 400

    return jsonify({'id': user.id, 'username': user.username}), 204


@user_app.route('/users/<int:_id>/', methods=['DELETE'])
@allow_superuser_and_owner
def delete_user(_id):
    User.query.filter_by(id=_id).delete()

    return jsonify({}), 204


@user_app.route('/users/', methods=['GET'])
@allow_superusers_only
def all_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])


@user_app.route('/token/', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.user.generate_rest_auth_token()
    return jsonify({'username': g.user.username,
                    'token': token.decode('ascii'),
                    'roles': [r.name for r in g.user.roles],
                    'id': g.user.id})

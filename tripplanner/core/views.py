from flask import Blueprint, request, abort, g, jsonify
from flask import make_response

from tripplanner import db, token_auth
from tripplanner.core.models import Trip
from tripplanner.users.models import User

core_app = Blueprint('core', __name__)


@core_app.route('/')
def index_page_redirect_to_angular(**kwargs):
    with open('tripplanner/templates/index.html') as f:
        return make_response(f.read())


@core_app.route('/trips/', methods=['POST'])
@token_auth.login_required
def create_trip():
    destination = request.get_json().get('destination')
    start_date = request.get_json().get('start_date')
    end_date = request.get_json().get('end_date')
    comment = request.get_json().get('comment')
    user_id = request.get_json().get('user_id')

    if (not destination or not start_date or not end_date or
            not comment or not user_id or len(request.get_json()) > 5):
        return abort(401)

    if not g.user.is_admin() and g.user.id != user_id:
        abort(401)

    user = User.query.get(user_id)
    if not user:
        abort(404)

    t = Trip(destination, start_date, end_date, comment, user)
    db.session.add(t)
    db.session.commit()

    return jsonify({'trip_id': t.id, 'destination': t.destination}), 201

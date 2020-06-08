from flask import jsonify, request, url_for, abort
from app import db
from app.models import User, UserSchema
from app.api import bp
from app.api.auth import token_auth


@bp.route('/users', methods=['GET'])
#@token_auth.login_required
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(users)
    return jsonify(output)

# @bp.route('/users', methods=['GET'])
# def get_users():
#     pass
#
# @bp.route('/users', methods=['POST'])
# def create_user():
#     pass
#
# @bp.route('/users', methods=['POST'])
# def update_user():
#     pass
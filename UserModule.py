from flask import Blueprint, jsonify, request, make_response
from UserService import UserService
from FileStorageManager import FileStorageManager
from Exceptions import *
from dblayer import db, User

user_module = Blueprint('user_module', __name__)

@user_module.route('/api/user', methods=["GET"])
def get_users():
    return jsonify([u.serialized for u in UserService(db).all_users()])

@user_module.route('/api/user', methods=["POST"])
def add_user():
    jsonObj = request.json
    try:
        User.validate(jsonObj)
        UserService(db).create_or_update(jsonObj)
        return make_response({'success': True}, 201)
    except (ValidationError, NotFoundObjectError) as e:
        return make_response({'error': f"{e!r}"}, 400)

@user_module.route('/api/user/<user_id>/skill', methods=["GET"])
def show_skills(user_id: int):
    try:
        userService = UserService(db)
        skills = userService.get_skills(user_id)
        return jsonify([s.serialized for s in skills])
    except (ValidationError, NotFoundObjectError) as e:
        return make_response({'error':f"{e!r}"}, 400)

@user_module.route('/api/user/<user_id>', methods=["DELETE"])
def delete_user(user_id: int):
    try:
        userService = UserService(db)
        userService.delete_user(user_id)
        return make_response('',204)
    except (ValidationError, NotFoundObjectError) as e:
        return make_response({'error':F"{e!r}"}, 400)

@user_module.route('/api/user/<user_id>/skill', methods=["POST"])
def add_skills(user_id: int):
    try:
        jsonSkills = request.json
        UserService(db).update_skills(user_id, jsonSkills)
        return make_response({'success': True}, 200)
    except (ValidationError, NotFoundObjectError) as e:
        return make_response({'error':F"{e!r}"}, 400)


@user_module.route('/api/user/<int:user_id>')
def get_user(user_id):
    try:
        return UserService(db).get_by_id(user_id).serialized
    except (ValidationError, NotFoundObjectError) as e:
        return make_response({'error': F"{e!r}"}, 400)


@user_module.route('/api/user/<int:user>/cv', methods=['POST'])
def upload_file(user):
    try:
        FileStorageManager.validate_content_type(request.content_type)
        UserService(db).upload_cv(user, request.data)
        return make_response('',200)
    except (NotSupportedContentType,NotFoundObjectError) as e:
        return make_response({'error': F"{e!r}"}, 400)

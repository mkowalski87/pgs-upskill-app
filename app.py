from flask import Flask, jsonify, abort, request, make_response
from dblayer import db, User
from UserService import UserService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

@app.route('/api/user', methods=["GET"])
def getUsers():
    return jsonify([u.serialized for u in UserService(db).all_users()])

@app.route('/api/user', methods=["POST"])
def addUser():
    jsonObj = request.json
    try:
        User.validate(jsonObj)
        UserService(db).create_or_update(jsonObj)
        return make_response({'success': True}, 201)
    except Exception as e:
        return make_response({'error': f"{e!r}"}, 400)

@app.route('/api/user/<user_id>/skill', methods=["GET"])
def showSkills(user_id: int):
    try:
        userService = UserService(db)
        skills = userService.get_skills(user_id)
        return jsonify([s.serialized for s in skills])
    except Exception as e:
        return make_response({'error':e.args[0]}, 400)

@app.route('/api/user/<user_id>', methods=["DELETE"])
def deleteUser(user_id: int):
    try:
        userService = UserService(db)
        userService.delete_user(user_id)
        return make_response('',204)
    except Exception as e:
        return make_response({'error':F"{e!r}"}, 400)

@app.route('/api/user/<user_id>/skill', methods=["POST"])
def addSkills(user_id: int):
    try:
        jsonSkills = request.json
        UserService(db).update_skills(user_id, jsonSkills)
        return make_response({'success': True}, 200)
    except Exception as e:
        return make_response({'error':F"{e!r}"}, 400)


@app.route('/api/user/<int:user_id>')
def getUser(user_id):
    try:
        return UserService(db).get_by_id(user_id).serialized
    except Exception as e:
        return make_response({'error': F"{e!r}"}, 400)

if __name__ == "__main__":
    app.run()
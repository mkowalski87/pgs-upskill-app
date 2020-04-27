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
    error = User.validate(jsonObj)
    if error:
        return make_response({'error': error}, 400)
    UserService(db).create_or_update(jsonObj)
    return make_response({'success':True}, 201)

@app.route('/api/user/<user_id>/skill', methods=["GET"])
def showSkills(user_id: int):
    try:
        userService = UserService(db)
        skills = userService.get_skills(user_id)
        return jsonify([s.serialized for s in skills])
    except Exception as e:
        return make_response({'error':e.args[0]}, 400)

@app.route('/api/user/<user_id>/skill', methods=["POST"])
def addSkills(user_id: int):
    jsonSkills = request.json
    userService = UserService(db)
    userService.update_skills(user_id, jsonSkills)
    return make_response({'success':True}, 200)

@app.route('/api/user/<int:user_id>')
def getUser(user_id):
    usr = UserService(db).get_by_id(user_id)
    if usr == None:
        return abort(404)
    return usr.serialized

if __name__ == "__main__":
    app.run()
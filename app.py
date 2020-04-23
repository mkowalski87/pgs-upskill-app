from flask import Flask, jsonify, abort
from dblayer import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

@app.route('/api/user', methods=["GET"])
def getUsers():
    return jsonify([u.serialize for u in User.query.all()])

@app.route('/api/user/<int:user_id>')
def getUser(user_id):
    usr = User.query.filter(User.id == user_id).first()
    if usr == None:
        return abort(404)
    return usr.serialize
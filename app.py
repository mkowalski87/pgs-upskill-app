from flask import Flask
from dblayer import db
from UserModule import user_module

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['UPLOAD_FOLDER'] = "/temp"
db.init_app(app)

app.register_blueprint(user_module)

if __name__ == "__main__":
    app.run()
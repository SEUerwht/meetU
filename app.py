from flask import Flask,redirect
from api.api_user import bp as user_bp
from util.before_request import before_request
from model.BaseModel import db
import util.config as config

app = Flask(__name__)
ctx = app.app_context()
ctx.push()
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db.init_app(app)
db.create_all()
app.register_blueprint(user_bp)


before_request

@app.route('/')
def hello_world():
    return redirect("/user/login")


if __name__ == '__main__':
    app.run()

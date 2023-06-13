from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.client import cliente, clientes
from resources.user import Users, userRegister, userLogin, userLogout
from blacklist import blacklist

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///JunkyardFollowUP.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "DontTellAnyone"
app.config["JWT_BLACKLIST_ENABLED"] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_request
def createDataBase():
    database.create_all()

@jwt.token_in_blocklist_loader
def verifyBlacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    tokenSet = jti in blacklist
    return tokenSet is not False

@jwt.revoked_token_loader
def invalidAccessToken(jwt_header, jwt_payload):
    return jsonify({"Message": "You have been logged out."}), 401

api.add_resource(cliente, '/client/<string:codCliente>')
api.add_resource(clientes, '/client')
api.add_resource(Users, '/users/<int:codUser>')
api.add_resource(userRegister, '/register')
api.add_resource(userLogin, '/login')
api.add_resource(userLogout, '/logout')

if __name__ == '__main__':
    from SQLAlchemy import database
    database.init_app(app)
    app.run(debug=True)
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, verify_jwt_in_request
import hmac
from models.user import userModel
from blacklist import blacklist


args = reqparse.RequestParser()
args.add_argument("Login", type = str, required = True, help = "The field 'login' can't be null.")
args.add_argument("Password", type = str, required = True, help = "The field 'password' can't be null.")

class Users(Resource):

    def get(self, codUser):
        user = userModel.findUser(codUser)
        if user:
            return user.json()
        return {"message": "User not found."}, 404

    @jwt_required()
    def delete(self, codUser):
        user = userModel.findUser(codUser)
        if user:
            try:
                user.deleteUser()
            except:
                return {"Message": "An internal error ocurred trying to delete user, please try again."}, 500
            return {"Message": "User deleted."}
        return {"Message": "User not found."}, 404

class userRegister(Resource):

    def post(self):
        data = args.parse_args()

        if userModel.findByLogin(data["Login"]):
            message = "Message:" "The Login '{}' already exists.".format(data["Login"])
            return message, 400

        user = userModel(**data)
        user.saveUser()
        message = "Message:" "User created successfully!"
        return message, 201

class userLogin(Resource):

    @classmethod
    def post(cls):
        data = args.parse_args()

        user = userModel.findByLogin(data["Login"])
        str_to_bytes = lambda s: s.encode("utf-8") if isinstance(s, str) else s
        safe_str_cmp = lambda a, b: hmac.compare_digest(str_to_bytes(a), str_to_bytes(b))

        if user and safe_str_cmp(user.Password, data["Password"]):
            accessToken = create_access_token(identity=user.codUser)
            return {"accessToken": accessToken}, 200
        return {"Message": "The username or password is incorrect."}, 401

class userLogout(Resource):

    @jwt_required()
    def post(self):
        IDjwt = verify_jwt_in_request()[1]["jti"]
        blacklist.add(IDjwt)
        return {"Message": "Logged out successfully!"}, 200

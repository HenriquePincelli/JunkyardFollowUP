from SQLAlchemy import database

class userModel(database.Model):

    __tablename__ = "users"

    codUser = database.Column("Cod_Usuário", database.Integer, primary_key = True)
    Login = database.Column(database.String(100))
    Password = database.Column("Senha", database.String(100))

    def __init__(self, Login, Password):
        self.Login = Login
        self.Password = Password

    def json(self):
        return {
            "codUser": self.codUser,
            "Login": self.Login
        }

    @classmethod
    def findUser(cls, codUser):
        user = cls.query.filter_by(codUser=codUser).first()
        if user:
            return user
        return None

    @classmethod
    def findByLogin(cls, Login):
        user = cls.query.filter_by(Login=Login).first()
        if user:
            return user
        return None

    def saveUser(self):
        database.session.add(self)
        database.session.commit()
        return

    def deleteUser(self):
        database.session.delete(self)
        database.session.commit()

from SQLAlchemy import database

class clienteModel(database.Model):

    __tablename__ = "clients"

    codCliente = database.Column("Cod_Cliente", database.Integer, primary_key = True)
    codEntrega = database.Column("Cod_Entrega", database.Integer)
    nomeCliente = database.Column("Nome_Cliente", database.String(100))
    CPF = database.Column(database.Integer)
    Email = database.Column(database.String(100))
    Logradouro = database.Column(database.String(255))
    Contato = database.Column(database.String(45))
    dataHomol = database.Column("Data_Homol", database.String(100))
    dataAtualiz = database.Column("Data_Atualiz", database.String(100))
    Status = database.Column(database.Integer)

    def __init__(self, codCliente, codEntrega, nomeCliente, CPF, Email, Logradouro, Contato, dataHomol, dataAtualiz, Status):
        self.codCliente = codCliente
        self.codEntrega = codEntrega
        self.nomeCliente = nomeCliente
        self.CPF = CPF
        self.Email = Email
        self.Logradouro = Logradouro
        self.Contato = Contato
        self.dataHomol = dataHomol
        self.dataAtualiz = dataAtualiz
        self.Status = Status

    def json(self):
        return {
            "codCliente": self.codCliente,
            "codEntrega": self.codEntrega,
            "nomeCliente": self.nomeCliente,
            "CPF": self.CPF,
            "Email": self.Email,
            "Logradouro": self.Logradouro,
            "Contato": self.Contato,
            "dataHomol": self.dataHomol,
            "dataAtualiz": self.dataAtualiz,
            "Status": self.Status
        }

    @classmethod
    def findClient(cls, codCliente):
        Client = cls.query.filter_by(codCliente=codCliente).first()
        if Client:
            return Client
        return None

    def saveClient(self):
        database.session.add(self)
        database.session.commit()
        return

    def updateClient(self, codCliente, codEntrega, nomeCliente, CPF, Email, Logradouro, Contato, dataHomol, dataAtualiz, Status):
        self.codCliente = codCliente
        self.codEntrega = codEntrega
        self.nomeCliente = nomeCliente
        self.CPF = CPF
        self.Email = Email
        self.Logradouro = Logradouro
        self.Contato = Contato
        self.dataHomol = dataHomol
        self.dataAtualiz = dataAtualiz
        self.Status = Status

    def deleteClient(self):
        database.session.delete(self)
        database.session.commit()

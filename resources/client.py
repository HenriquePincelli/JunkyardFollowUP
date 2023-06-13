from flask_restful import Resource, reqparse
from models.client import clienteModel
from flask_jwt_extended import jwt_required
import sqlite3


def normalizeUrlParams(status = None, limit = 50, offset = 0, **data):
    if status == 0:
        return {
            "status": status,
            "Limit": limit,
            "Offset": offset
        }
    return {
        "status": 1,
        "Limit": limit,
        "Offset": offset
        }

urlParams = reqparse.RequestParser()
urlParams.add_argument("status", type = int)
urlParams.add_argument("Limit", type = float)
urlParams.add_argument("Offset", type = float)

class clientes(Resource):
    def get(self):
        conn = sqlite3.connect("instance//JunkyardFollowUP.db")
        cursor = conn.cursor()

        data = urlParams.parse_args()
        trueData = {key:data[key] for key in data if data[key] is not None}
        parameters = normalizeUrlParams(**data)

        consult = """SELECT * FROM clients
                    WHERE (Status = ?)
                    LIMIT ?
                    OFFSET ?"""
        consultList = tuple([parameters[key] for key in parameters])
        result = cursor.execute(consult, consultList)

        clients = []
        for line in result:
            clients.append({
                "codCliente": line[0],
                "codEntrega": line[1],
                "nomeCliente": line[2],
                "CPF": line[3],
                "Email": line[4],
                "Logradouro": line[5],
                "Contato": line[6],
                "dataHomol": line[7],
                "dataAtualiz": line[8],
                "Status": line[9]
            })
        return {"Clientes": clients}, 200

class cliente(Resource):
    args = reqparse.RequestParser()
    args.add_argument("codCliente", type = int, required = True, help = "The field 'codCliente' must be a Integer not null.")
    args.add_argument("codEntrega", type = int)
    args.add_argument("nomeCliente", type = str)
    args.add_argument("CPF", type = int)
    args.add_argument("Email", type = str)
    args.add_argument("Logradouro", type = str)
    args.add_argument("Contato", type = str)
    args.add_argument("dataHomol", type = str)
    args.add_argument("dataAtualiz", type = str, required = True)
    args.add_argument("Status", type = int, required = True)

    def get(self, codCliente):
        client = clienteModel.findClient(codCliente)
        if client:
            return client.json()
        return {"message": "Client not found."}, 404

    @jwt_required()
    def post(self, codCliente):
        if clienteModel.findClient(codCliente):
            message = f"message: Cod_Cliente '{codCliente}' already exists."
            return message, 400

        data = cliente.args.parse_args()
        client = clienteModel(**data)
        try:
            client.saveClient()
        except:
            return {"Message": "An internal error ocurred trying to save client, please try again."}, 500
        return client.json()

    @jwt_required()
    def put(self, codCliente):
        data = cliente.args.parse_args()
        clientFound = clienteModel.findClient(codCliente)
        if clientFound:
            clientFound.updateClient(**data)
            clientFound.saveClient()
            return clientFound.json(), 200
        client = clienteModel(**data)
        try:
            client.saveClient()
        except:
            return {"Message": "An internal error ocurred trying to save client, please try again."}, 500
        return client.json(), 201

    @jwt_required()
    def delete(self, codCliente):
        client = clienteModel.findClient(codCliente)
        if client:
            try:
                client.deleteClient()
            except:
                return {"Message": "An internal error ocurred trying to delete client, please try again."}, 500
            return {"Message": "Client deleted."}
        return {"Message": "Client not found."}, 404
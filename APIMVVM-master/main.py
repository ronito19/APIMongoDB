import json
from datetime import datetime
from hashlib import sha256

from flask import Flask, request

from DBHandler import DBHandler
from ResponseModel import ResponseModel

app = Flask(__name__)

PASS = "abcd1234"

def checkTokenAuth(tokenSHA256Request, USER, route):

    passSHA256 = sha256(PASS.encode('utf-8')).hexdigest()
    minutes = datetime.now().minute

    tokenString = USER + route + passSHA256 + str(minutes)
    tokenSHA256 = sha256(tokenString.encode('utf-8')).hexdigest()

    print(tokenSHA256Request)
    print(tokenSHA256)

    if tokenSHA256 == tokenSHA256Request:
        print('acceso correcto')
        return True
    else:
        print('acceso denegado')
        return False

@app.route('/images', methods=['POST','PUT','DELETE','GET'])
def images():
    print(request.json)
    response = ResponseModel()
    tokenSHA256Request = request.authorization['password']
    user = request.authorization['username']
    route = request.json['route']

    if checkTokenAuth(tokenSHA256Request, user, route):
        try:
            if request.method == 'POST':
                response = addImage(request.json['data'])
            elif request.method == 'GET':
                response = getImages(request.json['data'])
                #response = getStudent(request.json['data'])
            elif request.method == 'PUT':
                pass
                #response = updateStudent(request.json['data'])
            elif request.method == 'DELETE':
                pass
                #response = deleteStudent(request.json['data'])


        except Exception as e:
            print(e)
    else:
        response.data = 'NO TIENES ACCESO'

    return json.dumps(response.__dict__)

def addImage(image):
    response = DBHandler().insertarImagen(image)
    return response

def getImages(_idE):
    response = DBHandler().obtenerImagenes(_idE)
    return response






@app.route('/students', methods=['POST','PUT','DELETE','GET'])
def students():
    print(request.json)
    response = ResponseModel()
    tokenSHA256Request = request.authorization['password']
    user = request.authorization['username']
    route = request.json['route']

    if checkTokenAuth(tokenSHA256Request, user, route):
        try:
            if request.method == 'POST':
                response = addStudent(request.json['data'])
            elif request.method == 'GET':
                response = getStudent(request.json['data'])
            elif request.method == 'PUT':
                response = updateStudent(request.json['data'])
            elif request.method == 'DELETE':
                response = deleteStudent(request.json['data'])


        except Exception as e:
            print(e)
    else:
        response.data = 'NO TIENES ACCESO'

    return json.dumps(response.__dict__)




def deleteStudent(_idE):
    response = DBHandler().eliminarEstudiante(_idE)
    return response




def updateStudent(estudiante):
    response = DBHandler().actualizar(estudiante)
    return response



def getStudent(_idE):
    if _idE == 'all':
        response = DBHandler().obtenerEstudiantes()
    else:
        response = DBHandler().obtenerEstudiante(_idE)

    return response




def addStudent(estudiante):
    response = DBHandler().insertarEstudiante(estudiante)
    return response





if __name__ == '__main__':
    app.run(debug=True, port=8071, host='0.0.0.0')
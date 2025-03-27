from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from pydantic import BaseModel
from modelsPydantic import modelUsuario, modelAuth
from genToken import createToken
from middleWares import BearerJWT
from DB.conexion import Session, engine, Base
from models.modelsDB import User

app = FastAPI(
    title="Mi primera API-196",
    description="Gerardo Ligorio Zea",
    version="1.0.3"
)

Base.metadata.create_all(bind=engine) #Levantar las tablas en la BD

usuarios = [
    {"id": 1, "nombre": "Gerardo", "edad": 20, "correo": "gerardo@example.com"},
    {"id": 2, "nombre": "Domingo", "edad": 20, "correo": "domingo@example.com"}, 
    {"id": 3, "nombre": "Lalo", "edad": 21, "correo": "lalo@example.com"},
    {"id": 4, "nombre": "Estrella", "edad": 20, "correo": "estrella@example.com"},
]

#EndPoint para el inicio de la API
@app.get("/", tags=["Inicio"])
def main():
    return {"Hola FastAPI": "Gerardo"}

#Endpoint para generar el token
@app.post('/auth', tags=['Autenticación']) #Decorador para el endpoint
def login(autorizado:modelAuth): #Función para la autenticación
    if autorizado.correo == 'gera@gmail.com' and autorizado.passw == '123456789': #Valida el usuario y contraseña
        token:str = createToken(autorizado.model_dump()) #Genera el token
        print(token)
        return JSONResponse(content={"token": token}) #Regresa el token generado
    else:
         return {"Aviso": "Usuario no Autorizado"} #Regresa un mensaje de error

#Endpoint para mostrar todos los usuarios
@app.get("/usuarios", dependencies=[Depends(BearerJWT())], response_model = List[modelUsuario], tags=["Operaciones CRUD"])
def ConsultarTodos():
    return usuarios

#Endpoint para agregar usuarios
@app.post("/usuarios/", response_model = modelUsuario, tags=["Operaciones CRUD"])
def AgregarUsuario(usuarioNuevo: modelUsuario):
    db = Session()
    try:
        db.add(User(**usuarioNuevo.model_dump()))
        db.commit()
        return JSONResponse(status_code=201, content={"mensaje": "Usuario guardado", "usuario": usuarioNuevo.model_dump()})
    
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=400, content={"mensaje": "No se guardó", "Excepción": str(e)})
    
    finally:
        db.close()

#Endpoint para actualizar un usuario por su id
@app.put("/usuarios/{id}", response_model = modelUsuario, tags=["Operaciones CRUD"])
def actualizarUsuario(id:int, usuario_actualizado: modelUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado.model_dump()
            return usuarios[index]
        
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#Endpoint para eliminar un usuario por su id
@app.delete("/usuarios/{id}", tags=["Operaciones CRUD"])
def eliminarUsuario(id:int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {"message" : "EL usuario fue eliminado"}
        
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
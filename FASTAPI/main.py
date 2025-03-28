from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder #Procesar objetos de Python a JSON
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

#EndPoint para el inicio de la API
@app.get("/", tags=["Inicio"])
def main():
    return {"Hola FastAPI": "Gerardo"}

#dependencies = [Depends(BearerJWT())] #Valida el token

#Endpoint para mostrar todos los usuarios
@app.get("/usuarios", tags=["Operaciones CRUD"])
def ConsultarTodos():
    db = Session()
    try:
        consulta = db.query(User).all()
        return JSONResponse(content = jsonable_encoder(consulta))
    
    except Exception as x:
        return JSONResponse(status_code=500, content={"mensaje": "No fue posible consultar los usuarios", "Excepción": str(x)})
    
    finally:
        db.close()
        
#Endpoint consulta por id
@app.get('/usuarios/{id}', tags=["Operaciones CRUD"])
def ConsultarUno(id:int):
    db = Session()
    try:
        consulta = db.query(User).filter(User.id == id).first()
        if not consulta:
            return JSONResponse(status_code=404, content={"mensaje":"Usuario no encontrado"})
        
        return JSONResponse(content = jsonable_encoder(consulta))
    
    except Exception as x:
        return JSONResponse(status_code=500, content={"mensaje": "No fue posible consultar el usuario", "Excepción": str(x)})
    
    finally:
        db.close()

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
@app.put("/usuarios/{usuario_id}", response_model=modelUsuario, tags=["Operaciones CRUD"])
def ActualizarUsuario(usuario_id: int, usuarioActualizado: modelUsuario):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == usuario_id).first()
        if not usuario:
            return JSONResponse(status_code=404, content={"mensaje": "Usuario no encontrado"})
        
        for key, value in usuarioActualizado.model_dump().items():
            setattr(usuario, key, value)
        db.commit()
        return JSONResponse(status_code=200, content={"mensaje": "Usuario actualizado", "usuario": usuarioActualizado.model_dump()})
    
    except Exception as y:
        db.rollback()
        return JSONResponse(status_code=400, content={"mensaje": "No se pudo actualizar el usuario", "Excepción": str(y)})
    finally:
        db.close()

#Endpoint para eliminar un usuario
@app.delete("/usuarios/{usuario_id}", tags=["Operaciones CRUD"])
def EliminarUsuario(usuario_id: int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == usuario_id).first()
        if not usuario:
            return JSONResponse(status_code=404, content={"mensaje": "Usuario no encontrado"})
        
        db.delete(usuario)
        db.commit()
        return JSONResponse(status_code=200, content={"mensaje": "Usuario eliminado"})
    
    except Exception as z:
        db.rollback()
        return JSONResponse(status_code=400, content={"mensaje": "No se pudo eliminar el usuario", "Excepción": str(z)})
    
    finally:
        db.close()

#Endpoint para generar el token
@app.post('/auth', tags=['Autenticación']) #Decorador para el endpoint
def login(autorizado:modelAuth): #Función para la autenticación
    if autorizado.correo == 'gera@gmail.com' and autorizado.passw == '123456789': #Valida el usuario y contraseña
        token:str = createToken(autorizado.model_dump()) #Genera el token
        print(token)
        return JSONResponse(content={"token": token}) #Regresa el token generado
    else:
         return {"Aviso": "Usuario no Autorizado"} #Regresa un mensaje de error
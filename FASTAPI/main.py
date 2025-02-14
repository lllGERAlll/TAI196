from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI(
    title="Mi primera API-196",
    description="Gerardo Ligorio Zea",
    version="1.0.2"
)

usuarios = [
    {"id": 1, "nombre": "Gerardo", "edad": 20},
    {"id": 2, "nombre": "Domingo", "edad": 20},
    {"id": 3, "nombre": "Lalo", "edad": 21},
    {"id": 4, "nombre": "Estrella", "edad": 20},
]

@app.get("/", tags=["Inicio"])
def main():
    return {"Hola FastAPI": "Gerardo"}

@app.get("/usuarios", tags=["Operaciones CRUD"])
def ConsultarTodos():
    return {"Todos los usuarios registrados": usuarios}

#endpoint para consultar un usuario por su id
@app.post("/usuarios/", tags=["Operaciones CRUD"])
def AgregarUsuario(usuario: dict):  # Usa el modelo Usuario en lugar de dict
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    usuarios.append(usuario)  
    return usuario

@app.put("/usuarios/{id}", tags=["Operaciones CRUD"])
def editarUsuario(id:int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(usuario)
            return usr
        
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.delete("/usuarios/{id}", tags=["Operaciones CRUD"])
def eliminarUsuario(id:int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {"message" : "EL usuario fue eliminado"}
        
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
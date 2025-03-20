#API para el registro de envios 
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from modelPydantic import modelEnvio

app = FastAPI(
    title = "API Envios",
    description = "Gerardo Ligorio Zea",
    version = "1.0.0"
)

class modelEnvio(BaseModel):
    cp: str
    destino: str
    peso: int

envios = [
    {"cp": "12345", "destino": "Cancun", "peso": 10},
    {"cp": "54321", "destino": "Mérida", "peso": 5}, 
    {"cp": "67890", "destino": "Tulum", "peso": 7},
    {"cp": "09876", "destino": "Querétaro", "peso": 8},
]

@app.get("/", tags="Inicio")
def main():
    return {"Examen": "Envios API"}


#Endpoin para registrar un envio y mostrar todos como resultado
@app.post("/registrarEnvio/", response_model = List[modelEnvio] ,tags="Examen") 
def registrarEnvio(envioNuevo: modelEnvio):
    for envio in envios:
        if envioNuevo.cp == envio["cp"]:
            raise HTTPException(status_code=100, detail="El envio ya existe")
        
    envios.append(envioNuevo)
    return envios

#Endpoint para eliminar un envio por su codigo postal
@app.delete("/eliminarEnvio/{cp}", tags="Examen")
def eliminarEnvio(cp: str):
    for envio in envios:
        if envio.cp == cp:
            envios.remove(envio)
            return {"message": "Envio eliminado"}
    raise HTTPException(status_code=404, detail="Envio no encontrado")
from fastapi import FastAPI
from typing import Optional

app = FastAPI(
    title = 'Mi primer API 196',
    description = 'Gerardo Ligorio Zea',
    version = '1.0.0'
)

usuarios = [
    {"id":1, "nombre":"Gerardo", "edad":21},
    {"id":2, "nombre":"Eduardo", "edad":21},
    {"id":3, "nombre":"Domingo", "edad":21},
    {"id":4, "nombre":"Estrella", "edad":21},
    {"id":5, "nombre":"Lucero", "edad":21}
]

@app.get('/',tags=['Inicio'])
def main():
    return {'hola FastAPI':'Gerardo Ligorio'}


@app.get('/promedio',tags=['Mi calificación TAI'])
def promedio():
    return  9.23

#Endpoint Parámetro Obligatorio
@app.get('/usuario/{id}',tags=['Parámetro Obligatorio'])
def consultaUsuario(id:int):
    #conectamosBF
    #hacemos consulta y retornamos resultados
    return {'Se encontró el usuario'}

#Endpoint Parámetro Opcional
@app.get('/usuario/',tags=['Parámetro Opcional'])
def consultaUsuario2(id :Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje":"Usuario encontrado", "usuario":usuario}
        return {"mensaje",f"No se encontro el id: {id}"}
    else:
        return {"mensaje":"No se proporcionó un ID"}

#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}
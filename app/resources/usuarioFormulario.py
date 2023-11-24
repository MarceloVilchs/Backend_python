import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime, date
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException



from app.auth import get_db
from app.models.model import usuarioFormularioModel

router = APIRouter(
    tags=["usuarioFormulario"],
    responses={404: {"description": "Not found"}},
)



#Metodo GET obtencion de datos
@router.get("/usuarioFormulario/GET")
async def get_usuario(name: str = None, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[usuarioFormularioModel] | usuarioFormularioModel:
    """Endpoint para obtener un dato de la base de datos"""
    # Buscar el dato por el nombre
    if name is None:
        logging.info("get all usuarios")
        try:
            data = await db["usuarioFormularios"].find().to_list(length=100)
            if data is None:
                data = []
        except Exception as err:
            logging.error(err)
        return data

    logging.info(f"get usuario with name: {name}")
    data = await db["usuarioFormularios"].find_one({"name": name})

    if data:
        # Si el dato existe, retornarlo
        return data

    else:
        # Si el dato no existe, retornar un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})



#Editar Usuario
@router.put("/usuarioFormulario/PUT")
async def put_usuario(
    nombre: str,
    data: usuarioFormularioModel,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))
):
    """Endpoint para actualizar una cita en la base de datos"""
    # Convertir el modelo a un diccionario
    data = jsonable_encoder(data)
    logging.info(f"put_usuario with nombre: {nombre} and data: {data}")

    # Actualizar la cita
    data['updated_at'] = datetime.now()
    result = await db["usuarioFormularios"].update_one(
        {"name": nombre},
        {"$set": data}
    )

    if result.modified_count == 1:
        # La cita fue actualizada exitosamente
        return JSONResponse(content={"message": "Cita actualizada correctamente"})
    else:
        # La cita no fue encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )

#Metodo Delete usuario
@router.delete("/usuarioFormulario/DELETE")
async def delete_usuario(
    nombre: str,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))
):
    """Endpoint para eliminar una cita de la base de datos"""
    logging.info(f"delete_usuario with nombre: {nombre}")

    # Eliminar la cita
    result = await db["usuarioFormularios"].delete_one({"name": nombre})

    if result.deleted_count == 1:
        # La cita fue eliminada exitosamente
        return JSONResponse(content={"message": "Cita eliminada correctamente"})
    else:
        # La cita no fue encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )



 #Post
@router.post("/usuarioFormularioP")
async def post_usuario(
    usuario_data: usuarioFormularioModel,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))
):
    """Endpoint para crear un dato en la base de datos"""
    data = jsonable_encoder(usuario_data)
    data["created_at"] = datetime.now()
    data["updated_at"] = datetime.now()

    logging.info(f"post usuarioFormularioP with: {data}")

    # Buscar si el dato ya existe
    db_data = await db["usuarioFormularios"].find_one({"email": data['email']})
    if db_data:
        # Si el dato ya existe, retornar un error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Data already exists"
        )

    # Si el dato no existe, crearlo con sus fechas de creación
    new_data = await db["usuarioFormularios"].insert_one(data)

    # Retornar el id del nuevo dato
    return JSONResponse(content={"inserted_id": str(new_data.inserted_id)})


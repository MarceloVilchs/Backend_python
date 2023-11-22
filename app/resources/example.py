import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient


from app.auth import get_db
from app.models.model import ExampleModel

router = APIRouter(
    tags=["example"],
    responses={404: {"description": "Not found"}},
)

@router.get("/example1")
async def example1():
    """Endpoint de ejemplo"""

    logging.info("Example1")
    # Retornar un mensaje de ejemplo
    return "Example1"


@router.post("/example2")
async def post_example2(data: ExampleModel, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))):
    """Endpoint para crear un dato en la base de datos"""
    # Convertir el modelo a un diccionario
    data = jsonable_encoder(data)
    logging.info(f"post example with: {data}")

    # Buscar si el dato ya existe
    db_data = await db["example"].find_one({"name": data['name']})
    if db_data:
        # Si el dato ya existe, retornar un error
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, 
                            content={"message": "Data already exists"})
    
    # Si el dato no existe, crearlo con sus fechas de creación
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    new_data = await db["example"].insert_one(data)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"

@router.get("/example2")
async def get_example2(name: str = None, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[ExampleModel] | ExampleModel:
    """Endpoint para obtener un dato de la base de datos"""
    # Buscar el dato por el nombre
    if name is None:
        logging.info("get all examples")
        try:
            data = await db["example"].find().to_list(length=100)
            if data is None:
                data = []
        except Exception as err:
            logging.error(err)
        return data

    logging.info(f"get example with name: {name}")
    data = await db["example"].find_one({"name": name})

    if data:
        # Si el dato existe, retornarlo
        return data

    else:
        # Si el dato no existe, retornar un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})

@router.put("/example2")
async def put_example2(data: ExampleModel, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="PUT"))):
    """Endpoint para actualizar un dato de la base de datos"""
    # Convertir el modelo a un diccionario
    data = jsonable_encoder(data)
    logging.info(f"put example with data: {data}")
    name = data["name"]
    data.pop("name")
    logging.info(f"put example with name: {name} and data: {data}")

    # Actualizar el dato
    data['updated_at'] = datetime.now()


    # Retornar un mensaje de éxito
    return "Ok"

@router.delete("/example2")
async def delete_example2(name: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un dato de la base de datos"""
    logging.info(f"delete example with name: {name}")

    # Eliminar el dato
    await db["example"].delete_one({"name": name})

    # Retornar un mensaje de éxito
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"message": "Data deleted successfully"})

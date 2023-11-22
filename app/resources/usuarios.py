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

@router.get("/usuario")
async def example1():
    data = jsonable_encoder(data)
    logging.info("usuario")

    # Buscar si el dato ya existe
    db_data = await db["usuario"].find_one({"name": data['name']})
    if db_data:
        # Si el dato ya existe, retornar un error
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, 
                            content={"message": "Data already exists"})
    
    # Si el dato no existe, crearlo con sus fechas de creación
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    new_data = await db["usuario"].insert_one(data)

    # Retornar el id del nuevo dato
    return f"{new_data.inserted_id}"

@router.get("/usuario")
async def get_example2(name: str = None, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[ExampleModel] | ExampleModel:
    """Endpoint para obtener un dato de la base de datos"""
    # Buscar el dato por el nombre
    if name is None:
        logging.info("Toma los usuarios")
        try:
            data = await db["usuario"].find().to_list(length=100)
            if data is None:
                data = []
        except Exception as err:
            logging.error(err)
        return data

    logging.info(f"Toma los nombres de usuario: {name}")
    data = await db["usuario"].find_one({"name": name})

    if data:
        # Si el dato existe, retornarlo
        return data

    else:
        # Si el dato no existe, retornar un error
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                            content={"message": "Data not found"})

@router.put("/usuario")
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

@router.delete("/usuario")
async def delete_example2(name: str, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))):
    """Endpoint para eliminar un dato de la base de datos"""
    logging.info(f"Borrar usuario con el nombre: {name}")

    # Eliminar el dato
    await db["usuario"].delete_one({"usuario": name})

    # Retornar un mensaje de éxito
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"message": "Data deleted successfully"})


 #Post
@router.post("/example2")
async def post_example2(
    email: str,
    pass_: str,
    pass_confirm: str,
    name: str,
    last_name: str,
    last_name2: str,
    run: str,
    phone: str,
    phone2: str = None,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))
):
    """Endpoint para crear un dato en la base de datos"""
    data = {
        "email": email,
        "pass": pass_,
        "pass_confirm": pass_confirm,
        "name": name,
        "last_name": last_name,
        "last_name2": last_name2,
        "run": run,
        "phone": phone,
        "phone2": phone2,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    logging.info(f"post example with: {data}")

    # Buscar si el dato ya existe
    db_data = await db["example"].find_one({"name": data['name']})
    if db_data:
        # Si el dato ya existe, retornar un error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Data already exists"
        )

    # Si el dato no existe, crearlo con sus fechas de creación
    new_data = await db["example"].insert_one(data)

    # Retornar el id del nuevo dato
    return JSONResponse(content={"inserted_id": str(new_data.inserted_id)})

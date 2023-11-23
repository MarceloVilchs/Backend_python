import logging
from datetime import datetime
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder

from app.auth import get_db
from app.models.model import createAccountModel

router = APIRouter(
    tags=["createAccount"],
    responses={404: {"description": "Not found"}},
)


@router.post("/createAccount1")
async def post_createAccount1(
    account_data: createAccountModel,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="POST"))
):
    """Endpoint para crear un dato en la base de datos"""
    data = jsonable_encoder(account_data)
    data["created_at"] = datetime.now()
    data["updated_at"] = datetime.now()

    logging.info(f"post createAccount1 with: {data}")

    # Buscar si el dato ya existe
    db_data = await db["createAccount"].find_one({"run": data['run']})
    if db_data:
        # Si el dato ya existe, retornar un error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Data already exists"
        )

    # Si el dato no existe, crearlo con sus fechas de creación
    new_data = await db["createAccount"].insert_one(data)

    # Retornar el id del nuevo dato
    return JSONResponse(content={"inserted_id": str(new_data.inserted_id)})

import logging
from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime, date
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from datetime import datetime
from bson import ObjectId


from app.auth import get_db
from app.models.model import usuarioFormularioModel


router = APIRouter(
    tags=["usuarioFormulario"],
    responses={404: {"description": "Not found"}},
)



# Método GET obtención de datos
@router.get("/usuarioFormulario/GET")
async def get_usuario(name: str = None, db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="GET"))) -> List[usuarioFormularioModel] | usuarioFormularioModel:
    """Endpoint para obtener un dato de la base de datos"""
    # Buscar el dato por el nombre
    if name is None:
        logging.info("get all usuarios")
        try:
            # Incluye el campo _id en la proyección para obtenerlo en el resultado
            projection = {"_id": 1, "email": 1, "name": 1, "last_name": 1, "last_name2": 1, "fecha": 1, "phone": 1, "hora": 1, "estado_pago": 1}  # Ajusta los campos según tu esquema
            data = await db["usuarioFormularios"].find({}, projection).to_list(length=100)

            if data is None:
                data = []
        except Exception as err:
            logging.error(err)
        return data

    logging.info(f"get usuario with name: {name}")
    data = await db["usuarioFormularios"].find_one({"name": name})


    
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
@router.delete("/usuarioFormulario")
async def delete_usuario(
    name: str,
    db: AsyncIOMotorClient = Depends(get_db(resource="resource1", method="DELETE"))
):
    """Endpoint para eliminar una cita de la base de datos por nombre"""
    logging.info(f"delete_usuario with name: {name}")

    # Eliminar la cita
    result = await db["usuarioFormularios"].delete_one({"name": name})

    if result.deleted_count > 0:
        # La cita fue eliminada exitosamente
        return {"message": "Cita eliminada correctamente", "deleted_count": result.deleted_count}
    else:
        # La cita no fue encontrada
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )





# Post
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

    # No es necesario convertir la cadena de fecha al formato deseado antes de insertarla
    # Guardará la fecha en formato YYYY-MM-DD en la base de datos

    # Verificar disponibilidad de horas
    if not await verificarDisponibilidadFechaHora(data["fecha"], data["hora"], db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Hora no disponible en la fecha especificada"
        )

    # Buscar si el dato ya existe
    db_data = await db["usuarioFormularios"].find_one({"name": data['name']})

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



#Metodo en el cual se verifica la hora y fecha
async def verificarDisponibilidadFechaHora(fecha: date, hora: str, db: AsyncIOMotorClient) -> bool:
    """Verifica si la hora está disponible en la fecha especificada"""
    # Obtén las citas existentes para la fecha y hora especificadas
    citas_exist = await db["usuarioFormularios"].count_documents({"fecha": fecha, "hora": hora})
    return citas_exist == 0


async def obtener_horas_ocupadas_desde_bd(fecha: date, db: AsyncIOMotorClient) -> List[str]:
    try:
        # Obtén las horas ocupadas para la fecha dada desde la base de datos
        horas_ocupadas_cursor = db["usuarioFormularios"].find(
            {"fecha": fecha},
            {"hora": 1, "_id": 0}
        )

        # Convierte el cursor a una lista de horas ocupadas
        horas_ocupadas = [cita["hora"] async for cita in horas_ocupadas_cursor]

        return horas_ocupadas

    except Exception as e:
        # Maneja cualquier excepción específica que pueda ocurrir durante la consulta
        logging.error(f"Error al obtener horas ocupadas: {e}")
        return []

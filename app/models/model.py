from bson import ObjectId
from datetime import date, datetime
from pydantic import BaseModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ExampleModel(BaseModel):
    name: str
    number: int
    # En la base de datos se guarda adicionalmente con fechas de creación y actualización

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class createAccountModel(BaseModel):
    email: str
    pass_: str
    pass_confirm: str
    name: str
    last_name: str
    last_name2: str
    run: str
    phone: str
    phone2: str 
    # En la base de datos se guarda adicionalmente con fechas de creación y actualización

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }



class usuarioFormularioModel(BaseModel):
    email: str
    name: str
    last_name: str
    last_name2: str
    fecha : str
    phone: str
    hora : str
    estado_pago : str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
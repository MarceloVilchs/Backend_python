import logging
import logging.config
import sys

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from asgi_logger import AccessLoggerMiddleware
from pydantic import BaseSettings
import motor.motor_asyncio
import httpx

class AppSettings(BaseSettings):
    # Registrar variables de entorno de app.env
    app_name: str = "FastAPI_Base"
    app_version: str = "0.0.1"
    app_description: str = "FastAPI with MongoDB & keycloak"

settings = AppSettings()


class MongoSettings(BaseSettings):
    """
        Variables de entorno para MongoDB
    """

    # Sólo se usa el string de conexión a la base de datos
    mongodb_connstring: str


mongo_settings = MongoSettings()
dbclient = motor.motor_asyncio.AsyncIOMotorClient(mongo_settings.mongodb_connstring)


def get_keycloak_public_key() -> str:
    """Gets the public key from keycloak to verify the token

    Returns:
        str: Public key
    """
    try:
        with httpx.Client() as client:
            response = client.get(keycloak_settings.keycloak_url, timeout=3)
        response.raise_for_status()
        response_json = response.json()
    except httpx.HTTPError as errh:
        logging.error("HTTP Error:", errh)
        sys.exit(1)
    except httpx.ConnectError as errc:
        logging.error("Error Connecting:", errc)
        sys.exit(1)
    except httpx.TimeoutException as errt:
        logging.error("Timeout Error:", errt)
        sys.exit(1)
    except httpx.RequestError as err:
        logging.error("OOps: Something Else", err)
        sys.exit(1)
    return f'-----BEGIN PUBLIC KEY-----\r\n{response_json["public_key"]}\r\n-----END PUBLIC KEY-----'


class KeyCloakSettings(BaseSettings):
    """
        Variables de entorno para Keycloak
    """
    keycloak_client_id: str
    keycloak_client_secret: str
    keycloak_realm: str
    keycloak_url: str
    keycloak_url_token: str
    keycloak_url_info: str
    keycloak_public_key: str = ""


keycloak_settings = KeyCloakSettings()
keycloak_settings.keycloak_public_key = get_keycloak_public_key()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    middleware=[Middleware(AccessLoggerMiddleware,
                           logger=logging.getLogger("asgi_access"),
                           format="%(p)s %(h)s %(r)s %(a)s %(s)s %(L)ss")]
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

""" 
Adds the client id and secret securely to the swagger ui.
Enabling Swagger ui users to perform actions they usually need the client credentials, without exposing them.
"""
app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True,
    "clientId": keycloak_settings.keycloak_client_id,
    "clientSecret": keycloak_settings.keycloak_client_secret,
}

logging.config.fileConfig('log.conf', disable_existing_loggers=True)
logging.getLogger("gunicorn.access").handler = []
logging.getLogger("uvicorn.access").handler = []

logging.info("Starting app")

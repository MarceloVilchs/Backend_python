# fastapi_base

Endpoint para que cada bot pida sus datos.

## Crear ambiente virtual

Crear un ambiente virtual (utilizar Python 3.10)

## Correr en local

    uvicorn app.main:app --reload


## Con Docker

    docker-compose up -d --build

## Rutas Web

Todas las rutas estan documentadas en ``/docs`` o ``/redoc`` con Swagger o ReDoc respectivamente.

## Estructura del proyecto

    fastapi_base                - Directorio raíz 
    ├── .docker                 - Directorio para Dockerfile
    │   └── Dockerfile          - Reglas para construir el contenedor de la API
    ├── .github/workflows       - 
    │   └── ci.yml              - GitHub Actions
    ├── app                     - Directorio de nuestra aplicación
    │   ├── __init__.py         - 
    │   ├── config.py           - Creacion y configuracion de aplicación FastAPI
    │   ├── auth.py             - 
    │   ├── roles.json          - 
    │   ├── models              -
    │   │   └── usuario.py      - Archivo con el modelo de los usuarios
    │   ├── resources           - Directorio para los archivos principales de la app
    │   │   ├── example.py      - Definición de las funciones CRUD  
    │   │   └── router.py       -
    │   └── utils               -
    │       └── utils.py        - 
    ├── env                     - Directorio para guardar variables de ambiente
    │   ├── app.env             - Archivo con variables de ambiente adicionales
    │   ├── keycloak.env        - Variables de ambiente para Keycloak
    │   └── mongo.env           - Variables de ambiente para MongoDB
    ├── .pre.commit.config.yaml - Definición de hooks para pre-commit
    ├── docker-compose.yml      - Reglas para levantar el contenedores de la API
    ├── README.md               - Archivo con detalles del proyecto
    ├── requirements-dev.txt    - Requerimientos necesarios para chequeos pre-commit
    ├── requirements.txt        - Requerimientos necesarios para que corra la app
    └── sonar-project.properties- Propiedades de projecto en SonarQube
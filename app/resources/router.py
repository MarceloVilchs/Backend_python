from fastapi import APIRouter
from app.resources.example import router as resources_router
from app.resources.usuarios import router as resources_router2
from app.resources.createAccount import router as resources_router3

router = APIRouter()
router.include_router(resources_router, prefix="/example", tags=["example"])
router.include_router(resources_router2, prefix="/usuarios", tags=["usuarios"])

#llamada del model al router para integracion de fastapi
router.include_router(resources_router3, prefix="/createAccount", tags=["createAccount"])
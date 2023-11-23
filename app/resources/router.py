from fastapi import APIRouter
from app.resources.example import router as resources_router
from app.resources.createAccount import router as resources_router3
from app.resources.usuarioFormulario import router as resources_router4

router = APIRouter()
router.include_router(resources_router, prefix="/example", tags=["example"])
router.include_router(resources_router3, prefix="/createAccount", tags=["createAccount"])
router.include_router(resources_router4, prefix="/usuarioFormulario", tags=["usuarioFormulario"])
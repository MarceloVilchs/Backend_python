import time

from app.config import app
from app.resources.router import router as example_router

# Agregar los endpoints adicionales por medio de routers
app.include_router(example_router)

@app.get("/health")
async def get():
    """Endpoint para verificar el estado de la aplicación"""
    return "Ok", 200

@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Middleware para agregar el tiempo de procesamiento de la petición"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response

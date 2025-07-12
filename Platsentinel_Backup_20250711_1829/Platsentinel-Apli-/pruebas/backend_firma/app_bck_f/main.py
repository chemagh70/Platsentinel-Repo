from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .generar_log import configurar_log, registrar_mensaje
from .logging_config import logger
from .backend_firma.app_bck_f.rutas import autenticacion, firma

app = FastAPI()

app.include_router(autenticacion.router)
app.include_router(firma.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logo
app = FastAPI(title="PlatSentinel API")

app.include_router(autenticacion.router)
app.include_router(firma.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando la API de PlatSentinel")

@app.get("/")
async def root():
    logger.debug("Acceso a la ruta raíz")
    return {"message": "Bienvenido a PlatSentinel"}

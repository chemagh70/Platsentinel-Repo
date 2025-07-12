# codigo_fuente/api/app_bck_f/module_one/controllers/module_one.py
from fastapi import APIRouter

router = APIRouter(prefix="/module_one", tags=["module_one"])

@router.get("/")
async def get_module_one():
    return {"message": "Módulo One funcionando"}

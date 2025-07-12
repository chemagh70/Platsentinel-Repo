from app.dependencias import obtener_usuario_actual
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/firma", tags=["Firma Digital"])

@router.post("/solicitar")
def firmar_documento(payload: dict, usuario=Depends(obtener_usuario_actual)):
    archivo = payload.get("archivo")
    print(f"Usuario {usuario['sub']} solicitó firmar: {archivo}")
    # Simular llamada a SealSign (puedes sustituir esto por una llamada real):
    return {"mensaje": f"Firma simulada de '{archivo}' enviada a SealSign."}

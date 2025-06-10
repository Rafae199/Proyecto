from pydantic import BaseModel
from typing import Optional

class Activo(BaseModel):
    tipo: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    serial: str
    etiqueta: str
    sede: str
    area: Optional[str] = None
    estado: str = "Activo"

class Movimiento(BaseModel):
    id_activo: int
    sede_anterior: str
    sede_nueva: str
    usuario_id: int

class Baja(BaseModel):
    id_activo: int
    motivo: str
    solicitud_people: Optional[str] = None
    guia_envio: Optional[str] = None
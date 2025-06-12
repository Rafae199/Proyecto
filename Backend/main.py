from fastapi import FastAPI, Depends, HTTPException
from database import get_db
# from models import Activo, Movimiento, Baja
import pandas as pd
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# --- Pydantic Models ---
class Activo(BaseModel):
    tipo: str
    marca: str
    modelo: str
    serial: str
    etiqueta: str
    sede: str
    area: str
    estado: str

class Movimiento(BaseModel):
    # Define the fields for Movimiento as needed
    pass

class Baja(BaseModel):
    # Define the fields for Baja as needed
    pass

@app.post("/activos/")
def crear_activo(activo: Activo, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO activos 
            (TIPO, MARCA, MODELO, SERIAL, ETIQUETA, SEDE, AREA, ESTADO) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (activo.tipo, activo.marca, activo.modelo, activo.serial, 
             activo.etiqueta, activo.sede, activo.area, activo.estado)
        )
        db.commit()
        return {"mensaje": "Activo creado"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Serial/Etiqueta ya existe")
        

@app.get("/activos/{sede}")
def listar_activos(sede: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM activos WHERE SEDE = ?", (sede,))
    return {"activos": cursor.fetchall()}

@app.post("/movimientos/")
def registrar_movimiento(movimiento: Movimiento, db: sqlite3.Connection = Depends(get_db)):
    # Implementa lógica de movimientos
    pass

@app.post("/bajas/")
def registrar_baja(baja: Baja, db: sqlite3.Connection = Depends(get_db)):
    # Implementa lógica de bajas
    pass

@app.get("/exportar-excel/")
def exportar_excel(db: sqlite3.Connection = Depends(get_db)) -> FileResponse:
    df = pd.read_sql("SELECT * FROM activos", con=db)  # type: ignore
    df.to_excel(excel_writer="activos.xlsx", index=False, engine="openpyxl")  # type: ignore
    return FileResponse("activos.xlsx")
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models import Activo, Movimiento, Baja
import pandas as pd
from fastapi.responses import FileResponse
import os

app = FastAPI()

# --- Endpoints ---
@app.post("/activos/")
def crear_activo(activo: Activo, db = Depends(get_db)):
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
def listar_activos(sede: str, db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM activos WHERE SEDE = ?", (sede,))
    return {"activos": cursor.fetchall()}

@app.post("/movimientos/")
def registrar_movimiento(movimiento: Movimiento, db = Depends(get_db)):
    # Implementa lógica de movimientos
    pass

@app.post("/bajas/")
def registrar_baja(baja: Baja, db = Depends(get_db)):
    # Implementa lógica de bajas
    pass

@app.get("/exportar-excel/")
def exportar_excel(db = Depends(get_db)):
    df = pd.read_sql("SELECT * FROM activos", db)
    df.to_excel("activos.xlsx", index=False)
    return FileResponse("activos.xlsx")
# Importacions
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi import File, UploadFile
from typing import Annotated
from typing import List
import db_alumne as db_alumne
import alumne as alumne
import alumnes as alumnes
import alumne_aula as alumne_aula
from pydantic import BaseModel

app = FastAPI()

# Configuració de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Classe base (BaseModel)
class tablaAlumne(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str
    DescAula: str


# Classe per crear alumnes
class AlumneCreate(BaseModel):
    idAula: int
    nomAlumne: str
    cicle: str
    curs: str
    grup: str

# Missatge que apareix al obrir l'API
@app.get("/")
def read_root():
    return {"Alumnat API"}

# Retorna una llista de tots els alumnes
@app.get("/alumne/list", response_model=List[dict])
def read_alumnes():
    
    adb = db_alumne.read()
    alumnes_sch = alumne.alumnes_schema(adb)
    return alumnes_sch


# Mostra un alumne segons el seu identificador
@app.get("/alumne/show/{id}", response_model=dict)
def read_alumne_id(id: int):
    student = db_alumne.read_id(id)
    if student is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return alumne.alumne_schema(student)

# Crea un alumne i mostra la seva informació
@app.post("/alumne/add")
async def create_alumne(data: AlumneCreate):
    if not db_alumne.aula_exists(data.idAula):
        raise HTTPException(status_code=400, detail="Aula no trobada")
    
    l_student_id = db_alumne.create(data.idAula, data.nomAlumne, data.cicle, data.curs, data.grup)  # Indentación corregida
    return {
        "msg": "S'ha afegit correctament",
        "id student": l_student_id,
        "nomAlumne": data.nomAlumne
    }


# Permet modificar un alumne
@app.put("/alumne/update/{idAlumne}")
def update_alumne(idAlumne: int, idAula: int, nomAlumne: str, cicle: str, curs: str, grup: str):
    if not db_alumne.aula_exists(idAula):
        raise HTTPException(status_code=400, detail="Aula no trobada")
    
    updated_records = db_alumne.update_alumne(idAlumne, idAula, nomAlumne, cicle, curs, grup)
    if updated_records == 0:
        raise HTTPException(status_code=404, detail="No s'han trobat ítems per actualitzar")
    
    return {
        "msg": "S’ha modificat correctament"
    }

    
# Permet borrar un alumne de la base de dades
@app.delete("/alumne/delete/{idAlumne}")
def delete_alumne(idAlumne: int):
    deleted_records = db_alumne.delete_alumne(idAlumne)
    if deleted_records == 0:
       raise HTTPException(status_code=404, detail="Ítems a esborrar no trobats")
   
    return {
        "msg": "S’ha esborrat correctament"
    }

# Retorna una llista de tots els alumnes i la informació de les aules
# Endpoint per obtenir llistat amb opcions de consulta avançada
@app.get("/alumne/listAll", response_model=List[tablaAlumne])
def read_alumnes(orderby: str | None = None, contain: str | None = None, skip: int = 0, limit: int = 10):
    try:
        conn = db_alumne.db_client()  # Conectar a la base de dades
        cur = conn.cursor()

        # Construir la consulta inicial
        query = "SELECT a.NomAlumne, a.Cicle, a.Curs, a.Grup, au.DescAula FROM alumne a JOIN aula au ON a.idAula = au.idAula"

        # Agregar filtre per "contain" si existeix
        query_values = []
        if contain:
            query += " WHERE a.NomAlumne LIKE %s OR au.DescAula LIKE %s"
            contain_value = f"%{contain}%"
            query_values += [contain_value, contain_value]

        # Agregar ordenació si "orderby" és ascendent o descendent
        if orderby and orderby.lower() in ["asc", "desc"]:
            query += f" ORDER BY a.NomAlumne {orderby.upper()}"

        # Agregar "limit" i "offset" per la paginació
        query += " LIMIT %s OFFSET %s"
        query_values += [limit, skip]

        # Executar la consulta SQL
        cur.execute(query, query_values)
        results = cur.fetchall()

        # Tancar la connexió
        conn.close()

        # Convertir els resultats a esquema d'alumnes
        alumnes_sch = alumnes.alumnes_schema(results)
        return alumnes_sch

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de connexió: {str(e)}")
    
# Crea molts alumnes amb la seva informació
@app.post("/alumne/loadAlumnes")
async def load_alumnes(data: AlumneCreate):
    if not db_alumne.aula_exists(data.idAula):
        raise HTTPException(status_code=400, detail="Aula no trobada")
    
    l_student_id = db_alumne.create(data.idAula, data.nomAlumne, data.cicle, data.curs, data.grup)  # Indentación corregida
    return {
        "msg": "S'ha afegit correctament",
        "id student": l_student_id,
        "nomAlumne": data.nomAlumne
    }

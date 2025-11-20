from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from .mqtt.services import start_mqtt
from .models.clases import Alumno, AlumnoRequest, Trabajador, TrabajadorRequest, Profesor, PersonalAux, Clase
import os
import threading

load_dotenv()

# Asegurar conexion DB
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
print("DB URL: ", DATABASE_URL)
print("engine: ", engine)

# Crear sesion para conexion con DB
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_mqtt)
    thread.daemon = True
    thread.start()

# ENDPOINTS

@app.post("/alumnos", response_model=Alumno)
def crear_alumno(request: AlumnoRequest, db: Session = Depends(get_db())):
    alumno = Alumno.model_validate(request)
    db.add(alumno)
    db.commit()
    db.refresh(alumno)
    return alumno

@app.post("/trabajadores", response_model=Trabajador)
def crear_trabajador(request: TrabajadorRequest, db: Session = Depends(get_db)):
    trabajador = Trabajador.model_validate(request)
    db.add(trabajador)
    db.commit()
    db.refresh(trabajador)

    if trabajador.rol_personal == "Profesor":
        profesor = Profesor(id_profesor=trabajador.id_trabajador)
        db.add(profesor)
    elif trabajador.rol_personal == "Personal Aux":
        personal_aux = PersonalAux(id_personal_aux=trabajador.id_trabajador)
        db.add(personal_aux)
    db.commit()
    return trabajador

@app.post("/clases", response_model=Clase)
def crear_clase(request: Clase, db: Session = Depends(get_db)):
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

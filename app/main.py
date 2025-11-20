from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from .mqtt.services import start_mqtt
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

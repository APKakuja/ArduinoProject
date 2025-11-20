from enum import Enum
from sqlmodel import SQLModel, Field
from datetime import date, time

class RolPersonal(str, Enum):
    profesor = "Profesor"
    personalAux = "Personal Aux"

class Alumno(SQLModel, table=True):
    id_alumno: int = Field(default=None, primary_key=True)
    nombre: str
    apellidos: str
    email: str
    id_tarjeta: str

class AlumnoRequest(SQLModel):
    nombre: str
    apellidos: str
    email: str
    id_tarjeta: str

class Trabajador(SQLModel, table=True):
    id_trabajador: int = Field(default=None, primary_key=True)
    nombre: str
    apellidos: str
    email: str
    rol_personal: RolPersonal
    id_tarjeta: str

class TrabajadorRequest(SQLModel):
    nombre: str
    apellidos: str
    email: str
    rol_personal: RolPersonal
    id_tarjeta: str

class PersonalAux(SQLModel, table=True):
    id_personal_aux: int = Field(foreign_key="Trabajador.id_trabajador")

class Profesor(SQLModel, table=True):
    id_profesor: int = Field(foreign_key="Trabajador.id_trabajador")

class Clase(SQLModel, table=True):
    id_clase: str = Field(primary_key=True)
    nombre: str
    descripcion: str
    id_profesor: str = Field(foreign_key="Profesor.id_profesor")

class Asiste(SQLModel, table=True):
    id_alumno: int = Field(foreign_key="Alumno.id_alumno", primary_key=True)
    id_clase: str = Field(foreign_key="Clase.id_clase", primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)
    asiste: bool

class Horario(SQLModel, table=True):
    id_horario: int = Field(default=None, primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)
    aula: str
    id_clase: str = Field(foreign_key="Clase.id_clase")

class Jornada(SQLModel, table=True):
    id_jornada: int = Field(default=None, primary_key=True)
    fecha: date = Field(primary_key=True)
    hora: time = Field(primary_key=True)
    id_trabajador: int = Field(foreign_key="Trabajador.id_trabajador")

class RegistroJornada(SQLModel):
    fecha: date
    hora: time
    id_trabajador: int


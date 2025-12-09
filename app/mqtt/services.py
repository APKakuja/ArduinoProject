from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from datetime import datetime, date, time, timedelta
import paho.mqtt.client as mqtt
import os

from app.models.clases import Alumno, Trabajador, RegistroJornada, Jornada, Asiste

load_dotenv()

# Conexion de prueba
'''
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID")
'''

# Conexion AWS
# AWS IOT MQTT
AWS_IOT_ENDPOINT = os.getenv("AWS_IOT_ENDPOINT")
AWS_IOT_PORT = int(os.getenv("AWS_IOT_PORT", 8883))
AWS_IOT_TOPIC = os.getenv("AWS_IOT_TOPIC")
AWS_IOT_CLIENT_ID = os.getenv("AWS_IOT_CLIENT_ID")
AWS_IOT_CERT = os.getenv("AWS_IOT_CERT")
AWS_IOT_KEY = os.getenv("AWS_IOT_PRIVATE_KEY")
AWS_IOT_ROOT_CA = os.getenv("AWS_IOT_ROOT_CA")

# Conexion BD
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

def on_connect(client, userdata, flags, rc):
    print(f"Conectado a AWS", rc)
    client.subscribe(AWS_IOT_TOPIC)
    #client.subscribe(MQTT_TOPIC)


def registro_reciente(db, modelo, campo_id, valor_id, minutos=60):
    ultimo = db.exec(
        select(modelo)
        .where(campo_id == valor_id)
        .order_by(modelo.fecha.desc(), modelo.hora.desc())
    ).first()

    if not ultimo:
        return False

    registro_dt = datetime.combine(ultimo.fecha, ultimo.hora)
    return registro_dt >= datetime.now() - timedelta(minutes=minutos)


def on_message(client, userdata, msg):
    print(f"Mensaje recibido en: {msg.topic}:{msg.payload}")
    try:
        payload = str(msg.payload.decode())
        print("mensaje descodificado:", payload)
    except Exception as error:
        print("formato incorrecto", error)
        payload = "No se recibio ningun id_tarjeta"
    id_tarjeta = payload
    fecha_completa = datetime.now()
    fecha_dd_mm_aa = fecha_completa.date()
    hh = fecha_completa.hour
    mm = fecha_completa.minute
    ss = fecha_completa.second
    hora_hh_mm_ss = time(hh,mm,ss)

# Codigo antiguo sin respuesta para AWS
    '''
    with (Session(engine) as db):
        query = select(Alumno).where(Alumno.id_tarjeta == id_tarjeta)
        alumno_encontrado = db.exec(query).first()
        if not (alumno_encontrado):
            query_trabajador = select(Trabajador).where(Trabajador.id_tarjeta == id_tarjeta)
            trabajador_encontrado = db.exec(query_trabajador).first()
            if not (trabajador_encontrado):
                return print(f"No hay assignacion para la tarjeta: {id_tarjeta}")
            else:
                registro_trabajador = RegistroJornada(
                    fecha=fecha_dd_mm_aa,
                    hora=hora_hh_mm_ss,
                    id_trabajador=trabajador_encontrado.id_trabajador
                )
                registro_jornada = Jornada.model_validate(registro_trabajador)
                db.add(registro_jornada)
                db.commit()
                return print(f"Ha venido a trabajar, registradoo: {id_tarjeta}")
        else:
            registro_alumno = Asiste(
                id_alumno=alumno_encontrado.id_alumno,
                id_clase="G5",
                fecha=fecha_dd_mm_aa,
                hora=hora_hh_mm_ss,
                asiste=True
            )
            db.add(registro_alumno)
            db.commit()
            return print(f"Presencia de alumno a la clase registrada: {id_tarjeta}")
'''

    # Codigo nuevo con respuesta a AWS

    with (Session(engine) as db):
        query = select(Alumno).where(Alumno.id_tarjeta == id_tarjeta)
        alumno_encontrado = db.exec(query).first()
        if not(alumno_encontrado):
            query_trabajador= select(Trabajador).where(Trabajador.id_tarjeta == id_tarjeta)
            trabajador_encontrado = db.exec(query_trabajador).first()
            if not(trabajador_encontrado):
                print(f"No hay assignacion para la tarjeta: {id_tarjeta}")
                client.publish("iticbcn/espnode01/sub", "error")
                return
            else:
                if registro_reciente(db, Jornada, Jornada.id_trabajador, trabajador_encontrado.id_trabajador):
                    print(f"Ya existe un registro reciente para trabajador {id_tarjeta}")
                    client.publish("iticbcn/espnode01/sub", "duplicado")
                    return

                registro_trabajador=RegistroJornada(
                    fecha=fecha_dd_mm_aa,
                    hora=hora_hh_mm_ss,
                    id_trabajador=trabajador_encontrado.id_trabajador
                )
                registro_jornada=Jornada.model_validate(registro_trabajador)
                db.add(registro_jornada)
                db.commit()
                print(f"Ha venido a trabajar, registradoo: {id_tarjeta}")
                client.publish("iticbcn/espnode01/sub", "OK")
                return
        else:
            if registro_reciente(db, Asiste, Asiste.id_alumno, alumno_encontrado.id_alumno):
                print(f"Ya existe un registro reciente para alumno {id_tarjeta}")
                client.publish("iticbcn/espnode01/sub", "duplicado")
                return

            registro_alumno=Asiste(
                id_alumno=alumno_encontrado.id_alumno,
                id_clase="G5",
                fecha=fecha_dd_mm_aa,
                hora=hora_hh_mm_ss,
                asiste= True
            )
            db.add(registro_alumno)
            db.commit()
            print(f"Presencia de alumno a la clase registrada: {id_tarjeta}")
            client.publish("iticbcn/espnode01/sub", "OK")
            return

'''
def start_mqtt():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT)
    client.loop_forever()
'''

def start_mqtt():
    client = mqtt.Client(client_id=AWS_IOT_CLIENT_ID)
    client.tls_set(ca_certs=AWS_IOT_ROOT_CA,
                   certfile=AWS_IOT_CERT,
                   keyfile=AWS_IOT_KEY,)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(AWS_IOT_ENDPOINT, AWS_IOT_PORT, 60)
    client.loop_forever()

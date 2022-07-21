import datetime

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import exc

from database.connector import get_database
from database.models import Doctor, Appointment
from database.connector import Base, engine
from request_models.models import PostAppointment

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/doctors")
def get_doctors():
    try:
        db = next(get_database())
        return db.query(Doctor).all()
    except exc.sa_exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/appointments")
def get_appointments_by_doctor_and_day(doctor_id: int, month: int, day: int, year: int):
    try:
        db = next(get_database())
        epoch_time = datetime.datetime(year, month, day).timestamp()
        appointments = db.query(Appointment).where(
            Appointment.date == epoch_time,
            Appointment.doctor_id == doctor_id).order_by(Appointment.time).all()
        for appointment in appointments:
            appointment.date = datetime.datetime.fromtimestamp(appointment.date).strftime("%d-%m-%Y")
            appointment.time = datetime.datetime.fromtimestamp(appointment.time).strftime("%I:%M%p")
        return appointments
    except exc.sa_exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/appointments")
def add_appointment(appointment_request: PostAppointment):

    hour = int(appointment_request.time.split(":")[0])

    hour += 12 if appointment_request.ampm is "PM" else 0
    minute = int(appointment_request.time.split(":")[1])

    if hour > 12 or hour < 1 or minute > 59 or minute < 0:
        raise HTTPException(status_code=400, detail="Invalid time")
    if minute % 15 != 0:
        raise HTTPException(status_code=400, detail="Time must be in 15 minute intervals")

    epoch_time = datetime.datetime(appointment_request.year, appointment_request.month, appointment_request.day, hour, minute).timestamp()
    db = next(get_database())
    appointments = db.query(Appointment).where(Appointment.time == epoch_time, Appointment.doctor_id == appointment_request.doctor_id).all()
    if len(appointments) >= 3:
        raise HTTPException(status_code=400, detail="Doctor has too many appointments at this time")

    try:
        appointment = Appointment(
            doctor_id=appointment_request.doctor_id,
            patient_first_name=appointment_request.patient_first_name,
            patient_last_name=appointment_request.patient_last_name,
            date=datetime.datetime(appointment_request.year, appointment_request.month, appointment_request.day).timestamp(),
            time=datetime.datetime(appointment_request.year, appointment_request.month, appointment_request.day,hour,minute).timestamp(),
            kind=appointment_request.kind
        )
        db.add(appointment)
        db.commit()
        return {"message": "Appointment added"}
    except exc.sa_exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@app.delete("/appointments")
def delete_appointment(appointment_id: int):
    try:
        db = next(get_database())
        db.query(Appointment).filter(Appointment.id == appointment_id).delete()
        db.commit()
        return {"message": "Appointment deleted"}
    except exc.sa_exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


def populate_test_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = next(get_database())

    julius = Doctor(first_name="Julius", last_name="Hibbert")
    algernop = Doctor(first_name="Algernop", last_name="Krieger")
    nick = Doctor(first_name="Nick", last_name="Rivera")

    db.add_all([julius, algernop, nick])
    db.flush()
    algapp1 = Appointment(
        doctor_id=algernop.id,
        patient_first_name="Woodhouse",
        patient_last_name="",
        date=datetime.datetime(2022, 7, 21).timestamp(),
        time=datetime.datetime(2022, 7, 21, 8, 0).timestamp(),
        kind="New Patient"
    )
    algapp2 = Appointment(
        doctor_id=algernop.id,
        patient_first_name="Cheryl",
        patient_last_name="Tunt",
        date=datetime.datetime(2022, 7, 21).timestamp(),
        time=datetime.datetime(2022, 7, 21, 8, 30).timestamp(),
        kind="Follow-Up"
    )
    algapp3 = Appointment(
        doctor_id=algernop.id,
        patient_first_name="Malory",
        patient_last_name="Archer",
        date=datetime.datetime(2022, 7, 21).timestamp(),
        time=datetime.datetime(2022, 7, 21,17,0).timestamp(),
        kind="Follow-Up"
    )

    db.add_all([algapp1, algapp2, algapp3])
    db.commit()


populate_test_data()

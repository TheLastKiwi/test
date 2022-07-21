from sqlalchemy import Column, Integer, String, ForeignKey
from database.connector import Base


class Doctor(Base):
    __tablename__ = 'doctor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)


class Appointment(Base):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=False)
    patient_first_name = Column(String)
    patient_last_name = Column(String)
    date = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    kind = Column(String, nullable=False)


# In reality we'd also have a patient table and that patient ID would be in the appointment table instead of first and last name
# Unless we're super off the books taking patients on paper
# class Patient(Base):
#     __tablename__ = 'patient'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     first_name = Column(String)
#     last_name = Column(String)

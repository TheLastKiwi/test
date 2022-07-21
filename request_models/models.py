from pydantic import BaseModel


class PostAppointment(BaseModel):
    doctor_id: int
    month: int
    day: int
    year: int
    time: str
    ampm: str
    kind: str
    patient_first_name: str
    patient_last_name: str

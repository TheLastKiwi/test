from starlette.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_appointment_invalid_hour():
    data = {
        "month": 7,
        "day": 21,
        "year": 2022,
        "time": "17:00",
        "ampm": "AM",
        "doctor_id": 1,
        "patient_first_name": "John",
        "patient_last_name": "Doe",
        "kind": "New Patient"
    }
    response = client.post("/appointments", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid time"}

def test_add_appointment_invalid_minute():
    data = {
        "month": 7,
        "day": 21,
        "year": 2022,
        "time": "12:60",
        "ampm": "AM",
        "doctor_id": 1,
        "patient_first_name": "John",
        "patient_last_name": "Doe",
        "kind": "New Patient"
    }
    response = client.post("/appointments", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid time"}

def test_add_appointment_not_15_min_interval():
    data = {
        "month": 7,
        "day": 21,
        "year": 2022,
        "time": "12:17",
        "ampm": "AM",
        "doctor_id": 1,
        "patient_first_name": "John",
        "patient_last_name": "Doe",
        "kind": "New Patient"
    }
    response = client.post("/appointments", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Time must be in 15 minute intervals"}

# def test_add_appointment_too_may_appointments():
#     data = {
#         "month": 7,
#         "day": 21,
#         "year": 2022,
#         "time": "12:15",
#         "ampm": "AM",
#         "doctor_id": 1,
#         "patient_first_name": "John",
#         "patient_last_name": "Doe",
#         "kind": "New Patient"
#     }
#     with patch.object(Session,"query") as mock_query:
#         with patch.object(mock_query,"where") as mock_add:
#             with patch.object(mock_add,"all",return_value=[{1},{2},{3}]):
#                 response = client.post("/appointments", json=data)
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Doctor has too many appointments at this time"}

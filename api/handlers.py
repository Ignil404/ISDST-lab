import json
import os
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from data import APPOINTMENTS, DOCTORS, MINSK, SLOTS, find_appointment, find_doctor
from pages import SWAGGER_HTML

SPEC_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "openapi.yaml")


class Handler(BaseHTTPRequestHandler):

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, code, err_code, message):
        self.send_json({"error": {"code": err_code, "message": message}}, code)

    def read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length == 0:
            return {}
        try:
            return json.loads(self.rfile.read(length))
        except ValueError:
            return None

    def do_GET(self):
        url = urlparse(self.path)
        parts = url.path.strip("/").split("/")
        query = parse_qs(url.query)

        if url.path == "/":
            self.send_json({"service": "Запись к врачу (mock)", "docs": "/docs"})

        elif url.path == "/openapi.yaml":
            with open(SPEC_PATH, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/yaml; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif url.path == "/docs":
            body = SWAGGER_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif parts == ["doctors"]:
            self.list_doctors(query)

        elif len(parts) == 2 and parts[0] == "doctors":
            self.get_doctor(parts[1])

        elif len(parts) == 3 and parts[0] == "doctors" and parts[2] == "slots":
            self.list_slots(parts[1], query)

        elif parts == ["appointments"]:
            self.list_appointments(query)

        elif len(parts) == 2 and parts[0] == "appointments":
            self.get_appointment(parts[1])

        else:
            self.send_error_json(404, "not_found", "маршрут не найден")

    def do_POST(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if parts == ["appointments"]:
            self.create_appointment()
        else:
            self.send_error_json(404, "not_found", "маршрут не найден")

    def do_DELETE(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "appointments":
            self.cancel_appointment(parts[1])
        else:
            self.send_error_json(404, "not_found", "маршрут не найден")

    def list_doctors(self, query):
        doctors = DOCTORS
        specialty = "".join(query.get("specialty", [])).strip().lower()
        if specialty:
            doctors = [d for d in doctors if specialty in d["specialty"].lower()]
        self.send_json(doctors)

    def get_doctor(self, doctor_id):
        doctor = find_doctor(doctor_id)
        if doctor is None:
            self.send_error_json(404, "doctor_not_found", "врач не найден")
            return
        self.send_json(doctor)

    def list_slots(self, doctor_id, query):
        if find_doctor(doctor_id) is None:
            self.send_error_json(404, "doctor_not_found", "врач не найден")
            return
        day = "".join(query.get("date", [])).strip()
        if day:
            try:
                date.fromisoformat(day)
            except ValueError:
                self.send_error_json(422, "bad_date", "дата должна быть в формате YYYY-MM-DD")
                return
        free_slots = []
        for slot in SLOTS.values():
            if slot["doctor_id"] != doctor_id:
                continue
            if day and not slot["start_time"].startswith(day):
                continue
            if find_appointment(slot["id"]) is None:
                free_slots.append({**slot, "status": "free"})
        self.send_json(free_slots)

    def create_appointment(self):
        data = self.read_body()
        if data is None:
            self.send_error_json(422, "bad_request", "тело запроса должно быть корректным JSON")
            return
        doctor_id = data.get("doctor_id")
        slot_id = data.get("slot_id")
        patient_name = str(data.get("patient_name") or "").strip()
        if not doctor_id or not slot_id or not patient_name:
            self.send_error_json(422, "missing_fields", "нужны поля doctor_id, slot_id и patient_name")
            return
        if find_doctor(doctor_id) is None:
            self.send_error_json(404, "doctor_not_found", "врач не найден")
            return
        slot = SLOTS.get(slot_id)
        if slot is None or slot["doctor_id"] != doctor_id:
            self.send_error_json(404, "slot_not_found", "слот не найден у этого врача")
            return
        if datetime.fromisoformat(slot["start_time"]) <= datetime.now(MINSK):
            self.send_error_json(422, "slot_in_past", "время приёма уже прошло")
            return
        if find_appointment(slot_id) is not None:
            self.send_error_json(409, "slot_busy", "слот уже занят")
            return
        appointment = {
            "id": "apt-%d" % (len(APPOINTMENTS) + 1),
            "doctor_id": doctor_id,
            "slot_id": slot_id,
            "patient_name": patient_name,
            "status": "booked",
        }
        if data.get("patient_birthday"):
            appointment["patient_birthday"] = str(data["patient_birthday"])
        if data.get("comment"):
            appointment["comment"] = str(data["comment"])
        APPOINTMENTS[appointment["id"]] = appointment
        self.send_json(appointment, 201)

    def list_appointments(self, query):
        items = list(APPOINTMENTS.values())
        status = "".join(query.get("status", [])).strip()
        if status:
            if status not in ("booked", "cancelled"):
                self.send_error_json(422, "bad_status", "допустимые значения: booked, cancelled")
                return
            items = [a for a in items if a["status"] == status]
        self.send_json(items)

    def get_appointment(self, appointment_id):
        appointment = APPOINTMENTS.get(appointment_id)
        if appointment is None:
            self.send_error_json(404, "appointment_not_found", "запись не найдена")
            return
        self.send_json(appointment)

    def cancel_appointment(self, appointment_id):
        appointment = APPOINTMENTS.get(appointment_id)
        if appointment is None:
            self.send_error_json(404, "appointment_not_found", "запись не найдена")
            return
        if appointment["status"] == "cancelled":
            self.send_error_json(409, "already_cancelled", "запись уже отменена")
            return
        appointment["status"] = "cancelled"
        self.send_json(appointment)

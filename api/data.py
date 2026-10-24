from datetime import date, datetime, timedelta, timezone

MINSK = timezone(timedelta(hours=3))

DOCTORS = [
    {"id": "doc-001", "name": "Иванова Анна Петровна", "specialty": "терапевт", "office": "каб. 214"},
    {"id": "doc-002", "name": "Сидоров Павел Олегович", "specialty": "педиатр", "office": "каб. 108"},
    {"id": "doc-003", "name": "Ковалёва Мария Сергеевна", "specialty": "лор", "office": "каб. 305"},
    {"id": "doc-004", "name": "Гринёв Дмитрий Витальевич", "specialty": "офтальмолог", "office": "каб. 210"},
]

SLOTS = {}
APPOINTMENTS = {}


def generate_slots():
    for doctor in DOCTORS:
        for shift in (1, 2):
            day = date.today() + timedelta(days=shift)
            for hour in range(9, 16):
                for minute in (0, 30):
                    if hour == 12:
                        continue
                    start = datetime(day.year, day.month, day.day, hour, minute, tzinfo=MINSK)
                    slot_id = doctor["id"] + "_" + day.isoformat() + "_%02d%02d" % (hour, minute)
                    SLOTS[slot_id] = {
                        "id": slot_id,
                        "doctor_id": doctor["id"],
                        "start_time": start.isoformat(),
                        "end_time": (start + timedelta(minutes=30)).isoformat(),
                    }


def find_doctor(doctor_id):
    for doctor in DOCTORS:
        if doctor["id"] == doctor_id:
            return doctor
    return None


def find_appointment(slot_id):
    for appointment in APPOINTMENTS.values():
        if appointment["slot_id"] == slot_id and appointment["status"] == "booked":
            return appointment
    return None

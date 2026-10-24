import os
from http.server import HTTPServer

from data import generate_slots
from handlers import Handler

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))


if __name__ == "__main__":
    generate_slots()
    print("Сервер запущен: http://%s:%d" % (HOST, PORT))
    print("Swagger UI:    http://%s:%d/docs" % (HOST, PORT))
    HTTPServer((HOST, PORT), Handler).serve_forever()

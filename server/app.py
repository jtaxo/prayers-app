import os
import sys
from flask import Flask, send_from_directory

# O servidor corre a partir da pasta raiz do projeto (um nível acima de server/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(__name__, static_folder=os.path.join(PROJECT_ROOT, "static"))

@app.route("/")
def index():
    return send_from_directory(PROJECT_ROOT, "index.html")

@app.route("/admin")
def admin():
    return send_from_directory(PROJECT_ROOT, "admin.html")

@app.route("/login")
def login():
    return send_from_directory(PROJECT_ROOT, "login.html")

@app.route("/success")
def success():
    return send_from_directory(PROJECT_ROOT, "success.html")

@app.route("/<path:path>")
def serve_root(path):
    full_path = os.path.join(PROJECT_ROOT, path)
    if os.path.isfile(full_path):
        directory = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        return send_from_directory(directory, filename)
    return "Not Found", 404

if __name__ == "__main__":
    print("=====================================================")
    print("Servidor local a correr!")
    print("Abra o seu browser em: http://localhost:5000")
    print("=====================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)

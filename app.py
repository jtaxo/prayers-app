import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/admin")
def admin():
    return send_from_directory(".", "admin.html")

@app.route("/login")
def login():
    return send_from_directory(".", "login.html")

@app.route("/success")
def success():
    return send_from_directory(".", "success.html")

@app.route("/<path:path>")
def serve_root(path):
    # Serve other files in the root like vercel.json if needed
    if os.path.exists(path):
        return send_from_directory(".", path)
    return "Not Found", 404

if __name__ == "__main__":
    print("=====================================================")
    print("🚀 Servidor local a correr!")
    print("Abra o seu browser em: http://localhost:5000")
    print("=====================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)

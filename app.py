from database import get_db_connection
from flask import Flask, render_template, request, redirect, url_for, send_file
import qrcode
import io
import socket
from database import init_db, add_prayer, get_all_prayers, delete_prayer

app = Flask(__name__)

# Initialize database on startup
init_db()


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        telemovel = request.form.get("telemovel", "")
        assunto = request.form["assunto"]
        add_prayer(nome, telemovel, assunto)
        return redirect(url_for("success"))
    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/admin")
def admin():
    prayers = get_all_prayers()
    local_ip = get_local_ip()
    return render_template("admin.html", prayers=prayers, local_ip=local_ip)


@app.route("/delete/<int:prayer_id>", methods=["POST"])
def delete(prayer_id):
    delete_prayer(prayer_id)
    return redirect(url_for("admin"))


@app.route("/qrcode")
def generate_qrcode():
    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000/"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


@app.route("/debug-db")
def debug_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        conn.close()
        return f"DB connected: {version}"
    except Exception as e:
        return f"DB connection error: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

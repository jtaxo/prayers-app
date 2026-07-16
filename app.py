import io
import socket
from database import (
    add_prayer,
    delete_prayer,
    get_all_prayers,
    get_db_connection,
    init_db,
)
from flask import Flask, redirect, render_template, request, send_file, session, url_for
import qrcode

app = Flask(__name__)

# IMPORTANTE: Mude isto para uma chave longa e aleatória qualquer para proteger as sessões
app.secret_key = "uma_chave_secreta_muito_segura_aqui"

# A sua palavra-passe estática
ADMIN_PASSWORD = "1234"

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
        nome = request.form.get("nome", "").strip()
        if not nome:
            nome = "Anónimo"
        telemovel = request.form.get("telemovel", "").strip()
        assunto = request.form.get("assunto", "")
        add_prayer(nome, telemovel, assunto)
        return redirect(url_for("success"))
    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")


# --- NOVAS ROTAS DE AUTENTICAÇÃO ---


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password_input = request.form.get("password")

        if password_input == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("admin"))
        else:
            error = "Palavra-passe incorreta!"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


# --- ROTA DO ADMIN PROTEGIDA ---


@app.route("/admin")
def admin():
    # Se não estiver logado, bloqueia e redireciona para o login
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    prayers = get_all_prayers()
    local_ip = get_local_ip()
    return render_template("admin.html", prayers=prayers, local_ip=local_ip)


@app.route("/delete/<int:prayer_id>", methods=["POST"])
def delete(prayer_id):
    # Protege também a ação de eliminar
    if not session.get("logged_in"):
        return "Não autorizado", 401

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

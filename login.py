from flask import Flask, request, render_template, redirect, url_for, jsonify
import mariadb

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configurazione per la connessione al database al database con MariaDB
db_config = {
    "user": "root",
    "password": None,  
    "host": "localhost",
    "database": "password",  
}

@app.route("/", methods=["GET"])
def home():
    return render_template ("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = None  # Inizializza connessione a None
        try:
            conn = mariadb.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password),
            )
            user = cursor.fetchone()

            if user:
                return jsonify(success=True)
            else:
                return jsonify(success=False)
        except mariadb.Error as e:
            return jsonify(success=False, error=str(e))
        finally:
            if conn:
                conn.close()
    return render_template("login.html")

@app.route("/analisi", methods=["GET"])
def analisi():
    return render_template("analisi.html")

if __name__ == "__main__":
    app.run(debug=True)
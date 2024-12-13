from flask import Flask, request, render_template, redirect, url_for, jsonify
import mariadb

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configurazione per la connessione al database al database con MariaDB
db_config = {
    "user": "root",
    "password": None,  
    "host": "localhost",
    "database": "Password",  
}

db_config_analisi = {
    "user": "root",
    "password": None,
    "host": "localhost",
    "database": "analisi_sangue",
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

@app.route("/analisi", methods=["GET", "POST"])
def analisi():
    conn = mariadb.connect(**db_config_analisi)
    cursor = conn.cursor()

    if request.method == "POST":
        # Inserire nuova analisi
        data = (
            request.form["nome"], request.form["cognome"], request.form["codice_fiscale"],
            request.form["sesso"], int(request.form["eta"]), request.form["data_ora_prelievo"],
            request.form["luogo_prelievo"], request.form["denominazione_analisi"],
            float(request.form["risultato"]), request.form["unita_misura"],
            request.form["valori_riferimento"]
        )
        cursor.execute("""
            INSERT INTO analisi (nome, cognome, codice_fiscale, sesso, eta, data_ora_prelievo, 
            luogo_prelievo, denominazione_analisi, risultato, unita_misura, valori_riferimento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()

    # Ottenere lista analisi
    cursor.execute("SELECT * FROM analisi")
    analisi_lista = cursor.fetchall()

    conn.close()
    return render_template("analisi.html", analisi_lista=analisi_lista)

@app.route("/elimina_analisi", methods=["POST"])
def elimina_analisi():
    conn = mariadb.connect(**db_config_analisi)
    cursor = conn.cursor()

    # Eliminare analisi per ID
    cursor.execute("DELETE FROM analisi WHERE id=?", (request.form["id"],))
    conn.commit()
    conn.close()
    return redirect("/analisi")




if __name__ == "__main__":
    app.run(debug=True)
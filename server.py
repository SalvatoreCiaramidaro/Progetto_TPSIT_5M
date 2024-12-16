from flask import Flask, request, render_template, redirect, jsonify, session
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
    return render_template("index.html")

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
                "SELECT nome FROM users WHERE username=%s AND password=%s",
                (username, password),
            )
            user = cursor.fetchone()

            if user:
                session['nome'] = user[0]
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
    conn = mariadb.connect(**db_config_analisi)  # Connessione al database analisi
    cursor = conn.cursor()

    if request.method == "POST":
        # Inserisci nuova analisi
        data = (
            request.form["nome"], request.form["cognome"], request.form["codice_fiscale"],
            request.form["sesso"], int(request.form["eta"]), request.form["data_ora_prelievo"],
            request.form["luogo_prelievo"], request.form["denominazione_analisi"],
            float(request.form["risultato"]), request.form["unita_misura"],
            request.form["valori_riferimento"], int(request.form["strumenti"]), int(request.form["cod_operatore"])
        )
        cursor.execute("""
            INSERT INTO analisi (nome, cognome, codice_fiscale, sesso, eta, data_ora_prelievo, 
            luogo_prelievo, denominazione_analisi, risultato, unita_misura, valori_riferimento, strumenti, cod_operatore)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()

    # Recupera i dati per la tabella
    search_query = request.args.get('search')
    if search_query:
        cursor.execute("SELECT * FROM analisi WHERE nome LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM analisi")
    
    analisi_lista = [
        {
            "id": row[0],
            "nome": row[1],
            "cognome": row[2],
            "codice_fiscale": row[3],
            "sesso": row[4],
            "eta": row[5],
            "data_ora_prelievo": row[6],
            "luogo_prelievo": row[7],
            "denominazione_analisi": row[8],
            "risultato": row[9],
            "unita_misura": row[10],
            "valori_riferimento": row[11],
            "strumenti": row[12],
            "cod_operatore": row[13]
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    nome = session.get('nome')
    return render_template("analisi.html", analisi_lista=analisi_lista, nome=nome, search_query=search_query)

@app.route("/elimina_analisi", methods=["POST"])
def elimina_analisi():
    conn = mariadb.connect(**db_config_analisi)
    cursor = conn.cursor()

    # Elimina analisi per ID
    cursor.execute("DELETE FROM analisi WHERE id=?", (request.form["id"],))
    conn.commit()

    # Riassegna gli ID consecutivi
    cursor.execute("SET @new_id = 0;")
    cursor.execute("UPDATE analisi SET id = (@new_id := @new_id + 1);")

    # Reset dell'AUTO_INCREMENT
    cursor.execute("ALTER TABLE analisi AUTO_INCREMENT = 1;")
    conn.commit()

    conn.close()
    return redirect("/analisi")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, render_template, redirect, jsonify, session
import mariadb
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configurazione per la connessioni ai database con MariaDB
db_config_analisi = {
    "user": "root",
    "password": None,
    "host": "localhost",
    "database": "analisi_sangue",
}


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            # Determina se la richiesta contiene JSON
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form

            username = data.get("username")
            password = data.get("password")

            logging.info(f"Tentativo di login per utente: '{username}'")
            logging.info(f"Username ricevuto: '{username}'")
            logging.info(f"Password ricevuta: '{password}'")

            conn = mariadb.connect(**db_config_analisi)
            cursor = conn.cursor()

            # Esegui la query per verificare le credenziali
            cursor.execute("SELECT nome_operatore FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

            if user:
                logging.info(f"Login riuscito per utente: '{username}', nome_operatore: '{user[0]}'")
                # Imposta le variabili di sessione
                session['username'] = username
                session['logged_in'] = True
                session['nome_operatore'] = user[0]
                return jsonify(success=True, message="Login avvenuto con successo."), 200
            else:
                logging.warning(f"Login fallito per utente: '{username}'")
                return jsonify(success=False, message="Credenziali non valide."), 401

        except mariadb.Error as e:
            logging.error(f"Errore del database durante il login: {e}")
            return jsonify(success=False, message="Errore del server."), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template("index.html")

@app.route('/analisi', methods=["GET", "POST"])
def analisi():
    if not session.get('logged_in'):
        return redirect('/')

    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**db_config_analisi)
        cursor = conn.cursor()

        # Recupera il nome_operatore dalla sessione
        nome_operatore = session.get('nome_operatore', "Operatore Sconosciuto")
        username = session.get('username')

        success = False

        if request.method == "POST":
            # Inserisci nuova analisi nel database
            data = (
                request.form["nome"], 
                request.form["cognome"], 
                request.form["codice_fiscale"],
                request.form["sesso"], 
                int(request.form["eta"]), 
                request.form["data_ora_prelievo"],
                request.form["luogo_prelievo"], 
                request.form["denominazione_analisi"],
                float(request.form["risultato"]), 
                request.form["unita_misura"],
                request.form["valori_riferimento"], 
                int(request.form["strumenti"]), 
                int(request.form["cod_operatore"]),
                nome_operatore  # Aggiungi il nome_operatore
            )
            # Esegui una query SQL per inserire dati nella tabella 'analisi'
            cursor.execute("""
                INSERT INTO analisi (nome, cognome, codice_fiscale, sesso, eta, data_ora_prelievo, 
                luogo_prelievo, denominazione_analisi, risultato, unita_misura, valori_riferimento, strumenti, cod_operatore, nome_operatore)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            
            conn.commit()
            success = True  # Imposta il successo a True dopo l'inserimento dei dati

        # Recupera i dati per la tabella delle analisi
        search_query = request.args.get('search', '')
        if search_query:
            cursor.execute("SELECT * FROM analisi WHERE codice_fiscale LIKE ?", ('%' + search_query + '%',))
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
                "cod_operatore": row[13],
                "nome_operatore": row[14]  # Aggiungi il nome_operatore
            }
            for row in cursor.fetchall()
        ]

    except mariadb.Error as e:
        logging.error(f"Errore del database: {e}")
        return jsonify(success=False, message="Errore del server."), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template("analisi.html", analisi_lista=analisi_lista, search_query=search_query, success=success, nome_operatore=nome_operatore)


@app.route("/elimina_analisi", methods=["POST"])
def elimina_analisi():
    conn = mariadb.connect(**db_config_analisi)
    cursor = conn.cursor()

    # Elimina analisi per ID dal database
    cursor.execute("DELETE FROM analisi WHERE id=?", (request.form["id"],))
    conn.commit()
    conn.close()
    return redirect("/analisi")


@app.route('/registrazione', methods=['GET', 'POST'])
def registrazione():
    if request.method == 'GET':
        return render_template("registrazione.html")
    
    elif request.method == 'POST':
        conn = None
        cursor = None
        try:
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form
            username = data.get('username')
            password = data.get('password')
            nome_operatore = data.get('nome_operatore')
            logging.info(f"Tentativo di registrazione utente: {username}")

            conn = mariadb.connect(**db_config_analisi)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                logging.info(f"Utente già esistente: {username}")
                return jsonify(success=False, message="Utente già esistente."), 409

            cursor.execute("""
                INSERT INTO users (username, password, nome_operatore)
                VALUES (?, ?, ?)
            """, (username, password, nome_operatore))
            conn.commit()

            session['username'] = username
            session['logged_in'] = True
            session['nome_operatore'] = nome_operatore
            logging.info(f"Utente registrato con successo: {username}")
            return jsonify(success=True, message="Registrazione avvenuta con successo."), 201

        except mariadb.Error as e:
            logging.error(f"Errore del database: {e}")
            return jsonify(success=False, message="Errore del server."), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('nome_operatore', None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
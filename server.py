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



@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = None  # Inizializza connessione a None
        try:
            conn = mariadb.connect(**db_config)  # Tenta di connettersi al database con la configurazione specificata
            cursor = conn.cursor()  # Crea un cursore per eseguire le query
            cursor.execute(
                "SELECT nome FROM users WHERE username=? AND password=?",  # Esegue una query per selezionare il nome dell'utente con username e password specificati
                (username, password),
            )
            user = cursor.fetchone()  # Recupera il primo risultato della query

            if user:
                session['nome'] = user[0]  # Salva il nome dell'utente nella sessione se l'utente esiste
                return jsonify(success=True)  # Restituisce una risposta JSON con successo
            else:
                return jsonify(success=False)  # Restituisce una risposta JSON con fallimento se l'utente non esiste
        except mariadb.Error as e:
            return jsonify(success=False, error=str(e))  # Gestisce gli errori del database e restituisce una risposta JSON con l'errore
        finally:
            if conn:
                conn.close()  # Chiude la connessione al database
    return render_template("index.html")  # Renderizza il template di login se non è stata effettuata una richiesta POST valida

@app.route("/analisi", methods=["GET", "POST"])
def analisi():
    conn = mariadb.connect(**db_config_analisi)  # Connessione al database analisi
    cursor = conn.cursor()  # Crea un cursore per eseguire le query

    if request.method == "POST":
        # Inserisci nuova analisi nel database
        data = (
            request.form["nome"], request.form["cognome"], request.form["codice_fiscale"],
            request.form["sesso"], int(request.form["eta"]), request.form["data_ora_prelievo"],
            request.form["luogo_prelievo"], request.form["denominazione_analisi"],
            float(request.form["risultato"]), request.form["unita_misura"],
            request.form["valori_riferimento"], int(request.form["strumenti"]), int(request.form["cod_operatore"])
        )
        # Esegue una query SQL per inserire dati nella tabella 'analisi'
        cursor.execute("""
            INSERT INTO analisi (nome, cognome, codice_fiscale, sesso, eta, data_ora_prelievo, 
            luogo_prelievo, denominazione_analisi, risultato, unita_misura, valori_riferimento, strumenti, cod_operatore)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        
        conn.commit()

    # Recupera i dati per la tabella delle analisi
    search_query = request.args.get('search', '')
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
    nome = session.get('nome')  # Recupera il nome dell'utente dalla sessione
    return render_template("analisi.html", analisi_lista=analisi_lista, nome=nome, search_query=search_query)

@app.route("/elimina_analisi", methods=["POST"])
def elimina_analisi():
    conn = mariadb.connect(**db_config_analisi)
    cursor = conn.cursor()

    # Elimina analisi per ID dal database
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

@app.route("/registrazione", methods=["GET", "POST"])
def registrazione():
    if request.method == "POST":
        conn = mariadb.connect(**db_config)  # Connessione al database
        cursor = conn.cursor()  # Crea un cursore per eseguire le query

        # Recupera i dati dal form
        nome = request.form["nome"]
        username = request.form["username"]
        password = request.form["password"]

        # Controlla se l'utente esiste già
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            # Se l'utente esiste già, restituisce una risposta JSON con un messaggio di errore
            return jsonify(success=False, message="Utente già esistente")

        # Se l'utente non esiste, inserisci i dati nel database
        data = (username, password, nome)
        cursor.execute("""
            INSERT INTO users (username, password, nome)
            VALUES (?, ?, ?)
        """, data)
        
        conn.commit()  # Conferma la transazione
        conn.close()  # Chiude la connessione

        return jsonify(success=True, message="Registrazione effettuata con successo")  # Restituisce una risposta JSON con successo

    return render_template("registrazione.html")  # Renderizza il template di registrazione

if __name__ == "__main__":
    app.run(debug=True)
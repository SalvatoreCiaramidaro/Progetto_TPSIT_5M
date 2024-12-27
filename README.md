### Progetto_TPSIT_5M

Per farlo funzionare bisogna scaricare mariadb e flask tramite terminale:

# Sistema di Gestione Analisi del Sangue

Sistema web per la gestione delle analisi del sangue sviluppato con Python Flask e MariaDB.

## Prerequisiti

- Python 3.x (che sia superiore alla 3.9)
- MariaDB
- Node.js e npm
- Sistema operativo Linux (Ubuntu consigliato) o Windows con WSL

## Installazione

### Su Linux/Ubuntu:

1. **Installare Python e pip**:
   ```bash
   sudo apt install python3
   ```
    ```bash
    sudo apt install python3-pip
    ```
2. **Installare MariaDB, Node.js e npm**:
   ```bash
   sudo apt install mariadb-server nodejs npm
   ```
3. **Installare le librerie di sviluppo per MariaDB**:
   ```bash
   sudo apt-get install libmariadb-dev
   ```

4. **Abilita MariaDB per l'avvio automatico all'avvio del sistema:**
   ```bash
   sudo systemctl enable mariadb
   ```

5. **Esegui lo script di sicurezza per configurare MariaDB:**
   ```bash
   sudo mysql_secure_installation
   ```
   Segui le istruzioni per impostare la password di root e configurare altre opzioni di sicurezza. Rispondi "yes" alle seguenti domande:
   
   - `Change the root password?` Rispondi `yes` e imposta la password desiderata.
   - `Reload privilege tables now?` Rispondi `yes`.

6. **Verifica che MariaDB sia in esecuzione:**
   ```bash
   sudo service mariadb status
   ```

7. **Importare i Database con MariaDB**:

   **Per importare il Database degli Utenti che sarebbero gli operatori con Username,nome e Password**:
   ```bash
   mysql -u root -p < /root/progetto/Progetto_TPSIT_5M/immissione_password.sql
    ```

    **Per importare il Database delle Analisi del Sangue con i valori di riferimento**:
   ```bash
   mysql -u root -p < /root/progetto/Progetto_TPSIT_5M/analisi_sangue.sql
   ```

8. **Controllare che i Database siano stati importati correttamente**:

   ```bash
   mysql -u root -p
   ```

   Ora si deve immettere la password di root e si aprirà il prompt di MariaDB. Per visualizzare i database importati, digitare:
   ```sql
   SHOW DATABASES;
   ```

   Se il tuo nome utente è root, e il file SQL si trova in /path/to/dump.sql, il comando sarà:


   Tutti questi comandi sono per linux e python, se si intende utilizzare windows bisogna cercarsi i comandi in windows.

   Per installare Linux, cercare sul Microsoft Store: Ubuntu con l'ultima versione.

Una volta aver importato i database si passa all'installazione delle librerie Python necessarie per il funzionamento del progetto.

   9. **Installare le librerie Python necessarie**:
   ```bash
   pip install -r requirements.txt
   ```
   10. **Avviare il server Flask eseguendo il file con l'apposito pulsante in visual studio code e una volta avviato il Browser immettere l'indirizzo IP**:
   ```bash
    127.0.0.1:5000
    ```
    così facendo si aprirà la pagina di login del sistema e funzionerà tutto normalmente.
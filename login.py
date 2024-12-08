from flask import Flask, request, render_template, redirect, url_for
import mariadb

app = Flask(__name__)

# Database connection configuration
db_config = {
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "database": "your_database",
}

@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = mariadb.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password),
            )
            user = cursor.fetchone()

            if user:
                return "Login successful!"
            else:
                return "Invalid credentials, please try again."
        except mariadb.Error as e:
            return f"Error connecting to MariaDB: {e}"
        finally:
            if conn:
                conn.close()
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

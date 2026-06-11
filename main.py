import os
from cs50 import SQL
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import buscar_libros, apology, login_required


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///biblioteca.db")

load_dotenv()

API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("No username")
        if not password:
            return apology("No password")
        if password != confirmation:
            return apology("Passwords don't mach")
        
        hash = generate_password_hash(password)
        print(hash)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, hash)
            return redirect("/")
        except ValueError:
            return apology("Username already in use")
        
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return apology("Error al buscar", 405)
    
    else:
        query = request.form.get("query")
        tipo = request.form.get("searchType")
        print(tipo)

        if not query or not tipo:
            return apology("Error en los terminos de busqueda", 406)
        
        libros = buscar_libros(query, API_KEY, tipo)
        if not libros:
            return apology("Error de busqueda interno")

        return render_template("search.html", libros=libros)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

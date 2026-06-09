import os
from flask import Flask, flash, redirect, render_template, request
from flask_session import Session
from helpers import buscar_libros

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
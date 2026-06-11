import requests
from flask import redirect, render_template, session
from functools import wraps

def buscar_libros(titulo=None, autor=None, genero=None):
    search_url = "https://openlibrary.org/search.json"
    query_parts = []
    if titulo:
        query_parts.append(f"title:{titulo}")

    if autor:
        query_parts.append(f"author:{autor}")

    if genero:
        query_parts.append(f"subject:{genero}")

    query = " ".join(query_parts)
    try:
        response = requests.get(search_url, params={"q": query})
        data = response.json()
        if not data["docs"]: return None
        resultados = data["docs"]
        libros = []

        for resultado in resultados:
            libro = {
                "key": resultado.get("key"),
                "titulo": resultado.get("title"),
                "autor": ", ".join(resultado.get("author_name", [])),
                "anio": resultado.get("first_publish_year"),
                "descripcion": "No hay descripción disponible.",
                "portada": None
            }
            cover_id = resultado.get("cover_i")
            if cover_id:
                libro["portada"] = (f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg")

            libros.append(libro)
        
        print(libros)
        return libros
        
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
        return []

def apology(message, code=400):

    def escape(s):
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code   

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

buscar_libros(None, None, "Fantasy")
import requests
from flask import redirect, render_template, session
from functools import wraps

def buscar_libros(termino_buscado, key,tipo_busqueda="titulo"):
    query = termino_buscado.replace(" ", "+")
    
    prefijos = {
        "titulo": "intitle:",
        "autor": "inauthor:",
        "genero": "subject:"
    }
    
    prefijo = prefijos.get(tipo_busqueda, "intitle:")
    
    url = f"https://www.googleapis.com/books/v1/volumes?q={prefijo}{query}&key={key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        quote_data = response.json()
        books = []
        for item in quote_data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            image_links = volume_info.get("imageLinks", {})
            isbn_list = volume_info.get("industryIdentifiers")                

            book = {
                "titulo": volume_info.get("title", "Sin título"),
                "autores": volume_info.get("authors", ["Sin autor especificado"]),
                "descripcion": volume_info.get("description", "Sin descripción"),
                "imagen": image_links.get("thumbnail", "/static/errorlibro.png"),
                "ISBN": isbn_list[1]["identifier"],
                "paginas": volume_info.get("pageCount", "Numero desconocido")
            }
            
            books.append(book)
        return books
        
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
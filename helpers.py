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
            
            book = {
                "titulo": volume_info.get("title", "Sin título"),
                "autores": volume_info.get("authors", ["Sin autor especificado"]),
                "descripcion": volume_info.get("description", "Sin descripción"),
                "imagen": image_links.get("thumbnail", "url_imagen_por_defecto.jpg")
            }
            
            books.append(book)
        return books
        
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
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
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
import requests

def buscar_libros(termino_buscado, tipo_busqueda="titulo"):
    query = termino_buscado.replace(" ", "+")
    
    prefijos = {
        "titulo": "intitle:",
        "autor": "inauthor:",
        "genero": "subject:"
    }
    
    prefijo = prefijos.get(tipo_busqueda, "intitle:")
    
    url = f"https://www.googleapis.com/books/v1/volumes?q={prefijo}{query}&key=AIzaSyAJ6PqrVIX5ijF1h5v-C60hQmxlgp9oK1I"
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

    
    
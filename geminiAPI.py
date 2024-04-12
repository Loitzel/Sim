
import google.generativeai as genai
import os

class GeminiAPI:
    def __init__(self):
        """Inicializa la clase y configura la API"""
        os.environ['API_KEY'] = 'AIzaSyB86IMkIMmwAuXJ5sWq7bymyPAW9Ommn8c'  # Reemplaza con tu clave de API
        genai.configure(api_key=os.environ['API_KEY'])
        self.model = genai.GenerativeModel('gemini-pro')

    def summarize(self, document):
        """Genera un resumen del documento dado"""
        response = self.model.generate_content(f'Please summarize this document: {document}')
        return response.text

    # Agrega otros métodos para otras funciones de la API según sea necesario



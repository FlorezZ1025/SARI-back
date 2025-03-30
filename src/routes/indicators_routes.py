from flask import Blueprint, make_response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
import time
from utils.db import db
# from models.article import Article

# Configurar el navegador (Chrome)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecutar sin ventana gráfica
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# Crear el driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


indicator_bp = Blueprint('indicators', __name__, url_prefix='/indicators')

#Revisar e implementar la ruta de los articulos


#Prueba de web Scrapping
@indicator_bp.route('/scrap', methods=['GET'])
def scrap():
    try:
    # URL de la página de publicaciones
        url = 'https://investigaciones-pure.udemedellin.edu.co/es/persons/gloria-piedad-gasca-hurtado/publications/'
        driver.get(url)

        # Esperar a que la página cargue completamente
        time.sleep(5)  # Ajusta el tiempo según la velocidad de tu conexión y la carga del sitio

        # Obtener el HTML de la página
        page_source = driver.page_source

        info = []

        # Analizar el HTML con BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Encontrar todos los elementos que contienen las publicaciones
        publications = soup.find_all('div', class_='result-container')

        # Extraer y mostrar la información de cada publicación
        for pub in publications:
            title_tag = pub.find('h3', class_='title')
            date_tag = pub.find('span', class_='date')
            title = title_tag.text.strip() if title_tag else 'Título no disponible'
            date = date_tag.text.strip() if date_tag else 'Fecha no disponible'
            info.append({'title': title, 'date': date})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
    # Cerrar el navegador
        driver.quit()
    return jsonify({'message': 'Scraping realizado con éxito', 'data': info}), 200
        


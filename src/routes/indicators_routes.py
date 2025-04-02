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
import os
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

PURE_URL = os.getenv('PURE_URL')

indicator_bp = Blueprint('indicators', __name__, url_prefix='/indicators')

#Revisar e implementar la ruta de los articulos


#Prueba de web Scrapping

@indicator_bp.route('/pure_articles', methods=['POST'])
@jwt_required()
def get_pure():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        full_name = data.get('fullname')

        url = PURE_URL + full_name +'/publications/'
        print('URL:', url)
        driver.get(url)

        time.sleep(1)  # Ajusta el tiempo según la velocidad de tu conexión y la carga del sitio

        page_source = driver.page_source
        info = []

        soup = BeautifulSoup(page_source, 'html.parser')

        publications = soup.find_all('div', class_='result-container')

        for pub in publications:
             title_tag = pub.find('h3', class_='title')
             date_tag = pub.find('span', class_='date')
             title = title_tag.text.strip() if title_tag else 'Título no disponible'
             date = date_tag.text.strip() if date_tag else 'Fecha no disponible'
             info.append({'title': title, 'date': date})
        driver.quit()  # Cerrar el navegador después de usarlo

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = make_response(jsonify({
        'message': 'Scraping realizado con éxito',
        'data': info,
    }), 200)
    return response


###################################################################

######################################################
  
   # URL de la página de publicaciones

  #
        # url2 = 'elkin-lubin-arias-londoño/publications/'
        # driver.get(url)

        # # Esperar a que la página cargue completamente

        # # Obtener el HTML de la página
        # page_source = driver.page_source
        # info = []

        # # Analizar el HTML con BeautifulSoup
        # soup = BeautifulSoup(page_source, 'html.parser')

        # # Encontrar todos los elementos que contienen las publicaciones
        # publications = soup.find_all('div', class_='result-container')

        # # Extraer y mostrar la información de cada publicación
        # for pub in publications:
        #     title_tag = pub.find('h3', class_='title')
        #     date_tag = pub.find('span', class_='date')
        #     title = title_tag.text.strip() if title_tag else 'Título no disponible'
        #     date = date_tag.text.strip() if date_tag else 'Fecha no disponible'
        #     info.append({'title': title, 'date': date})

    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

    # finally:
    # # Cerrar el navegador
    #     driver.quit()
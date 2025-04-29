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
from src.utils.db import db
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

        time.sleep(3)  # Ajusta el tiempo según la velocidad de tu conexión y la carga del sitio
        print('Esperando a que la página cargue completamente...')
        page_source = driver.page_source
        info = []

        soup = BeautifulSoup(page_source, 'html.parser')
        h3_tags = soup.find_all('h3', class_='title')


        publications_links = [h3.find('a') for h3 in h3_tags if h3.find('a') ]
        for pub in publications_links:
             article_url = pub['href']
             driver.get(article_url)

             time.sleep(1)  # Esperar a que la página cargue completamente
             article_source = driver.page_source
             article_soup = BeautifulSoup(article_source, 'html.parser')
            
            #Titulos
             title_element = driver.find_element(By.CSS_SELECTOR, "div.rendering h1 span")
             title = title_element.text.strip()

            #Autores
             authors = []
             authors_block = article_soup.find('p', class_='relations persons')
             if authors_block:
        # 1. Obtener nombres dentro de <a>
                for a in authors_block.find_all('a'):
                    name = a.get_text(strip=True)
                    if name:
                        authors.append(name)

                text_parts = authors_block.find_all(text=True, recursive=False)
                for text in text_parts:
                    # Separar por coma y limpiar
                    parts = [t.strip() for t in text.split(',') if t.strip()]
                    authors.extend(parts)
             
             #Fechas
             date = article_soup.find('span', class_='date').text.strip() if article_soup.find('span', class_='date') else 'Fecha no disponible'
            

             #Hyperlink
             try:
               hyperlink_tag = driver.find_element(By.CSS_SELECTOR, "div.doi a")
               hyperlink = hyperlink_tag.get_attribute('href') if hyperlink_tag else 'No disponible'
               print('Hyperlink:', hyperlink)
             except Exception as e:
                hyperlink = 'No disponible'
                print('Error al obtener el hyperlink:', e)

             info.append({
                 'title': title,
                 'authors': authors,
                 'date': date,
                 'hyperlink': hyperlink
             })


        #     time.sleep(1)  # Esperar a que la página cargue completamente
        driver.quit()  # Cerrar el navegador después de usarlo

    except Exception as e:
        print('Error:', e)
        return jsonify({'message': 'Hubo un error recuperando los artículos', 'statusCode':500}), 500

    response = make_response(jsonify({
        'message': 'Scraping realizado con éxito',
        'data': info,
        'statusCode': 200
    }), 200)
    return response

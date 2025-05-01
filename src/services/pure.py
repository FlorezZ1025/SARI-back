import uuid
from flask import make_response, jsonify
from bs4 import BeautifulSoup
import time
from config import PURE
from models.article import Article
from services.web_scrapping import get_web_scrapping

from selenium.webdriver.common.by import By

article = Article()

def get_pure_articles(request):
    driver = get_web_scrapping()

    print('Iniciando el scraping de PURE...')
    print(request.json['email'])
    try:

        # data = request.get_json()
        full_name = request.json['fullname']

        url = PURE.PURE_ARTICLES_URL + full_name +'/publications/'
        print('entrandooo')
        driver.get(url)
        print('entre eh eh eh')

        time.sleep(1)  # Ajusta el tiempo según la velocidad de tu conexión y la carga del sitio
        print('Esperando a que la página cargue completamente...')
        page_source = driver.page_source
        info = []

        soup = BeautifulSoup(page_source, 'html.parser')
        h3_tags = soup.find_all('h3', class_='title')


        publications_links = [h3.find('a') for h3 in h3_tags if h3.find('a') ]
        for pub in publications_links:
             article_url = pub['href']
             driver.get(article_url)

            #  time.sleep(0.5)  # Esperar a que la página cargue completamente
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
                print(hyperlink)

             info.append({
                 'id': str(uuid.uuid4()),  # Generar un ID único para cada artículo
                 'title': title,
                 'authors': authors,
                 'date': date,
                 'hyperlink': hyperlink,
                 'state':'publicado'
             })


        #     time.sleep(1)  # Esperar a que la página cargue completamente
        driver.quit()  # Cerrar el navegador después de usarlo

    except Exception as e:
        print('Error:', e)
        return jsonify({'message': 'Hubo un error recuperando los artículos', 'statusCode':500}), 500

    article.insert_articles(email=request.json['email'], articles=info)



    response = make_response(jsonify({
        'message': 'Scraping realizado con éxito',
        'data': info,
        'statusCode': 200
    }), 200)
    return response

def get_pure_projects(request):
    print('capturando los proyectos de pure...')
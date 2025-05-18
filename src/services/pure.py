import uuid
from flask import make_response, jsonify
from bs4 import BeautifulSoup
import time
from config import PURE
from src.models.article import Article
from src.models.project import Project
from src.services.web_scrapping import get_web_scrapping
from selenium.webdriver.common.by import By

article = Article()
project = Project()

def get_pure_articles(request):
    driver = get_web_scrapping()

    print(request.json['email'])
    try:

        # data = request.get_json()
        full_name = request.json['fullname']
        print('Nombre completo:', full_name)
        url = PURE.PURE_PERSONS_URL + full_name +'/publications/'
        print('entrandooo')
        driver.get(url)
        print('entre eh eh eh')

        time.sleep(1)  # Ajusta el tiempo según la velocidad de tu conexión y la carga del sitio
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
        'articles': info,
        'statusCode': 200
    }), 200)
    return response

def get_pure_projects(request):
    driver = get_web_scrapping()

    print(request.json['email'])
    try:
        full_name = request.json['fullname']
        print('Nombre completo:', full_name)
        url = PURE.PURE_PERSONS_URL + full_name +'/projects/'
        print('entrandooo')
        driver.get(url)
        print('entre eh eh eh')
        time.sleep(1)
        page_source = driver.page_source
        info = []

        soup = BeautifulSoup(page_source, 'html.parser')
        h3_tags = soup.find_all('h3', class_='title')

        publications_links = [h3.find('a') for h3 in h3_tags if h3.find('a') ]
        for pub in publications_links:
             project_url = pub['href']
             driver.get(project_url)

            #  time.sleep(0.5)  # Esperar a que la página cargue completamente
             project_source = driver.page_source
             project_soup = BeautifulSoup(project_source, 'html.parser')
            
            #Titulos
             title_element = driver.find_element(By.CSS_SELECTOR, "section.introduction h1")
             title = title_element.text.strip()

            #Estado
             status_element = driver.find_element(By.CSS_SELECTOR, "tr.status td")
             status = status_element.text.strip()
             #Fecha
             date_element = driver.find_element(By.CSS_SELECTOR, "tr.effective-startend-date td span")
             date = date_element.text.strip() if date_element else 'Fecha no disponible'

            #investigadores
             investigators = []
             investigators_block = driver.find_elements(By.CSS_SELECTOR, "ul.relations.persons li a.link.person span")
             for investigator in investigators_block:
                 name = investigator.text.strip()
                 if name:
                     investigators.append(name)

             print('status', status)
             print('title', title)
             print('date', date)
             print('investigators', investigators)

             info.append({
                 'id': str(uuid.uuid4()),  # Generar un ID único para cada proyecto
                 'title': title,
                 'investigators': investigators,
                 'date': date,
                 'status': status,
             })
        
       
        driver.quit()    
    except Exception as e:
        print('Error:', e)
        return jsonify([]), 500

    project.insert_projects(email=request.json['email'], projects=info)
    response = make_response(jsonify(info)), 200
    return response
             
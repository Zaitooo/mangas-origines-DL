# F12 FOR DEBUGGING
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests, os, shutil, cloudscraper
from zipfile import ZipFile

scraper = cloudscraper.create_scraper()
r = scraper.get(input('URL : ')).text

soup = BeautifulSoup(r, 'html.parser')

pageNum = 0

name = soup.find('h1', id='chapter-heading')
pages = soup.find_all('img', 'wp-manga-chapter-img')
nbpage = int(len(pages))

titles = []

with tqdm(total=nbpage) as pbar:
    pbar.set_description(f'Téléchargement de {nbpage} page(s)')
    for page in pages:
        img_data = scraper.get(page['data-src']).content
        pageNum = pageNum + 1
        with open(f'./cache/{pageNum}.jpg', 'wb') as handler:
            titles.append(f'./cache/{pageNum}.jpg')
            handler.write(img_data)
            pbar.update(1)
with tqdm(total=nbpage) as pbar:
    pbar.set_description(f'Création de {name.string}.cbr')
    with ZipFile(f'{name.string}.cbr', 'w') as myzip:
            for title in titles:
                myzip.write(title)
                pbar.update(1)

for files in os.listdir("./cache"):
    path = os.path.join("./cache", files)
    try:
        shutil.rmtree(path)
    except OSError:
        os.remove(path)

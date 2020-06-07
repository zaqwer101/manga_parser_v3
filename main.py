from bs4 import BeautifulSoup
import requests

URL = 'https://readmanga.me/rassvet_iony'
r = requests.get(URL)

parser = BeautifulSoup(r.content, 'html.parser')

data = parser.find_all('div')
for elem in data:
    if 'class' in elem.attrs and 'chapters-link' in elem.attrs['class']:
        chapter_links = elem
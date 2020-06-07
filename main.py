from bs4 import BeautifulSoup
import requests

URL = 'https://readmanga.me'
MANGA = 'rassvet_iony'
r = requests.get(f'{URL}/{MANGA}')

parser = BeautifulSoup(r.content, 'html.parser')

data = parser.find_all('div')
for elem in data:
    if 'class' in elem.attrs and 'chapters-link' in elem.attrs['class']:
        chapter_links_parser = elem
        break

if chapter_links_parser is None:
    print("Can not find chapters list")
    exit(1)

chapter_links = []
for elem in chapter_links_parser.find('table').find_all('a'):
    chapter_links.append(URL + "/" + elem.attrs['href'])
print(chapter_links)
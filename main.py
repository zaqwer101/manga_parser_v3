from bs4 import BeautifulSoup
import requests
import json

URL = 'https://readmanga.me'
MANGA = 'rassvet_iony'

r = requests.get(f'{URL}/{MANGA}')

## Парсим страницу манги на предмет глав
parser = BeautifulSoup(r.content, 'html.parser')
data = parser.find_all('div')
for elem in data:
    if 'class' in elem.attrs and 'chapters-link' in elem.attrs['class']:
        chapter_links_parser = elem
        break

if chapter_links_parser is None:
    print("Can not find chapters list")
    exit(1)
###

## Преобразуем ссылки из chapter_links_parser в массив ссылок на главы
chapter_links = []
for elem in chapter_links_parser.find('table').find_all('a'):
    chapter_links.append(URL + "/" + elem.attrs['href'])
chapter_links.reverse()
###

chapter_link = chapter_links[0]

r = requests.get(chapter_link)
content = r.content.decode('utf-8')
chapter = content.split('rm_h.init( ')[1].split(', 0, false')[0]
chapter = eval(chapter)

for elem in chapter:
    image_link = elem[0] + elem[2]
    print(image_link)
    filename = image_link.split('/')[-1]
    file = open(filename, 'wb')
    r = requests.get(image_link)
    file.write(r.content)
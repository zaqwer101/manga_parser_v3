from bs4 import BeautifulSoup
import requests
import os

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
    chapter_links.append(URL + elem.attrs['href'])
chapter_links.reverse()
###


for chapter_link in chapter_links:
    # chapter_link - 'https://readmanga.me/rassvet_iony/vol1/1'
    vol = chapter_link.split('/')[4]
    chapter = chapter_link.split('/')[-1]
    current_directory = f'{MANGA}/{vol}/{chapter}'

    if not os.path.exists(current_directory):
        os.makedirs(current_directory)

    r = requests.get(chapter_link)
    content = r.content.decode('utf-8')
    chapter = content.split('rm_h.init( ')[1].split(', 0, false')[0] # магическое вырезание списка картинок
    chapter = eval(chapter)                                          # и преобразование списка в читаемый массив

    for elem in chapter:
        # elem - ['https://t8.mangas.rocks/', 'https://h23.mangas.rocks/manga/', 'auto/05/33/30/0Yona_0000.png_res.jpg', 799, 572]
        image_link = elem[0] + elem[2]
        # print(image_link)
        filename = current_directory +'/'+ image_link.split('/')[-1]
        print(filename)
        if not os.path.exists(filename):
            r = requests.get(image_link)
            open(filename, 'wb').write(r.content)
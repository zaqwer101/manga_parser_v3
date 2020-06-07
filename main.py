from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter

URL = 'https://readmanga.me'
MANGA = 'rassvet_iony'


def fillPage(path, canvas):
    page_width, page_height = canvas._pagesize
    image = Image.open(path)
    draw_width, draw_height = page_width, page_height
    canvas.setPageRotation(0)
    canvas.drawImage(path, 0, 0, width=draw_width, height=draw_height, preserveAspectRatio=True)


def createPDF(vol):
    directory = f'{MANGA}/{vol}'
    pdf = Canvas(f'{MANGA}/{MANGA}_{vol}.pdf')
    for chapter in os.listdir(directory):
        for image in os.listdir(directory +'/'+ chapter):
            fillPage(directory +'/'+ chapter +'/'+ image, pdf)
            pdf.showPage()
    pdf.save()


r = requests.get(f'{URL}/{MANGA}')

## Парсим страницу манги на предмет глав
parser = BeautifulSoup(r.content, 'html.parser')
data = parser.find_all('div')
for elem in data:
    if 'class' in elem.attrs and 'chapters-link' in elem.attrs['class']:
        chapter_links_parser = elem
        break

if chapter_links_parser is None:
    print("Не смог найти список глав")
    exit(1)
###

## Преобразуем ссылки из chapter_links_parser в массив ссылок на главы
chapter_links = []
for elem in chapter_links_parser.find('table').find_all('a'):
    chapter_links.append(URL + elem.attrs['href'])
chapter_links.reverse()
###

old_vol = chapter_links[0].split('/')[4] # чтобы понимать, когда начался новый том

for chapter_link in chapter_links:
    # chapter_link - 'https://readmanga.me/rassvet_iony/vol1/1'
    vol = chapter_link.split('/')[4]

    if vol != old_vol: # если это уже новый том - старый собираем в pdf
        print("Собираем PDF")
        createPDF(old_vol)

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
    old_vol = vol
createPDF(old_vol)

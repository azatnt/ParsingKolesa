import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://kolesa.kz/cars/toyota/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
           'accept': '*/*'}
HOST = 'https://kolesa.kz'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url=url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find('div', class_='pager').get_text()
    if rows:
        return int(rows[16])
    else:
        return 1


def save_to_file(item, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'link', 'price', 'city', 'added_date'])
        for item in item:
            writer.writerow([item['title'], item['link'], item['price'], item['city'], item['added_date']])


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='row vw-item list-item blue a-elem')

    cars = []
    for item in items:
        price = item.find('span', class_='price').get_text(strip=True).replace(u'\xa0', u'')
        cars.append({
            'title': item.find('span', class_='a-el-info-title').get_text(strip=True),
            'link': HOST + item.find('a', class_='list-link').get('href'),
            'price': price,
            'city': item.find('div', class_='list-region').get_text(strip=True),
            'added_date': item.find('span', class_='date').get_text(strip=True),
        })
    return cars


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count+1):
            print(f' Parsing page {page} from {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        # cars = get_content(html.text)
        print(f'Get {len(cars)} cars')
        save_to_file(cars, FILE)
    else:
        print("Error")

parse()



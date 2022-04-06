import requests
import lxml
import os
import json
from bs4 import BeautifulSoup as BS


def get_all():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.43'
    }
    
    # ill check last 'i' (100) news. It can be changed later
    # I decided to get all links to web pages, open it and take all needed information, but there is easier way.
    # I could open first url (https://www.rt.com/listing/category.worldnews_v.xwidget.newsWidgets/prepare/last-news/{i}/0) and take all information from it, without accessing other pages
    i = 100
    url = f'https://www.rt.com/listing/category.worldnews_v.xwidget.newsWidgets/prepare/last-news/{i}/0'

    q = requests.get(url=url, headers=headers)
    result = q.content

    soup = BS(result, 'lxml')
    all_news = soup.find_all('a', class_='link link_hover')

    if not os.path.exists('data'):
        os.mkdir('data')

    with open('data/url_list.txt', 'a') as file:
        for line in all_news:
            file.write('https://www.rt.com' + str(line.get('href')) + '\n')


    with open('data/url_list.txt') as file:
        lines = [line.strip() for line in file.readlines()]


        i = 0
        for line in lines:
            i += 1
            q = requests.get(url=line, headers=headers)
            result = q.content

            soup = BS(result, 'lxml')

            data = (
                {
                    'Heading': str(soup.find(class_='article__heading').text).strip(),
                    'Summary': str(soup.find(class_='article__heading').next_element.next_element.text).strip()
                }
            )

            with open('data/info.json', 'a', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            print(f"Article #{i} is done")

def main():
    get_all()

if __name__ == '__main__':
    main()

import requests
import lxml
import os
import json
from bs4 import BeautifulSoup as BS


def get_all():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.43'
    }

    r = requests.get(url='https://www.swatch.com/en-gb/our-styles/mens-watches/?cgid=mens-watches&srule=bestseller-swatch&start=0&sz=600', headers=headers)
    result = r.content

    soup = BS(result, 'lxml')
    watches = soup.find_all(class_='b-product_tile-title')

    if not os.path.exists('data'):
        os.mkdir('data')

    with open('data/urls_list.txt', 'a') as file:
        for line in watches:
            file.write('https://www.swatch.com' + str(line.find('a').get('href')) + '\n')


    with open('data/urls_list.txt') as file:
        lines = [line.strip() for line in file.readlines()]

        i = 0
        for line in lines:
            i += 1
            print(f'watches #{i}')
            q = requests.get(url=line, headers=headers)
            result = q.content

            soup = BS(result, 'lxml')
            features = soup.find_all('div', class_='b-pdp_features-description')
            features_text = []

            for feats in features:
                text = feats.text
                features_text.append(text[1:-1])


            data = (
                
                {
                    'Name': soup.find(class_='b-pdp_tile-name').text[1:-1],
                    'Movement':features_text[0],
                    'Water resistant':features_text[1],
                    'Strap material':features_text[2],
                    'Clasp material':features_text[3],
                    'Strap buckle':features_text[4],
                    'Case material':features_text[5]
                }
                
            )


            with open('data/info.json', 'a', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            
            print(f'Page #{i} is done!')


def main():
    get_all()

if __name__ == '__main__':
    main()

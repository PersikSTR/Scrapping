import requests
import lxml
from bs4 import BeautifulSoup as BS
import json


# pages = ['https://cheb.ru/tc.htm', 'https://cheb.ru/bizcentr.htm']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.43'
}
pages = ['https://cheb.ws/str.htm', 'https://cheb.ws/zhkh.htm']
for page in pages:
    i = 0
    while i < 30:
        
        i += 1
        urls = []

        q = requests.get(url = (page + f'?page={i}'), headers=headers)
        result = q.content


        soup = BS(result, 'lxml')
        places = soup.find_all('div', class_='anryblimg2')


        for place in places:
            place_url = place.find('h2').find('a').get('href')
            urls.append('https://cheb.ws/' + place_url)


        j = 1
        for url in urls:

            w = requests.get(url=url, headers=headers)
            result = w.content

            soup_ = BS(result, 'lxml')
            try:
                name_of_company = soup_.find('h1', itemprop='name').text
            except Exception:
                name_of_company = 'miss'

            try:
                description = soup_.find('p', class_='sm').text
            except Exception:
                description = 'miss'

            try:    
                adress = soup_.find('td', itemprop='address').find('a').text
            except Exception:
                adress = 'miss'

            try:
                telephone = soup_.find('span', class_='tel').text
            except Exception:
                telephone = 'miss'
                
            try:    
                site = soup_.find(class_='xapa').find(target='_blank').text
            except Exception:
                site = 'miss'    
            try:    
                e_mail = soup_.find('span', itemprop='email').text
            except Exception:
                e_mail = 'miss'

            info = (
                
                {'Name': name_of_company,
                    'Description': description,
                    'Adress': adress,
                    'Telephone number': telephone,
                    'Website': site,
                    'E-mail': e_mail
                    }

            )

            with open('information.json', 'a', encoding='utf-8') as file:
                json.dump(info, file, indent=4, ensure_ascii=False)

            
            print(f'Company #{j} is recorded')
            j += 1

print('Done')






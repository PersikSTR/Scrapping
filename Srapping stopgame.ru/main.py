import requests
from bs4 import BeautifulSoup

list_url = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.43'
}
for i in range(1, 2):
    url = f"https://stopgame.ru/review/new/prohodnjak/p{i}"

    q = requests.get(url=url, headers=headers)
    result = q.content

    soup = BeautifulSoup(result, "lxml")
    games = soup.find_all(class_="article-image image")

    for game in games:
        game_url = game.get('href')
        list_url.append(game_url)


with open('list_url.txt', 'a') as file:
    for line in list_url:
        file.write('https://stopgame.ru' + f'{line}\n')

data_dict = []
count = 0

with open('list_url.txt') as file:
    lines = [line.strip() for line in file.readlines()]

for line in lines:
    q = requests.get(line)
    result = q.content

    soup = BeautifulSoup(result, "lxml")
    name = soup.find(class_='article-title').find('a').text
    score = soup.find(class_='game-info').next_element.next_element.next_element.next_element.next_element.next_element.next_element.text

    game_spec = soup.find_all(class_='game-spec')
    label = []
    for spec in game_spec:
        label.append(spec.find(class_='value').text)

    data = {
        'Название': name ,
        'Оценка': score ,
        'Платформа': label[0] ,
        'Жанр': label[1],
        'Дата выхода': label[2],
        'Разработчик': label[3],
        'Издатель': label[4]
    }
    count += 1
    print(f"#{count}: {line} is done!")

    data_dict.append(data)

    with open('data_dict.txt', 'w', encoding="utf-8") as file:
        for line in data_dict:
            file.write(f"{line}\n")



    
        
        


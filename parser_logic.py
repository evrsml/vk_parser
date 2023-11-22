import json
import requests
from datetime import datetime, date
from urllib.parse import urlparse
from creds import token
import re

url = 'https://vk.com/inorz'


'''Парсим ссылку'''
def user_link_parse(link):
    parsed_url = urlparse(link)
    parts_url = parsed_url.path.split('/')
    last_part = parts_url[-1]

    pattern_id = r'id\d+'
    pattern_public = r'public\d+'
    id_check = re.match(pattern_id, parts_url[-1])
    public_check = re.match(pattern_public, parts_url[-1])


    if id_check is not None:
        id_check = str(id_check)
        last_part.startswith(id_check)
        result = last_part.replace('id', '')
        get_posts_id(result)
        return result
    
    if public_check is not None:
        public_check = str(public_check)
        last_part.startswith(public_check)
        res = last_part.replace('public', '')
        result = f'-{res}'
        get_posts_id(result)
        return result
    else:
        get_posts_name(last_part)
        return last_part

'''Получаем словарь постов с аккаунта или группы по id'''
def get_posts_id(id):
    url = f"https://api.vk.com/method/wall.get?owner_id={id}&count={3}&extended=1&v=5.131&access_token={token}"
    response = requests.get(url)
    data = json.loads(response.text)
    if 'error' not in data:
        from_posts_get_post(data)
        return data
    else:
        print(data['error']['error_msg'])
        pass

'''Получаем словарь постов с аккаунта или группы по короткому имени'''
def get_posts_name(name):
    url = f"https://api.vk.com/method/wall.get?domain={name}&count={3}&extended=1&v=5.131&access_token={token}"
    response = requests.get(url)
    data = json.loads(response.text)
    if 'error' not in data:
        from_posts_get_post(data)
        return data
    else:
        print(data['error']['error_msg'])
        pass

'''Из вложенного словаря достаем отдельные посты и офрмляем для пересылки'''
def from_posts_get_post(data):
    num = (len(data['response']['items']))
    items = data['response']['items']

    for i in range(num):
        text = items[i]['text']
        date = datetime.fromtimestamp(items[i]['date'])
        date_from_post = date.strftime('%Y-%m-%d')
        current_day = date.today().strftime('%Y-%m-%d')
        if date_from_post == current_day:                                   
            owner_id = items[i]['owner_id']
            id_post = items[i]['id']
            result = f"{text}\n\nДата публикации: {date}\nСсылка: https://vk.com/wall{owner_id}_{id_post}"
            print(result)
        else:
            print('Пост не за сегодня')
            pass

#user_link_parse(url)

import json
import asyncio
import re
import requests
import time
import logging
from datetime import datetime
from urllib.parse import urlparse
from creds import vk_token
from bot import send_message
from redisConfig import rc

logging.basicConfig(level=logging.DEBUG,
                  format='%(asctime)s %(levelname)s %(message)s',
                  filename='app.log',
                  filemode='w')

#url= 'https://vk.com/ufa_sluhi'

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
        get_posts_id(result,get_page_name_by_id(result))
        return result
    
    if public_check is not None:
        public_check = str(public_check)
        last_part.startswith(public_check)
        res = last_part.replace('public', '')
        result = f'-{res}'
        get_posts_id(result, get_page_name_by_id(result))
        return result
    else:
        get_posts_name(last_part, get_page_name_by_name(last_part))
        return last_part

'''Получаем словарь постов с аккаунта или группы по id'''

def get_posts_id(id, name):
    url = f"https://api.vk.com/method/wall.get?owner_id={id}&count={5}&extended=1&v=5.199&access_token={vk_token}"
    response = requests.get(url)
    data = json.loads(response.text)
    if 'error' not in data:
        from_posts_get_post(data, name)
        return data
    else:
        logging.error('Ошибка в ответе ВК: %s', data)
        #print(data['error']['error_msg'])
        pass

'''Получаем словарь постов с аккаунта или группы по короткому имени'''

def get_posts_name(shortname,name):
    url = f"https://api.vk.com/method/wall.get?domain={shortname}&count={5}&extended=1&v=5.199&access_token={vk_token}"
    response = requests.get(url)
    data = json.loads(response.text)
    if 'error' not in data:
        from_posts_get_post(data, name)
        return data
    else:
        logging.error('Ошибка в ответе ВК: %s', data)
        #print(data['error']['error_msg'])
        pass

'''Получаем название паблика или аккаунта по айди'''

def get_page_name_by_id(id):

    if  str(id).startswith('-'):
        id = id.split('-')
        url_group = f"https://api.vk.com/method/groups.getById?group_id={id[1]}&v=5.199&access_token={vk_token}"
        response = requests.get(url_group)
        data = json.loads(response.text)
        name = data['response']['groups'][0]['name']
        return name
    
    if str(id).isdigit():
        url_account = f"https://api.vk.com/method/users.get?user_ids={id}&v=5.199&access_token={vk_token}"
        response = requests.get(url_account)
        data = json.loads(response.text)
        last_name = data['response'][0]['last_name']
        first_name = data['response'][0]['first_name']
        full_name = f'{first_name} {last_name}'
        return full_name

'''Получаем название паблика или аккаунта по короткому адресу'''   
            
def get_page_name_by_name(name):
    resolve_name = f"https://api.vk.com/method/utils.resolveScreenName?screen_name={name}&v=5.199&access_token={vk_token}"
    response = requests.get(resolve_name)
    data = json.loads(response.text)
    if data['response']['type'] == 'user':
        res = data['response']['object_id']
        result = get_page_name_by_id(res)
        return result
    else:
        data = data['response']['object_id']
        res = f'-{data}'
        result = get_page_name_by_id(res)
        return result
       
'''Из вложенного словаря достаем отдельные посты и офрмляем для пересылки'''
  
def from_posts_get_post(data, name):
    num = (len(data['response']['items']))
    items = data['response']['items']

    loop = asyncio.get_event_loop()

    for i in range(num):
        text = items[i]['text']
        date = datetime.fromtimestamp(items[i]['date'])
        date_from_post = date.strftime('%Y-%m-%d')
        current_day = date.today().strftime('%Y-%m-%d')
        if date_from_post == current_day:

            owner_id = items[i]['owner_id']
            id_post = items[i]['id']
            key = f'{owner_id}_{id_post}'
            value = f'{owner_id}_{id_post}'

        #проверяем есть ли сообщение в кэше редиса

            if rc.check_n_write(key, value):
                pass
            else:

        #проверяем на лимит текста для телеграм        
                if len(text) > 3950:
                    text_short = text[:3950]
                    result = f"Источник: {name}\n\n{text_short}\n..полный текст по ссылке..\n\nДата публикации: {date}\nСсылка: https://vk.com/wall{owner_id}_{id_post}"
                else:
                    result = f"Источник: {name}\n\n{text}\n\nДата публикации: {date}\nСсылка: https://vk.com/wall{owner_id}_{id_post}"
                time.sleep(3)

                task = loop.create_task(send_message(result))
                loop.run_until_complete(task)
                logging.info('Пересылаем сообщение в бот %s')
                
                #print(result)
        else:
            logging.info('Пост не за сегодня: %s', date_from_post)
            #print('Пост не за сегодня')
            pass

#user_link_parse(url)

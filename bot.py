from aiogram import Bot
from creds import tg_token
import logging

logging.basicConfig(level=logging.DEBUG,
                  format='%(asctime)s %(levelname)s %(message)s',
                  filename='app.log',
                  filemode='w')

bot  = Bot(token=tg_token)

ads_filter = ['скидка','₽','ERID','erid', 'Erid', 'реклама', 'Администрация сообщества поздравляет с Днем Рождения']

async def send_message(msg):
        if not any(word in msg for word in ads_filter):
                await bot.send_message(chat_id= '@mytesr27', text= str(msg))
                logging.info('Бот отправил сообщение')
        else:
             logging.info('Реклмное сообщение', msg)
             print('не прошел рекламный фильтр')
             pass



#'-1002057457095' - рабочий чат Лента ВК
    
    
    
   



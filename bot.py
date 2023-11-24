from aiogram import Bot
from creds import tg_token


bot  = Bot(token=tg_token)

async def send_message(msg):
        await bot.send_message(chat_id='-1002057457095', text= str(msg))
    
    
    
   



import asyncio
from aiogram import Bot
from creds import tg_token


bot  = Bot(token=tg_token)

async def send_message(msg):
        await bot.send_message(chat_id='@mytesr27', text= str(msg))
    
    
    
   



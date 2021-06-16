from time import sleep
from telethon import TelegramClient, events
import os
import time
import asyncio
import nest_asyncio
from send_request import create_session

client = TelegramClient('anon', os.getenv('API_ID'), os.getenv('API_HASH'))
print('{}'.format(os.getenv('CHATS')))


@client.on(events.NewMessage(chats=['tutby_official', 'FloodInterview',' FaangInterview', 'belteanews', 'BotFather', 'CryptoComOfficial']))
async def my_event_handler(event):
    time_current = time.localtime()
    dt = event.message.date
    print(dt)
    chat_from = event.chat if event.chat else (await event.get_chat())  # telegram MAY not send the chat enity
    chat_title = chat_from.username
    message_from_channel = {
        "source": "telegram",
        "sender": chat_title,
        "content": event.raw_text,
        "url": "",
        "created_date": time.strftime('%Y-%m-%dT%H:%M:%S.866Z', time_current)
    }
    print(message_from_channel)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(await create_session(message_from_channel))
    else:
        nest_asyncio.apply(loop)
        return asyncio.run(await create_session(message_from_channel))


client.start(phone=os.getenv('PHONE'))
#client.run_until_disconnected()

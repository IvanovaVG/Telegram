from time import sleep
from typing import Dict, Any, Union

from telethon import TelegramClient, events
import os
import time
import asyncio
import nest_asyncio
from send_request import create_session

client = TelegramClient('anon', os.getenv('API_ID'), os.getenv('API_HASH'))
# print('{}'.format(os.getenv('CHATS')))


async def run():
    await client.connect()

    await client.start(os.getenv('PHONE'))


@client.on(events.NewMessage(chats=['tutby_official', 'FloodInterview', 'FaangInterview', 'belteanews', 'BotFather', 'CryptoComOfficial']))
async def my_event_handler(event):
    time_current = time.localtime()
    dt = event.message.date
    chat_from = event.chat if event.chat else (await event.get_chat())
    chat_title = chat_from.username
    message_from_channel: Dict[str, Union[str, Any]] = {
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





client.loop.run_until_complete(run())
client.run_until_disconnected()


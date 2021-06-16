import json
import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()

url_connection = os.getenv('URL')


async def do_post(session, url_request: str, message_from_channel: str, i: int):
    try:
        await session.post(url=url_request, data=json.dumps(message_from_channel), headers={'content-type': 'application/json'})
        try:
            resp = await read_file(session, url_request)
            return resp
        except:
            return 'No such file or some problems with it'
    except aiohttp.client_exceptions.ClientConnectorError:
        if i == 4:
            await create_file(message_from_channel)
            return 'Write to file'
        else:
            return 'Error send message'


async def create_session(data_message: str):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=4)) as session:
        await asyncio.sleep(15)
        resp = await do_post(session, url_connection, data_message, 0)
        if resp == 'Error send message':
            for i in range(1, 5):
                await asyncio.sleep(5)
                resp = await do_post(session, url_connection, data_message, i)
                if resp == 'Error send message':
                    continue
        return asyncio.sleep(0)


async def create_file(message_from_channel):
    with open('data.json', 'a', encoding='utf-8') as file_json:
        json.dump(message_from_channel, file_json, ensure_ascii=False)
        file_json.write("\n")
        file_json.close()
        return 'created'


async def read_file(session, url_request: str):
    with open('data.json', 'r', encoding='utf-8') as json_file:
        for line in json_file.readlines():
            old_message = json.loads(line)
            try:
                await session.post(url=url_request, data=old_message,headers={'content-type': 'application/json'})
            except (aiohttp.client_exceptions.ClientConnectorError, RuntimeError):
                return await aiohttp.client_exceptions.ClientConnectorError
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json_file.writelines('')
        json_file.close()
        return 'File started be a clean'



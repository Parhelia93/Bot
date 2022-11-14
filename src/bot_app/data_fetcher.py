import json
from tokenize import String
import aiohttp
from .local_settings import WORDS_API_URL_RANDOM, WORDS_API_URL_ANSWER, WORDS_API_URL_ANSWERS


async def get_random(telegram_id: String):
    async with aiohttp.ClientSession() as session:
        async with session.get(WORDS_API_URL_RANDOM + str(telegram_id)) as responce:
            return await responce.json()


async def put_answer(data):
    async with aiohttp.ClientSession() as session:
        async with session.patch(WORDS_API_URL_ANSWER, json=data):
            pass


async def put_answers(data):
    async with aiohttp.ClientSession() as session:
        async with session.put(WORDS_API_URL_ANSWERS, json=data):
            pass
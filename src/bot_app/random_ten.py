from aiogram import types
from bot_app.states import GameStates
from .app import dp, bot
from .keyboards import inline_kb
from .data_fetcher import get_random, put_answer, put_answers
from aiogram.dispatcher import FSMContext
from .messages import EMPTY_DICTIONARY_EMPTYING, TRAINING_DONE, WRONG_ANSWER, START_TRAIN_MESSAGE
from .local_settings import CNT_TRAINT_STEP
from .utils import prepare_dict, find_answer, prepare_list_dict
import random


@dp.message_handler(commands='train_ten', state="*")
async def train_ten(message: types.Message, state: FSMContext):
    await GameStates.random_ten.set()
    await message.answer(START_TRAIN_MESSAGE, reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data in ['En-Rus', 'Rus-En'], state=GameStates.random_ten)
async def language_choose_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    res = await get_random(callback_query.from_user.id)
    async with state.proxy() as data:
        result = prepare_dict(res, answer)
        data.update(choose_language=answer, step=1, word=result.get('word'), translate=result.get('translate_list'), example=result.get('example'), stat_id=result.get('stat_id'), telegram_id=str(callback_query.from_user.id), all_pk=result.get('all_pk'), all_message=result.get('all_msg'))
        await GameStates.random_ten.set()
        if not res:
            await state.finish()
            return await bot.send_message(callback_query.from_user.id, EMPTY_DICTIONARY_EMPTYING)
        if answer == 'En-Rus':
            await bot.send_message(callback_query.from_user.id, f"Step: {data['step']}, Как переводится: {data['word']}")
        else:
            word = random.choice(data['word'])
            await bot.send_message(callback_query.from_user.id, f"Step: {data['step']}, Как переводится: {word}")

@dp.message_handler(lambda message: message.text not in ["/start", "/help", "/asd"], state=GameStates.random_ten)
async def answer_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() in data.get('translate') and data['choose_language'] == 'En-Rus' or data['choose_language'] == 'Rus-En' and message.text.lower() in data.get('translate'):
            # await message.answer(f"Step: {data.get('translate')}")
            data['step']+=1
            if data['choose_language'] == 'En-Rus':
                true_pk = find_answer(data.get('all_message'), message.text)
                await put_answer({'pk': true_pk, 'answer': 'True'})
            else:
                # for pk in data['all_pk']:
                #     await put_answer({'pk': pk, 'answer': 'True'})
                # prepare_list_dict
                pks = [pk for pk in data['all_pk']]
                res = prepare_list_dict(pks,'True')
                await put_answers(res)

            if data['step'] > CNT_TRAINT_STEP:
                await state.finish()
                return await message.answer(TRAINING_DONE)

            res = await get_random(message.from_user.id)
            result = prepare_dict(res, data['choose_language'])
            data.update(word=result.get('word'), translate=result.get('translate_list'), example=result.get('example'), stat_id=result.get('stat_id'), telegram_id=str(message.from_user.id), all_pk=result.get('all_pk'), all_message=result.get('all_msg'))
            if data['choose_language'] == 'En-Rus':
                await message.answer(f"Step: {data['step']}, Как переводится: {data['word']}")
            else:
                word = random.choice(data['word'])
                await message.answer(f"Step: {data['step']}, Как переводится: {word}")
        else:
            await message.answer(WRONG_ANSWER)
            # for pk in data['all_pk']:
            #     await put_answer({'pk': pk, 'answer': 'False'})
            pks = [pk for pk in data['all_pk']]
            res = prepare_list_dict(pks,'False')
            await put_answers(res)

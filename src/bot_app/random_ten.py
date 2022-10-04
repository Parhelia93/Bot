
from aiogram import types
from bot_app.states import GameStates
from .app import dp
from .keyboards import inline_kb
from .data_fetcher import get_random, put_answer
from aiogram.dispatcher import FSMContext
from .messages import EMPTY_DICTIONARY_EMPTYING, TRAINING_DONE, WRONG_ANSWER
from .local_settings import CNT_TRAINT_STEP
from .utils import get_random_word_detail, get_all_translate

@dp.message_handler(commands='train_ten', state="*")
async def train_ten(message: types.Message, state: FSMContext):
    await GameStates.random_ten.set()
    res = await get_random(message.from_user.id)
    async with state.proxy() as data:
        word = res.get('word')
        word_detail = res.get('words_detail')
        translate, example, stat_id = get_random_word_detail(word_detail)
        translate_list = get_all_translate(word_detail)
        
        data['step'] = 1
        data['word'] = word
        data['translate'] = translate_list
        data['example'] = example
        data['stat_id'] = stat_id
        data['telegram_id'] = str(message.from_user.id)
        if not data['word']:
            await state.finish()
            return await message.reply(EMPTY_DICTIONARY_EMPTYING)
        await message.reply(f"Step: {data['step']}, {data['word']}, {data['stat_id']}")


# @dp.message_handler(lambda message: message.text not in ["/start", "/help", "/asd"], state=GameStates.random_ten)
# async def answer_handler(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if message.text in data.get('translate'):
#             user_answer_dict = {'pk': data.get('stat_id'), 'answer': 'True'}
#             await put_answer(user_answer_dict)
#             data['step']+=1
#             if data['step'] > CNT_TRAINT_STEP:
#                 await state.finish()
#                 return await message.answer(TRAINING_DONE)    
#             res = await get_random(message.from_user.id)
#             data['translate'] = res.get('translate')
#             data['word'] = res.get('word')
#             data['example'] = res.get('example')
#             data['stat_id'] = res.get('word_stat').get('pk')
#             data['telegram_id'] = str(message.from_user.id)
#             await message.answer(f"Step: {data['step']}, {data['word']}, {data['stat_id']}")
#         else:
#             await message.answer(WRONG_ANSWER)

@dp.message_handler(lambda message: message.text not in ["/start", "/help", "/asd"], state=GameStates.random_ten)
async def answer_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text in data.get('translate'):
            user_answer_dict = {'pk': data.get('stat_id'), 'answer': 'True'}
            await put_answer(user_answer_dict)
            data['step']+=1
            if data['step'] > CNT_TRAINT_STEP:
                await state.finish()
                return await message.answer(TRAINING_DONE)    
            res = await get_random(message.from_user.id)
            word = res.get('word')
            word_detail = res.get('words_detail')
            translate, example, stat_id = get_random_word_detail(word_detail)
            translate_list = get_all_translate(word_detail)
            data['translate'] = translate
            data['word'] = word
            data['example'] = example
            data['stat_id'] = stat_id
            data['telegram_id'] = str(message.from_user.id)
            await message.answer(f"Step: {data['step']}, {data['word']}, {data['stat_id']}")
        else:
            await message.answer(WRONG_ANSWER)


            # Добавить функцию, увеличиваем True/False именно того pk, на который ответили правильно, ели ответили неверно, то тот который был в памяти
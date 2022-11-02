from aiogram import types
from .states import GameStates
from .app import dp, bot
from .keyboards import inline_kb
from .data_fetcher import get_random, put_answer, put_answers
from aiogram.dispatcher import FSMContext
from .messages import EMPTY_DICTIONARY_EMPTYING, TRAINING_DONE, WRONG_ANSWER, START_TRAIN_MESSAGE, RUS_EN, EN_RUS, \
    DONT_KNOW_CMD, NEW_MESSAGE, FINISH
from .local_settings import CNT_TRAINT_STEP
from .utils import prepare_dict, find_answer, prepare_list_dict, prepare_server_word
import random
from .data_struct import ServerRandomWord, CheckAnswer
from .game_play import check_user_answer


@dp.message_handler(commands='end', state=GameStates.random_ten)
async def end_training(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(TRAINING_DONE)


@dp.message_handler(commands='train', state="*")
async def train_ten(message: types.Message, state: FSMContext):
    await GameStates.random_ten.set()
    await message.answer(START_TRAIN_MESSAGE, reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data in [RUS_EN, EN_RUS], state=GameStates.random_ten)
async def language_choose_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    answer = callback_query.data
    res = await get_random(callback_query.from_user.id)
    async with state.proxy() as data:
        data.update(server_word=prepare_server_word(res, answer, 1, callback_query.from_user.id))
        await GameStates.random_ten.set()
        if not res:
            await state.finish()
            return await bot.send_message(callback_query.from_user.id, EMPTY_DICTIONARY_EMPTYING)
        await bot.send_message(callback_query.from_user.id,
                               f"Step: {data['server_word'].step}, How to translate the word: {data['server_word'].word}")


@dp.message_handler(lambda message: message.text not in ["/start", "/help", "/end"], state=GameStates.random_ten)
async def answer_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        server_word: ServerRandomWord = data.get('server_word')
        user_answer = message.text.lower()
        checked_answer = await check_user_answer(user_answer=user_answer, server_word=server_word)

        if checked_answer.status == FINISH:
            await state.finish()
            return await message.answer(TRAINING_DONE)

        if checked_answer.status == NEW_MESSAGE:
            res = await get_random(message.from_user.id)
            server_word = prepare_server_word(res, checked_answer.server_word.choose_language,
                                              checked_answer.server_word.step,
                                              message.from_user.id)
            data.update(server_word=server_word)
            return await message.answer(f"Step: {data['server_word'].step}, How to translate the word: {data['server_word'].word}")

        if checked_answer.status == WRONG_ANSWER:
            return await message.answer(f"Step: {data['server_word'].step}, {WRONG_ANSWER}")

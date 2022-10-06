from aiogram import types
from bot_app.states import GameStates
from .app import dp
from .keyboards import inline_kb
from .data_fetcher import get_random, put_answer
from aiogram.dispatcher import FSMContext
from .messages import EMPTY_DICTIONARY_EMPTYING, TRAINING_DONE, WRONG_ANSWER
from .local_settings import CNT_TRAINT_STEP
from .utils import prepare_dict, find_answer

@dp.message_handler(commands='train_ten', state="*")
async def train_ten(message: types.Message, state: FSMContext):
    await GameStates.random_ten.set()
    res = await get_random(message.from_user.id)
    async with state.proxy() as data:
        result = prepare_dict(res)
        await message.answer(result)
        data.update(step=1, word=result.get('word'), translate=result.get('translate_list'), example=result.get('example'), stat_id=result.get('stat_id'), telegram_id=str(message.from_user.id), all_pk=result.get('all_pk'), all_message=result.get('all_msg'))
        if not res:
            await state.finish()
            return await message.reply(EMPTY_DICTIONARY_EMPTYING)
        await message.reply(f"Step: {data['step']}, {data['word']}, {data['stat_id']}")


@dp.message_handler(lambda message: message.text not in ["/start", "/help", "/asd"], state=GameStates.random_ten)
async def answer_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text in data.get('translate'):
            data['step']+=1
            true_pk = find_answer(data.get('all_message'), message.text)
            await put_answer({'pk': true_pk, 'answer': 'True'})
            
            if data['step'] > CNT_TRAINT_STEP:
                await state.finish()
                return await message.answer(TRAINING_DONE)

            res = await get_random(message.from_user.id)
            result = prepare_dict(res)
            data.update(word=result.get('word'), translate=result.get('translate_list'), example=result.get('example'), stat_id=result.get('stat_id'), telegram_id=str(message.from_user.id), all_pk=result.get('all_pk'), all_message=result.get('all_msg'))
            await message.answer(f"Step: {data['step']}, {data['word']}, {data['stat_id']}")
        else:
            await message.answer(WRONG_ANSWER)
            for pk in data['all_pk']:
                await put_answer({'pk': pk, 'answer': 'False'})


from aiogram import types
from bot_app.states import GameStates
from .app import dp
from .keyboards import inline_kb
from .data_fetcher import get_random, put_answer
from aiogram.dispatcher import FSMContext



@dp.message_handler(commands='train_ten', state="*")
async def train_ten(message: types.Message, state: FSMContext):
    await GameStates.random_ten.set()
    res = await get_random(message.from_user.id)
    async with state.proxy() as data:
        data['step'] = 1
        data['translate'] = res.get('translate')
        data['word'] = res.get('word')
        data['example'] = res.get('example')
        data['stat_id'] = res.get('word_stat').get('pk')
        data['telegram_id'] = str(message.from_user.id)
        await message.reply(f"Step: {data['step']}, {data['word']}, {data['stat_id']}")


@dp.message_handler(lambda message: message.text not in ["/start", "/help", "/asd"], state=GameStates.random_ten)
async def answer_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == data.get('translate'):
            d = {'pk': data.get('stat_id'), 'answer': 'True'}
            await put_answer(d)
            data['step']+=1
            if data['step'] > 5:
                await state.finish()
                return await message.answer('Training done')    
            res = await get_random(message.from_user.id)
            data['translate'] = res.get('translate')
            data['word'] = res.get('word')
            data['example'] = res.get('example')
            data['stat_id'] = res.get('word_stat').get('pk')
            data['telegram_id'] = str(message.from_user.id)
            await message.answer(f"Step: {data['step']}, {data['word']}, {data['stat_id']}")
            
        else:
            await message.answer('Wrong answer, try again')
from aiogram.dispatcher.filters.state import State, StatesGroup

class GameStates(StatesGroup):
    start=State()
    choose_language = State()
    random_ten = State()
    all_words = State()


from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

inline_button_def = InlineKeyboardButton('En-Rus', callback_data='En-Rus')
inline_button_die = InlineKeyboardButton('Rus-En', callback_data='Rus-En')


inline_kb = InlineKeyboardMarkup()
inline_kb.add(inline_button_def)
inline_kb.add(inline_button_die)

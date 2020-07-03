from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_1 = InlineKeyboardButton('Style Transfer', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('GAN', callback_data='button2')
inline_kb = InlineKeyboardMarkup().row(inline_btn_1, inline_btn_2)

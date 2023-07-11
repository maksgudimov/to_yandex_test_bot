from aiogram import types

# создание стартовой инлайн клавиатуры
def start_keyboard():
    kb_start = types.InlineKeyboardMarkup(row_width=2)
    b1_start = types.InlineKeyboardMarkup(text=f"Посмотреть 🖼", callback_data="start_photo")
    b2_start = types.InlineKeyboardMarkup(text=f"Пост 📝", callback_data="start_postabout")
    b3_start = types.InlineKeyboardMarkup(text=f"Мои голосовые 🎵", callback_data="start_voices")
    kb_start.add(b1_start, b2_start,b3_start)
    return kb_start
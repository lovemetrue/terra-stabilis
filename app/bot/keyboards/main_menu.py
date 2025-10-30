from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard():
    """Главное меню"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="🚀 Рассчитать стоимость"))
    builder.add(KeyboardButton(text="📞 Оставить контакты"))
    builder.add(KeyboardButton(text="ℹ️ О компании"))

    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_geodata_keyboard():
    """Клавиатура для сбора исходных данных"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="📝 Разработка программы геотехнических исследований"))
    builder.add(KeyboardButton(text="💎 Геотехническое документирование керна"))
    builder.add(KeyboardButton(text="⬅️ Главное меню"))

    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def get_stability_keyboard():
    """Клавиатура для расчетов устойчивости"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="2D ОГР"))
    builder.add(KeyboardButton(text="2D ПГР"))
    builder.add(KeyboardButton(text="3D ОГР"))
    builder.add(KeyboardButton(text="3D ПГР"))
    builder.add(KeyboardButton(text="⬅️ Главное меню"))

    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_geomechanic_keyboard():
    """Клавиатура для геомеханика на час"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="👨‍💼 Ведущий геомеханик"))
    builder.add(KeyboardButton(text="👨‍🔬 Главный геомеханик"))
    builder.add(KeyboardButton(text="⬅️ Главное меню"))

    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_monitoring_keyboard():
    """Клавиатура для мониторинга"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="🔺 Призменный мониторинг"))
    builder.add(KeyboardButton(text="📡 Интерпретация данных радарного мониторинга"))
    builder.add(KeyboardButton(text="⚙️ Настройка пороговых значений по TARP"))
    builder.add(KeyboardButton(text="📋 Разработка документа TARP"))
    builder.add(KeyboardButton(text="⬅️ Главное меню"))

    builder.adjust(1, 1, 1, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def get_hydrogeology_keyboard():
    """Клавиатура для гидрогеологии"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="🌊 Гидрогеологическое обследование участка"))
    builder.add(KeyboardButton(text="📊 Интерпретация данных наблюдательных скважин"))
    builder.add(KeyboardButton(text="💻 Моделирование фильтрационного потока"))
    builder.add(KeyboardButton(text="🔧 Расчет депрессии и проект дренажной системы"))
    builder.add(KeyboardButton(text="📈 Гидрогеологический мониторинг"))
    builder.add(KeyboardButton(text="⚖️ Оценка влияния подземных вод на устойчивость"))
    builder.add(KeyboardButton(text="⬅️ Главное меню"))

    builder.adjust(1, 1, 1, 1, 1, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def get_contact_keyboard():
    """Клавиатура для перехода к контактам"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="✅ Оставить контакты"))
    builder.add(KeyboardButton(text="⬅️ Главное меню"))

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_yes_no_keyboard():
    """Клавиатура ДА/НЕТ"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="✅ Да"))
    builder.add(KeyboardButton(text="❌ Нет"))
    builder.add(KeyboardButton(text="⬅️ Назад"))

    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_back_keyboard():
    """Клавиатура с кнопкой Назад"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Reply-клавиатура главного меню"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="📊 Сбор исходных данных"),
        KeyboardButton(text="📐 Расчёт устойчивости"),
        KeyboardButton(text="👨‍💼 Геомеханик на час"),
        KeyboardButton(text="📡 Мониторинг"),
        KeyboardButton(text="💧 Гидрогеология"),
        KeyboardButton(text="🏢 О компании"),
        KeyboardButton(text="ℹ️ Помощь"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup(resize_keyboard=True)


def get_geodata_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для сбора исходных данных"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="📝 Разработка программы геотехнических исследований"),
        KeyboardButton(text="💎 Геотехническое документирование керна"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_stability_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для расчета устойчивости"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="2D ОГР"),
        KeyboardButton(text="2D ПГР"),
        KeyboardButton(text="3D ОГР"),
        KeyboardButton(text="3D ПГР"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_monitoring_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для мониторинга"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="🔺 Призменный мониторинг"),
        KeyboardButton(text="📡 Интерпретация данных георадарного мониторинга"),
        KeyboardButton(text="⚙️ Настройка пороговых значений по TARP"),
        KeyboardButton(text="📋 Разработка документа TARP"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_hydrogeology_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для гидрогеологии"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="🌊 Гидрогеологическое обследование участка"),
        KeyboardButton(text="📊 Интерпретация данных наблюдательных скважин"),
        KeyboardButton(text="💻 Моделирование фильтрационного потока"),
        KeyboardButton(text="🔧 Расчет депрессии и проект дренажной системы"),
        KeyboardButton(text="📈 Гидрогеологический мониторинг"),
        KeyboardButton(text="⚖️ Оценка влияния подземных вод на устойчивость"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_geomechanic_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для геомеханика на час"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="👨‍💼 Ведущий геомеханик"),
        KeyboardButton(text="👨‍🔬 Главный геомеханик"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для запроса контактов"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="✅ Оставить контакты"),
        KeyboardButton(text="⬅️ Назад в меню"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_skip_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для пропуска необязательных полей"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="⏭️ Пропустить"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_back_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура только с кнопкой Назад"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_phone_input_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора способа ввода телефона"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="📞 Отправить контакт", request_contact=True),
        KeyboardButton(text="📝 Ввести номер вручную"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_manual_phone_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для ручного ввода телефона"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_yes_no_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура Да/Нет"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="✅ Да"),
        KeyboardButton(text="❌ Нет"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
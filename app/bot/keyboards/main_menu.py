from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Reply-клавиатура главного меню"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="📊 Сбор исходных гео данных"),
        KeyboardButton(text="📐 Расчеты устойчивости"),
        KeyboardButton(text="👨‍💼 Консультации геомеханика"),
        KeyboardButton(text="📡 Мониторинг инженерных объектов"),
        KeyboardButton(text="🏢 О компании"),
        KeyboardButton(text="ℹ️ Помощь"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup(resize_keyboard=True)


def get_geodata_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для сбора гео данных"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="📝 Разработка программы"),
        KeyboardButton(text="🗺️ Геотехническое картирование"),
        KeyboardButton(text="💎 Документирование керна"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)  # 1 кнопка в строке
    return builder.as_markup(resize_keyboard=True)


def get_stability_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для расчета устойчивости"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="2D расчеты"),
        KeyboardButton(text="3D расчеты"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_2d_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для 2D расчета"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="2D ОГР"),
        KeyboardButton(text="2D ПГР"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_3d_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для 3D расчета"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="3D ОГР"),
        KeyboardButton(text="3D ПГР"),
        KeyboardButton(text="⬅️ Назад"),
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_monitoring_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для мониторинга"""
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="📡 Георадарный мониторинг"),
        KeyboardButton(text="🔺 Призменный мониторинг"),
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
    """Клавиатура только с кнопкой Назад для обязательных полей"""
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
from aiogram import Router, F
from aiogram.types import Message, Contact
from aiogram.fsm.context import FSMContext
import re

from app.bot.states import ContactCollection, PhoneInput
from app.bot.keyboards.main_menu import *
from apps.bot_data.bot_utils import save_user_event, save_contact

router = Router()


def validate_phone_number(phone: str) -> bool:
    """Проверка номера телефона"""
    # Убираем все нецифровые символы кроме +
    cleaned_phone = re.sub(r'[^\d+]', '', phone)

    # Проверяем российские номера
    russian_pattern = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')

    # Проверяем международные номера
    international_pattern = re.compile(r'^\+\d{1,3}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{1,4}$')

    return bool(russian_pattern.match(phone) or international_pattern.match(cleaned_phone))


def format_phone_number(phone: str) -> str:
    """Форматирование номера телефона"""
    # Убираем все нецифровые символы
    digits = re.sub(r'\D', '', phone)

    # Если номер начинается с 8, заменяем на +7
    if digits.startswith('8') and len(digits) == 11:
        digits = '7' + digits[1:]

    # Если номер без кода страны, добавляем +7
    if len(digits) == 10:
        digits = '7' + digits

    # Форматируем как +7 (XXX) XXX-XX-XX
    if digits.startswith('7') and len(digits) == 11:
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"

    return f"+{digits}" if not phone.startswith('+') else phone


@router.message(ContactCollection.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Обработка имени"""
    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer(
            "Возвращаемся в главное меню:",
            reply_markup=get_main_menu_keyboard()
        )
        return

    await state.update_data(name=message.text)
    await state.set_state(ContactCollection.waiting_for_phone)

    await save_user_event(
        user_id=message.from_user.id,
        event_type='contact_name_provided',
        event_data={'name': message.text},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    phone_text = """
📱 Телефон для связи

Вы можете:
• Поделиться контактом (рекомендуется)
• Ввести номер вручную

Выберите способ:
    """

    await message.answer(
        phone_text,
        reply_markup=get_phone_input_keyboard()
    )


@router.message(ContactCollection.waiting_for_phone, F.text == "📞 Отправить контакт")
async def request_contact(message: Message, state: FSMContext):
    """Запрос отправки контакта"""
    await message.answer(
        "Пожалуйста, нажмите кнопку '📞 Отправить контакты' ниже:",
        reply_markup=get_phone_input_keyboard()
    )


@router.message(ContactCollection.waiting_for_phone, F.text == "📝 Ввести номер вручную")
async def request_manual_phone(message: Message, state: FSMContext):
    """Запрос ручного ввода телефона"""
    await state.set_state(PhoneInput.waiting_for_phone_input)

    await message.answer(
        "📝 Введите ваш номер телефона:\n\n"
        "Формат: +7 XXX XXX-XX-XX или 8 XXX XXX-XX-XX\n"
        "Пример: +7 (912) 345-67-89",
        reply_markup=get_manual_phone_keyboard()
    )


@router.message(ContactCollection.waiting_for_phone, F.text == "⬅️ Назад")
async def back_from_phone_selection(message: Message, state: FSMContext):
    """Возврат от выбора способа ввода телефона к имени"""
    await state.set_state(ContactCollection.waiting_for_name)

    await message.answer(
        "Введите ваше имя:",
        reply_markup=get_back_keyboard()
    )


@router.message(ContactCollection.waiting_for_phone, F.contact)
async def process_contact(message: Message, state: FSMContext):
    """Обработка отправленного контакта"""
    contact = message.contact
    phone_number = contact.phone_number

    # Форматируем номер
    formatted_phone = format_phone_number(phone_number)

    # Получаем данные из состояния
    user_data = await state.get_data()
    name = user_data.get('name')

    # Сохраняем контакт
    await save_contact(
        user_id=message.from_user.id,
        phone=formatted_phone,
        name=name,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await save_user_event(
        user_id=message.from_user.id,
        event_type='contact_shared',
        event_data={'phone': formatted_phone, 'source': 'contact'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    # Очищаем состояние
    await state.clear()

    success_text = f"""
✅ Спасибо, {name}!

Ваш контакт успешно сохранён. 
Наш специалист свяжется с вами в ближайшее время.

Если у вас есть срочные вопросы, звоните: +7 (XXX) XXX-XX-XX

Хотите рассчитать еще одну услугу?
    """

    await message.answer(
        success_text,
        reply_markup=get_main_menu_keyboard()
    )


@router.message(PhoneInput.waiting_for_phone_input, F.text)
async def process_manual_phone(message: Message, state: FSMContext):
    """Обработка ручного ввода телефона"""
    if message.text == "⬅️ Назад":
        await state.set_state(ContactCollection.waiting_for_phone)
        await message.answer(
            "Выберите способ ввода телефона:",
            reply_markup=get_phone_input_keyboard()
        )
        return

    phone_number = message.text

    # Проверяем валидность номера
    if not validate_phone_number(phone_number):
        await message.answer(
            "❌ Неверный формат номера телефона.\n\n"
            "Пожалуйста, введите номер в формате:\n"
            "• +7 (912) 345-67-89\n"
            "• 8 (912) 345-67-89\n"
            "• 89123456789\n\n"
            "Попробуйте еще раз:",
            reply_markup=get_manual_phone_keyboard()
        )
        return

    # Форматируем номер
    formatted_phone = format_phone_number(phone_number)

    # Получаем данные из состояния
    user_data = await state.get_data()
    name = user_data.get('name')

    # Сохраняем контакт
    await save_contact(
        user_id=message.from_user.id,
        phone=formatted_phone,
        name=name,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await save_user_event(
        user_id=message.from_user.id,
        event_type='contact_phone_provided',
        event_data={'phone': formatted_phone, 'source': 'manual'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    # Очищаем состояние
    await state.clear()

    success_text = f"""
✅ Спасибо, {name}!

Ваш контакт успешно сохранён. 
Наш специалист свяжется с вами в ближайшее время.

Если у вас есть срочные вопросы, звоните: +7 (XXX) XXX-XX-XX

Хотите рассчитать еще одну услугу?
    """

    await message.answer(
        success_text,
        reply_markup=get_main_menu_keyboard()
    )
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from app.bot.states import ContactCollection
from app.bot.keyboards.main_menu import (get_skip_keyboard,
                                         get_main_menu_keyboard,
                                         get_contact_keyboard,
                                         get_back_keyboard)  # Добавим клавиатуру только с "Назад"
from apps.bot_data.models import BotLead, BotUserEvent

router = Router()


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

    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='contact_name_provided',
        event_data={'name': message.text}
    )

    await message.answer(
        "📱 Теперь введите ваш номер телефона:",
        reply_markup=get_back_keyboard()  # Для обязательных полей - только кнопка "Назад"
    )


@router.message(ContactCollection.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Обработка телефона"""
    if message.text == "⬅️ Назад":
        await state.set_state(ContactCollection.waiting_for_name)
        await message.answer(
            "Введите ваше имя:",
            reply_markup=get_back_keyboard()
        )
        return

    await state.update_data(phone=message.text)
    await state.set_state(ContactCollection.waiting_for_email)

    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='contact_phone_provided',
        event_data={'phone': message.text}
    )

    await message.answer(
        "📧 Введите ваш email (необязательно):",
        reply_markup=get_skip_keyboard()  # Для необязательных полей - "Пропустить" и "Назад"
    )


@router.message(ContactCollection.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    """Обработка email"""
    if message.text == "⬅️ Назад":
        await state.set_state(ContactCollection.waiting_for_phone)
        await message.answer(
            "Введите ваш номер телефона:",
            reply_markup=get_back_keyboard()
        )
        return

    email = None
    if message.text != "⏭️ Пропустить":
        email = message.text

    await state.update_data(email=email)
    await state.set_state(ContactCollection.waiting_for_company)

    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='contact_email_provided',
        event_data={'email': email}
    )

    await message.answer(
        "🏢 Введите название вашей компании (необязательно):",
        reply_markup=get_skip_keyboard()
    )


@router.message(ContactCollection.waiting_for_company)
async def process_company(message: Message, state: FSMContext):
    """Обработка компании и сохранение лида"""
    if message.text == "⬅️ Назад":
        await state.set_state(ContactCollection.waiting_for_email)
        await message.answer(
            "Введите ваш email:",
            reply_markup=get_skip_keyboard()
        )
        return

    company = None
    if message.text != "⏭️ Пропустить":
        company = message.text

    # Получаем все данные
    user_data = await state.get_data()

    # Создаем лид в базе данных
    lead = await sync_to_async(BotLead.objects.create)(
        name=user_data['name'],
        phone=user_data['phone'],
        email=user_data.get('email'),
        company=company,
        service_type=user_data.get('final_service'),
        calculated_price=user_data.get('calculated_price'),
        source="telegram"
    )

    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='lead_created',
        event_data={'lead_id': lead.id}
    )

    # Очищаем состояние
    await state.clear()

    success_text = f"""
✅ Спасибо, {user_data['name']}!

Ваши контакты успешно сохранены. 
Наш специалист свяжется с вами в ближайшее время для уточнения деталей.

Номер вашей заявки: #{lead.id}

Если у вас есть срочные вопросы, звоните: +7 (XXX) XXX-XX-XX

Хотите рассчитать еще одну услугу?
    """

    await message.answer(
        success_text,
        reply_markup=get_main_menu_keyboard()
    )
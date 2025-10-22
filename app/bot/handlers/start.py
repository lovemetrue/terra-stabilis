from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.bot.keyboards.main_menu import get_main_menu_keyboard
from apps.bot_data.bot_utils import save_user_event

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    await save_user_event(
        user_id=message.from_user.id,
        event_type='start',
        event_data={'source': 'telegram', 'command': 'start'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await state.clear()

    welcome_text = """
🏗️ Добро пожаловать в GeoEngineering Services!

Мы специализируемся на геоинженерных услугах и расчетах. 

Выберите интересующую вас услугу:
    """

    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )

@router.message(F.text == "🏢 О компании")
async def about_company(message: Message):
    """Информация о компании"""
    await save_user_event(
        user_id=message.from_user.id,
        event_type='about_view',
        event_data={},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    about_text = """
🏢 TerraStabilis - Ваш надежный партнер в геоинженерных решениях

Наша компания более 15 лет предоставляет комплексные услуги в области геотехнических исследований и расчетов устойчивости сооружений.

🔹 Наши компетенции:
• Геотехнические изыскания и исследования
• Расчеты устойчивости склонов и откосов
• Мониторинг деформаций инженерных сооружений
• Консультации по геомеханике и стабилизации грунтов

🔹 Наши преимущества:
✅ Команда сертифицированных специалистов
✅ Современное оборудование и ПО
✅ Более 200 успешных проектов
✅ Гарантия качества и сроков

📞 Свяжитесь с нами для консультации - поможем решить ваши задачи!
    """

    await message.answer(about_text)


@router.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: Message):
    """Команда помощи"""
    await save_user_event(
        user_id=message.from_user.id,
        event_type='help_request',
        event_data={},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    help_text = """
❓ Помощь по использованию бота TerraStabilis

🤖 Как работает бот:
1. Выберите услугу из главного меню
2. Уточните тип услуги в подменю
3. Получите расчет стоимости
4. Оставьте контакты для связи с менеджером

💡 Доступные услуги:
• Сбор исходных гео данных
• Расчеты устойчивости (2D/3D)
• Консультации геомеханика
• Мониторинг инженерных объектов

🛠️ Если возникли проблемы:
• Нажмите /start для перезапуска бота
• Используйте кнопку "⬅️ Назад" для возврата
• Для срочной помощи: +7 (XXX) XXX-XX-XX

Мы всегда готовы помочь вам!
    """

    await message.answer(help_text)


@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()

    await save_user_event(
        user_id=message.from_user.id,
        event_type='navigation',
        event_data={'page': 'main_menu'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await message.answer(
        "📋 Главное меню - выберите услугу:",
        reply_markup=get_main_menu_keyboard()
    )

@router.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()

    await save_user_event(
        user_id=message.from_user.id,
        event_type='navigation',
        event_data={'page': 'main_menu'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await message.answer(
        "📋 Главное меню - выберите услугу:",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "⬅️ Назад в меню")
async def back_to_main_from_calculation(message: Message, state: FSMContext):
    """Возврат в главное меню из расчета"""
    await state.clear()

    await save_user_event(
        user_id=message.from_user.id,
        event_type='navigation',
        event_data={'page': 'main_menu', 'from': 'calculation'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await message.answer(
        "📋 Главное меню - выберите услугу:",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "🏢 О компании")
async def about_company(message: Message):
    """Информация о компании"""
    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='about_view',
        event_data={}
    )

    about_text = """
🏢 О компании

GeoEngineering Services - ведущий поставщик геоинженерных решений.

Наши услуги:
• Сбор исходных геологических данных
• Расчеты устойчивости сооружений  
• Консультации геомеханика
• Мониторинг инженерных объектов

💼 Наши клиенты: строительные компании, проектные организации, промышленные предприятия.

📞 Для связи выберите услугу и оставьте контакты - мы перезвоним вам!
    """

    await message.answer(about_text)


@router.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: Message):
    """Команда помощи"""
    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='help_request',
        event_data={}
    )

    help_text = """
❓ Помощь

Как пользоваться ботом:
1. Выберите интересующую услугу из меню
2. Уточните тип услуги в подменю
3. Получите примерный расчет стоимости
4. Оставьте контакты для связи

Команды:
/start - Главное меню
/help - Эта справка

Если у вас возникли проблемы, просто начните с /start
    """

    await message.answer(help_text)
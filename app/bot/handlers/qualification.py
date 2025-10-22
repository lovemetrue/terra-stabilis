from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.keyboards.main_menu import (
    get_main_menu_keyboard, get_geodata_keyboard, get_stability_keyboard,
    get_2d_keyboard, get_3d_keyboard, get_monitoring_keyboard, get_contact_keyboard
)
from app.bot.states import ServiceSelection, Calculation
from apps.bot_data.bot_utils import save_user_event, save_calculation, save_lead

router = Router()

# Цены для услуг
SERVICE_PRICES = {
    "program_development": 25000,
    "mapping": 18000,
    "core_documentation": 22000,
    "2d_ogr": 35000,
    "2d_pgr": 45000,
    "3d_ogr": 55000,
    "3d_pgr": 65000,
    "geomechanic": 20000,
    "georadar": 30000,
    "prism": 28000,
}


@router.message(F.text == "📊 Сбор исходных гео данных")
async def service_geodata(message: Message, state: FSMContext):
    """Услуга 1: Сбор исходных гео данных"""
    await state.set_state(ServiceSelection.waiting_for_subservice)
    await state.update_data(main_service="geodata_collection")

    await save_user_event(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'geodata_collection'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    service_text = """
📊 Сбор исходных гео данных

Выберите конкретную услугу:
    """

    await message.answer(
        service_text,
        reply_markup=get_geodata_keyboard()
    )


@router.message(F.text == "📐 Расчеты устойчивости")
async def service_stability(message: Message, state: FSMContext):
    """Услуга 2: Расчеты устойчивости"""
    await state.set_state(ServiceSelection.waiting_for_subservice)
    await state.update_data(main_service="stability_calculation")

    await save_user_event(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'stability_calculation'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    service_text = """
📐 Расчеты устойчивости

Выберите тип расчета:
    """

    await message.answer(
        service_text,
        reply_markup=get_stability_keyboard()
    )


@router.message(F.text == "👨‍💼 Консультации геомеханика")
async def service_geomechanic(message: Message, state: FSMContext):
    """Услуга 3: Консультации геомеханика"""
    await process_final_service(message, state, "geomechanic")


@router.message(F.text == "📡 Мониторинг инженерных объектов")
async def service_monitoring(message: Message, state: FSMContext):
    """Услуга 4: Мониторинг инженерных объектов"""
    await state.set_state(ServiceSelection.waiting_for_subservice)
    await state.update_data(main_service="monitoring")

    await save_user_event(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'monitoring'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    service_text = """
📡 Мониторинг инженерных объектов

Выберите тип мониторинга:
    """

    await message.answer(
        service_text,
        reply_markup=get_monitoring_keyboard()
    )


# Обработчики для подуслуг сбора геоданных
@router.message(F.text == "📝 Разработка программы")
async def service_program_development(message: Message, state: FSMContext):
    """Разработка программы геотехнических исследований"""
    await process_final_service(message, state, "program_development")


@router.message(F.text == "🗺️ Геотехническое картирование")
async def service_mapping(message: Message, state: FSMContext):
    """Геотехническое картирование"""
    await process_final_service(message, state, "mapping")


@router.message(F.text == "💎 Документирование керна")
async def service_core_documentation(message: Message, state: FSMContext):
    """Геотехническое документирование керна"""
    await process_final_service(message, state, "core_documentation")


# Обработчики для подуслуг расчетов устойчивости
@router.message(F.text == "2D расчеты")
async def service_2d_calculations(message: Message, state: FSMContext):
    """2D расчеты устойчивости"""
    await state.update_data(sub_service="2d_calculations")

    service_text = """
📐 2D расчеты устойчивости

Выберите тип грунта:
• ОГР - отвальные горные породы
• ПГР - природные горные породы
    """

    await message.answer(
        service_text,
        reply_markup=get_2d_keyboard()
    )


@router.message(F.text == "3D расчеты")
async def service_3d_calculations(message: Message, state: FSMContext):
    """3D расчеты устойчивости"""
    await state.update_data(sub_service="3d_calculations")

    service_text = """
📊 3D расчеты устойчивости

Выберите тип грунта:
• ОГР - отвальные горные породы  
• ПГР - природные горные породы
    """

    await message.answer(
        service_text,
        reply_markup=get_3d_keyboard()
    )


# Обработчики для конкретных типов расчетов
@router.message(F.text == "2D ОГР")
async def service_2d_ogr(message: Message, state: FSMContext):
    """2D расчет для ОГР"""
    await process_final_service(message, state, "2d_ogr")


@router.message(F.text == "2D ПГР")
async def service_2d_pgr(message: Message, state: FSMContext):
    """2D расчет для ПГР"""
    await process_final_service(message, state, "2d_pgr")


@router.message(F.text == "3D ОГР")
async def service_3d_ogr(message: Message, state: FSMContext):
    """3D расчет для ОГР"""
    await process_final_service(message, state, "3d_ogr")


@router.message(F.text == "3D ПГР")
async def service_3d_pgr(message: Message, state: FSMContext):
    """3D расчет для ПГР"""
    await process_final_service(message, state, "3d_pgr")


# Обработчики для подуслуг мониторинга
@router.message(F.text == "📡 Георадарный мониторинг")
async def service_georadar(message: Message, state: FSMContext):
    """Георадарный мониторинг"""
    await process_final_service(message, state, "georadar")


@router.message(F.text == "🔺 Призменный мониторинг")
async def service_prism(message: Message, state: FSMContext):
    """Призменный мониторинг"""
    await process_final_service(message, state, "prism")


# Обработчики для кнопок Назад в услугах
@router.message(ServiceSelection.waiting_for_subservice, F.text == "⬅️ Назад")
async def back_from_subservice(message: Message, state: FSMContext):
    """Возврат из подуслуг в главное меню"""
    await state.clear()

    await save_user_event(
        user_id=message.from_user.id,
        event_type='navigation',
        event_data={'page': 'main_menu', 'from': 'subservice'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await message.answer(
        "📋 Главное меню - выберите услугу:",
        reply_markup=get_main_menu_keyboard()
    )


async def process_final_service(message: Message, state: FSMContext, service_key: str):
    """Обработка конечного выбора услуги с расчетом цены"""
    price = SERVICE_PRICES.get(service_key, 0)

    if price == 0:
        await message.answer("❌ Услуга временно недоступна")
        return

    # Сохраняем данные о выборе
    user_data = await state.get_data()

    user_info = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    # Сохраняем расчет
    await save_calculation(
        user_id=message.from_user.id,
        service_type=service_key,
        parameters={},
        result=f"Рассчитана стоимость услуги: {price} руб.",
        price=price,
        **user_info
    )

    # Сохраняем лид (даже без контакта)
    await save_lead(
        user_id=message.from_user.id,
        service_type=service_key,
        calculated_price=price,
        **user_info
    )

    await save_user_event(
        user_id=message.from_user.id,
        event_type='final_service_select',
        event_data={
            'main_service': user_data.get('main_service'),
            'sub_service': user_data.get('sub_service'),
            'final_service': service_key,
            'calculated_price': price
        },
        **user_info
    )

    # Формируем текст в зависимости от услуги
    service_descriptions = {
        "program_development": "📝 Разработка программы геотехнических исследований",
        "mapping": "🗺️ Геотехническое картирование",
        "core_documentation": "💎 Геотехническое документирование керна",
        "2d_ogr": "📐 2D расчет устойчивости (ОГР)",
        "2d_pgr": "📐 2D расчет устойчивости (ПГР)",
        "3d_ogr": "📊 3D расчет устойчивости (ОГР)",
        "3d_pgr": "📊 3D расчет устойчивости (ПГР)",
        "geomechanic": "👨‍💼 Геомеханик на час",
        "georadar": "📡 Георадарный мониторинг",
        "prism": "🔺 Призменный мониторинг"
    }

    service_name = service_descriptions.get(service_key, "Услуга")

    service_text = f"""
{service_name}

Примерная стоимость: {price:,} руб.

Хотите оставить контакты для подробной консультации и точного расчета?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


@router.message(F.text == "✅ Оставить контакты")
async def request_contacts(message: Message, state: FSMContext):
    """Запрос контактов после расчета"""
    await save_user_event(
        user_id=message.from_user.id,
        event_type='contacts_request',
        event_data={},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    from app.bot.states import ContactCollection
    await state.set_state(ContactCollection.waiting_for_name)

    contacts_text = """
📞 Сбор контактов

Для связи с нашими специалистами и подготовки коммерческого предложения нам потребуется ваша контактная информация.

Пожалуйста, введите ваше имя:
    """

    from app.bot.keyboards.main_menu import get_skip_keyboard
    await message.answer(
        contacts_text,
        reply_markup=get_skip_keyboard()
    )
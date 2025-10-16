from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from app.bot.keyboards.main_menu import (
    get_main_menu_keyboard, get_geodata_keyboard, get_stability_keyboard,
    get_2d_keyboard, get_3d_keyboard, get_monitoring_keyboard, get_contact_keyboard
)
from app.bot.states import ServiceSelection, Calculation
from apps.bot_data.models import BotUserEvent, BotCalculation

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

    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'geodata_collection'}
    )

    service_text = """
📊 Сбор исходных гео данных

Выберите конкретную услугу:
    """

    await message.answer(
        service_text,
        reply_markup=get_geodata_keyboard()
    )


@router.message(F.text == "🏗️ Расчёт устойчивости")
async def service_stability(message: Message, state: FSMContext):
    """Услуга 2: Расчет устойчивости"""
    await state.set_state(ServiceSelection.waiting_for_subservice)
    await state.update_data(main_service="stability_calculation")

    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'stability_calculation'}
    )

    service_text = """
🏗️ Расчёт устойчивости

Выберите тип расчета:
    """

    await message.answer(
        service_text,
        reply_markup=get_stability_keyboard()
    )


@router.message(F.text == "👨‍💼 Геомеханик на час")
async def service_geomechanic(message: Message, state: FSMContext):
    """Услуга 3: Геомеханик на час"""
    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'geomechanic_per_hour'}
    )

    price = SERVICE_PRICES["geomechanic"]
    service_text = f"""
👨‍💼 Геомеханик на час

Условия:
• Минимальный пакет: 4 часа
• Срок заключения: 1 месяц
• Цена за пакет: {price:,} руб.

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        main_service="geomechanic_per_hour",
        final_service="geomechanic",
        calculated_price=price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


@router.message(F.text == "📡 Мониторинг")
async def service_monitoring(message: Message, state: FSMContext):
    """Услуга 4: Мониторинг"""
    await state.set_state(ServiceSelection.waiting_for_subservice)
    await state.update_data(main_service="monitoring")

    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'monitoring'}
    )

    service_text = """
📡 Мониторинг

Выберите тип мониторинга:
    """

    await message.answer(
        service_text,
        reply_markup=get_monitoring_keyboard()
    )


# Обработчики подуслуг для геоданных
@router.message(F.text == "📝 Разработка программы геотех. исследований")
async def subservice_program_development(message: Message, state: FSMContext):
    """Обработка выбора разработки программы"""
    await process_final_service(message, state, "program_development")


@router.message(F.text == "🗺️ Геотехническое картирование")
async def subservice_mapping(message: Message, state: FSMContext):
    """Обработка выбора картирования"""
    await process_final_service(message, state, "mapping")


@router.message(F.text == "💎 Геотехническое документирование керна")
async def subservice_core_documentation(message: Message, state: FSMContext):
    """Обработка выбора документирования керна"""
    await process_final_service(message, state, "core_documentation")


# Обработчики для устойчивости
@router.message(F.text == "📐 2D расчет устойчивости")
async def subservice_2d(message: Message, state: FSMContext):
    """2D расчет устойчивости"""
    await state.set_state(ServiceSelection.waiting_for_final_service)
    await state.update_data(sub_service="2d")

    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='subservice_select',
        event_data={'service': '2d_calculation'}
    )

    service_text = """
📐 2D расчет устойчивости

Выберите метод расчета:
    """

    await message.answer(
        service_text,
        reply_markup=get_2d_keyboard()
    )


@router.message(F.text == "📊 3D расчет устойчивости")
async def subservice_3d(message: Message, state: FSMContext):
    """3D расчет устойчивости"""
    await state.set_state(ServiceSelection.waiting_for_final_service)
    await state.update_data(sub_service="3d")

    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='subservice_select',
        event_data={'service': '3d_calculation'}
    )

    service_text = """
📊 3D расчет устойчивости

Выберите метод расчета:
    """

    await message.answer(
        service_text,
        reply_markup=get_3d_keyboard()
    )


# Обработчики методов расчета
@router.message(F.text == "2D → ОГР")
async def final_2d_ogr(message: Message, state: FSMContext):
    """2D ОГР расчет"""
    await process_final_service(message, state, "2d_ogr")


@router.message(F.text == "2D → ПГР")
async def final_2d_pgr(message: Message, state: FSMContext):
    """2D ПГР расчет"""
    await process_final_service(message, state, "2d_pgr")


@router.message(F.text == "3D → ОГР")
async def final_3d_ogr(message: Message, state: FSMContext):
    """3D ОГР расчет"""
    await process_final_service(message, state, "3d_ogr")


@router.message(F.text == "3D → ПГР")
async def final_3d_pgr(message: Message, state: FSMContext):
    """3D ПГР расчет"""
    await process_final_service(message, state, "3d_pgr")


# Обработчики для мониторинга
@router.message(F.text == "📡 Георадарный мониторинг")
async def subservice_georadar(message: Message, state: FSMContext):
    """Георадарный мониторинг"""
    await process_final_service(message, state, "georadar")


@router.message(F.text == "🔺 Призменный мониторинг")
async def subservice_prism(message: Message, state: FSMContext):
    """Призменный мониторинг"""
    await process_final_service(message, state, "prism")


async def process_final_service(message: Message, state: FSMContext, service_key: str):
    """Обработка конечного выбора услуги с расчетом цены"""
    price = SERVICE_PRICES.get(service_key, 0)

    if price == 0:
        await message.answer("❌ Услуга временно недоступна")
        return

    # Сохраняем данные о выборе
    user_data = await state.get_data()
    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='final_service_select',
        event_data={
            'main_service': user_data.get('main_service'),
            'sub_service': user_data.get('sub_service'),
            'final_service': service_key,
            'calculated_price': price
        }
    )

    # Создаем запись расчета
    await sync_to_async(BotCalculation.objects.create)(
        user_id=message.from_user.id,
        service_type=service_key,
        parameters={},
        result=f"Рассчитана стоимость услуги: {price} руб.",
        price=price
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
    await sync_to_async(BotUserEvent.objects.create)(
        user_id=message.from_user.id,
        event_type='contacts_request',
        event_data={}
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
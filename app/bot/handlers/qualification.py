from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import re

from app.bot.keyboards.main_menu import (
    get_main_menu_keyboard, get_geodata_keyboard, get_stability_keyboard,
    get_monitoring_keyboard, get_hydrogeology_keyboard, get_geomechanic_keyboard,
    get_contact_keyboard, get_yes_no_keyboard, get_back_keyboard
)
from app.bot.states import ContactCollection, ServiceSelection, Calculation
from apps.bot_data.bot_utils import save_user_event, save_calculation, save_lead

router = Router()

# Базовая стоимость услуг
SERVICE_BASE_PRICES = {
    # Сбор исходных данных
    "program_development": 300000,
    "core_documentation": 200000,

    # Расчеты устойчивости
    "2d_ogr": 60000,
    "2d_pgr": 80000,
    "3d_ogr": 150000,
    "3d_pgr": 180000,

    # Геомеханик на час
    "senior_geomechanic": 6000,
    "chief_geomechanic": 12000,

    # Мониторинг
    "prism_monitoring": 150000,
    "georadar_interpretation": 400000,
    "tarps_setup": 500000,
    "tarps_development": 650000,

    # Гидрогеология
    "hydro_survey": 120000,
    "well_interpretation": 100000,
    "filtration_modeling": 250000,
    "drainage_calculation": 200000,
    "hydro_monitoring": 150000,
    "water_impact_assessment": 180000,
}


# Обработчики для сбора исходных данных
@router.message(F.text == "📝 Разработка программы геотехнических исследований")
async def service_program_development(message: Message, state: FSMContext):
    """Разработка программы геотехнических исследований - сначала вопросы"""
    await state.set_state(ServiceSelection.waiting_for_geotech_wells)
    await state.update_data(
        service_key="program_development",
        main_service="geodata_collection"
    )

    question_text = """
📝 <b>Разработка программы геотехнических исследований</b>

Подготовка программы, ТЗ и перечня полевых и лабораторных работ.

Для точного расчета ответьте на вопросы:

<b>Какие исходные данные есть?</b>
1. База данных по геотехническим скважинам? (да/нет)
2. База данных по геологическим скважинам? (да/нет)  
3. Есть ли база данных по ФМС? (да/нет)

<b>Ответьте на первый вопрос:</b>
Есть ли база данных по геотехническим скважинам?
    """

    await message.answer(
        question_text,
        reply_markup=get_yes_no_keyboard(),
        parse_mode='HTML'
    )


# Обработчики для расчетов устойчивости
@router.message(F.text.in_(["2D ОГР", "2D ПГР", "3D ОГР", "3D ПГР"]))
async def service_stability_calculation(message: Message, state: FSMContext):
    """Обработка выбора расчета устойчивости - сначала количество"""
    service_map = {
        "2D ОГР": "2d_ogr",
        "2D ПГР": "2d_pgr",
        "3D ОГР": "3d_ogr",
        "3D ПГР": "3d_pgr"
    }

    service_key = service_map[message.text]
    await state.set_state(ServiceSelection.waiting_for_calculations_count)
    await state.update_data(
        service_key=service_key,
        main_service="stability_calculation"
    )

    descriptions = {
        "2d_ogr": "2D расчет устойчивости откосов и уступов для <b>открытых горных работ</b> (Slide, RS2)",
        "2d_pgr": "2D анализ устойчивости подземных камер, штреков и целиков для <b>подземных горных работ</b>",
        "3d_ogr": "3D моделирование устойчивости откосов и уступов для <b>открытых горных работ</b> (RS3)",
        "3d_pgr": "3D-анализ напряженно-деформированного состояния массива для <b>подземных горных работ</b>"
    }

    question_text = f"""
{message.text}

{descriptions[service_key]}

<b>Для расчета стоимости введите количество расчетов:</b>
• От 5 расчетов - скидка 10%
• От 10 расчетов - скидка 20%
    """

    await message.answer(
        question_text,
        reply_markup=get_back_keyboard(),
        parse_mode='HTML'
    )


# Обработчики для геомеханика на час
@router.message(F.text.in_(["👨‍💼 Ведущий геомеханик", "👨‍🔬 Главный геомеханик"]))
async def service_geomechanic_level(message: Message, state: FSMContext):
    """Обработка выбора уровня геомеханика - сначала количество часов"""
    service_map = {
        "👨‍💼 Ведущий геомеханик": "senior_geomechanic",
        "👨‍🔬 Главный геомеханик": "chief_geomechanic"
    }

    service_key = service_map[message.text]
    await state.set_state(ServiceSelection.waiting_for_hours_count)
    await state.update_data(
        service_key=service_key,
        main_service="geomechanic_hourly"
    )

    specialist_level = "Ведущий геомеханик" if service_key == "senior_geomechanic" else "Главный геомеханик"

    question_text = f"""
👨‍💼 <b>{specialist_level}</b>

Онлайн-консультация, аудит расчетов или сопровождение проекта
Минимальный пакет — 4 часа в месяц

<b>Введите количество часов:</b>
• При запросе от 10 часов - скидка 10%
    """

    await message.answer(
        question_text,
        reply_markup=get_back_keyboard(),
        parse_mode='HTML'
    )


# Обработчики для мониторинга с указанием "от ..."
@router.message(F.text == "🔺 Призменный мониторинг")
async def service_prism_monitoring(message: Message, state: FSMContext):
    """Призменный мониторинг"""
    await process_direct_service(message, state, "prism_monitoring",
                                 "Анализ данных тахеометрических наблюдений за смещениями призм",
                                 "от 150,000 ₽")


@router.message(F.text == "📡 Интерпретация данных радарного мониторинга")
async def service_georadar_interpretation(message: Message, state: FSMContext):
    """Интерпретация данных радарного мониторинга"""
    await process_direct_service(message, state, "georadar_interpretation",
                                 "Обработка и анализ данных радарных систем (IDS/GroundProbe)",
                                 "от 400,000 ₽")


@router.message(F.text == "⚙️ Настройка пороговых значений по TARP")
async def service_tarps_setup(message: Message, state: FSMContext):
    """Настройка пороговых значений по TARP"""
    await process_direct_service(message, state, "tarps_setup",
                                 "Определение уровней тревоги, калибровка скоростей смещений",
                                 "от 500,000 ₽")


@router.message(F.text == "📋 Разработка документа TARP")
async def service_tarps_development(message: Message, state: FSMContext):
    """Разработка документа TARP"""
    await process_direct_service(message, state, "tarps_development",
                                 "Подготовка полного плана действий при достижении пороговых значений",
                                 "от 650,000 ₽")


# Обработчики для гидрогеологии с указанием "от ..."
@router.message(F.text == "🌊 Гидрогеологическое обследование участка")
async def service_hydro_survey(message: Message, state: FSMContext):
    """Гидрогеологическое обследование участка"""
    await process_direct_service(message, state, "hydro_survey",
                                 "Сбор исходных данных, визуальный осмотр, описание водопроявлений",
                                 "от 120,000 ₽")


@router.message(F.text == "📊 Интерпретация данных наблюдательных скважин")
async def service_well_interpretation(message: Message, state: FSMContext):
    """Интерпретация данных наблюдательных скважин"""
    await process_direct_service(message, state, "well_interpretation",
                                 "Обработка данных по уровням и дебитам, построение графиков",
                                 "от 100,000 ₽")


@router.message(F.text == "💻 Моделирование фильтрационного потока")
async def service_filtration_modeling(message: Message, state: FSMContext):
    """Моделирование фильтрационного потока"""
    await process_direct_service(message, state, "filtration_modeling",
                                 "Построение численной модели подземных вод (MODFLOW, FEFLOW)",
                                 "от 250,000 ₽")


@router.message(F.text == "🔧 Расчет депрессии и проект дренажной системы")
async def service_drainage_calculation(message: Message, state: FSMContext):
    """Расчет депрессии и проект дренажной системы"""
    await process_direct_service(message, state, "drainage_calculation",
                                 "Определение расположения водопонизительных скважин",
                                 "от 200,000 ₽")


@router.message(F.text == "📈 Гидрогеологический мониторинг")
async def service_hydro_monitoring(message: Message, state: FSMContext):
    """Гидрогеологический мониторинг"""
    await process_direct_service(message, state, "hydro_monitoring",
                                 "Построение сети наблюдений, контроль уровней подземных вод",
                                 "от 150,000 ₽")


@router.message(F.text == "⚖️ Оценка влияния подземных вод на устойчивость")
async def service_water_impact_assessment(message: Message, state: FSMContext):
    """Оценка влияния подземных вод на устойчивость"""
    await process_direct_service(message, state, "water_impact_assessment",
                                 "Комплексный анализ взаимодействия фильтрации и механической устойчивости",
                                 "от 180,000 ₽")


async def process_direct_service(message: Message, state: FSMContext, service_key: str, description: str, price_text: str):
    """Обработка услуг с прямой стоимостью (показываем 'от ...')"""
    price = SERVICE_BASE_PRICES.get(service_key, 0)

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
        parameters={'description': description},
        result=f"Стоимость: {price_text}",
        price=price,
        **user_info
    )

    # Сохраняем лид
    await save_lead(
        user_id=message.from_user.id,
        service_type=service_key,
        calculated_price=price,
        **user_info
    )

    await save_user_event(
        user_id=message.from_user.id,
        event_type='service_inquiry',
        event_data={
            'main_service': user_data.get('main_service'),
            'final_service': service_key,
            'price_indication': price_text
        },
        **user_info
    )

    service_names = {
        "prism_monitoring": "🔺 Призменный мониторинг",
        "georadar_interpretation": "📡 Интерпретация данных радарного мониторинга",
        "tarps_setup": "⚙️ Настройка пороговых значений по TARP",
        "tarps_development": "📋 Разработка документа TARP",
        "hydro_survey": "🌊 Гидрогеологическое обследование участка",
        "well_interpretation": "📊 Интерпретация данных наблюдательных скважин",
        "filtration_modeling": "💻 Моделирование фильтрационного потока",
        "drainage_calculation": "🔧 Расчет депрессии и проект дренажной системы",
        "hydro_monitoring": "📈 Гидрогеологический мониторинг",
        "water_impact_assessment": "⚖️ Оценка влияния подземных вод на устойчивость"
    }

    service_text = f"""
{service_names.get(service_key, "Услуга")}

{description}

<b>Стоимость:</b> {price_text}

Хотите оставить контакты для подробной консультации и точного расчета?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard(),
        parse_mode='HTML'
    )


# Хендлер для обработки количества расчетов устойчивости
@router.message(ServiceSelection.waiting_for_calculations_count, F.text)
async def process_calculations_count(message: Message, state: FSMContext):
    """Обработка ввода количества расчетов устойчивости - потом стоимость"""
    if message.text == "⬅️ Назад":
        await state.set_state(ServiceSelection.waiting_for_subservice)
        await message.answer(
            "Выберите тип расчета:",
            reply_markup=get_stability_keyboard()
        )
        return

    # Проверяем, что введено число
    if not message.text.isdigit():
        await message.answer(
            "❌ Пожалуйста, введите количество расчетов:",
            reply_markup=get_back_keyboard()
        )
        return

    calculations_count = int(message.text)

    if calculations_count <= 0:
        await message.answer(
            "❌ Количество расчетов должно быть больше 0:",
            reply_markup=get_back_keyboard()
        )
        return

    user_data = await state.get_data()
    service_key = user_data.get('service_key')

    if not service_key:
        await message.answer("❌ Ошибка сервиса. Начните заново.")
        await state.clear()
        return

    base_price = SERVICE_BASE_PRICES.get(service_key, 0)

    if base_price == 0:
        await message.answer("❌ Услуга временно недоступна")
        return

    # Применяем скидки
    discount = 0
    if calculations_count >= 10:
        discount = 20
    elif calculations_count >= 5:
        discount = 10

    total_price = base_price * calculations_count
    final_price = total_price * (100 - discount) / 100

    user_info = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    # Сохраняем расчет
    await save_calculation(
        user_id=message.from_user.id,
        service_type=service_key,
        parameters={'calculations_count': calculations_count},
        result=f"Рассчитана стоимость: {final_price:,.0f} ₽ ({calculations_count} расчетов, скидка {discount}%)",
        price=final_price,
        **user_info
    )

    # Сохраняем лид
    await save_lead(
        user_id=message.from_user.id,
        service_type=service_key,
        calculated_price=final_price,
        **user_info
    )

    await save_user_event(
        user_id=message.from_user.id,
        event_type='final_service_select',
        event_data={
            'main_service': user_data.get('main_service'),
            'final_service': service_key,
            'calculations_count': calculations_count,
            'discount': discount,
            'calculated_price': final_price
        },
        **user_info
    )

    service_names = {
        "2d_ogr": "2D ОГР (открытые горные работы)",
        "2d_pgr": "2D ПГР (подземные горные работы)",
        "3d_ogr": "3D ОГР (открытые горные работы)",
        "3d_pgr": "3D ПГР (подземные горные работы)"
    }

    service_text = f"""
{service_names.get(service_key, "Расчет устойчивости")}

<b>Количество расчетов:</b> {calculations_count}
<b>Скидка:</b> {discount}%

<b>Предварительная стоимость:</b> {final_price:,.0f} ₽

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard(),
        parse_mode='HTML'
    )


# Хендлер для обработки количества часов геомеханика
@router.message(ServiceSelection.waiting_for_hours_count, F.text)
async def process_hours_count(message: Message, state: FSMContext):
    """Обработка ввода количества часов для геомеханика - потом стоимость"""
    if message.text == "⬅️ Назад":
        await state.set_state(ServiceSelection.waiting_for_subservice)
        await message.answer(
            "Выберите уровень специалиста:",
            reply_markup=get_geomechanic_keyboard()
        )
        return

    # Проверяем, что введено число
    if not re.match(r'^\d+$', message.text):
        await message.answer(
            "❌ Пожалуйста, введите количество часов (целое число):",
            reply_markup=get_back_keyboard()
        )
        return

    hours_count = int(message.text)

    # Минимальный пакет - 4 часа
    if hours_count < 4:
        await message.answer(
            "❌ Минимальный пакет - 4 часа. Введите количество часов:",
            reply_markup=get_back_keyboard()
        )
        return

    user_data = await state.get_data()
    service_key = user_data.get('service_key')

    if not service_key:
        await message.answer("❌ Ошибка сервиса. Начните заново.")
        await state.clear()
        return

    base_hourly_rate = SERVICE_BASE_PRICES.get(service_key, 0)

    if base_hourly_rate == 0:
        await message.answer("❌ Услуга временно недоступна")
        return

    # Применяем скидку при большом количестве часов
    discount = 10 if hours_count >= 10 else 0

    total_price = base_hourly_rate * hours_count
    final_price = total_price * (100 - discount) / 100

    user_info = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    # Сохраняем расчет
    await save_calculation(
        user_id=message.from_user.id,
        service_type=service_key,
        parameters={'hours_count': hours_count},
        result=f"Рассчитана стоимость: {final_price:,.0f} ₽ ({hours_count} часов, ставка {base_hourly_rate:,.0f} ₽/час, скидка {discount}%)",
        price=final_price,
        **user_info
    )

    # Сохраняем лид
    await save_lead(
        user_id=message.from_user.id,
        service_type=service_key,
        calculated_price=final_price,
        **user_info
    )

    await save_user_event(
        user_id=message.from_user.id,
        event_type='final_service_select',
        event_data={
            'main_service': user_data.get('main_service'),
            'final_service': service_key,
            'hours_count': hours_count,
            'discount': discount,
            'calculated_price': final_price
        },
        **user_info
    )

    specialist_level = "Ведущий геомеханик" if service_key == "senior_geomechanic" else "Главный геомеханик"

    service_text = f"""
👨‍💼 <b>{specialist_level}</b>

<b>Количество часов:</b> {hours_count}
<b>Ставка:</b> {base_hourly_rate:,.0f} ₽/час
<b>Скидка:</b> {discount}%

<b>Предварительная стоимость:</b> {final_price:,.0f} ₽

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard(),
        parse_mode='HTML'
    )
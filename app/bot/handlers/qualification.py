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
    "georadar_interpretation": 400000,  # Изменено на 400 000
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


@router.message(F.text == "🚀 Рассчитать стоимость")
async def start_calculation(message: Message, state: FSMContext):
    """Начало расчета стоимости - показ главного меню услуг"""
    await save_user_event(
        user_id=message.from_user.id,
        event_type='calculation_started',
        event_data={},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await message.answer(
        "📋 Выберите категорию услуги:",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "📊 Сбор исходных данных")
async def service_geodata(message: Message, state: FSMContext):
    """Услуга: Сбор исходных данных"""
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
📊 Сбор исходных данных

Выберите конкретную услугу:
    """

    await message.answer(
        service_text,
        reply_markup=get_geodata_keyboard()
    )


@router.message(F.text == "📐 Расчёт устойчивости")
async def service_stability(message: Message, state: FSMContext):
    """Услуга: Расчет устойчивости"""
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
📐 Расчет устойчивости

Выберите тип расчета:
    """

    await message.answer(
        service_text,
        reply_markup=get_stability_keyboard()
    )


@router.message(F.text == "👨‍💼 Геомеханик на час")
async def service_geomechanic(message: Message, state: FSMContext):
    """Услуга: Геомеханик на час"""
    await state.set_state(ServiceSelection.waiting_for_subservice)
    await state.update_data(main_service="geomechanic_hourly")

    await save_user_event(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'geomechanic_hourly'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    service_text = """
👨‍💼 Геомеханик на час

Консультационные услуги:
• Онлайн-консультация
• Аудит расчетов  
• Сопровождение проекта

Минимальный пакет — 4 часа в месяц
Выберите уровень специалиста:
    """

    await message.answer(
        service_text,
        reply_markup=get_geomechanic_keyboard()
    )


@router.message(F.text == "📡 Мониторинг")
async def service_monitoring(message: Message, state: FSMContext):
    """Услуга: Мониторинг"""
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
📡 Мониторинг

Выберите тип мониторинга:
    """

    await message.answer(
        service_text,
        reply_markup=get_monitoring_keyboard()
    )


@router.message(F.text == "💧 Гидрогеология")
async def service_hydrogeology(message: Message, state: FSMContext):
    """Услуга: Гидрогеология"""
    await state.set_state(ServiceSelection.waiting_for_subservice)
    await state.update_data(main_service="hydrogeology")

    await save_user_event(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'hydrogeology'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    service_text = """
💧 Гидрогеология

Комплексные решения по управлению подземными водами:
    """

    await message.answer(
        service_text,
        reply_markup=get_hydrogeology_keyboard()
    )


# Обработчики для сбора исходных данных
@router.message(F.text == "📝 Разработка программы геотехнических исследований")
async def service_program_development(message: Message, state: FSMContext):
    """Разработка программы геотехнических исследований"""
    await state.set_state(ServiceSelection.waiting_for_geotech_wells)
    await state.update_data(
        service_key="program_development",
        main_service="geodata_collection"
    )

    await save_user_event(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'program_development'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    question_text = """
📝 Разработка программы геотехнических исследований

Подготовка программы, ТЗ и перечня полевых и лабораторных работ.

Для точного расчета ответьте на вопросы:

Какие исходные данные есть?
1. База данных по геотехническим скважинам? (да/нет)
2. База данных по геологическим скважинам? (да/нет)  
3. Есть ли база данных по ФМС? (да/нет)

Ответьте на первый вопрос:
Есть ли база данных по геотехническим скважинам?
    """

    await message.answer(
        question_text,
        reply_markup=get_yes_no_keyboard()
    )


@router.message(F.text == "💎 Геотехническое документирование керна")
async def service_core_documentation(message: Message, state: FSMContext):
    """Геотехническое документирование керна"""
    await state.set_state(ServiceSelection.waiting_for_drilling_rigs)
    await state.update_data(
        service_key="core_documentation",
        main_service="geodata_collection"
    )

    await save_user_event(
        user_id=message.from_user.id,
        event_type='service_select',
        event_data={'service': 'core_documentation'},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    question_text = """
💎 Геотехническое документирование керна

Описание керна, расчет RQD, выделение зон нарушенности, формирование отчетов.

Для расчета стоимости введите количество буровых станков:
    """

    await message.answer(
        question_text,
        reply_markup=get_back_keyboard()
    )


# Хендлер для обработки ДА/НЕТ для геотехнических скважин
@router.message(ServiceSelection.waiting_for_geotech_wells, F.text.in_(["✅ Да", "❌ Нет"]))
async def process_geotech_wells_answer(message: Message, state: FSMContext):
    """Обработка ответа о наличии базы геотехнических скважин"""
    answer = message.text == "✅ Да"

    await state.update_data(geotech_wells=answer)
    await state.set_state(ServiceSelection.waiting_for_geo_wells)

    next_question = """
Отлично! Следующий вопрос:

Есть ли база данных по геологическим скважинам?
    """

    await message.answer(
        next_question,
        reply_markup=get_yes_no_keyboard()
    )


# Хендлер для обработки ДА/НЕТ для геологических скважин
@router.message(ServiceSelection.waiting_for_geo_wells, F.text.in_(["✅ Да", "❌ Нет"]))
async def process_geo_wells_answer(message: Message, state: FSMContext):
    """Обработка ответа о наличии базы геологических скважин"""
    answer = message.text == "✅ Да"

    await state.update_data(geo_wells=answer)
    await state.set_state(ServiceSelection.waiting_for_fms_data)

    next_question = """
Отлично! Последний вопрос:

Есть ли база данных по ФМС?
    """

    await message.answer(
        next_question,
        reply_markup=get_yes_no_keyboard()
    )


# Хендлер для обработки ДА/НЕТ для ФМС и финального расчета
@router.message(ServiceSelection.waiting_for_fms_data, F.text.in_(["✅ Да", "❌ Нет"]))
async def process_fms_answer_and_calculate(message: Message, state: FSMContext):
    """Обработка ответа о наличии ФМС и расчет стоимости"""
    answer = message.text == "✅ Да"

    user_data = await state.get_data()
    service_key = user_data.get('service_key', 'program_development')

    # Базовая цена
    base_price = SERVICE_BASE_PRICES.get(service_key, 300000)

    # Логика расчета на основе ответов
    final_price = base_price

    # Если есть все данные - скидка
    if (user_data.get('geotech_wells') and
        user_data.get('geo_wells') and
        answer):
        final_price = int(base_price * 0.9)  # 10% скидка за полный комплект данных
    # Если есть 2 из 3 данных - небольшая скидка
    elif ((user_data.get('geotech_wells') and user_data.get('geo_wells')) or
          (user_data.get('geotech_wells') and answer) or
          (user_data.get('geo_wells') and answer)):
        final_price = int(base_price * 0.95)  # 5% скидка

    user_info = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    # Сохраняем расчет
    await save_calculation(
        user_id=message.from_user.id,
        service_type=service_key,
        parameters={
            'geotech_wells': user_data.get('geotech_wells'),
            'geo_wells': user_data.get('geo_wells'),
            'fms_data': answer
        },
        result=f"Рассчитана стоимость услуги: {final_price:,} ₽",
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
            'calculated_price': final_price,
            'answers': {
                'geotech_wells': user_data.get('geotech_wells'),
                'geo_wells': user_data.get('geo_wells'),
                'fms_data': answer
            }
        },
        **user_info
    )

    # Формируем текст с ответами
    answers_text = "Ваши ответы:\n"
    answers_text += f"• Геотехнические скважины: {'✅ Да' if user_data.get('geotech_wells') else '❌ Нет'}\n"
    answers_text += f"• Геологические скважины: {'✅ Да' if user_data.get('geo_wells') else '❌ Нет'}\n"
    answers_text += f"• Данные ФМС: {'✅ Да' if answer else '❌ Нет'}"

    service_text = f"""
📝 Разработка программы геотехнических исследований

{answers_text}

Предварительная стоимость: от {final_price:,} ₽

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


# Хендлер для обработки количества буровых станков
@router.message(ServiceSelection.waiting_for_drilling_rigs, F.text)
async def process_drilling_rigs_count(message: Message, state: FSMContext):
    """Обработка ввода количества буровых станков"""
    if message.text == "⬅️ Назад":
        await state.set_state(ServiceSelection.waiting_for_subservice)
        await message.answer(
            "Выберите услугу:",
            reply_markup=get_geodata_keyboard()
        )
        return

    # Проверяем, что введено число
    if not message.text.isdigit():
        await message.answer(
            "❌ Пожалуйста, введите число буровых станков:",
            reply_markup=get_back_keyboard()
        )
        return

    rigs_count = int(message.text)

    if rigs_count <= 0:
        await message.answer(
            "❌ Количество станков должно быть больше 0:",
            reply_markup=get_back_keyboard()
        )
        return

    user_data = await state.get_data()
    service_key = user_data.get('service_key', 'core_documentation')

    # Расчет стоимости: 3 документатора на станок, каждый по 300,000 руб/мес
    documentators_per_rig = 3
    cost_per_documentator = 300000
    total_documentators = rigs_count * documentators_per_rig
    final_price = total_documentators * cost_per_documentator

    user_info = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    # Сохраняем расчет
    await save_calculation(
        user_id=message.from_user.id,
        service_type=service_key,
        parameters={'rigs_count': rigs_count},
        result=f"Рассчитана стоимость: {final_price:,} ₽/мес ({rigs_count} станков × {documentators_per_rig} документаторов)",
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
            'rigs_count': rigs_count,
            'calculated_price': final_price
        },
        **user_info
    )

    service_text = f"""
💎 Геотехническое документирование керна

Количество станков: {rigs_count}
Необходимо документаторов: {total_documentators}

Предварительная стоимость: от  {final_price:,} ₽ в месяц

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


# Хендлер для кнопки Назад в различных состояниях ввода
@router.message(
    ServiceSelection.waiting_for_geotech_wells,
    ServiceSelection.waiting_for_geo_wells,
    ServiceSelection.waiting_for_fms_data,
    F.text == "⬅️ Назад"
)
async def back_from_questions(message: Message, state: FSMContext):
    """Возврат из вопросов к выбору услуги"""
    await state.set_state(ServiceSelection.waiting_for_subservice)

    user_data = await state.get_data()
    main_service = user_data.get('main_service', 'geodata_collection')

    if main_service == 'geodata_collection':
        await message.answer(
            "Выберите услугу:",
            reply_markup=get_geodata_keyboard()
        )
    else:
        await message.answer(
            "Выберите услугу:",
            reply_markup=get_main_menu_keyboard()
        )


# Обработчики некорректных ответов для вопросов ДА/НЕТ
@router.message(
    ServiceSelection.waiting_for_geotech_wells,
    ServiceSelection.waiting_for_geo_wells,
    ServiceSelection.waiting_for_fms_data
)
async def handle_invalid_yes_no_answer(message: Message):
    """Обработка некорректных ответов на вопросы ДА/НЕТ"""
    await message.answer(
        "❌ Пожалуйста, используйте кнопки для ответа:",
        reply_markup=get_yes_no_keyboard()
    )


# Обработчики для расчетов устойчивости
@router.message(F.text.in_(["2D ОГР", "2D ПГР", "3D ОГР", "3D ПГР"]))
async def service_stability_calculation(message: Message, state: FSMContext):
    """Обработка выбора расчета устойчивости"""
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

    # Расшифровка аббревиатур
    abbreviations = {
        "2d_ogr": " (ОГР – открытые горные работы)",
        "2d_pgr": " (ПГР – подземные горные работы)",
        "3d_ogr": " (ОГР – открытые горные работы)",
        "3d_pgr": " (ПГР – подземные горные работы)"
    }

    descriptions = {
        "2d_ogr": "2D расчет устойчивости откосов и уступов (Slide, RS2)",
        "2d_pgr": "2D анализ устойчивости подземных камер, штреков и целиков",
        "3d_ogr": "3D моделирование устойчивости откосов и уступов (RS3)",
        "3d_pgr": "3D-анализ напряженно-деформированного состояния массива"
    }

    question_text = f"""
{message.text}{abbreviations.get(service_key, "")}

{descriptions[service_key]}

Для расчета стоимости введите количество расчетов:
• От 5 расчетов - скидка 10%
• От 10 расчетов - скидка 20%
    """

    await message.answer(
        question_text,
        reply_markup=get_back_keyboard()
    )


# Обработчики для геомеханика на час
@router.message(F.text.in_(["👨‍💼 Ведущий геомеханик", "👨‍🔬 Главный геомеханик"]))
async def service_geomechanic_level(message: Message, state: FSMContext):
    """Обработка выбора уровня геомеханика"""
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

    question_text = f"""
{message.text}

Онлайн-консультация, аудит расчетов или сопровождение проекта
Минимальный пакет — 4 часа в месяц

• При запросе от 10 часов - скидка 10%

Введите количество часов:
    """

    await message.answer(
        question_text,
        reply_markup=get_back_keyboard()
    )


# Обработчики для мониторинга
@router.message(F.text == "🔺 Призменный мониторинг")
async def service_prism_monitoring(message: Message, state: FSMContext):
    """Призменный мониторинг"""
    await process_direct_service(message, state, "prism_monitoring",
                                 "Анализ данных тахеометрических наблюдений за смещениями призм")


@router.message(F.text == "📡 Интерпретация данных георадарного мониторинга")
async def service_georadar_interpretation(message: Message, state: FSMContext):
    """Интерпретация данных георадарного мониторинга"""
    await process_direct_service(message, state, "georadar_interpretation",
                                 "Обработка и анализ данных радарных систем (IDS/GroundProbe)")


@router.message(F.text == "⚙️ Настройка пороговых значений по TARP")
async def service_tarps_setup(message: Message, state: FSMContext):
    """Настройка пороговых значений по TARP"""
    await process_direct_service(message, state, "tarps_setup",
                                 "Определение уровней тревоги, калибровка скоростей смещений")


@router.message(F.text == "📋 Разработка документа TARP")
async def service_tarps_development(message: Message, state: FSMContext):
    """Разработка документа TARP"""
    await process_direct_service(message, state, "tarps_development",
                                 "Подготовка полного плана действий при достижении пороговых значений")


# Обработчики для гидрогеологии
@router.message(F.text == "🌊 Гидрогеологическое обследование участка")
async def service_hydro_survey(message: Message, state: FSMContext):
    """Гидрогеологическое обследование участка"""
    await process_direct_service(message, state, "hydro_survey",
                                 "Сбор исходных данных, визуальный осмотр, описание водопроявлений")


@router.message(F.text == "📊 Интерпретация данных наблюдательных скважин")
async def service_well_interpretation(message: Message, state: FSMContext):
    """Интерпретация данных наблюдательных скважин"""
    await process_direct_service(message, state, "well_interpretation",
                                 "Обработка данных по уровням и дебитам, построение графиков")


@router.message(F.text == "💻 Моделирование фильтрационного потока")
async def service_filtration_modeling(message: Message, state: FSMContext):
    """Моделирование фильтрационного потока"""
    await process_direct_service(message, state, "filtration_modeling",
                                 "Построение численной модели подземных вод (MODFLOW, FEFLOW)")


@router.message(F.text == "🔧 Расчет депрессии и проект дренажной системы")
async def service_drainage_calculation(message: Message, state: FSMContext):
    """Расчет депрессии и проект дренажной системы"""
    await process_direct_service(message, state, "drainage_calculation",
                                 "Определение расположения водопонизительных скважин")


@router.message(F.text == "📈 Гидрогеологический мониторинг")
async def service_hydro_monitoring(message: Message, state: FSMContext):
    """Гидрогеологический мониторинг"""
    await process_direct_service(message, state, "hydro_monitoring",
                                 "Построение сети наблюдений, контроль уровней подземных вод")


@router.message(F.text == "⚖️ Оценка влияния подземных вод на устойчивость")
async def service_water_impact_assessment(message: Message, state: FSMContext):
    """Оценка влияния подземных вод на устойчивость"""
    await process_direct_service(message, state, "water_impact_assessment",
                                 "Комплексный анализ взаимодействия фильтрации и механической устойчивости")


async def process_direct_service(message: Message, state: FSMContext, service_key: str, description: str):
    """Обработка услуг с прямой стоимостью"""
    price = SERVICE_BASE_PRICES.get(service_key, 0)

    if price == 0:
        await message.answer("❌ Услуга временно недоступна")
        return

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
        result=f"Предварительная стоимость от: {price:,} ₽",
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
        event_type='final_service_select',
        event_data={
            'main_service': user_data.get('main_service'),
            'final_service': service_key,
            'calculated_price': price
        },
        **user_info
    )

    service_names = {
        "prism_monitoring": "🔺 Призменный мониторинг",
        "georadar_interpretation": "📡 Интерпретация данных георадарного мониторинга",
        "tarps_setup": "⚙️ Настройка пороговых значений по TARP",
        "tarps_development": "📋 Разработка документа TARP",
        "hydro_survey": "🌊 Гидрогеологическое обследование участка",
        "well_interpretation": "📊 Интерпретация данных наблюдательных скважин",
        "filtration_modeling": "💻 Моделирование фильтрационного потока",
        "drainage_calculation": "🔧 Расчет депрессии и проект дренажной системы",
        "hydro_monitoring": "📈 Гидрогеологический мониторинг",
        "water_impact_assessment": "⚖️ Оценка влияния подземных вод на устойчивость"
    }

    # Для услуг гидрогеологии и TARP используем "Предварительная стоимость: от"
    service_text = f"""
{service_names.get(service_key, "Услуга")}

{description}

Предварительная стоимость: от {price:,} ₽

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


# Хендлер для обработки количества часов геомеханика
@router.message(ServiceSelection.waiting_for_hours_count, F.text)
async def process_hours_count(message: Message, state: FSMContext):
    """Обработка ввода количества часов для геомеханика"""
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
👨‍💼 {specialist_level}

Количество часов: {hours_count}
Ставка: {base_hourly_rate:,.0f} ₽/час
Скидка: {discount}%

Предварительная стоимость: от {final_price:,.0f} ₽

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


# Хендлер для обработки количества расчетов устойчивости
@router.message(ServiceSelection.waiting_for_calculations_count, F.text)
async def process_calculations_count(message: Message, state: FSMContext):
    """Обработка ввода количества расчетов устойчивости"""
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
        "2d_ogr": "2D ОГР (ОГР – открытые горные работы)",
        "2d_pgr": "2D ПГР (ПГР – подземные горные работы)",
        "3d_ogr": "3D ОГР (ОГР – открытые горные работы)",
        "3d_pgr": "3D ПГР (ПГР – подземные горные работы)"
    }

    service_text = f"""
{service_names.get(service_key, "Расчет устойчивости")}

Количество расчетов: {calculations_count}
Скидка: {discount}%

Предварительная стоимость: от {final_price:,.0f} ₽

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


# ... остальные функции (process_geotech_wells_answer, process_geo_wells_answer,
# process_fms_answer_and_calculate, process_drilling_rigs_count) остаются без изменений ...

@router.message(F.text == "✅ Оставить контакты")
async def request_contacts(message: Message, state: FSMContext):
    """Запрос контактов после расчета"""
    # Очищаем предыдущее состояние квалификации
    await state.clear()

    await save_user_event(
        user_id=message.from_user.id,
        event_type='contacts_request',
        event_data={},
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await state.set_state(ContactCollection.waiting_for_name)

    contacts_text = """
📞 Сбор контактов

Для связи с нашими специалистами и подготовки коммерческого предложения нам потребуется ваша контактная информация.

Пожалуйста, введите ваше имя:
    """

    await message.answer(
        contacts_text,
        reply_markup=get_back_keyboard()
    )

# ... остальные функции (back_from_questions, back_from_subservice) остаются без изменений ...
# Хендлер для обработки ДА/НЕТ для геологических скважин
@router.message(ServiceSelection.waiting_for_geo_wells, F.text.in_(["✅ Да", "❌ Нет"]))
async def process_geo_wells_answer(message: Message, state: FSMContext):
    """Обработка ответа о наличии базы геологических скважин"""
    answer = message.text == "✅ Да"

    await state.update_data(geo_wells=answer)
    await state.set_state(ServiceSelection.waiting_for_fms_data)

    next_question = """
Отлично! Последний вопрос:

Есть ли база данных по ФМС?
    """

    await message.answer(
        next_question,
        reply_markup=get_yes_no_keyboard()
    )


# Хендлер для обработки ДА/НЕТ для ФМС и финального расчета
@router.message(ServiceSelection.waiting_for_fms_data, F.text.in_(["✅ Да", "❌ Нет"]))
async def process_fms_answer_and_calculate(message: Message, state: FSMContext):
    """Обработка ответа о наличии ФМС и расчет стоимости"""
    answer = message.text == "✅ Да"

    user_data = await state.get_data()
    service_key = user_data.get('service_key', 'program_development')

    # Базовая цена
    base_price = SERVICE_BASE_PRICES.get(service_key, 300000)

    # Логика расчета (можно усложнить в зависимости от ответов)
    final_price = base_price

    # Если есть все данные - небольшая скидка
    if (user_data.get('geotech_wells') and
            user_data.get('geo_wells') and
            answer):
        final_price = int(base_price * 0.9)  # 10% скидка

    user_info = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    # Сохраняем расчет
    await save_calculation(
        user_id=message.from_user.id,
        service_type=service_key,
        parameters={
            'geotech_wells': user_data.get('geotech_wells'),
            'geo_wells': user_data.get('geo_wells'),
            'fms_data': answer
        },
        result=f"Рассчитана стоимость услуги: {final_price:,} ₽",
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
            'calculated_price': final_price,
            'answers': {
                'geotech_wells': user_data.get('geotech_wells'),
                'geo_wells': user_data.get('geo_wells'),
                'fms_data': answer
            }
        },
        **user_info
    )

    service_text = f"""
📝 Разработка программы геотехнических исследований

Предварительная стоимость: от {final_price:,} ₽

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


# Хендлер для обработки количества буровых станков
@router.message(ServiceSelection.waiting_for_drilling_rigs, F.text)
async def process_drilling_rigs_count(message: Message, state: FSMContext):
    """Обработка ввода количества буровых станков"""
    if message.text == "⬅️ Назад":
        await state.set_state(ServiceSelection.waiting_for_subservice)
        await message.answer(
            "Выберите услугу:",
            reply_markup=get_geodata_keyboard()
        )
        return

    # Проверяем, что введено число
    if not message.text.isdigit():
        await message.answer(
            "❌ Пожалуйста, введите число буровых станков:",
            reply_markup=get_back_keyboard()
        )
        return

    rigs_count = int(message.text)

    if rigs_count <= 0:
        await message.answer(
            "❌ Количество станков должно быть больше 0:",
            reply_markup=get_back_keyboard()
        )
        return

    user_data = await state.get_data()
    service_key = user_data.get('service_key', 'core_documentation')

    # Расчет стоимости: 3 документатора на станок, каждый по 300,000 руб/мес
    documentators_per_rig = 3
    cost_per_documentator = 300000
    total_documentators = rigs_count * documentators_per_rig
    final_price = total_documentators * cost_per_documentator

    user_info = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }

    # Сохраняем расчет
    await save_calculation(
        user_id=message.from_user.id,
        service_type=service_key,
        parameters={'rigs_count': rigs_count},
        result=f"Рассчитана стоимость: {final_price:,} ₽/мес ({rigs_count} станков × {documentators_per_rig} документаторов)",
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
            'rigs_count': rigs_count,
            'calculated_price': final_price
        },
        **user_info
    )

    service_text = f"""
💎 Геотехническое документирование керна

Количество станков: {rigs_count}
Необходимо документаторов: {total_documentators}

Предварительная стоимость: от {final_price:,} ₽ в месяц

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


# Хендлер для обработки количества расчетов устойчивости
@router.message(ServiceSelection.waiting_for_calculations_count, F.text)
async def process_calculations_count(message: Message, state: FSMContext):
    """Обработка ввода количества расчетов устойчивости"""
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
        "2d_ogr": "2D ОГР",
        "2d_pgr": "2D ПГР",
        "3d_ogr": "3D ОГР",
        "3d_pgr": "3D ПГР"
    }

    service_text = f"""
{service_names.get(service_key, "Расчет устойчивости")}

Количество расчетов: {calculations_count}
Скидка: {discount}%

Предварительная стоимость: от {final_price:,.0f} ₽

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


# Хендлер для обработки количества часов геомеханика
@router.message(ServiceSelection.waiting_for_hours_count, F.text)
async def process_hours_count(message: Message, state: FSMContext):
    """Обработка ввода количества часов для геомеханика"""
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
👨‍💼 {specialist_level}

Количество часов: {hours_count}
Ставка: {base_hourly_rate:,.0f} ₽/час
Скидка: {discount}%

Предварительная стоимость: от {final_price:,.0f} ₽

Хотите оставить контакты для подробной консультации?
    """

    await state.set_state(Calculation.showing_price)
    await state.update_data(
        final_service=service_key,
        calculated_price=final_price
    )

    await message.answer(
        service_text,
        reply_markup=get_contact_keyboard()
    )


# Хендлер для кнопки Назад в различных состояниях ввода
@router.message(
    ServiceSelection.waiting_for_geotech_wells,
    ServiceSelection.waiting_for_geo_wells,
    ServiceSelection.waiting_for_fms_data,
    F.text == "⬅️ Назад"
)
async def back_from_questions(message: Message, state: FSMContext):
    """Возврат из вопросов к выбору услуги"""
    await state.set_state(ServiceSelection.waiting_for_subservice)

    user_data = await state.get_data()
    main_service = user_data.get('main_service', 'geodata_collection')

    if main_service == 'geodata_collection':
        await message.answer(
            "Выберите услугу:",
            reply_markup=get_geodata_keyboard()
        )
    else:
        await message.answer(
            "Выберите услугу:",
            reply_markup=get_main_menu_keyboard()
        )


# Обработчики для кнопки Назад
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
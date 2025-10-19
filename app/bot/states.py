from aiogram.fsm.state import State, StatesGroup

class ServiceSelection(StatesGroup):
    """Состояния для выбора услуги"""
    waiting_for_subservice = State()
    waiting_for_final_service = State()

class Calculation(StatesGroup):
    """Состояния для расчета"""
    showing_price = State()  # Показ цены и предложение оставить контакты

class ContactCollection(StatesGroup):
    """Состояния для сбора контактов"""
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_company = State()

class PhoneInput(StatesGroup):
    """Состояния для ввода телефона"""
    waiting_for_phone_input = State()
from aiogram.fsm.state import State, StatesGroup

class ServiceSelection(StatesGroup):
    """Состояния для выбора услуг"""
    waiting_for_main_service = State()
    waiting_for_subservice = State()
    waiting_for_final_service = State()

class ContactCollection(StatesGroup):
    """Состояния для сбора контактов"""
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_company = State()

class Calculation(StatesGroup):
    """Состояния для расчета"""
    showing_price = State()
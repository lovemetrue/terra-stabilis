from aiogram.fsm.state import State, StatesGroup

class ServiceSelection(StatesGroup):
    waiting_for_subservice = State()
    waiting_for_program_data = State()
    waiting_for_geotech_wells = State()
    waiting_for_geo_wells = State()
    waiting_for_fms_data = State()
    waiting_for_drilling_rigs = State()
    waiting_for_calculations_count = State()
    waiting_for_hours_count = State()

class Calculation(StatesGroup):
    showing_price = State()

class ContactCollection(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()

class PhoneInput(StatesGroup):
    waiting_for_phone_input = State()
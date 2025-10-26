from aiogram.fsm.state import State, StatesGroup


class ContactCollection(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_organization = State()
    confirmation = State()


class PhoneInput(StatesGroup):
    waiting_for_phone_input = State()


class EmailInput(StatesGroup):
    waiting_for_email_input = State()


class OrganizationInput(StatesGroup):
    waiting_for_organization_input = State()
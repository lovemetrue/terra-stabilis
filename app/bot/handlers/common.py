from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.keyboards.main_menu import get_main_menu_keyboard

router = Router()


@router.message()
async def handle_unprocessed_messages(message: Message, state: FSMContext):
    """Обработчик для необработанных сообщений"""
    current_state = await state.get_state()

    # Если есть активное состояние, игнорируем лишние сообщения
    if current_state:
        await message.answer(
            "Пожалуйста, используйте кнопки для взаимодействия с ботом.",
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Если нет активного состояния, показываем главное меню
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=get_main_menu_keyboard()
    )
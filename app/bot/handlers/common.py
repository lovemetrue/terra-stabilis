from aiogram import Router
from aiogram.types import Message
from asgiref.sync import sync_to_async

from apps.bot_data.models import BotUserEvent

router = Router()


# @router.message()
# async def handle_other_messages(message: Message):
#     """Обработка всех остальных сообщений"""
#     await sync_to_async(BotUserEvent.objects.create)(
#         user_id=message.from_user.id,
#         event_type='unknown_message',
#         event_data={'text': message.text}
#     )
#
#     await message.answer(
#         "🤔 Я не понял ваше сообщение. Используйте меню или команду /start для начала работы."
#     )
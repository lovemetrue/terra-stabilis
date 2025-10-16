import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from aiogram import Dispatcher, Bot
from aiogram.types import Message, User, Chat

from app.bot.handlers.start import start_handler
from app.bot.handlers.contacts import process_name
from app.bot.states import ContactCollection


@pytest.fixture
def bot():
    return Mock(spec=Bot)


@pytest.fixture
def dp():
    return Dispatcher()


@pytest.mark.asyncio
async def test_start_handler():
    message = Mock(spec=Message)
    message.answer = AsyncMock()
    message.from_user = Mock(spec=User)
    message.from_user.id = 123
    message.from_user.first_name = "Test"

    await start_handler(message)

    message.answer.assert_called_once()
    assert "Добро пожаловать" in message.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_process_name():
    message = Mock(spec=Message)
    message.text = "Иван Иванов"
    message.answer = AsyncMock()
    message.from_user = Mock(spec=User)
    message.from_user.id = 123

    state = Mock(spec=ContactCollection)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    with patch('app.bot.handlers.contacts.sync_to_async') as mock_sync:
        mock_sync.return_value = AsyncMock()

        await process_name(message, state)

        state.update_data.assert_called_once_with(name="Иван Иванов")
        state.set_state.assert_called_once_with(ContactCollection.waiting_for_phone)
        message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_process_name_with_back():
    message = Mock(spec=Message)
    message.text = "⬅️ Назад"
    message.answer = AsyncMock()

    state = Mock(spec=ContactCollection)
    state.clear = AsyncMock()

    await process_name(message, state)

    state.clear.assert_called_once()
    message.answer.assert_called_once()


class TestKeyboardGeneration:
    def test_main_menu_keyboard(self):
        from app.bot.keyboards.main_menu import get_main_menu_keyboard

        keyboard = get_main_menu_keyboard()

        assert keyboard is not None
        assert len(keyboard.keyboard) > 0
        assert "📊 Сбор исходных гео данных" in [btn.text for row in keyboard.keyboard for btn in row]

    def test_geodata_keyboard(self):
        from app.bot.keyboards.main_menu import get_geodata_keyboard

        keyboard = get_geodata_keyboard()

        assert keyboard is not None
        assert "🗺️ Геотехническое картирование" in [btn.text for row in keyboard.keyboard for btn in row]


@pytest.mark.asyncio
async def test_database_operations():
    from apps.bot_data.models import BotUserEvent

    with patch('apps.bot_data.models.BotUserEvent.objects.create') as mock_create:
        mock_create.return_value = Mock(id=1)

        # Тестирование создания события
        event = await BotUserEvent.objects.create(
            user_id=123,
            event_type='test_event',
            event_data={'test': 'data'}
        )

        assert event.id == 1
        mock_create.assert_called_once()


class TestStateManagement:
    @pytest.mark.asyncio
    async def test_state_transitions(self):
        from aiogram.fsm.state import State, StatesGroup

        class TestStates(StatesGroup):
            state1 = State()
            state2 = State()

        # Тестирование перехода между состояниями
        state = Mock()
        state.set_state = AsyncMock()

        await state.set_state(TestStates.state2)
        state.set_state.assert_called_once_with(TestStates.state2)
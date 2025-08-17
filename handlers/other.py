from aiogram import Router
from aiogram.fsm.context import FSMContext
from telegram import CallbackQuery

router = Router()

@router.callback_query()
async def debug_callback(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    print(f"Received callback: {callback.data} in state: {current_state}")
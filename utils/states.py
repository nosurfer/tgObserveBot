from aiogram.fsm.state import StatesGroup, State

class PollState(StatesGroup):
    poll = State()
    group = State()
    check = State()
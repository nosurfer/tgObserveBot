from aiogram.fsm.state import StatesGroup, State

class GroupState(StatesGroup):
    group = State()

class PollState(StatesGroup):
    poll = State()
    group = State()
    check = State()

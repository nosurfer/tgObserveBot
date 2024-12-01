admin_kbrd = get_keyboard(
    "Создать опрос",
    "Закрыть панель",
    placeholder="Админ панель:",
    sizes=(2, 2, 1)
)


@router.message(StateFilter(None), Command("admin"))
async def admin_kbrd_handler(message: Message):
    text = """**Админ панель**
    
    Для того, чтобы опубликовать опрос, просто оптравьте мне опрос, который необходимо отправить в группу!
    Для побликации сообщения в личные сообщения студентам, просто отправьте сообщение!"""
    await message.answer("**Админ панель**", parse_mode="Markdown")


@router.message(StateFilter(None), F.text.lower() == "создать опрос")
async def create_poll_handler(message: Message, state: FSMContext):
    poll_kbrd = get_keyboard("Отмена", placeholder="Создание опроса:")
    await message.answer("Отправьте опрос", reply_markup=poll_kbrd)
    await state.set_state(PollState.poll)


@router.message(PollState.poll, F.poll)
async def pollstate_poll_handler(message: Message, state: FSMContext):
    check_kbrd = get_inline_keyboard(
        ("✅Да", "да", None),
        ("❌Нет", "нет", None),
    )
    await state.update_data(poll = message.poll)
    await message.answer(str(message.poll))
    await message.answer("Вы уверены что хотите отправить этот опрос?", reply_markup=check_kbrd)
    await state.set_state(PollState.check)


@router.callback_query(PollState.check)
async def pollstate_check_handler(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "да":
        poll = await state.get_data()

        await callback_query.message.answer(str(poll))

        await callback_query.message.answer("Опрос отправлен", reply_markup=admin_kbrd)
        await callback_query.answer(text="Опрос отправлен")
        await state.clear()
    elif callback_query.data == "нет":
        current_state = await state.get_state()
        
        previous = None
        for step in PollState.__all_states__:
            if step.state == current_state:
                await state.set_state(previous)
                await callback_query.answer("Отправьте опрос ещё раз")
                await callback_query.message.answer("Отправьте опрос ещё раз")
                return
            previous = step
        


@router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_state_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == PollState.poll:
        await message.answer("Действие не возможно")
        return
    
    previous = None
    for step in PollState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer("Отправьте запрос ещё раз")
            return
        previous = step


@router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_state_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Все действия были отменены", reply_markup=admin_kbrd)


@router.message(StateFilter(None), F.text.lower() == "закрыть панель")
async def close_kbrd_handler(message: Message):
    await message.answer("Панель закрыта", reply_markup=ReplyKeyboardRemove())
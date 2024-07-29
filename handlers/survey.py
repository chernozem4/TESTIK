from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import database


survey_router = Router()


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary = State()


@survey_router.message(Command("opros_dlya_pupsuka"))
async def start_survey(message: types.Message, state: FSMContext):
    await state.set_state(BookSurvey.name)
    await message.answer("Твое имя, сладки?~~")


@survey_router.message(BookSurvey.name)
async def process_name(message: types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookSurvey.age)
    await message.answer('Сколько лун прожил?')





@survey_router.message(BookSurvey.age)
async def process_age(message: types.Message, state: FSMContext):
    age = int(message.text)
    if age < 17:
        await message.answer("Маленький еще, иди отсюда!")
        await state.clear()
    else:
        await state.update_data(age=message.text)
        await message.answer("И кем ты работаешь?)")
        await state.set_state(BookSurvey.occupation)

@survey_router.message(BookSurvey.occupation)
async def process_occupation(message: types.Message, state: FSMContext):
    await state.update_data(occupation=message.text)
    await message.answer("При деньгах?")
    await state.set_state(BookSurvey.salary)

@survey_router.message(BookSurvey.salary)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    data = await state.get_data()
    print(data)
    await database.execute('''
                        INSERT INTO survay (name, age, occupation, salary) 
                        VALUES (?, ?, ?, ?)
    ''', (data['name'], data['age'], data['occupation'], data['salary']))
    await state.clear()
    await message.answer('Спасибо за мнение')





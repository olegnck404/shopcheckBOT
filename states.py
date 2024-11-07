from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminStates(StatesGroup):
    ENTER_PASSWORD = State()       # Ввод пароля для админа
    CHOOSE_ACTION = State()        # Выбор действия после входа в админ-панель
    ADD_PRODUCT = State()          # Состояние для добавления нового товара
    EDIT_PRODUCT = State()         # Состояние для редактирования товара
    VIEW_PRODUCT = State()         # Состояние для просмотра товара

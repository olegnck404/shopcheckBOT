import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import API_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # Подключаем хранилище для состояний
dp = Dispatcher(bot, storage=storage)

# Подключение к базе данных SQLite
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Создание таблицы для хранения информации о товарах
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo TEXT,
    name TEXT,
    sku TEXT UNIQUE,
    quantity INTEGER,
    price REAL
)
''')
conn.commit()

# Состояния
class AdminStates(StatesGroup):
    ENTER_PASSWORD = State()  # Ввод пароля для админа
    CHOOSE_ACTION = State()  # Выбор действия после входа в админ-панель
    ADD_PRODUCT_NAME = State()  # Ввод названия товара
    ADD_PRODUCT_SKU = State()  # Ввод артикула товара
    ADD_PRODUCT_PRICE = State()  # Ввод цены товара
    ADD_PRODUCT_QUANTITY = State()  # Ввод количества товара
    ADD_PRODUCT_PHOTO = State()  # Ввод фото товара

# Пароль для доступа в админ-панель
ADMIN_PASSWORD = "158x12llo"

# Функция для создания основной клавиатуры с кнопками
def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("🔍 Поиск по артикулу"),
        KeyboardButton("📋 Все товары")
    )
    return keyboard

# Функция для создания админ панели
def create_admin_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("📋 Отобразить все товары")
    )
    return keyboard

# Функция для создания инлайн клавиатуры с товарами
def create_products_keyboard(is_admin=False):
    keyboard = InlineKeyboardMarkup(row_width=1)
    cursor.execute("SELECT sku, name FROM products")
    products = cursor.fetchall()
    
    if products:
        for sku, name in products:
            keyboard.add(InlineKeyboardButton(name, callback_data=f"view_product_{sku}"))
    
    if is_admin:
        keyboard.add(InlineKeyboardButton("➕ Добавить товар", callback_data="add_product"))
    
    return keyboard

# Функция для создания инлайн клавиатуры для редактирования товара
def create_product_edit_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("✏️ Изменить товар", callback_data="edit_product"),
        InlineKeyboardButton("❌ Удалить товар", callback_data="delete_product"),
        InlineKeyboardButton("↩️ Вернуться назад", callback_data="back_to_product_list")
    )
    return keyboard

# Функция для создания инлайн клавиатуры для изменения параметров товара
def create_change_product_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("📝 Изменить название", callback_data="edit_name"),
        InlineKeyboardButton("💲 Изменить цену", callback_data="edit_price"),
        InlineKeyboardButton("📦 Изменить количество", callback_data="edit_quantity"),
        InlineKeyboardButton("↩️ Вернуться назад", callback_data="back_to_product")
    )
    return keyboard

# Функция для получения товара по артикулу
def get_product_by_sku(sku):
    cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
    return cursor.fetchone()

# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я помогу тебе с поиском товаров. Выберите действие:",
        reply_markup=create_main_keyboard()
    )

# Обработчик нажатия на кнопку "Все товары"
@dp.message_handler(lambda message: message.text == "📋 Все товары")
async def all_products(message: types.Message):
    keyboard = create_products_keyboard(is_admin=False)
    await message.answer("Вот список всех товаров:", reply_markup=keyboard)

# Обработчик нажатия на кнопку "Поиск по артикулу"
@dp.message_handler(lambda message: message.text == "🔍 Поиск по артикулу")
async def search_product(message: types.Message):
    await message.answer("Введите артикул товара:")
    await AdminStates.ENTER_PASSWORD.set()

# Обработчик для ввода артикулов и поиска товара
@dp.message_handler(lambda message: message.text.isdigit(), state=AdminStates.ENTER_PASSWORD)
async def search_by_sku(message: types.Message, state: FSMContext):
    sku = message.text.strip()
    product = get_product_by_sku(sku)
    
    if product:
        _, photo, name, sku, quantity, price = product
        if photo:
            await message.answer_photo(photo, caption=f"Товар найден: {name}\n📦 Артикул: {sku}\n💲 Цена: {price}\n📈 Количество: {quantity}")
        else:
            await message.answer(f"Товар найден: {name}\n📦 Артикул: {sku}\n💲 Цена: {price}\n📈 Количество: {quantity}")
        # Обычный пользователь не может редактировать товар
        await message.answer("Выберите действие:", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("↩️ Назад", callback_data="back_to_main_menu")))
    else:
        await message.answer("❌ Товар с таким артикулом не найден.")
    await state.finish()

# Обработчик для входа в админ-панель
@dp.message_handler(lambda message: message.text.startswith("admin://"))
async def admin_login(message: types.Message):
    password = message.text.split("://")[1]
    if password == ADMIN_PASSWORD:
        await message.answer("Привет, администратор! Выберите действие:",
                             reply_markup=create_admin_keyboard())
        await AdminStates.CHOOSE_ACTION.set()
    else:
        await message.answer("❌ Неверный пароль!")

# Обработчик для отображения всех товаров в админ-панели
@dp.message_handler(lambda message: message.text == "📋 Отобразить все товары", state=AdminStates.CHOOSE_ACTION)
async def show_all_products_admin(message: types.Message):
    keyboard = create_products_keyboard(is_admin=True)
    await message.answer("Вот список всех товаров:", reply_markup=keyboard)

# Обработчик для кнопки "Добавить товар" (отображение инлайн кнопок)
@dp.callback_query_handler(lambda c: c.data == "add_product")
async def add_product(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите название товара:")
    await AdminStates.ADD_PRODUCT_NAME.set()
    await callback_query.answer()

# Обработчик для нажатия на кнопку товара
@dp.callback_query_handler(lambda c: c.data.startswith('view_product_'))
async def view_product(callback_query: CallbackQuery):
    sku = callback_query.data.split('_')[2]
    product = get_product_by_sku(sku)
    
    if product:
        _, photo, name, sku, quantity, price = product
        if photo:
            await bot.send_photo(callback_query.from_user.id, photo, caption=f"Товар: {name}\nАртикул: {sku}\nЦена: {price}\nКоличество: {quantity}")
        else:
            await bot.send_message(callback_query.from_user.id, f"Товар: {name}\nАртикул: {sku}\nЦена: {price}\nКоличество: {quantity}")
        await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=create_product_edit_keyboard())
    await callback_query.answer()

# Обработчик для кнопки "Изменить товар"
@dp.callback_query_handler(lambda c: c.data == 'edit_product')
async def edit_product(callback_query: CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите, что хотите изменить:", reply_markup=create_change_product_keyboard())
    await callback_query.answer()

# Обработчик для кнопки "Вернуться назад"
@dp.callback_query_handler(lambda c: c.data == 'back_to_product_list')
async def back_to_product_list(callback_query: CallbackQuery):
    keyboard = create_products_keyboard(is_admin=True)
    await bot.send_message(callback_query.from_user.id, "Выберите товар:", reply_markup=keyboard)
    await callback_query.answer()

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

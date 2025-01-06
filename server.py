from flask import Flask, send_from_directory
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command
from aiogram import F
from threading import Thread

# === Настройки Telegram-бота ===
TOKEN = '7930529716:AAF5TYEKKTsG_jUD3k0gtzIa3YvAfikUIdk'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# === Настройки Flask-сервера ===
app = Flask(__name__, static_folder='../src')


# === Роуты Flask ===
@app.route('/')
def index():
    return send_from_directory('../src', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('../src', filename)


@app.route('/assets/<path:filename>')
def assets_files(filename):
    return send_from_directory('../src/assets', filename)


# === Telegram-бот: Обработчики ===
@dp.message(Command("start"))
async def start(message: types.Message):
    username = message.from_user.username or message.from_user.first_name or "User"
    web_app_url = f"https://mmm-coin.web.app/"  # URL вашего Flask-сервера

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть в 1 клик 🎮', web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton(text='Подписаться на канал 📢', url='https://t.me/your_channel')],
        [InlineKeyboardButton(text='Как заработать на игре 💰', callback_data='how_to_earn')]
    ])

    await message.answer(
        "Привет! Добро пожаловать в MMM Coin 🎮!\n"
        "Отныне ты — директор криптобиржи. Какой? Выбирай сам. Тапай по экрану, собирай монеты, качай пассивный доход, разрабатывай собственную стратегию дохода. Мы в свою очередь оценим это во время листинга токена, даты которого ты узнаешь совсем скоро. Про друзей не забывай — зови их в игру и получайте вместе ещё больше монет!",
        reply_markup=keyboard
    )


@dp.callback_query(F.data.in_({'how_to_earn'}))
async def button_handler(callback_query: types.CallbackQuery):
    if callback_query.data == 'how_to_earn':
        await bot.send_message(callback_query.from_user.id, "Чтобы заработать, приглашай друзей и получай бонусы!")
    await callback_query.answer()


# === Запуск Telegram-бота ===
async def telegram_main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# === Запуск Flask и Telegram параллельно ===
def run_flask():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)



if __name__ == '__main__':
    # Flask запускается в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Telegram запускается в основном asyncio-событии
    asyncio.run(telegram_main())

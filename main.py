from aiogram.utils import executor
from loader import dp
from handlers import start, chat

start.register(dp)
chat.register(dp)

print("✅ YuktiAI Started")

executor.start_polling(dp, skip_updates=True)

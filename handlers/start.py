from aiogram import types

def register(dp):

    @dp.message_handler(commands=["start"])
    async def start_handler(message: types.Message):

        await message.reply(
            "👋 Welcome to YuktiAI\n\n"
            "• AI Chat\n"
            "• Live Amazon Search\n"
            "• Memory"
        )

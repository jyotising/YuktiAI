from aiogram import types

from services.ai_service import ask_ai
from services.amazon_service import (
    is_shopping_query,
    search_amazon_products
)

from memory import save_memory, load_memory

def register(dp):

    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def chat_handler(message: types.Message):

        user_id = str(message.from_user.id)
        user_text = message.text

        try:

            if is_shopping_query(user_text):

                await message.reply(
                    "🔍 Searching Amazon..."
                )

                products = search_amazon_products(
                    user_text
                )

                if not products:
                    await message.reply(
                        "❌ No products found."
                    )
                    return

                for product in products:

                    caption = (
                        f"📦 {product['title']}\n\n"
                        f"💰 {product['price']}\n"
                        f"⭐ {product['rating']}\n\n"
                        f"🛒 {product['link']}"
                    )

                    if product["image"]:

                        await message.reply_photo(
                            photo=product["image"],
                            caption=caption
                        )

                    else:

                        await message.reply(caption)

                return

            history = load_memory(user_id)

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are YuktiAI, "
                        "a smart AI assistant."
                    )
                }
            ]

            messages.extend(history)

            messages.append({
                "role": "user",
                "content": user_text
            })

            reply = ask_ai(messages)

            save_memory(user_id, "user", user_text)
            save_memory(user_id, "assistant", reply)

            await message.reply(reply)

        except Exception as e:

            await message.reply(
                f"⚠️ Error:\n{e}"
            )

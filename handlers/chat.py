# handlers/chat.py

import os
import random
import asyncio

from aiogram import types

from loader import dp, bot

from services.ai_service import ask_ai

from services.amazon_service import (
    is_shopping_query,
    search_amazon_products
)

from services.vision_service import (
    analyze_image
)


# ==========================================
# PREMIUM SEARCH LOADING
# ==========================================

premium_loading = [

    "🧠 YuktiAI is thinking...",

    "🔍 Finding the best products for you...",

    "⚡ AI is analyzing live Amazon deals...",

    "🛒 Searching premium recommendations...",

    "✨ Curating smart suggestions..."
]


# ==========================================
# MAIN CHAT HANDLER
# ==========================================

@dp.message_handler(
    content_types=types.ContentType.TEXT
)
async def chat_handler(
    message: types.Message
):

    user_message = message.text


    # ======================================
    # SHOPPING MODE
    # ======================================

    if is_shopping_query(user_message):

        loading = await message.reply(
            random.choice(premium_loading)
        )

        try:

            products = search_amazon_products(
                user_message
            )

            if not products:

                await loading.edit_text(
                    "❌ No products found."
                )

                return

            await loading.delete()

            for product in products:

                caption = f"""
🛍 {product['title']}

💰 Price: {product['price']}
⭐ Rating: {product['rating']}

🛒 Buy Now:
{product['link']}
"""

                # SEND PRODUCT IMAGE

                if product["image"]:

                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=product["image"],
                        caption=caption
                    )

                else:

                    await message.reply(
                        caption
                    )

                await asyncio.sleep(1)

        except Exception as e:

            await loading.edit_text(
                f"❌ Shopping Error:\n{e}"
            )

        return


    # ======================================
    # NORMAL AI CHAT
    # ======================================

    try:

        thinking = await message.reply(
            "🧠 Thinking..."
        )

        ai_reply = ask_ai(
            user_message
        )

        await thinking.edit_text(
            ai_reply
        )

    except Exception as e:

        await message.reply(
            f"❌ AI Error:\n{e}"
        )


# ==========================================
# IMAGE AI VISION
# ==========================================

@dp.message_handler(
    content_types=types.ContentType.PHOTO
)
async def image_handler(
    message: types.Message
):

    try:

        loading = await message.reply(
            "🧠 YuktiAI Vision is analyzing your image..."
        )

        # GET IMAGE

        photo = message.photo[-1]

        # GET FILE INFO

        file_info = await bot.get_file(
            photo.file_id
        )

        # DOWNLOAD IMAGE

        downloaded_file = await bot.download_file(
            file_info.file_path
        )

        # SAVE TEMP FILE

        image_path = f"temp_{photo.file_id}.jpg"

        with open(
            image_path,
            "wb"
        ) as new_file:

            new_file.write(
                downloaded_file.read()
            )

        # AI ANALYSIS

        result = analyze_image(
            image_path
        )

        # FINAL RESPONSE

        final_text = f"""
✨ YuktiAI Vision Result

{result}

━━━━━━━━━━━━━━━
🧠 Powered by YuktiAI Vision
"""

        await loading.edit_text(
            final_text
        )

        # DELETE TEMP FILE

        os.remove(
            image_path
        )

    except Exception as e:

        await message.reply(
            f"❌ Vision Error:\n{e}"
        )


# ==========================================
# FIX REGISTER ERROR
# ==========================================

def register(dp):
    pass
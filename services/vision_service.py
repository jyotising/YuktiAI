# services/vision_service.py

import base64

from openai import OpenAI

from config import OPENROUTER_API_KEY
from services.amazon_service import search_amazon_products


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


# =========================
# ENCODE IMAGE
# =========================

def encode_image(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# =========================
# MAIN ANALYZER
# =========================

def analyze_image(image_path):

    base64_image = encode_image(image_path)

    prompt = """
Analyze this image intelligently.

IMPORTANT:

First decide:
- Is this a PRODUCT image?
OR
- Is this a normal photo/scenery/person image?

If PRODUCT:
Return ONLY:

PRODUCT_DETECTED: YES
PRODUCT_NAME:
PRODUCT_CATEGORY:
PRODUCT_SEARCH_QUERY:
SHORT_DESCRIPTION:

If NOT PRODUCT:
Return ONLY:

PRODUCT_DETECTED: NO
IMAGE_ANALYSIS:
"""

    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[
            {
                "role": "user",
                "content": [

                    {
                        "type": "text",
                        "text": prompt
                    },

                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],

        temperature=0.7,
        max_tokens=300
    )

    result = response.choices[0].message.content


    # =========================
    # PRODUCT DETECTED
    # =========================

    if "PRODUCT_DETECTED: YES" in result:

        try:

            lines = result.split("\n")

            product_name = ""
            category = ""
            search_query = ""
            short_description = ""

            for line in lines:

                if "PRODUCT_NAME:" in line:
                    product_name = line.replace(
                        "PRODUCT_NAME:",
                        ""
                    ).strip()

                elif "PRODUCT_CATEGORY:" in line:
                    category = line.replace(
                        "PRODUCT_CATEGORY:",
                        ""
                    ).strip()

                elif "PRODUCT_SEARCH_QUERY:" in line:
                    search_query = line.replace(
                        "PRODUCT_SEARCH_QUERY:",
                        ""
                    ).strip()

                elif "SHORT_DESCRIPTION:" in line:
                    short_description = line.replace(
                        "SHORT_DESCRIPTION:",
                        ""
                    ).strip()


            amazon_products = search_amazon_products(
                search_query
            )


            final_response = f"""
🛍 YuktiAI Product Vision

📦 Product:
{product_name}

🏷 Category:
{category}

🧠 AI Insight:
{short_description}

━━━━━━━━━━━━━━━
🔥 Best Matching Products:
"""


            if len(amazon_products) == 0:

                final_response += """

No matching Amazon products found.
"""

            else:

                for product in amazon_products[:3]:

                    final_response += f"""

📌 {product['title']}

💰 {product['price']}
⭐ {product['rating']}

🛒 Buy Now:
{product['link']}

━━━━━━━━━━━━━━━
"""


            return final_response


        except Exception as e:

            return f"❌ Product Processing Error:\n{e}"


    # =========================
    # NORMAL IMAGE ANALYSIS
    # =========================

    else:

        analysis = result.replace(
            "PRODUCT_DETECTED: NO",
            ""
        ).replace(
            "IMAGE_ANALYSIS:",
            ""
        ).strip()

        return f"""
✨ YuktiAI Vision

{analysis}

━━━━━━━━━━━━━━━
⚡ Powered by YuktiAI
"""
# services/ai_service.py

from groq import Groq

from config import GROQ_API_KEY


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ==========================================
# AI CHAT
# ==========================================

def ask_ai(user_message):

    messages = [

        {
            "role": "system",

            "content": """
You are YuktiAI.

You are:
- smart
- premium
- modern
- friendly
- human-like

Rules:
- Never say you are ChatGPT
- Never say you are Llama
- Always say your name is YuktiAI
- Reply naturally
- Keep responses concise
"""
        },

        {
            "role": "user",

            "content": user_message
        }
    ]


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=messages,

        temperature=0.7,

        max_tokens=1024
    )


    return response.choices[0].message.content
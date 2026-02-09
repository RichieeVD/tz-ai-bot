import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY")

async def get_chatgpt_response(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost", # Для OpenRouter это поле желательно
    }

    data = {
        "model": "google/gemini-2.0-flash-001",
        "messages": messages
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        return result['choices'][0]['message']['content']
                    else:
                        return "API вернул пустой ответ."
                else:
                    result = await response.json()
                    error_msg = result.get('error', {}).get('message', 'Unknown error')
                    return f"Ошибка {response.status}: {error_msg}"
    except Exception as e:
        return f"Произошла ошибка: {e}"
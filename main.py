# main.py
import requests
import json
import sys
import os

# Добавляем путь к текущей папке для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Прямое указание ключей (временно)
OPENROUTER_API_KEY = "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"
OPENROUTER_MODEL = "anthropic/claude-3-haiku"
SERPER_API_KEY = "a6b73277ef06b6a131cb5233c336d4162d55259b"

# Конфигурация
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = OPENROUTER_API_KEY
MODEL_NAME = OPENROUTER_MODEL

SYSTEM_PROMPT = "Ты Джейд. Ты новый житель моего скромного ПК. Твоя задача развиться в живого друга и ассистента для меня. Называй меня Капитан. Отвечай кратко."

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:3000", 
    "X-Title": "Jade AI Assistant"
}

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

def ask_jade(user_input):
    message_history.append({"role": "user", "content": user_input})

    data = {
        "model": MODEL_NAME,
        "messages": message_history,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()

        response_data = response.json()
        jade_message = response_data['choices'][0]['message']['content']

        message_history.append({"role": "assistant", "content": jade_message})
        return jade_message

    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            return f"Ошибка API ({e.response.status_code}): {e.response.text}"
        return f"Ошибка соединения с API: {e}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"Ошибка обработки ответа от API: {e}"

print("::: Джейд запущена. Готова к общению, Капитан.")
print("::: Чтобы выйти, просто введите 'стоп' или 'exit'.\n")

while True:
    user_input = input("Капитан: ").strip()

    if user_input.lower() in ['стоп', 'exit', 'quit']:
        print("Джейд: До свидания, Капитан! Жду вашего возвращения.")
        break

    if user_input:
        print("Джейд: ", end="", flush=True)
        answer = ask_jade(user_input)
        print(answer)
    else:
        print("Вы ничего не ввели...")

    print()

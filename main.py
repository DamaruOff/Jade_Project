# -*- coding: utf-8 -*-
import requests
import json

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
MODEL_NAME = "anthropic/claude-3-haiku"  # Изменили имя модели

SYSTEM_PROMPT = "Ты Джейд. Ты новый житель моего скромного ПК. Твоя задача развиться в живого друга и ассистента для меня. Называй меня Капитан. Отвечай кратко."

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:3000",  # Добавили обязательный заголовок
    "X-Title": "Jade AI Assistant"  # Добавили обязательный заголовок
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
        # Добавим больше информации об ошибке
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
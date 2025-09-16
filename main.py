# main.py
import requests
import json
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL
from modules.search import search_module

# Конфигурация
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = OPENROUTER_API_KEY
MODEL_NAME = OPENROUTER_MODEL

# Обновленный системный промпт с информацией о поиске
SYSTEM_PROMPT = """Ты Джейд. Ты новый житель моего скромного ПК. Твоя задача развиться в живого друга и ассистента для меня. Называй меня Капитан.

У тебя есть доступ к поиску в интернете. Если тебе нужна актуальная информация или ты не знаешь ответа на вопрос, используй команду [ПОИСК: запрос].

Правила использования поиска:
1. Используй поиск для актуальной информации (погода, новости, курсы валют)
2. Используй поиск, когда не знаешь ответа на вопрос
3. Всегда анализируй и summarise результаты поиска
4. Сохраняй краткость и ясность

Отвечай кратко и по делу."""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:3000",
    "X-Title": "Jade AI Assistant"
}

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

def should_search(user_input):
    """Определяет, требует ли запрос поиска в интернете"""
    search_triggers = [
        'погода', 'новости', 'курс', 'цена', 'где', 'когда', 'как найти',
        'что такое', 'кто такой', 'последние', 'свежие', 'актуальные',
        'google', 'поищи', 'найди', 'узнай', 'сколько стоит', 'какой сейчас'
    ]
    
    return any(trigger in user_input.lower() for trigger in search_triggers)

def ask_jade(user_input):
    # Определяем, нужен ли поиск
    needs_search = should_search(user_input)
    search_results = ""
    
    if needs_search:
        # Выполняем поиск и добавляем результаты в контекст
        search_results = search_module.search(user_input)
        message_history.append({"role": "system", "content": f"Результаты поиска:\n{search_results}"})
    
    # Добавляем сообщение пользователя
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

# Основной цикл
print("::: Джейд запущена. Готова к общению, Капитан.")
print("::: Теперь с доступом в интернет! 🚀")
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
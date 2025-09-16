# modules/search.py
import requests
from config import SERPER_API_KEY

class SearchModule:
    def __init__(self):
        self.api_key = SERPER_API_KEY
        self.api_url = "https://google.serper.dev/search
    
    def search(self, query):
        """Выполняет поиск в интернете через Serper API"""
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            "q": query,
            "num": 5  # Количество результатов
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            return self._format_results(response.json())
            
        except Exception as e:
            return f"❌ Ошибка поиска: {str(e)}"
    
    def _format_results(self, results):
        """Форматирует результаты поиска в читаемый текст"""
        if not results.get('organic'):
            return "Поиск не дал результатов"
        
        formatted = "🔍 Результаты поиска:\n\n"
        
        for i, result in enumerate(results['organic'][:3], 1):  # Берем топ-3
            formatted += f"{i}. {result.get('title', '')}\n"
            formatted += f"   {result.get('link', '')}\n"
            formatted += f"   {result.get('snippet', '')}\n\n"
        
        return formatted

# Создаем глобальный экземпляр для импорта
search_module = SearchModule()
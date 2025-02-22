import requests
import json
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich import print
import emoji

# Код от Antric
# API Keys, Работа GeMini В России а так же чучуть кода - Cubbe
API_KEY = "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"
MODEL = "deepseek/deepseek-r1-distill-llama-70b:free"

# Функция для обработки контента (если нужно удалять лишние теги)
def process_content(content):
    return content.replace('<think>', '').replace('</think>', '')

# Хранение истории диалога
conversation_history = []

# Потоковый вывод для DeepSeek
def chat_stream(prompt):
    """
    Реализует потоковый вывод ответа от DeepSeek.
    
    :param prompt: Текст запроса (строка)
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Создаем данные для запроса, включая историю диалога
    data = {
        "model": MODEL,
        "messages": conversation_history + [{"role": "user", "content": prompt}],  # Добавляем текущий запрос
        "stream": True
    }

    with requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        stream=True
    ) as response:
        if response.status_code != 200:
            print(f"[bold red]Ошибка API:[/bold red] {response.status_code}")
            return ""
        
        full_response = []
        
        for chunk in response.iter_lines():
            if chunk:
                chunk_str = chunk.decode('utf-8').replace('data: ', '')
                try:
                    chunk_json = json.loads(chunk_str)
                    if "choices" in chunk_json:
                        content = chunk_json["choices"][0]["delta"].get("content", "")
                        if content:
                            cleaned = process_content(content)
                            print(cleaned, end='', flush=True)
                            full_response.append(cleaned)
                except:
                    pass
        
        print()  # Перенос строки после завершения потока
        return ''.join(full_response)

# Основной цикл программы
def main():
    print("DeepSeek-R1\nДля выхода введите 'exit'\n")
    
    while True:
        user_input = input("\nВы: ").strip()
        
        if user_input.lower() == 'exit':
            print("Завершение работы...")
            break
        
        # Добавляем запрос пользователя в историю диалога
        conversation_history.append({"role": "user", "content": user_input})
        
        print("[bold blue]DeepSeek[/bold blue]: ", end=' ', flush=True)
        
        # Получаем ответ от ИИ и добавляем его в историю диалога
        ai_response = chat_stream(user_input)
        if ai_response:
            conversation_history.append({"role": "assistant", "content": ai_response})

if __name__ == "__main__":
    main()
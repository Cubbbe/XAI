import requests
import json
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich import print
import emoji
from dns import resolver
import threading
from fake_useragent import UserAgent
import time

# Инициализация User-Agent
ua = UserAgent()

# Хранение истории диалога
conversation_history = []

# Настройки DNS-сервера
def start_dns_server():
    resolver.get_default_resolver().nameservers = ['https://dns.comss.one/dns-query']

def stop_dns_server():
    resolver.get_default_resolver().nameservers = []

# Функция для обработки контента (если нужно удалять лишние теги)
def process_content(content):
    return content.replace('<think>', '').replace('</think>', '')

# Отправка запроса к stablediffusion.fr
def send_prompt_to_chatgpt(prompt):
    """
    Отправляет промпт на сайт stablediffusion.fr и возвращает ответ от ИИ.
    
    :param prompt: Текст запроса (строка)
    :return: Ответ от ИИ (строка) или сообщение об ошибке
    """
    url = "https://stablediffusion.fr/gpt4/predict2"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": ua.random,  # Случайный User-Agent
        "Referer": "https://stablediffusion.fr/chatgpt4?lng=en",
        "Origin": "https://stablediffusion.fr",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    # Добавляем cookies (замените значения на реальные)
    cookies = {
        "connect.sid": "s%3AIvTSphGiWak9iyv9mHZj5_nJ_BdwSIjZ.2bsBQhaasl8%2BDxq9VvW5Iv%2FL1WWSQdWqVLIb%2BMoD%2FUI",
        "i18next": "en"
    }

    # Добавляем историю диалога к текущему запросу
    full_prompt = "\n".join(conversation_history + [prompt])
    data = {
        "prompt": full_prompt
    }

    try:
        response = requests.post(url, json=data, headers=headers, cookies=cookies, timeout=30)
        
        # Проверяем статус-код ответа
        if response.status_code != 200:
            print(f"[bold red]Ошибка сервера:[/bold red] Код состояния {response.status_code}.")
            print(f"Сырой ответ: {response.text}")
            return f"Ошибка сервера: Код состояния {response.status_code}."
        
        try:
            result = response.json()
        except ValueError:
            print("[bold red]Ошибка:[/bold red] Сервер вернул недопустимый JSON.")
            print(f"Сырой ответ: {response.text}")
            return "Ошибка: Недопустимый JSON."
        
        # Проверяем наличие ключа 'message' или 'response' в ответе
        if "message" in result:
            return result["message"]
        elif "response" in result:
            return result["response"]
        else:
            print("[bold red]Ошибка:[/bold red] Неправильный формат ответа от сервера.")
            print(f"Сырой ответ: {result}")
            return "Ошибка: Неправильный формат ответа."
    except requests.exceptions.RequestException as e:
        print(f"[bold red]Ошибка:[/bold red] При отправке запроса возникла ошибка: {e}")
        return f"Ошибка при отправке запроса: {e}"

# Потоковый вывод для stablediffusion.fr
def chat_stream(prompt):
    """
    Реализует потоковый вывод ответа от ИИ.
    
    :param prompt: Текст запроса (строка)
    """
    response = send_prompt_to_chatgpt(prompt)
    
    if response.startswith("Ошибка"):
        print(f"[bold red]{response}[/bold red]")
        return
    
    # Разбиваем ответ на части для имитации потокового вывода
    for char in response:
        print(char, end='', flush=True)
        time.sleep(0.03)  # Задержка для эффекта потокового вывода
    print()  # Перенос строки после завершения вывода

# Основной цикл программы
def main():
    print("ChatGPT-4o - XAIv2\nДля выхода введите 'exit'\n")
    
    # Запуск DNS-сервера
    start_dns_server()
    
    while True:
        user_input = input("\nВы: ").strip()
        
        if user_input.lower() == 'exit':
            print("Завершение работы...")
            # Остановка DNS-сервера
            stop_dns_server()
            break
        
        # Добавляем запрос пользователя в историю
        conversation_history.append(f"Вы: {user_input}")
        
        # Вывод ответа ИИ
        print("[bold green]ChatGPT-4o[/bold green]: ", end=' ', flush=True)
        chat_stream(user_input)

if __name__ == "__main__":
    main()
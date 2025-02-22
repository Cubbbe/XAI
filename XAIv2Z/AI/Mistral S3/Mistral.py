import requests
import json
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich import print
import emoji

# Код от Antric
# API Keys, Работа GeMini В России а так же чучуть кода - Cubbe

API_KEY = "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"
MODEL = "mistralai/mistral-small-24b-instruct-2501:free"

def process_content(content):
    return content.replace('<think>', '').replace('</think>', '')

def chat_stream(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }

    with requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        stream=True
    ) as response:
        if response.status_code != 200:
            print("[bold red]Ошибка API:[/bold red]:", response.status_code)
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
def main():
    print("Mistral\nДля выхода введите 'exit'\n")

    while True:
        user_input = input("Вы: ")
        
        if user_input.lower() == 'exit':
            print("Завершение работы...")
            break
            
        print("[bold yellow]Mistral[/bold yellow]: ", end=' ', flush=True)
        chat_stream(user_input)

if __name__ == "__main__":
    main()
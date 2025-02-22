import os
import sys
import subprocess
from colorama import Fore, Back, Style

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear_screen()
    print(Fore.RED + "[Автор - Cubbe, Код - Antric]" + Style.RESET_ALL)
    print(Fore.BLUE + "  " + Style.RESET_ALL)
    print(Fore.YELLOW + "XAIv1" + Style.RESET_ALL)
    print(Fore.BLUE + "[1] - DeepSeek" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "[2] - LLaMa" + Style.RESET_ALL)
    print(Fore.BLUE + "[3] - Qwen" + Style.RESET_ALL)
    print(Fore.YELLOW + "[4] - GeMini" + Style.RESET_ALL)
    print(Fore.YELLOW + "[5] - Mistral" + Style.RESET_ALL)
    print(Fore.RED + "[6] - Rogue Rose" + Style.RESET_ALL)
    print(Fore.RED + "[7] - Microsoft PHI-3" + Style.RESET_ALL)
    print(Fore.BLUE + "  " + Style.RESET_ALL)
    print(Fore.YELLOW + "XAIv2" + Style.RESET_ALL)
    print(Fore.GREEN + "[8] - ChatGPT-4o" + Style.RESET_ALL)
    print(Fore.RED + "[0] - Выход" + Style.RESET_ALL)
    print(Fore.BLUE + "  " + Style.RESET_ALL)
    print(Fore.GREEN + "V.1.1" + Style.RESET_ALL)
    print(Fore.BLUE + "  " + Style.RESET_ALL)
    choice = input("Введи номер выбора: ")
    return choice

def run_program(choice):
    if choice == '1':
        clear_screen()
        subprocess.call([sys.executable, "AI/DeepSeek R1/DeepSeek.py"])
    elif choice == '2':
        clear_screen()
        subprocess.call([sys.executable, "AI/LLaMa 3B/LLaMa.py"])
    elif choice == '3':
        clear_screen()
        subprocess.call([sys.executable, "AI/Qwen 72/Qwen.py"])
    elif choice == '4':
        clear_screen()
        subprocess.call([sys.executable, "AI/GeMini Pro 2.0/GeMini.py"])
    elif choice == '5':
        clear_screen()
        subprocess.call([sys.executable, "AI/Mistral S3/Mistral.py"])
    elif choice == '6':
        clear_screen()
        subprocess.call([sys.executable, "AI/Rogue Rose/Rogue Rose.py"])
    elif choice == '7':
        clear_screen()
        subprocess.call([sys.executable, "AI/Microsoft PHI-3/Phi.py"])
    elif choice == '8':
        clear_screen()
        subprocess.call([sys.executable, "AI/ChatGPT-4o/ChatGPT.py"])
    elif choice == '42':
        clear_screen()
        subprocess.call([sys.executable, "AI/42GPT-1T/BOSSGPT.py"])
    elif choice == '0':
        sys.exit()
    else:
        print("Не правильный выбор, введи адекватно")
        input("Нажми Enter чтобы продолжить.")

    clear_screen()

from colorama import init
init()

while True:
    choice = main_menu()
    run_program(choice)
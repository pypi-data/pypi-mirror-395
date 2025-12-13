import time
import os
import importlib.metadata
from cerebras.cloud.sdk import Cerebras
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True, strip=False, convert=False)


def load_key():
    """
    Loads API key from:
    1. Environment variable
    2. cerebras_key.txt inside package
    """
    api_key = os.getenv("CEREBRAS_API_KEY")
    if api_key:
        return api_key.strip()

    key_path = os.path.join(os.path.dirname(__file__), "cerebras_key.txt")

    if os.path.exists(key_path):
        with open(key_path, "r") as f:
            return f.read().strip()

    return None


def start_chat():
    RED = "\033[91m"
    RESET = "\033[0m"

    api_key = load_key()
    if not api_key:
        print(f"{Fore.YELLOW}⚠ No API key found!")
        api_key = input("Enter your Cerebras API key: ").strip()

    client = Cerebras(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": "You are Errol 4 Sonic."},
                {"type": "text", "text": "You live inside the Python library archit_ug."},
                {"type": "text", "text": "Your creator is 2AM mimo!"},
            ],
        }
    ]

    print("Chat started! (type 'exit' or 'quit' to stop)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": user_input}],
        })

        stream = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=messages,
            stream=True,
            temperature=0.7,
            top_p=0.8,
            max_completion_tokens=5000,
        )

        print("Assistant: ", end="", flush=True)
        reply = ""

        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            print(token, end="", flush=True)
            reply += token

        print()
        messages.append({"role": "assistant", "content": [{"type": "text", "text": reply}]})


def details():
    """Prints the library details."""
    version = importlib.metadata.version("archit_ug")

    RED = "\033[91m"
    RESET = "\033[0m"

    print(Fore.CYAN + "=== Archit_UG Library Details ===" + Style.RESET_ALL)
    print(f"{RED}Author: 2AM mimo!{RESET}")
    print(f"{RED}Real Name: A***** R*****{RESET}")
    print(f"{RED}Email: fearmimo2012@gmail.com{RESET}")
    print(f"{RED}GitHub: Archit-web-29{RESET}")
    print(f"{RED}Model: Errol 4 Sonic - 120B Formal{RESET}")
    print(f"{Fore.GREEN}Version: {version}{Fore.RESET}")
    print("PyPI: https://pypi.org/project/archit-ug/")
    print(Style.RESET_ALL)
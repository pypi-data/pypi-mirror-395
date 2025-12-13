import time
import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras
from colorama import Fore, Style, init

# Auto color reset
init(autoreset=True)

# Load from current working directory (if .env is here)
load_dotenv()

# If still not loaded, try absolute library path
if "CEREBRAS_API_KEY" not in os.environ:
    load_dotenv("/Users/raviranjan/archit_ug/.env")

def start_chat():
    print(f"{Fore.RED}Author: 2AM mimo!")
    print("Real name: A***** R*****")
    print("Email: fearmimo2012@gmail.com")
    print("GitHub: Archit-web-29")
    print("Model: Errol 4 Sonic - 120B Formal")
    print(f"{Fore.RESET}")
    print("Hope you have a great time using my library\n")

    time.sleep(2)

    # ===== Load API key =====
    api_key = os.getenv("CEREBRAS_API_KEY")

    if not api_key:
        print(f"{Fore.YELLOW}⚠ Warning: No API key found in environment variable 'CEREBRAS_API_KEY'")
        print("Please add your API key to a .env file or enter it now.")
        api_key = input("Enter your Cerebras API Key: ").strip()

    # ===== Create client =====
    client = Cerebras(api_key=api_key)

    # ===== System prompt =====
    messages = [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": "You are Errol 4 Sonic."},
                {"type": "text", "text": "You are inside the Python Library archit_ug."},
                {"type": "text", "text": "Your author and creator is 2AM mimo!"},
            ],
        }
    ]

    print("Chat started! (type 'exit' or 'quit' to stop)\n")

    # ===== Main chat loop =====
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Add user message
        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": user_input}],
        })

        # Stream response
        stream = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=messages,
            stream=True,
            max_completion_tokens=20000,
            temperature=0.7,
            top_p=0.8,
        )

        print("Assistant: ", end="", flush=True)
        full = ""

        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            print(token, end="", flush=True)
            full += token

        print()

        # Add assistant message
        messages.append({
            "role": "assistant",
            "content": [{"type": "text", "text": full}],
        })

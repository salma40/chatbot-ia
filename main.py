"""
main.py - Interface en ligne de commande du chatbot
Usage : python main.py
"""

import os
import sys
from chatbot import Chatbot

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.rule import Rule
    RICH = True
except ImportError:
    RICH = False

console = Console() if RICH else None


def print_banner():
    if RICH:
        console.print(Panel.fit(
            "[bold blue]Chatbot IA[/bold blue] — propulse par Claude (Anthropic)\n"
            "[dim]Commandes : 'exit' pour quitter | 'reset' pour nouvelle conversation | 'stats' pour les statistiques[/dim]",
            border_style="blue"
        ))
    else:
        print("=" * 60)
        print("  Chatbot IA — propulse par Claude (Anthropic)")
        print("  Commandes : exit | reset | stats")
        print("=" * 60)


def print_user(msg: str):
    if RICH:
        console.print(f"\n[bold green]Vous[/bold green] : {msg}")
    else:
        print(f"\nVous : {msg}")


def print_bot(msg: str):
    if RICH:
        console.print(Panel(msg, title="[bold blue]Assistant[/bold blue]",
                            border_style="dim blue", padding=(0, 1)))
    else:
        print(f"\nAssistant : {msg}\n")


def print_stats(stats: dict):
    lines = "\n".join(f"  {k:<28} {v}" for k, v in stats.items())
    if RICH:
        console.print(Panel(lines, title="[bold]Statistiques de session[/bold]",
                            border_style="yellow"))
    else:
        print("\n--- Statistiques ---")
        print(lines)


def check_api_key():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nErreur : la variable ANTHROPIC_API_KEY n'est pas definie.")
        print("Ajoutez-la avec : export ANTHROPIC_API_KEY='votre-cle'")
        print("Obtenez une cle sur : https://console.anthropic.com\n")
        sys.exit(1)


def main():
    check_api_key()
    print_banner()

    bot = Chatbot()

    while True:
        try:
            if RICH:
                user_input = console.input("\n[bold green]Vous[/bold green] : ").strip()
            else:
                user_input = input("\nVous : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nAu revoir !")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\nAu revoir !")
            break
        elif user_input.lower() == "reset":
            bot.reset()
            continue
        elif user_input.lower() == "stats":
            print_stats(bot.get_stats())
            continue

        print_user(user_input) if not RICH else None

        try:
            response = bot.send(user_input)
            print_bot(response)
        except Exception as e:
            print(f"\nErreur : {e}")


if __name__ == "__main__":
    main()

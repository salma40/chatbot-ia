"""
analysis.py - Analyse et visualisation de l'historique des conversations
Usage : python analysis.py
"""

import json
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import Counter
import re

HISTORY_FILE = "data/conversations.json"
OUTPUT       = "charts"

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.linestyle":    "--",
})

COLORS = {"user": "#2A9D8F", "assistant": "#457B9D"}


def load_history() -> dict:
    if not os.path.exists(HISTORY_FILE):
        raise FileNotFoundError(
            f"Aucun historique trouve. Lance d'abord : python main.py"
        )
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def flatten_messages(sessions: dict) -> list:
    """Aplati toutes les sessions en une liste de messages avec metadata."""
    messages = []
    for session_id, session in sessions.items():
        for msg in session["messages"]:
            messages.append({
                "session":  session_id,
                "date":     session["date"],
                "role":     msg["role"],
                "content":  msg["content"],
                "words":    len(msg["content"].split()),
                "length":   len(msg["content"]),
            })
    return messages


def save(fig, filename):
    os.makedirs(OUTPUT, exist_ok=True)
    path = os.path.join(OUTPUT, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"[chart] {path}")
    plt.close(fig)


def plot_message_stats(messages: list):
    user_msgs = [m for m in messages if m["role"] == "user"]
    bot_msgs  = [m for m in messages if m["role"] == "assistant"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Statistiques des conversations", fontsize=14, fontweight="bold")

    # Nombre de mots par message
    for ax, data, label, color in [
        (axes[0], [m["words"] for m in user_msgs],  "Utilisateur", COLORS["user"]),
        (axes[0], [m["words"] for m in bot_msgs],   "Assistant",   COLORS["assistant"]),
    ]:
        ax.hist(data, bins=20, alpha=0.6, color=color, label=label, edgecolor="white")
    axes[0].set_xlabel("Nombre de mots par message")
    axes[0].set_ylabel("Frequence")
    axes[0].set_title("Distribution de la longueur des messages")
    axes[0].legend()

    # Messages par session
    from collections import Counter
    session_counts = Counter(m["session"] for m in messages)
    sessions = list(session_counts.keys())
    counts   = list(session_counts.values())
    short_labels = [f"Session {i+1}" for i in range(len(sessions))]

    axes[1].bar(short_labels, counts, color=COLORS["user"], edgecolor="white", alpha=0.85)
    axes[1].set_xlabel("Session")
    axes[1].set_ylabel("Nombre de messages")
    axes[1].set_title("Messages par session")
    plt.setp(axes[1].get_xticklabels(), rotation=30, ha="right")

    fig.tight_layout()
    save(fig, "1_message_stats.png")


def plot_top_words(messages: list):
    """Mots les plus utilises par l'utilisateur."""
    stop_words = {
        "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
        "le", "la", "les", "un", "une", "des", "de", "du", "en",
        "et", "est", "que", "qui", "pour", "pas", "sur", "dans",
        "avec", "ce", "se", "si", "au", "aux", "me", "ne", "on",
        "the", "a", "an", "is", "are", "to", "of", "in", "it",
        "i", "you", "he", "she", "we", "they", "this", "that",
    }

    user_text = " ".join(m["content"] for m in messages if m["role"] == "user")
    words = re.findall(r"\b[a-zA-Zàâéèêëîïôùûüç]{3,}\b", user_text.lower())
    words = [w for w in words if w not in stop_words]
    top_words = Counter(words).most_common(20)

    if not top_words:
        print("[analysis] Pas assez de donnees pour le graphique des mots.")
        return

    words_list, counts = zip(*top_words)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(list(words_list)[::-1], list(counts)[::-1],
            color=COLORS["user"], alpha=0.85, edgecolor="white")
    ax.set_xlabel("Occurrences")
    ax.set_title("Mots les plus utilises par l'utilisateur\n(hors mots vides)",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, "2_top_words.png")


def print_summary(messages: list, sessions: dict):
    user_msgs = [m for m in messages if m["role"] == "user"]
    bot_msgs  = [m for m in messages if m["role"] == "assistant"]

    print("\n-- Resume de l'historique --------------------------------")
    print(f"Sessions totales       : {len(sessions)}")
    print(f"Messages utilisateur   : {len(user_msgs)}")
    print(f"Messages assistant     : {len(bot_msgs)}")
    print(f"Mots ecrits (user)     : {sum(m['words'] for m in user_msgs)}")
    print(f"Mots generes (bot)     : {sum(m['words'] for m in bot_msgs)}")
    if user_msgs:
        print(f"Message le + long      : {max(m['words'] for m in user_msgs)} mots")
    print("----------------------------------------------------------\n")


def run():
    print("[analysis] Chargement de l'historique...")
    sessions = load_history()
    messages = flatten_messages(sessions)
    print(f"[analysis] {len(messages)} messages charges sur {len(sessions)} session(s)\n")

    print_summary(messages, sessions)

    print("[analysis] Generation des graphiques...")
    plot_message_stats(messages)
    plot_top_words(messages)
    print(f"\n[analysis] Graphiques sauvegardes dans '{OUTPUT}/'")


if __name__ == "__main__":
    run()

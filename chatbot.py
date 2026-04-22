"""
chatbot.py - Logique principale du chatbot avec memoire de conversation
"""

import anthropic
import json
import os
from datetime import datetime
from config import MODEL, SYSTEM_PROMPT, MAX_TOKENS, MAX_HISTORY, HISTORY_FILE


class Chatbot:
    def __init__(self):
        self.client = anthropic.Anthropic()  # lit ANTHROPIC_API_KEY automatiquement
        self.history = []                    # memoire de la conversation en cours
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("data", exist_ok=True)

    # ── Envoi d'un message ────────────────────────────────────────────────────

    def send(self, user_message: str) -> str:
        # Ajouter le message de l'utilisateur a l'historique
        self.history.append({"role": "user", "content": user_message})

        # Garder uniquement les N derniers messages (fenetre glissante)
        trimmed = self.history[-MAX_HISTORY:]

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=trimmed,
        )

        assistant_message = response.content[0].text

        # Ajouter la reponse a l'historique
        self.history.append({"role": "assistant", "content": assistant_message})

        # Sauvegarder
        self._save_history()

        return assistant_message

    # ── Sauvegarde ────────────────────────────────────────────────────────────

    def _save_history(self):
        """Sauvegarde toutes les sessions dans un fichier JSON."""
        sessions = {}
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    sessions = json.load(f)
                except json.JSONDecodeError:
                    sessions = {}

        sessions[self.session_id] = {
            "date":     datetime.now().isoformat(),
            "messages": self.history,
        }

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)

    def reset(self):
        """Remet la conversation a zero (nouvelle session)."""
        self.history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        print("[chatbot] Conversation reinitialise.")

    def get_stats(self) -> dict:
        """Retourne des statistiques sur la session en cours."""
        user_msgs = [m for m in self.history if m["role"] == "user"]
        bot_msgs  = [m for m in self.history if m["role"] == "assistant"]
        return {
            "messages_utilisateur": len(user_msgs),
            "messages_bot":         len(bot_msgs),
            "mots_utilisateur":     sum(len(m["content"].split()) for m in user_msgs),
            "mots_bot":             sum(len(m["content"].split()) for m in bot_msgs),
        }

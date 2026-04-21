# config.py - Configuration du chatbot

# Modele a utiliser
MODEL = "claude-sonnet-4-6"

# Comportement du bot
SYSTEM_PROMPT = """Tu es un assistant IA utile, concis et bienveillant.
Tu reponds toujours en francais sauf si l'utilisateur ecrit dans une autre langue.
Tu es direct et tu evites les formules creuses."""

# Limites
MAX_TOKENS = 1024
MAX_HISTORY = 20       # nombre max de messages gardes en memoire
TEMPERATURE = 1        # entre 0 (deterministe) et 1 (creatif)

# Fichier de sauvegarde des conversations
HISTORY_FILE = "data/conversations.json"

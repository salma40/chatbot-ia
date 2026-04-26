# Chatbot IA avec memoire de conversation

Chatbot en ligne de commande propulse par Claude (Anthropic) — avec memoire de session, historique JSON et analyse des conversations.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Claude](https://img.shields.io/badge/Claude-Sonnet_4.6-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Fonctionnalites

- Conversation naturelle en francais (ou toute autre langue)
- Memoire de session : le bot se souvient des messages precedents
- Fenetre glissante : evite de depasser la limite de tokens
- Sauvegarde automatique de toutes les conversations en JSON
- Commandes internes : reset, stats, exit
- Analyse et visualisation de l'historique des conversations

---

## Structure du projet

```
chatbot/
│
├── main.py         # Interface en ligne de commande
├── chatbot.py      # Logique principale + memoire
├── config.py       # Parametres du bot (modele, persona, limites)
├── analysis.py     # Visualisation de l'historique
├── requirements.txt
│
├── data/
│   └── conversations.json   # Historique sauvegarde automatiquement
│
└── charts/
    ├── 1_message_stats.png
    └── 2_top_words.png
```

---

## Tutoriel complet

### Etape 1 — Verifier que Python est installe

```bash
python --version
```

Python 3.10 minimum requis. Telecharge sur https://www.python.org/downloads/ si besoin.

---

### Etape 2 — Recuperer le projet

```bash
git clone https://github.com/salma40/chatbot-ia.git
cd chatbot-ia
```

---

### Etape 3 — Installer les dependances

```bash
pip install -r requirements.txt
```

---

### Etape 4 — Obtenir une cle API Anthropic

1. Va sur https://console.anthropic.com
2. Cree un compte (un credit gratuit est offert au depart)
3. Va dans "API Keys" et cree une nouvelle cle
4. Copie la cle (elle commence par `sk-ant-...`)

---

### Etape 5 — Configurer la cle API

**Sur Mac / Linux**, dans le terminal :

```bash
export ANTHROPIC_API_KEY="sk-ant-ta-cle-ici"
```

**Sur Windows**, dans le terminal :

```cmd
set ANTHROPIC_API_KEY=sk-ant-ta-cle-ici
```

Pour ne pas avoir a le refaire a chaque fois, ajoute cette ligne dans ton fichier `.bashrc` (Mac/Linux) ou configure une variable d'environnement systeme (Windows).

---

### Etape 6 — Lancer le chatbot

```bash
python main.py
```

Tu vas voir :

```
Chatbot IA — propulse par Claude (Anthropic)
Commandes : 'exit' pour quitter | 'reset' pour nouvelle conversation | 'stats' pour les statistiques

Vous : Bonjour, explique moi ce qu'est le machine learning

Assistant : Le machine learning est une branche de l'IA ou les algorithmes
apprennent a partir de donnees plutot que d'etre explicitement programmes...
```

---

### Etape 7 — Commandes disponibles

| Commande | Action |
|----------|--------|
| `reset` | Reinitialie la conversation (nouvelle session) |
| `stats` | Affiche le nombre de messages et de mots echanges |
| `exit` | Quitte le programme |

---

### Etape 8 — Analyser les conversations

Apres avoir eu quelques echanges, tu peux visualiser l'historique :

```bash
python analysis.py
```

Cela genere deux graphiques dans `charts/` :
- Distribution de la longueur des messages
- Mots les plus utilises dans tes questions

---

### Personnaliser le chatbot

Ouvre `config.py` pour modifier le comportement :

```python
# Changer la personnalite
SYSTEM_PROMPT = """Tu es un assistant specialise en cuisine.
Tu reponds uniquement aux questions culinaires."""

# Changer le modele
MODEL = "claude-sonnet-4-6"

# Ajuster la creativite (0 = deterministe, 1 = creatif)
TEMPERATURE = 0.7

# Nombre de messages gardes en memoire
MAX_HISTORY = 20
```

---

### Problemes courants

**"ANTHROPIC_API_KEY n'est pas definie"**
Tu as oublie l'etape 5. Configure la variable d'environnement avant de lancer le chatbot.

**"anthropic.AuthenticationError"**
Ta cle API est incorrecte ou a expire. Verifie sur https://console.anthropic.com

**"ModuleNotFoundError"**
Lance `pip install -r requirements.txt`.

**Le bot ne se souvient pas de la conversation precedente**
Normal : la memoire est par session. Chaque fois que tu lances `python main.py`, c'est une nouvelle session. L'historique complet est dans `data/conversations.json`.

---

## Comment ca marche

```
Utilisateur tape un message
   -> Ajout a l'historique (liste de dicts role/content)
   -> Envoi de tout l'historique a l'API Claude
   -> Reponse ajoutee a l'historique
   -> Sauvegarde en JSON
   -> Affichage a l'utilisateur
```

La memoire de conversation fonctionne en envoyant l'integralite de l'historique a chaque appel API. Une fenetre glissante (MAX_HISTORY) evite de depasser la limite de tokens sur les longues conversations.

---

## Stack technique

- anthropic — SDK officiel Claude
- rich — Interface terminal coloree
- matplotlib — Visualisations

---

## Licence

MIT

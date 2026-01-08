# 🤖 PropFirm Tracker Bot - Bot Telegram

Bot Telegram pour suivre vos comptes de trading PropFirm avec un dashboard graphique complet.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Telegram Bot](https://img.shields.io/badge/telegram-bot-blue.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Commandes disponibles](#-commandes-disponibles)
- [Exemples](#-exemples)
- [Architecture](#-architecture)
- [Captures d'écran](#-captures-décran)
- [FAQ](#-faq)

## ✨ Fonctionnalités

### Suivi des Comptes
- 📊 **Suivi multi-comptes** - Gérez plusieurs comptes PropFirm simultanément
- 💰 **Tracking en temps réel** - Mettez à jour vos balances et equity instantanément
- 📈 **Historique complet** - Conservez l'historique de toutes vos mises à jour
- 🎯 **Calcul automatique** - P/L, Drawdown, et métriques calculés automatiquement

### PropFirms Supportées
- ✅ FTMO
- ✅ The5ers
- ✅ TopstepTrader
- ✅ OneUp Trader
- ✅ MyFundedFX
- ✅ Funded Next
- ✅ Autres PropFirms personnalisées

### Dashboard & Visualisation
- 📊 **Graphiques interactifs** - Visualisez l'évolution de vos comptes
- 📉 **Analyse du Drawdown** - Suivez votre drawdown en temps réel
- 💹 **P/L Cumulé** - Graphique de votre profit/loss cumulé
- 📈 **Comparaison multi-comptes** - Comparez vos différents comptes

### Alertes & Notifications
- ⚠️ **Alertes de Drawdown** - Recevez des alertes quand votre drawdown est trop élevé
- 🎯 **Objectifs de profit** - Définissez et suivez vos objectifs
- 🔔 **Notifications personnalisées** - Configurez vos propres alertes

### Statuts de Compte
- 🟢 **Actif** - Compte en trading actif
- 🔵 **En Challenge** - Compte en phase de challenge
- 🟡 **En Vérification** - Compte en phase de vérification
- 💰 **Financé** - Compte financé par la PropFirm
- 🔴 **Échoué** - Challenge échoué
- ✅ **Réussi** - Challenge réussi
- ⏸️ **Suspendu** - Compte temporairement suspendu

## 🛠️ Installation

### Prérequis

- Python 3.8 ou supérieur
- Un bot Telegram (créé via [@BotFather](https://t.me/botfather))
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Cloner le repository (si pas déjà fait)
git clone https://github.com/megadose/holehe.git
cd holehe

# Installer les dépendances du bot
pip install -r propfirm_bot/requirements.txt
```

### Dépendances principales

```
python-telegram-bot>=20.0
matplotlib>=3.5.0
seaborn>=0.12.0
numpy>=1.21.0
```

## ⚙️ Configuration

### 1. Créer un bot Telegram

1. Ouvrez Telegram et cherchez [@BotFather](https://t.me/botfather)
2. Envoyez `/newbot` et suivez les instructions
3. Récupérez votre **token d'API** (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Configurer le token

**Option 1: Variable d'environnement (recommandé)**

```bash
export TELEGRAM_BOT_TOKEN='votre_token_ici'
```

**Option 2: Modifier le fichier config.py**

Éditez `propfirm_bot/config.py` et remplacez:

```python
TELEGRAM_BOT_TOKEN = 'VOTRE_TOKEN_ICI'
```

### 3. Configuration avancée (optionnel)

Dans `propfirm_bot/config.py`, vous pouvez personnaliser:

```python
# Alertes
MAX_DRAWDOWN_ALERT = 10.0  # Alerte si drawdown > 10%
MIN_PROFIT_TARGET = 5.0     # Objectif de profit minimum

# Couleurs des graphiques
CHART_COLORS = {
    'profit': '#00FF00',
    'loss': '#FF0000',
    'balance': '#0099FF',
    'equity': '#FF9900',
    'drawdown': '#FF3366'
}
```

## 🚀 Utilisation

### Démarrer le bot

```bash
# Depuis le dossier racine du projet
python -m propfirm_bot.bot

# Ou avec le token en variable d'environnement
TELEGRAM_BOT_TOKEN='votre_token' python -m propfirm_bot.bot
```

### Alternative avec Python

```python
from propfirm_bot import PropFirmBot

bot = PropFirmBot(token='votre_token')
bot.run()
```

## 📱 Commandes disponibles

### Commandes de base

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/start` | Démarrer le bot | `/start` |
| `/help` | Afficher l'aide | `/help` |

### Gestion des comptes

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/add` | Ajouter un compte | `/add MonCompte 100000 FTMO` |
| `/list` | Liste de vos comptes | `/list` |
| `/status` | Statut détaillé d'un compte | `/status MonCompte` |
| `/update` | Mettre à jour un compte | `/update MonCompte 105000 105500` |
| `/delete` | Supprimer un compte | `/delete MonCompte` |

### Visualisation & Statistiques

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/dashboard` | Générer un dashboard | `/dashboard MonCompte` |
| `/stats` | Statistiques globales | `/stats` |

### Alertes

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/alert` | Configurer une alerte | `/alert MonCompte drawdown 10` |

## 📖 Exemples

### Exemple 1: Créer et suivre un compte FTMO

```
Vous: /add FTMO_Challenge1 100000 FTMO
Bot: ✅ Compte FTMO_Challenge1 créé avec succès!
     💰 Capital initial: $100,000.00
     🏢 PropFirm: FTMO
     📊 Statut: En Challenge

# Quelques jours plus tard...
Vous: /update FTMO_Challenge1 105000 105200
Bot: ✅ Compte FTMO_Challenge1 mis à jour!
     💰 Nouvelle Balance: $105,000.00
     📊 Equity: $105,200.00
     📈 P/L: +$5,000.00
     📉 Drawdown: 0.00%

# Voir le dashboard
Vous: /dashboard FTMO_Challenge1
Bot: [Envoie un graphique avec 4 visualisations]
```

### Exemple 2: Gérer plusieurs comptes

```
# Ajouter plusieurs comptes
/add FTMO_1 100000 FTMO
/add TopStep_1 50000 TOPSTEP
/add The5ers_1 20000 THE5ERS

# Voir tous les comptes
Vous: /list
Bot: 📋 Vos Comptes PropFirm:

     🔵 FTMO_1
        🏢 FTMO
        💰 $105,000.00
        📈 +5.00%
        📉 DD: 0.00%

     🔵 TopStep_1
        🏢 TopstepTrader
        💰 $52,500.00
        📈 +5.00%
        📉 DD: 0.50%

     🔵 The5ers_1
        🏢 The5ers
        💰 $19,000.00
        📉 -5.00%
        📉 DD: 5.00%

# Statistiques globales
Vous: /stats
Bot: 📊 STATISTIQUES GLOBALES
     ━━━━━━━━━━━━━━━━━━━━
     📋 Nombre de comptes: 3
     🟢 Comptes actifs: 3
     📈 En profit: 2
     📉 En perte: 1

     💰 Capital total initial: $170,000.00
     💵 Capital total actuel: $176,500.00
     📈 P/L Total: +$6,500.00 (+3.82%)

     [+ Graphique de comparaison]
```

### Exemple 3: Configurer des alertes

```
# Alerte de drawdown
Vous: /alert FTMO_1 drawdown 10
Bot: ✅ Alerte configurée pour FTMO_1
     Type: drawdown
     Seuil: 10

# Si le drawdown dépasse 10%
Vous: /update FTMO_1 90000 89500
Bot: ✅ Compte FTMO_1 mis à jour!
     💰 Nouvelle Balance: $90,000.00
     📊 Equity: $89,500.00
     📉 P/L: -$10,000.00
     📉 Drawdown: 10.00%

     ⚠️ ATTENTION: Drawdown élevé (10.00%)!
```

## 🏗️ Architecture

### Structure du projet

```
propfirm_bot/
├── __init__.py          # Package initialization
├── bot.py               # Bot Telegram principal
├── config.py            # Configuration
├── models.py            # Modèles de données
├── database.py          # Gestion SQLite
├── dashboard.py         # Génération de graphiques
└── requirements.txt     # Dépendances

Base de données:
└── propfirm_accounts.db # SQLite database (créée automatiquement)
```

### Schéma de base de données

**Table: accounts**
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER) - ID Telegram de l'utilisateur
- account_name (TEXT) - Nom du compte
- propfirm (TEXT) - PropFirm associée
- initial_balance (REAL) - Capital initial
- current_balance (REAL) - Balance actuelle
- current_equity (REAL) - Equity actuelle
- status (TEXT) - Statut du compte
- created_at (TEXT) - Date de création
- last_updated (TEXT) - Dernière mise à jour
- max_balance (REAL) - Balance maximum atteinte
- max_drawdown (REAL) - Drawdown maximum
- total_profit_loss (REAL) - P/L total

**Table: trade_history**
- id (INTEGER PRIMARY KEY)
- account_id (INTEGER) - Référence au compte
- timestamp (TEXT) - Date/heure
- balance (REAL) - Balance à ce moment
- equity (REAL) - Equity à ce moment
- profit_loss (REAL) - P/L de cette mise à jour
- drawdown (REAL) - Drawdown à ce moment
- note (TEXT) - Note optionnelle

**Table: alerts**
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER) - ID utilisateur
- account_name (TEXT) - Nom du compte
- alert_type (TEXT) - Type d'alerte
- threshold (REAL) - Seuil de déclenchement
- is_active (INTEGER) - Alerte active ou non
- created_at (TEXT) - Date de création

### Modèles de données

#### Account
Représente un compte PropFirm avec toutes ses métriques.

#### TradeHistory
Enregistre chaque mise à jour du compte.

#### PropFirmType (Enum)
- FTMO
- THE5ERS
- TOPSTEP
- ONEUP
- MYFUNDEDFX
- FUNDED_NEXT
- OTHER

#### AccountStatus (Enum)
- ACTIVE
- CHALLENGE
- VERIFICATION
- FUNDED
- FAILED
- PASSED
- SUSPENDED

## 📊 Captures d'écran

### Dashboard complet
Le dashboard génère 4 graphiques:
1. **Évolution du Balance et Equity** - Ligne temporelle montrant l'évolution
2. **Drawdown (%)** - Graphique du drawdown avec limite
3. **P/L Cumulé** - Barres colorées (vert=profit, rouge=perte)
4. **Statistiques** - Tableau récapitulatif des métriques

### Graphique de comparaison
Quand vous avez plusieurs comptes:
- Comparaison des profits/pertes en %
- Comparaison des drawdowns maximum

## 🔧 Personnalisation

### Ajouter une nouvelle PropFirm

Éditez `propfirm_bot/models.py`:

```python
class PropFirmType(Enum):
    FTMO = "FTMO"
    THE5ERS = "The5ers"
    # ... autres PropFirms
    MA_PROPFIRM = "Ma PropFirm"  # Ajoutez ici
```

### Modifier les couleurs des graphiques

Éditez `propfirm_bot/config.py`:

```python
CHART_COLORS = {
    'profit': '#00FF00',      # Vert
    'loss': '#FF0000',        # Rouge
    'balance': '#0099FF',     # Bleu
    'equity': '#FF9900',      # Orange
    'drawdown': '#FF3366'     # Rose
}
```

### Ajouter des règles de PropFirm

Dans `propfirm_bot/models.py`, classe Account:

```python
def __init__(self, ...):
    # ...
    self.profit_target = 10.0      # Objectif 10%
    self.max_daily_loss = 0.05     # Perte max journalière 5%
    self.max_total_loss = 0.10     # Perte max totale 10%
```

## ❓ FAQ

### Comment obtenir un token de bot Telegram ?

1. Cherchez [@BotFather](https://t.me/botfather) sur Telegram
2. Envoyez `/newbot`
3. Suivez les instructions
4. Récupérez votre token

### Mes données sont-elles sécurisées ?

Oui, toutes les données sont stockées localement dans une base SQLite sur votre machine. Rien n'est envoyé à des serveurs tiers (sauf Telegram pour les messages du bot).

### Puis-je utiliser le bot sur un serveur ?

Oui ! Installez le bot sur un VPS ou serveur et il fonctionnera 24/7.

### Le bot envoie-t-il des notifications automatiques ?

Actuellement, le bot répond aux commandes. Les notifications automatiques peuvent être ajoutées en programmant des vérifications périodiques.

### Combien de comptes puis-je suivre ?

Illimité ! Vous pouvez suivre autant de comptes que vous voulez.

### Puis-je partager mon bot avec d'autres ?

Chaque utilisateur Telegram aura ses propres comptes dans la base de données. Le bot est multi-utilisateurs.

### Les graphiques ne s'affichent pas

Vérifiez que matplotlib est bien installé:
```bash
pip install matplotlib seaborn
```

### Comment sauvegarder mes données ?

Sauvegardez simplement le fichier `propfirm_accounts.db` qui contient toute votre base de données.

### Puis-je exporter mes données ?

Vous pouvez accéder directement à la base SQLite avec n'importe quel outil SQLite ou ajouter une fonctionnalité d'export CSV.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Reporter des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Soumettre des pull requests

## 📝 License

Ce projet est sous licence GNU General Public License v3.0.

Construit à des fins éducatives uniquement.

## 🙏 Remerciements

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Framework pour bots Telegram
- [matplotlib](https://matplotlib.org/) - Bibliothèque de visualisation
- [SQLite](https://www.sqlite.org/) - Base de données

## 📧 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation

---

**Note**: Ce bot est un outil de suivi personnel. Il ne remplace pas une analyse professionnelle de trading et ne garantit pas le succès dans les challenges PropFirm.

**Disclaimer**: Utilisez ce bot à vos propres risques. Les auteurs ne sont pas responsables des pertes financières.

Bon trading ! 📈💰

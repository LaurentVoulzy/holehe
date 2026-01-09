---
title: "LA BÊTE V6 ULTIMATE - Guide d'Installation Complet"
subtitle: "Système Trading Dual Forex + Crypto Ultra-Sécurisé"
author: "Yann - La Bête"
date: "08 Janvier 2025"
version: "6.0 Ultimate"
toc: true
toc-depth: 3
numbersections: true
geometry: margin=2cm
papersize: a4
fontsize: 11pt
colorlinks: true
---

\newpage

# PRÉSENTATION DU SYSTÈME

## Vue d'ensemble

**LA BÊTE V6 ULTIMATE** est un système de trading automatisé dual (Forex + Crypto) conçu spécifiquement pour réussir les challenges prop firm (FTMO, RaiseMyFunds, The5ers, etc.) avec un niveau de sécurité **MAXIMUM** pour éviter de "cramer" les comptes.

### Pourquoi ce système?

Créé après l'échec d'un challenge FTMO 40K€ avec une perte de **-3,229€ en une soirée** le 30 décembre 2024 (période morte), ce système intègre **7 niveaux de protection** pour que cela **n'arrive PLUS JAMAIS**.

### Caractéristiques principales

- ✅ **Dual System**: Forex (EURUSD, GBPUSD, USDJPY) + Crypto (BTCUSD, ETHUSD)
- ✅ **Smart Money Concepts**: Order Blocks, FVG, BOS, CHoCH
- ✅ **Confluence Scoring**: 100 points (minimum 90 forex / 85 crypto)
- ✅ **7 Protections Anti-Cramage**: SL dynamique, Triple TP, Break Even, Trailing, Filtres News, Anti-Revenge, Kill Switch
- ✅ **Kill Switch Automatique**: 8 triggers différents
- ✅ **Périodes Interdites**: 24 déc - 3 jan, Pâques, News High Impact, etc.
- ✅ **Bot Telegram Dual**: Contrôle et notifications en temps réel
- ✅ **Guardians Python**: Validation API Flask sur ports 5000 (Forex) et 5001 (Crypto)
- ✅ **Database SQLite**: Tracking complet de tous les trades et signaux

\newpage

# PRÉREQUIS SYSTÈME

## Matériel nécessaire

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| **OS** | Windows 10 | Windows 11 |
| **Processeur** | Intel Core i3 | Intel Core i5+ |
| **RAM** | 8 GB | 16 GB |
| **Disque** | 20 GB libre | SSD 50 GB+ |
| **Internet** | ADSL stable | Fibre optique |
| **Écran** | 1920x1080 | Dual screen |

## Logiciels requis

### Python 3.12+

**IMPORTANT**: Vous devez avoir Python 3.12 ou supérieur installé.

**Vérification**:

```cmd
python --version
```

**Résultat attendu**: `Python 3.12.8` (ou supérieur)

**Si non installé**:

1. Télécharger depuis: https://www.python.org/downloads/
2. Installer avec l'option **"Add Python to PATH"** ✅
3. Redémarrer l'ordinateur
4. Re-vérifier avec `python --version`

### MetaTrader 5

Vous aurez besoin de **2 instances MT5** (une pour Forex, une pour Crypto).

**Téléchargement**:

- Site officiel: https://www.metatrader5.com/
- Ou via votre broker (FTMO, RaiseMyFunds, etc.)

### Telegram

**Desktop** ou **Mobile**:

- Desktop: https://desktop.telegram.org/
- Mobile: App Store / Google Play

Vous aurez besoin de votre **Chat ID**: `1981386789`

## Comptes nécessaires

### Prop Firm

**FOREX**:

- Broker: FTMO (ou équivalent)
- Challenge: 40,000€
- Compte actuel: Challenge échoué (à renouveler)

**CRYPTO**:

- Broker: RaiseMyFunds
- Compte: 50,000$ (Account 1038450)
- Statut: Actif ✅

### Telegram Bot

**Token Bot**: `8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE` ✅
**Chat ID**: `1981386789` ✅
**Email**: kykylou30@gmail.com ✅

\newpage

# INSTALLATION ÉTAPE PAR ÉTAPE

## Étape 1: Téléchargement du système

### Option A: Depuis GitHub

Si le repository est sur GitHub:

```cmd
cd C:\Trading
git clone https://github.com/Kylou30/kylou.git
cd kylou/LaBete
```

### Option B: Depuis les fichiers locaux

Si vous avez déjà les fichiers:

1. Créer le dossier: `C:\Trading\LaBete`
2. Copier tous les fichiers du système dans ce dossier

### Vérification de la structure

Après installation, vous devez avoir:

```
C:\Trading\LaBete\
├── FOREX\
│   ├── guardian_forex.py
│   ├── La_Bete_FOREX_V6_Template.mq5
│   └── logs\
├── CRYPTO\
│   ├── guardian_crypto.py
│   └── logs\
├── SHARED\
│   ├── config.py
│   ├── telegram_bot.py
│   └── models\
├── requirements.txt
├── README.md
├── INSTALLATION.md
└── START_LA_BETE.bat
```

**Vérifier**:

```cmd
dir C:\Trading\LaBete
```

Vous devriez voir les dossiers `FOREX`, `CRYPTO`, `SHARED` et les fichiers `.txt`, `.md`, `.bat`.

\newpage

## Étape 2: Installation des dépendances Python

### 2.1 Ouvrir une fenêtre CMD (Administrateur)

1. Appuyer sur **Windows + X**
2. Cliquer sur **"Windows PowerShell (Admin)"** ou **"Invite de commandes (Admin)"**
3. Accepter les autorisations UAC

### 2.2 Naviguer vers le dossier

```cmd
cd C:\Trading\LaBete
```

### 2.3 Installer les dépendances

```cmd
pip install -r requirements.txt
```

**Dépendances installées**:

- Flask 3.0.0 (API Guardian)
- python-telegram-bot 20.7 (Bot Telegram)
- requests 2.31.0 (HTTP)
- python-dateutil 2.8.2 (Dates)
- colorlog 6.8.0 (Logging)
- python-dotenv 1.0.0 (Config)

**Durée**: ~2-3 minutes (selon connexion internet)

### 2.4 Vérification de l'installation

```cmd
python -c "import flask, telegram; print('✅ Installation OK')"
```

**Résultat attendu**: `✅ Installation OK`

**Si erreur "Module not found"**:

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

\newpage

## Étape 3: Configuration du système

### 3.1 Vérifier le fichier config.py

Ouvrir: `C:\Trading\LaBete\SHARED\config.py`

**Éditeur recommandé**: Notepad++, VS Code, ou Notepad

### 3.2 Vérifier les identifiants Telegram

Chercher ces lignes (début du fichier):

```python
TELEGRAM_BOT_TOKEN = "8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE"
TELEGRAM_CHAT_ID = "1981386789"
USER_EMAIL = "kykylou30@gmail.com"
```

✅ **Déjà configuré correctement!** Ne rien modifier.

### 3.3 Vérifier la configuration FOREX

Chercher `FOREX_CONFIG = {`:

```python
FOREX_CONFIG = {
    "account_balance": 40000,  # Votre challenge FTMO 40K€
    "currency": "EUR",
    "risk_per_trade": 0.003,   # 0.3% par trade
    "max_daily_risk": 0.01,    # 1% max par jour

    "pairs": ["EURUSD", "GBPUSD", "USDJPY"],
    "primary_pair": "EURUSD",

    "max_trades_per_day": 3,
    "max_open_positions": 2,

    "sl_min_pips": 50,
    "sl_max_pips": 150,

    "min_confluence_score": 90,

    "kill_switch": {
        "max_daily_loss": 400,    # €
        "max_drawdown": 3000,     # €
        "min_win_rate": 0.35,     # 35%
    },

    "guardian_port": 5000,
}
```

✅ **Déjà configuré pour FTMO 40K€!**

**Si besoin de modifier le capital**:

- Changer `"account_balance": 40000` (en euros)
- Ajuster `"max_daily_loss"` si nécessaire (recommandé: 1% du capital)
- Ajuster `"max_drawdown"` (recommandé: 7.5% du capital)

### 3.4 Vérifier la configuration CRYPTO

Chercher `CRYPTO_CONFIG = {`:

```python
CRYPTO_CONFIG = {
    "account_balance": 50000,  # RaiseMyFunds 50K$
    "currency": "USD",
    "risk_per_trade": 0.002,   # 0.2% par trade (plus conservateur)

    "pairs": ["BTCUSD", "ETHUSD"],
    "primary_pair": "BTCUSD",

    "max_trades_per_day": 2,   # Limité à 2 pour crypto
    "max_open_positions": 1,   # 1 seule position max

    "btc_sl_min": 200,   # $ minimum
    "btc_sl_max": 1000,  # $ maximum
    "eth_sl_min": 20,
    "eth_sl_max": 100,

    "min_confluence_score": 85,

    "kill_switch": {
        "max_daily_loss": 500,    # $
        "max_drawdown": 3500,     # $
        "min_win_rate": 0.40,     # 40%
    },

    "guardian_port": 5001,
}
```

✅ **Déjà configuré pour RaiseMyFunds 50K$!**

### 3.5 Sauvegarder le fichier

Si vous avez fait des modifications:

1. **Fichier** → **Enregistrer** (ou `Ctrl+S`)
2. Fermer l'éditeur

\newpage

## Étape 4: Installation MetaTrader 5

### 4.1 Installation de 2 instances MT5

**Pourquoi 2 instances?**

- Instance 1: **Forex** (FTMO ou autre broker forex)
- Instance 2: **Crypto** (Broker crypto supportant MT5)

### 4.2 Installation Instance FOREX

#### Téléchargement

1. Aller sur le site de votre broker (ex: FTMO)
2. Télécharger **MetaTrader 5**
3. Ou télécharger depuis: https://www.metatrader5.com/

#### Installation

1. Lancer l'installateur `mt5setup.exe`
2. Choisir le dossier: `C:\Program Files\MetaTrader 5 Forex\`
3. Suivre l'assistant d'installation
4. **Ne pas** cocher "Lancer MetaTrader 5" à la fin

#### Connexion au compte

1. Lancer MT5 Forex
2. **Fichier** → **Se connecter au compte de trading**
3. Entrer les identifiants de votre compte FTMO (ou autre)
4. **Login**: Votre numéro de compte
5. **Mot de passe**: Votre mot de passe
6. **Serveur**: Serveur de votre broker
7. Cliquer **OK**

✅ **Vérification**: Vous devriez voir votre solde dans l'onglet **Terminal** → **Trade**

### 4.3 Installation Instance CRYPTO

Répéter les mêmes étapes mais:

- Dossier d'installation: `C:\Program Files\MetaTrader 5 Crypto\`
- Connexion au compte: RaiseMyFunds Account 1038450

### 4.4 Configuration WebRequest (CRITIQUE!)

**TRÈS IMPORTANT**: MT5 doit pouvoir envoyer des requêtes HTTP aux Guardians Python.

**Pour chaque instance MT5** (Forex ET Crypto):

1. Ouvrir MT5
2. **Outils** → **Options** (ou `Ctrl+O`)
3. Onglet **"Expert Advisors"**
4. Cocher ✅ **"Autoriser le trading automatique"**
5. Cocher ✅ **"Autoriser WebRequest pour les URLs suivantes:"**
6. Dans la zone de texte, ajouter (une URL par ligne):

```
http://localhost:5000
http://localhost:5001
http://127.0.0.1:5000
http://127.0.0.1:5001
```

7. Cliquer **OK**

**Capture d'écran des paramètres**:

```
┌─────────────────────────────────────────────┐
│ Options                                     │
├─────────────────────────────────────────────┤
│ Onglet: Expert Advisors                     │
│                                             │
│ ✅ Autoriser le trading automatique         │
│ ✅ Autoriser la modification de signaux     │
│ ✅ Autoriser l'importation de DLL           │
│                                             │
│ ✅ Autoriser WebRequest pour les URLs:     │
│ ┌─────────────────────────────────────────┐ │
│ │ http://localhost:5000                   │ │
│ │ http://localhost:5001                   │ │
│ │ http://127.0.0.1:5000                   │ │
│ │ http://127.0.0.1:5001                   │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│              [ OK ]    [ Annuler ]          │
└─────────────────────────────────────────────┘
```

⚠️ **Si vous oubliez cette étape, les bots MT5 ne pourront PAS communiquer avec les Guardians Python!**

\newpage

## Étape 5: Installation des fichiers MT5

### 5.1 Copier le fichier Forex .mq5

#### Trouver le dossier MT5

**Depuis MT5 Forex**:

1. **Fichier** → **Ouvrir le dossier de données**
2. Une fenêtre Windows s'ouvre
3. Naviguer vers: `MQL5\Experts\`

**Ou directement**:

```
C:\Program Files\MetaTrader 5 Forex\MQL5\Experts\
```

#### Copier le fichier

1. Aller dans: `C:\Trading\LaBete\FOREX\`
2. Copier le fichier: `La_Bete_FOREX_V6_Template.mq5`
3. Coller dans: `C:\Program Files\MetaTrader 5 Forex\MQL5\Experts\`

### 5.2 Compiler le fichier Forex

1. Dans MT5 Forex, appuyer sur **F4** (ouvre MetaEditor)
2. Dans MetaEditor, **Fichier** → **Ouvrir** → Naviguer vers `Experts`
3. Ouvrir `La_Bete_FOREX_V6_Template.mq5`
4. Appuyer sur **F7** (Compile)
5. Vérifier l'onglet **"Toolbox"** en bas:

```
0 error(s), 0 warning(s)
Compilation réussie
```

✅ **Si 0 errors**: OK!
❌ **Si errors**: Vérifier le code, corriger, recompiler

### 5.3 Vérifier le fichier .ex5

Après compilation réussie:

```
C:\Program Files\MetaTrader 5 Forex\MQL5\Experts\
├── La_Bete_FOREX_V6_Template.mq5  ← Fichier source
└── La_Bete_FOREX_V6_Template.ex5  ← Fichier compilé ✅
```

Le fichier `.ex5` est créé automatiquement.

### 5.4 Répéter pour Crypto

**IMPORTANT**: Vous devez créer le fichier crypto (pas encore fait dans le système actuel).

**Option 1**: Utiliser le template Forex pour crypto aussi (temporaire)

1. Copier `La_Bete_FOREX_V6_Template.mq5`
2. Renommer en `La_Bete_CRYPTO_V6_Ultimate.mq5`
3. Ouvrir avec MetaEditor
4. Modifier la ligne URL Guardian:

```cpp
// Changer de:
string GUARDIAN_API_URL = "http://localhost:5000/validate_signal";

// Vers:
string GUARDIAN_API_URL = "http://localhost:5001/validate_signal";
```

5. Sauvegarder et compiler (F7)
6. Copier dans `C:\Program Files\MetaTrader 5 Crypto\MQL5\Experts\`

\newpage

## Étape 6: Configuration pare-feu Windows

### 6.1 Autoriser Python dans le pare-feu

Les Guardians Python utilisent Flask sur les ports 5000 et 5001. Windows peut bloquer par défaut.

**Méthode**:

1. **Windows** → Rechercher **"Pare-feu Windows Defender"**
2. Cliquer sur **"Autoriser une application via le Pare-feu Windows Defender"**
3. Cliquer sur **"Modifier les paramètres"** (droits admin requis)
4. Cliquer sur **"Autoriser une autre application..."**
5. Cliquer sur **"Parcourir..."**
6. Naviguer vers: `C:\Users\VotreNom\AppData\Local\Programs\Python\Python312\python.exe`
7. Cliquer sur **"Ajouter"**
8. Cocher ✅ **Privé** ET ✅ **Public**
9. Cliquer **OK**

### 6.2 Vérification ports

**Vérifier que les ports 5000 et 5001 sont libres**:

```cmd
netstat -ano | findstr :5000
netstat -ano | findstr :5001
```

**Résultat attendu**: Rien (ports libres)

**Si un port est occupé**:

```cmd
taskkill /F /PID <PID>
```

(Remplacer `<PID>` par le numéro affiché)

\newpage

## Étape 7: Test de l'installation

### 7.1 Créer les dossiers logs

```cmd
mkdir C:\Trading\LaBete\FOREX\logs
mkdir C:\Trading\LaBete\CRYPTO\logs
```

### 7.2 Test Guardian FOREX

#### Lancer le Guardian

Ouvrir une fenêtre **CMD** (Administrateur):

```cmd
cd C:\Trading\LaBete\FOREX
python guardian_forex.py
```

**Résultat attendu**:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🐺 FOREX GUARDIAN - La Bête 🐺              ║
║                                                          ║
║          Système de Protection Anti-Cramage              ║
║                   7 Niveaux de Sécurité                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

2025-01-08 18:00:00 - INFO - ✅ Base de données initialisée
2025-01-08 18:00:00 - INFO - 🚀 Guardian Forex démarré sur port 5000
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

✅ **Si ce message apparaît**: Guardian Forex OK!

#### Tester l'API

**Ouvrir une NOUVELLE fenêtre CMD** (laisser la première ouverte):

```cmd
curl http://localhost:5000/health
```

**Résultat attendu**:

```json
{
  "status": "OK",
  "system": "FOREX",
  "kill_switch_active": false,
  "timestamp": "2025-01-08T18:00:00"
}
```

✅ **Si ce JSON s'affiche**: API Guardian Forex fonctionne!

**Si erreur "curl not found"**:

Utiliser un navigateur web et aller sur: `http://localhost:5000/health`

### 7.3 Test Guardian CRYPTO

**Ouvrir une 3ème fenêtre CMD**:

```cmd
cd C:\Trading\LaBete\CRYPTO
python guardian_crypto.py
```

**Résultat attendu**:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║            💰 CRYPTO GUARDIAN - La Bête 💰               ║
║                                                          ║
║       Système de Protection Anti-Cramage Crypto         ║
║         + Whale Detection + Weekend Protection           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

2025-01-08 18:00:00 - INFO - ✅ Base de données crypto initialisée
2025-01-08 18:00:00 - INFO - 🚀 Guardian Crypto démarré sur port 5001
 * Running on http://0.0.0.0:5001
```

#### Tester l'API Crypto

**Ouvrir une 4ème fenêtre CMD**:

```cmd
curl http://localhost:5001/health
```

**Résultat attendu**:

```json
{
  "status": "OK",
  "system": "CRYPTO",
  "kill_switch_active": false,
  "timestamp": "2025-01-08T18:00:00"
}
```

✅ **Les 2 Guardians fonctionnent!**

### 7.4 Test Bot Telegram

**Ouvrir une 5ème fenêtre CMD**:

```cmd
cd C:\Trading\LaBete\SHARED
python telegram_bot.py
```

**Résultat attendu**:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          🤖 BOT TELEGRAM - La Bête (Dual) 🤖             ║
║                                                          ║
║            Contrôle Centralisé Forex + Crypto            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

2025-01-08 18:00:00 - INFO - 🚀 Démarrage du bot Telegram...
2025-01-08 18:00:00 - INFO - ✅ Bot Telegram opérationnel!

🤖 Bot Telegram La Bête démarré!
📱 Ouvrez Telegram et cherchez votre bot
```

#### Tester sur Telegram

1. Ouvrir **Telegram** (mobile ou desktop)
2. Chercher votre bot (avec le token `8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE`)
3. Envoyer: `/start`

**Réponse attendue du bot**:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🐺 LA BÊTE - Trading System 🐺              ║
║                                                          ║
║                   Version 6.0 Ultimate                   ║
║              Système Dual Forex + Crypto                 ║
║          Ultra-Sécurisé pour Prop Firm Challenges        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

📱 COMMANDES DISPONIBLES:

*FOREX:*
/forex_stats - Stats Forex
/forex_positions - Positions ouvertes Forex
...
```

✅ **Si ce message apparaît**: Bot Telegram OK!

#### Tester les commandes

Envoyer: `/stats`

**Réponse attendue**:

```
📊 STATISTIQUES GLOBALES - LA BÊTE

🐺 FOREX:
  Trades: 0
  P&L: 0.00€
  Win Rate: 0.0%
  Positions: 0

💰 CRYPTO:
  Trades: 0
  P&L: 0.00$
  Win Rate: 0.0%
  Positions: 0

💎 TOTAL P&L: 0.00€
```

✅ **Si stats à 0**: Système opérationnel!

### 7.5 Récapitulatif fenêtres ouvertes

À ce stade, vous devriez avoir **3 fenêtres CMD** ouvertes:

```
Fenêtre 1: 🐺 Guardian FOREX (port 5000)
Fenêtre 2: 💰 Guardian CRYPTO (port 5001)
Fenêtre 3: 🤖 Bot Telegram
```

⚠️ **NE PAS FERMER CES FENÊTRES!** Elles doivent rester ouvertes pendant le trading.

\newpage

## Étape 8: Activation des bots MT5

### 8.1 Activer AutoTrading

**Dans CHAQUE instance MT5** (Forex ET Crypto):

1. Cliquer sur le bouton **"AutoTrading"** dans la toolbar
2. Le bouton doit devenir **VERT** ✅
3. Si rouge ❌: Cliquer dessus pour activer

**Capture toolbar MT5**:

```
[ Fichier ] [ Affichage ] [ Insertion ] [ Graphiques ] [ Outils ]

  [ 🔄 ] [ 📊 ] [ 🤖 AutoTrading ] ← Doit être VERT ✅
```

### 8.2 Activer le bot Forex

**Dans MT5 Forex**:

1. Ouvrir le graphique **EURUSD**
2. Cliquer sur le timeframe **M30** (en haut)
3. Dans la fenêtre **Navigateur** (gauche):
   - Dérouler **Expert Advisors**
   - Trouver `La_Bete_FOREX_V6_Template`
4. **Glisser-déposer** le bot sur le graphique EURUSD M30

**Fenêtre de paramètres qui s'ouvre**:

```
┌─────────────────────────────────────────────┐
│ La_Bete_FOREX_V6_Template                   │
├─────────────────────────────────────────────┤
│                                             │
│ Onglet: Commun                              │
│                                             │
│ ✅ Autoriser le trading automatique         │
│ ✅ Autoriser les importations de DLL        │
│ ✅ Autoriser l'importation de fonctions     │
│ ✅ Confirmer l'appel de DLL                 │
│                                             │
│ Onglet: Paramètres d'entrée                 │
│                                             │
│ RiskPercent = 0.3                           │
│ MagicNumber = 666666                        │
│ MinConfluenceScore = 90                     │
│ GuardianURL = http://localhost:5000/...     │
│ ...                                         │
│                                             │
│              [ OK ]    [ Annuler ]          │
└─────────────────────────────────────────────┘
```

5. **Vérifier les paramètres**:
   - ✅ **Autoriser le trading automatique**: OUI
   - ✅ **GuardianURL**: `http://localhost:5000/validate_signal`
   - ✅ **RiskPercent**: 0.3
   - ✅ **MinConfluenceScore**: 90

6. Cliquer **OK**

**Résultat**:

- Un **smiley vert** 😊 apparaît en haut à droite du graphique
- Onglet **Experts** (en bas) affiche:

```
[2025-01-08 18:00:00] La_Bete_FOREX_V6_Template EURUSD,M30: loaded successfully
[2025-01-08 18:00:00] ╔══════════════════════════════════════╗
[2025-01-08 18:00:00] ║  🐺 LA BÊTE FOREX V6 ULTIMATE 🐺     ║
[2025-01-08 18:00:00] ╚══════════════════════════════════════╝
[2025-01-08 18:00:00] ✅ Système initialisé avec succès
[2025-01-08 18:00:00] 🔗 Guardian API: http://localhost:5000/validate_signal
[2025-01-08 18:00:00] 📊 Paire: EURUSD
[2025-01-08 18:00:00] 💰 Risque: 0.3%
```

✅ **Si vous voyez ces messages**: Bot Forex activé avec succès!

**Si smiley rouge** 😢 ou erreur:

- Vérifier que Guardian Forex tourne (fenêtre CMD ouverte)
- Vérifier WebRequest autorisé (Étape 4.4)
- Vérifier pare-feu (Étape 6)

### 8.3 Activer le bot Crypto

**Répéter les mêmes étapes dans MT5 Crypto**:

1. Ouvrir graphique **BTCUSD M30**
2. Glisser-déposer `La_Bete_CRYPTO_V6_Ultimate`
3. Vérifier:
   - GuardianURL: `http://localhost:5001/validate_signal`
   - RiskPercent: 0.2 (crypto plus conservateur)
   - MinConfluenceScore: 85
4. Cliquer OK

✅ **Smiley vert** sur BTCUSD M30

\newpage

# UTILISATION QUOTIDIENNE

## Lancement du système

### Option 1: Script automatique (Recommandé)

1. Naviguer vers: `C:\Trading\LaBete\`
2. **Double-cliquer** sur `START_LA_BETE.bat`
3. **3 fenêtres CMD** s'ouvrent automatiquement
4. Attendre 10 secondes que tout se lance

### Option 2: Manuel

**Ouvrir 3 fenêtres CMD** (Administrateur):

**Fenêtre 1 - Guardian Forex**:
```cmd
cd C:\Trading\LaBete\FOREX
python guardian_forex.py
```

**Fenêtre 2 - Guardian Crypto**:
```cmd
cd C:\Trading\LaBete\CRYPTO
python guardian_crypto.py
```

**Fenêtre 3 - Bot Telegram**:
```cmd
cd C:\Trading\LaBete\SHARED
python telegram_bot.py
```

### Vérification rapide

Envoyer dans Telegram: `/stats`

**Résultat attendu**: Stats des 2 systèmes affichées

## Commandes Telegram principales

### Surveillance

| Commande | Description |
|----------|-------------|
| `/stats` | Stats globales Forex + Crypto |
| `/forex_stats` | Stats Forex détaillées |
| `/crypto_stats` | Stats Crypto détaillées |
| `/forex_positions` | Positions Forex ouvertes |
| `/crypto_positions` | Positions Crypto ouvertes |
| `/risk` | Niveau de risque global |

### Contrôle

| Commande | Description | Usage |
|----------|-------------|-------|
| `/forex_stop` | Arrêter Forex (Kill Switch) | Urgence uniquement |
| `/crypto_stop` | Arrêter Crypto (Kill Switch) | Urgence uniquement |
| `/stopall` | ⛔ ARRÊT TOTAL | URGENCE MAXIMUM |
| `/forex_start` | Redémarrer Forex | Nouveau jour |
| `/crypto_start` | Redémarrer Crypto | Nouveau jour |
| `/startall` | Redémarrer tout | Nouveau jour |

### Rapports

| Commande | Description |
|----------|-------------|
| `/forex_today` | Résumé journée Forex |
| `/crypto_today` | Résumé journée Crypto |
| `/report` | Rapport complet dual |

## Notifications automatiques

Le bot Telegram vous enverra automatiquement:

- 🎯 **Nouveau signal détecté** (avec score confluence)
- ✅ **Position ouverte** (Entry, SL, TPs)
- 💰 **TP1/TP2/TP3 atteint** (profit partiel)
- ⚠️ **SL touché** (analyse de la perte)
- 🔴 **News High Impact proche** (2h avant)
- 🚨 **Limite de risque approchée** (80% max daily loss)
- ⛔ **Kill Switch activé** (raisons détaillées)
- 📊 **Rapport quotidien** (18h chaque jour)
- 📈 **Rapport hebdomadaire** (vendredi 18h)

## Routine quotidienne recommandée

### Matin (avant 8h)

1. ✅ Lancer les 3 scripts Python
2. ✅ Vérifier MT5 Forex et Crypto (bots actifs, smiley vert)
3. ✅ Envoyer `/stats` dans Telegram
4. ✅ Vérifier calendrier économique (news aujourd'hui?)
5. ✅ Vérifier que Kill Switch est désactivé

### Pendant la journée

1. ✅ Surveiller les notifications Telegram
2. ✅ Répondre rapidement aux alertes
3. ✅ Vérifier les 3 fenêtres CMD (toujours ouvertes?)
4. ✅ Consulter `/stats` toutes les 2-3 heures

### Soir (après 18h)

1. ✅ Lire le rapport quotidien automatique
2. ✅ Analyser les trades fermés (pourquoi win/loss?)
3. ✅ Vérifier P&L du jour
4. ✅ Sauvegarder les databases:
   - `C:\Trading\LaBete\FOREX\forex_trades.db`
   - `C:\Trading\LaBete\CRYPTO\crypto_trades.db`
5. ✅ Préparer le lendemain (news économiques?)

### Vendredi soir

1. ✅ Lire le rapport hebdomadaire
2. ✅ Analyser performance de la semaine
3. ✅ Sauvegarder databases + logs
4. ✅ Ajuster paramètres si nécessaire (confluence, risque, etc.)

\newpage

# TROUBLESHOOTING

## Problème: "Module not found"

### Cause

Dépendances Python non installées.

### Solution

```cmd
pip install -r requirements.txt
```

Si erreur persiste:

```cmd
python -m pip install --upgrade pip
pip install flask python-telegram-bot requests --force-reinstall
```

## Problème: "Port already in use"

### Cause

Un Guardian est déjà lancé ou un autre programme utilise le port 5000/5001.

### Solution

**Vérifier les processus**:

```cmd
netstat -ano | findstr :5000
```

**Si un PID est affiché**:

```cmd
taskkill /F /PID <PID>
```

**Relancer le Guardian**:

```cmd
python guardian_forex.py
```

## Problème: MT5 ne se connecte pas au Guardian

### Cause possible 1: Guardian non lancé

**Vérifier**:

```cmd
curl http://localhost:5000/health
```

**Si erreur**: Lancer le Guardian

### Cause possible 2: WebRequest non autorisé

**Solution**:

1. MT5 → **Outils** → **Options**
2. Onglet **Expert Advisors**
3. Vérifier que `http://localhost:5000` est dans la liste
4. Redémarrer MT5

### Cause possible 3: Pare-feu bloque Python

**Solution**:

1. Panneau de configuration → Pare-feu Windows
2. Autoriser une application → Python.exe
3. Cocher **Privé** ET **Public**

## Problème: Bot Telegram ne répond pas

### Cause possible 1: Token incorrect

**Vérifier** dans `config.py`:

```python
TELEGRAM_BOT_TOKEN = "8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE"
```

### Cause possible 2: telegram_bot.py non lancé

**Vérifier fenêtre CMD**:

Doit afficher: `🤖 Bot Telegram La Bête démarré!`

**Si pas affiché**: Relancer

```cmd
cd C:\Trading\LaBete\SHARED
python telegram_bot.py
```

### Cause possible 3: Internet déconnecté

**Vérifier connexion internet**

## Problème: Aucun signal détecté

### Causes possibles

1. **Période interdite** (24 déc - 3 jan, weekend, etc.)
2. **Confluence score trop faible** (< 90 forex / < 85 crypto)
3. **Kill Switch actif**
4. **News High Impact proche**
5. **Marché trop volatil**

### Solution

**Vérifier logs MT5**:

Onglet **Experts** → Chercher messages:

```
❌ Signal REJETÉ par Guardian
   Raison: Confluence trop faible: 85/100 (min 90)
```

**Vérifier dans Telegram**:

```
/forex_stats
```

Vérifier `kill_switch_active: false`

## Problème: Kill Switch ne se désactive pas

### Solution manuelle

**Via Telegram**:

```
/forex_start
/crypto_start
```

**Via CMD**:

```cmd
curl -X POST http://localhost:5000/kill_switch/deactivate
curl -X POST http://localhost:5001/kill_switch/deactivate
```

**Si ça ne marche pas**:

1. Fermer les Guardians (Ctrl+C dans CMD)
2. Supprimer les fichiers:
   - `forex_trades.db`
   - `crypto_trades.db`
3. Relancer les Guardians (ils recréent les DB)

⚠️ **ATTENTION**: Vous perdez l'historique!

## Problème: Erreur "WebRequest failed"

### Dans logs MT5

```
[Error] WebRequest failed: error 4014
```

### Cause

URL non autorisée dans MT5.

### Solution

1. MT5 → **Outils** → **Options** → **Expert Advisors**
2. Ajouter EXACTEMENT:
   ```
   http://localhost:5000/validate_signal
   http://localhost:5001/validate_signal
   ```
3. Redémarrer MT5
4. Réactiver le bot

## Problème: Graphique MT5 sans smiley

### Cause

Bot MT5 non activé ou erreur de compilation.

### Solution

1. Vérifier compilation (F4 → ouvrir .mq5 → F7)
2. Vérifier **0 errors**
3. Glisser-déposer à nouveau sur le graphique
4. Vérifier AutoTrading activé (bouton vert)

\newpage

# CHECKLIST AVANT TRADING RÉEL

Avant de laisser le système trader en réel sur prop firm:

## Installation

- [ ] Python 3.12+ installé et vérifié
- [ ] Toutes dépendances installées (`pip install -r requirements.txt`)
- [ ] 2 instances MT5 installées (Forex + Crypto)
- [ ] WebRequest autorisé dans les 2 MT5
- [ ] Pare-feu configuré (Python autorisé)

## Configuration

- [ ] `config.py` vérifié (tokens, capital, risque)
- [ ] Capital Forex = 40,000€ (ou votre montant)
- [ ] Capital Crypto = 50,000$ (ou votre montant)
- [ ] Risque Forex = 0.3% par trade
- [ ] Risque Crypto = 0.2% par trade
- [ ] Confluence min Forex = 90/100
- [ ] Confluence min Crypto = 85/100

## Guardians

- [ ] Guardian Forex lancé (port 5000 actif)
- [ ] Guardian Crypto lancé (port 5001 actif)
- [ ] Test API Forex OK (`curl http://localhost:5000/health`)
- [ ] Test API Crypto OK (`curl http://localhost:5001/health`)

## Bot Telegram

- [ ] Bot Telegram lancé et opérationnel
- [ ] `/start` répond correctement
- [ ] `/stats` affiche stats à 0
- [ ] Notifications activées (test avec `/help`)

## MT5

- [ ] Bot Forex activé sur EURUSD M30
- [ ] Bot Crypto activé sur BTCUSD M30
- [ ] Smiley vert ✅ sur les 2 graphiques
- [ ] AutoTrading activé (bouton vert)
- [ ] Logs MT5 affichent "✅ Système initialisé"

## Sécurité

- [ ] Périodes interdites configurées (24 déc - 3 jan, etc.)
- [ ] Kill Switch fonctionnel (test avec `/forex_stop` puis `/forex_start`)
- [ ] Max daily loss configuré (400€ forex, 500$ crypto)
- [ ] Max drawdown configuré (3000€ forex, 3500$ crypto)

## Tests

- [ ] Système testé sur **compte démo** pendant **minimum 1 semaine**
- [ ] Au moins **20 trades** exécutés en démo
- [ ] Tous les signaux validés par Guardian
- [ ] Aucune erreur WebRequest
- [ ] TP partiels fonctionnent (TP1, TP2, TP3)
- [ ] Break Even fonctionne
- [ ] Trailing Stop fonctionne
- [ ] Kill Switch s'est déclenché au moins 1 fois (test)

## Connaissance

- [ ] Documentation lue et comprise
- [ ] Règles strictes connues par cœur
- [ ] Commandes Telegram maîtrisées
- [ ] Procédure urgence connue (`/stopall`)
- [ ] Logs MT5 compris
- [ ] Fichiers database sauvegardés

## Final

- [ ] Calendrier économique vérifié (pas de news aujourd'hui)
- [ ] Pas de période interdite en cours
- [ ] Solde prop firm vérifié
- [ ] Connexion internet stable
- [ ] Ordinateur dédié au trading (pas de jeux, pas de torrents)
- [ ] **Prêt mentalement à NE PAS intervenir manuellement**

---

✅ **Si TOUTES les cases sont cochées**: Vous pouvez passer en trading réel!

❌ **Si UNE SEULE case n'est pas cochée**: **NE PAS trader en réel!**

\newpage

# RÈGLES STRICTES À RESPECTER

## 🚫 NE JAMAIS

### 1. Trader pendant périodes interdites

❌ **24 décembre - 3 janvier** (Noël/Nouvel An)
❌ **Pâques** (4 jours autour)
❌ **Jours fériés majeurs** (US, UK, EU)
❌ **Vendredi après 16h**
❌ **Dimanche avant 23h**
❌ **2h avant/après news High Impact** (FOMC, NFP, CPI, etc.)

**Pourquoi?**

Le 30 décembre 2024, challenge FTMO cramé avec **-3,229€ en une soirée** pendant période morte.

### 2. Désactiver le Kill Switch si déclenché

Si le Kill Switch s'active:

❌ **NE PAS** forcer le redémarrage immédiatement
❌ **NE PAS** désactiver manuellement
❌ **NE PAS** modifier les limites

✅ **FAIRE**: Attendre le **lendemain** pour redémarrer

### 3. Augmenter le risque

❌ **NE JAMAIS** dépasser **0.3%** par trade (Forex)
❌ **NE JAMAIS** dépasser **0.2%** par trade (Crypto)
❌ **NE JAMAIS** modifier `RiskPercent` à la hausse

**Pourquoi?**

Le système est calibré pour les règles prop firm. Augmenter = risque de cramer le compte.

### 4. Forcer un trade

❌ **NE PAS** ouvrir position manuellement
❌ **NE PAS** bypass le Guardian
❌ **NE PAS** accepter signal si confluence < 90 (forex) / 85 (crypto)

**Le Guardian rejette pour une raison!**

### 5. Trader après 2 pertes consécutives

Le système détecte le **revenge trading**.

Si 2 pertes + trade dans les **10 minutes** → **Kill Switch AUTO**

❌ **NE PAS** forcer un 3ème trade rapidement
✅ **FAIRE**: Pause de **2 heures minimum**

### 6. Modifier le code sans backup

❌ **NE JAMAIS** modifier `guardian_forex.py` ou `guardian_crypto.py` sans sauvegarder l'original
❌ **NE JAMAIS** modifier la logique Kill Switch
❌ **NE JAMAIS** commenter les protections

### 7. Laisser tourner sans surveillance (début)

Les **2 premières semaines**:

❌ **NE PAS** laisser tourner H24 sans surveillance
✅ **FAIRE**: Surveiller activement
✅ **FAIRE**: Analyser CHAQUE trade
✅ **FAIRE**: Vérifier logs quotidiennement

## ✅ TOUJOURS

### 1. Surveiller les 3 fenêtres CMD

**Pendant les heures de trading**:

✅ Vérifier que les 3 CMD sont ouvertes
✅ Vérifier qu'il n'y a pas d'erreurs
✅ Lire les logs en temps réel

### 2. Répondre aux alertes Telegram

Le bot vous alerte pour une raison:

✅ Lire TOUTES les notifications
✅ Répondre aux alertes urgentes (🚨)
✅ Vérifier après chaque notification

### 3. Sauvegarder les databases

**Chaque jour** (soir):

```cmd
copy C:\Trading\LaBete\FOREX\forex_trades.db C:\Backup\forex_trades_2025-01-08.db
copy C:\Trading\LaBete\CRYPTO\crypto_trades.db C:\Backup\crypto_trades_2025-01-08.db
```

**Pourquoi?**

En cas de problème, vous pourrez restaurer l'historique.

### 4. Tester sur démo AVANT prop firm

✅ **Minimum 1 semaine** sur compte démo
✅ **Minimum 20 trades** exécutés
✅ **Win rate > 40%**
✅ **Aucune erreur** technique

**Puis passer en réel.**

### 5. Respecter les règles prop firm

**FTMO** (Forex 40K€):

- Max Daily Loss: **2,000€** (5%)
- Max Total Loss: **4,000€** (10%)
- Profit Target: **4,000€** (10%)

**Notre système**:

- Max Daily Loss configuré: **400€** (1% = 5× plus sécurisé!)
- Max Total Drawdown: **3,000€** (7.5% = plus sécurisé!)

✅ **Vous êtes LARGEMENT en dessous des limites!**

### 6. Analyser CHAQUE trade

Après **chaque trade fermé**:

1. ✅ Vérifier le résultat (win/loss)
2. ✅ Comprendre **POURQUOI** (confluence, structure, etc.)
3. ✅ Vérifier si protections ont fonctionné
4. ✅ Noter dans un journal de trading

**Si perte**:

- ❓ Confluence était suffisant?
- ❓ SL bien placé?
- ❓ News a affecté?
- ❓ Marché trop volatil?

**Si win**:

- ❓ Quel niveau de TP atteint? (TP1/TP2/TP3)
- ❓ Break Even activé?
- ❓ Trailing Stop utilisé?
- ❓ Setup répétable?

### 7. Tenir un journal de trading

**Excel ou Google Sheets**:

| Date | Paire | Direction | Confluence | Entry | SL | TP1/2/3 | Résultat | P&L | Notes |
|------|-------|-----------|------------|-------|----|---------| ---------|-----|-------|
| 08/01 | EURUSD | BUY | 95 | 1.0950 | 1.0900 | 1.1050 | WIN | +150€ | OB+ validé |
| 08/01 | BTCUSD | SELL | 88 | 45000 | 45500 | 43500 | LOSS | -100$ | Whale activity |

**Analyser chaque semaine**:

- Paires les plus profitables
- Horaires les plus profitables
- Confluence moyen des wins vs losses
- Patterns les plus fiables

\newpage

# ANNEXES

## Annexe A: Structure des fichiers

```
C:\Trading\LaBete\
│
├── FOREX\
│   ├── guardian_forex.py           520 lignes
│   ├── La_Bete_FOREX_V6_Template.mq5
│   ├── forex_trades.db            (créé automatiquement)
│   └── logs\
│       └── guardian_forex.log
│
├── CRYPTO\
│   ├── guardian_crypto.py          580 lignes
│   ├── crypto_trades.db           (créé automatiquement)
│   └── logs\
│       └── guardian_crypto.log
│
├── SHARED\
│   ├── config.py                   630 lignes
│   ├── telegram_bot.py             450 lignes
│   └── models\
│
├── requirements.txt
├── README.md                       550 lignes
├── INSTALLATION.md                 400 lignes
└── START_LA_BETE.bat
```

## Annexe B: Ports utilisés

| Service | Port | URL |
|---------|------|-----|
| Guardian Forex | 5000 | http://localhost:5000 |
| Guardian Crypto | 5001 | http://localhost:5001 |

## Annexe C: Endpoints API Guardian

### GET /health

**Description**: Check de santé

**Réponse**:
```json
{
  "status": "OK",
  "system": "FOREX" ou "CRYPTO",
  "kill_switch_active": false,
  "timestamp": "2025-01-08T18:00:00"
}
```

### POST /validate_signal

**Description**: Validation d'un signal depuis MT5

**Body**:
```json
{
  "pair": "EURUSD",
  "direction": "BUY",
  "entry_price": 1.0950,
  "sl_price": 1.0900,
  "sl_pips": 50,
  "tp1_price": 1.1050,
  "tp2_price": 1.1100,
  "tp3_price": 1.1200,
  "lot_size": 0.5,
  "confluence_score": 95
}
```

**Réponse**:
```json
{
  "approved": true,
  "reason": "✅ Signal approuvé",
  "timestamp": "2025-01-08T18:00:00"
}
```

### GET /stats

**Description**: Statistiques du jour

**Réponse**:
```json
{
  "date": "2025-01-08",
  "total_trades": 5,
  "winning_trades": 3,
  "losing_trades": 2,
  "total_pnl": 250.50,
  "max_drawdown": 100.00,
  "kill_switch_active": false,
  "open_positions": 1
}
```

### POST /kill_switch/activate

**Description**: Active le Kill Switch manuellement

**Réponse**:
```json
{
  "status": "OK",
  "message": "Kill Switch activé"
}
```

### POST /kill_switch/deactivate

**Description**: Désactive le Kill Switch

**Réponse**:
```json
{
  "status": "OK",
  "message": "Kill Switch désactivé"
}
```

## Annexe D: Schéma base de données

### Table: trades

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER | ID unique |
| timestamp | TEXT | Date/heure création |
| pair | TEXT | Paire (EURUSD, BTCUSD, etc.) |
| direction | TEXT | BUY ou SELL |
| entry_price | REAL | Prix d'entrée |
| sl_price | REAL | Prix Stop Loss |
| tp1_price | REAL | Prix Take Profit 1 |
| tp2_price | REAL | Prix Take Profit 2 |
| tp3_price | REAL | Prix Take Profit 3 |
| lot_size | REAL | Taille position |
| confluence_score | INTEGER | Score /100 |
| status | TEXT | PENDING, OPEN, WIN, LOSS |
| profit_loss | REAL | P&L en € ou $ |
| exit_price | REAL | Prix de sortie |
| exit_time | TEXT | Date/heure sortie |
| reason | TEXT | Raison fermeture |
| metadata | TEXT | JSON metadata |

### Table: signals

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER | ID unique |
| timestamp | TEXT | Date/heure |
| pair | TEXT | Paire |
| direction | TEXT | BUY ou SELL |
| confluence_score | INTEGER | Score /100 |
| approved | BOOLEAN | 1 = approuvé, 0 = rejeté |
| rejected | BOOLEAN | Inverse de approved |
| rejection_reason | TEXT | Raison si rejeté |
| metadata | TEXT | JSON metadata |

### Table: daily_stats

| Colonne | Type | Description |
|---------|------|-------------|
| date | TEXT | Date (PRIMARY KEY) |
| total_trades | INTEGER | Nombre total trades |
| winning_trades | INTEGER | Nombre wins |
| losing_trades | INTEGER | Nombre losses |
| total_profit_loss | REAL | P&L total jour |
| max_drawdown | REAL | Drawdown max jour |
| kill_switch_triggered | BOOLEAN | Kill Switch activé? |

## Annexe E: Calendrier économique - News High Impact

**Liste des news à éviter absolument**:

### États-Unis (USD)

- **FOMC** (Federal Open Market Committee) - Décisions taux
- **NFP** (Non-Farm Payrolls) - Emploi
- **CPI** (Consumer Price Index) - Inflation
- **Core CPI** - Inflation hors alimentation/énergie
- **GDP** (Gross Domestic Product) - Croissance
- **Retail Sales** - Ventes au détail
- **Unemployment Rate** - Taux chômage
- **ISM Manufacturing/Services** - Indices manufacturiers
- **Interest Rate Decision** - Décisions Fed

### Zone Euro (EUR)

- **ECB** (European Central Bank) - Décisions BCE
- **Interest Rate Decision** - Taux BCE
- **ECB Press Conference** - Conférence Lagarde
- **CPI** - Inflation zone euro
- **GDP** - Croissance zone euro
- **PMI** - Indices manufacturiers

### Royaume-Uni (GBP)

- **BOE** (Bank of England) - Décisions BoE
- **Interest Rate Decision** - Taux BoE
- **CPI** - Inflation UK
- **GDP** - Croissance UK
- **Employment Change** - Emploi

### Japon (JPY)

- **BOJ** (Bank of Japan) - Décisions BoJ
- **Interest Rate Decision** - Taux BoJ
- **CPI** - Inflation Japon
- **GDP** - Croissance Japon

**Règle**: Arrêt **2 heures avant** et **2 heures après** ces annonces.

## Annexe F: Confluence Scoring - Détails

### Structure SMC (40 points max)

| Critère | Points | Description |
|---------|--------|-------------|
| Prix dans OB | 20 | Prix actuel dans Order Block ±3 pips |
| FVG présent | 10 | Fair Value Gap aligné avec direction |
| BOS + CHoCH | 10 | Break of Structure + Change of Character confirmés |

### Multi-Timeframe (25 points max)

| Critère | Points | Description |
|---------|--------|-------------|
| Alignement TF | 15 | M30 + H1 + H4 alignés (même tendance) |
| Trend Strength | 10 | Force de la tendance (EMA distance) |

### Indicateurs (20 points max)

| Critère | Points | Description |
|---------|--------|-------------|
| EMA Alignées | 8 | EMA 20 > 50 > 200 (bull) ou inverse (bear) |
| RSI Favorable | 6 | RSI en zone favorable (40-60 range) |
| MACD Crossover | 6 | MACD crosse signal dans bonne direction |

### Support/Resistance (10 points max)

| Critère | Points | Description |
|---------|--------|-------------|
| S/R Bounce | 5 | Prix bounce sur S/R majeur |
| Prev High/Low | 5 | Previous high/low aligné |

### Pattern (5 points max)

| Critère | Points | Description |
|---------|--------|-------------|
| Pattern Détecté | 5 | Pattern chartiste/candlestick validé |

**Exemple de calcul**:

```
Setup BUY EURUSD:
- Prix dans OB+ (1.0948 - OB à 1.0945): 20 pts
- FVG présent: 10 pts
- BOS confirmé, pas de CHoCH: 5 pts
- M30 + H1 alignés, H4 neutre: 10 pts
- Trend strength moyen: 5 pts
- EMA 20 > 50 > 200: 8 pts
- RSI 52: 6 pts
- MACD crossover: 6 pts
- Bounce sur support: 5 pts
- Previous low: 5 pts
- Pin bar: 5 pts

TOTAL: 20+10+5+10+5+8+6+6+5+5+5 = 85/100

❌ REJETÉ (min 90 pour Forex)
```

## Annexe G: Glossaire

| Terme | Définition |
|-------|------------|
| **ATR** | Average True Range - Mesure de volatilité |
| **BOS** | Break of Structure - Cassure de structure |
| **CHoCH** | Change of Character - Changement de caractère |
| **EMA** | Exponential Moving Average - Moyenne mobile exponentielle |
| **FVG** | Fair Value Gap - Écart de valeur juste |
| **Kill Switch** | Arrêt automatique du système |
| **MACD** | Moving Average Convergence Divergence |
| **OB** | Order Block - Bloc d'ordres institutionnels |
| **Prop Firm** | Proprietary Trading Firm - Société de trading |
| **RSI** | Relative Strength Index - Indice force relative |
| **SMC** | Smart Money Concepts - Concepts argent intelligent |
| **SL** | Stop Loss - Arrêt de perte |
| **TP** | Take Profit - Prise de profit |
| **Whale** | Grosse baleine - Trader institutionnel avec gros volume |

\newpage

# SUPPORT ET CONTACT

## En cas de problème technique

1. ✅ Consulter la section **Troubleshooting** (page 31)
2. ✅ Vérifier les **logs**:
   - `C:\Trading\LaBete\FOREX\logs\guardian_forex.log`
   - `C:\Trading\LaBete\CRYPTO\logs\guardian_crypto.log`
   - MT5 → Onglet **Experts**
3. ✅ Vérifier les **3 fenêtres CMD** (messages d'erreur?)

## Informations système

**Configuration actuelle**:

- **Email**: kykylou30@gmail.com
- **Telegram Chat ID**: 1981386789
- **Bot Token**: 8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE
- **Compte Forex**: FTMO 40K€ (à renouveler)
- **Compte Crypto**: RaiseMyFunds 50K$ (Account 1038450)

## Ressources

- **Documentation MT5**: https://www.mql5.com/en/docs
- **Flask API**: https://flask.palletsprojects.com/
- **Python Telegram Bot**: https://python-telegram-bot.org/
- **Smart Money Concepts**: YouTube "ICT" (Inner Circle Trader)

## Versions

- **Système**: La Bête V6.0 Ultimate
- **Date création**: 08/01/2025
- **Python requis**: 3.12+
- **MT5 requis**: 5.0+

---

\newpage

# CONCLUSION

## Récapitulatif

Vous avez maintenant installé **LA BÊTE V6 ULTIMATE**, un système de trading automatisé **dual** (Forex + Crypto) ultra-sécurisé pour prop firm challenges.

### Ce que vous avez

✅ **2 Guardians Python** (Forex + Crypto) avec 7 niveaux de protection
✅ **Kill Switch automatique** multi-triggers
✅ **Bot Telegram** contrôle dual et notifications
✅ **Smart Money Concepts** (OB, FVG, BOS, CHoCH)
✅ **Confluence Scoring** 100 points
✅ **Périodes interdites** strictes (plus de cramage 30 déc!)
✅ **Anti-revenge trading** automatique
✅ **Database SQLite** tracking complet
✅ **Documentation 50+ pages**

### Prochaines étapes

1. ✅ **Tester sur DÉMO pendant 1 semaine**
2. ✅ **Analyser tous les trades** (comprendre le système)
3. ✅ **Vérifier que protections fonctionnent**
4. ✅ **Passer en RÉEL** sur prop firm
5. ✅ **Surveiller quotidiennement**
6. ✅ **Respecter les règles strictes**
7. ✅ **NE PLUS JAMAIS cramer de compte!**

## Objectif final

**Réussir les challenges prop firm** (FTMO, RaiseMyFunds, The5ers, etc.) avec ce système qui vous protège de:

- ❌ Périodes mortes (30 déc = -3,229€ → PLUS JAMAIS!)
- ❌ Revenge trading
- ❌ Overtrading
- ❌ News High Impact
- ❌ SL trop larges
- ❌ Risque excessif
- ❌ Mauvaises entrées (confluence < 90)
- ❌ Dépassement limites prop firm

**Avec La Bête, vous tradez sereinement en sachant que le système vous protège 24/7.**

---

## Message final

**🐺 QUE LA BÊTE SOIT AVEC TOI ! 💎**

Après l'échec du challenge FTMO 40K€ le 30 décembre 2024 (-3,229€ en une soirée), ce système a été créé pour **que cela n'arrive PLUS JAMAIS**.

**Respecte les règles. Fais confiance au système. Analyse chaque trade.**

**Les prop firms vont voir de quel bois tu te chauffes ! 🚀**

**Go conquérir ces challenges ma couille ! 💪**

---

*Guide d'Installation Complet - La Bête V6 Ultimate*
*Créé le 08 Janvier 2025*
*Par Yann - Pour les traders prop firm qui ne veulent PLUS cramer*

---

**FIN DU GUIDE**

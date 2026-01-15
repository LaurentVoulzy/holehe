# 🐺 LA BÊTE - SYSTÈME PROP FIRM PROFESSIONNEL

**Système de trading automatisé V8 organisé par devise avec contrôle Telegram**

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![MT5](https://img.shields.io/badge/MT5-5.0-green.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![FTMO](https://img.shields.io/badge/FTMO-Ready-green.svg)

---

## ⚡ DÉMARRAGE RAPIDE

### 1. Double-cliquez sur `START_SYSTEM.bat`

### 2. Choisissez option [4] TOUT

### 3. Ouvrez Telegram et tapez `/start`

### 4. Chargez les bots sur MT5:

| Bot | Paire | Timeframe | Magic |
|-----|-------|-----------|-------|
| **La_Bete_EUR.mq5** | EURUSD | M30 | 666001 |
| **La_Bete_GBP.mq5** | GBPUSD | M30 | 666002 |
| **La_Bete_JPY.mq5** | USDJPY | M30 | 666003 |
| **La_Bete_GOLD.mq5** | XAUUSD | M30 | 666004 |
| **La_Bete_BTC.mq5** | BTCUSD | M30 | 777001 |
| **La_Bete_ETH.mq5** | ETHUSD | M30 | 777002 |

---

## 📱 CONTRÔLE TELEGRAM

### Menu Principal

```
╔════════════════════════════════════╗
║   🐺 LA BÊTE - PROP FIRM SYSTEM   ║
╚════════════════════════════════════╝

📱 CONTRÔLE PAR DEVISE

[🇪🇺 EUR/USD]  [🇬🇧 GBP/USD]
[🇯🇵 USD/JPY]  [🥇 GOLD]
[₿ BTC/USD]    [Ξ ETH/USD]

[📊 Vue Globale]  [⚙️ Contrôle Total]
```

### Commandes Rapides

- `/eur` - Menu EUR/USD
- `/gbp` - Menu GBP/USD
- `/jpy` - Menu USD/JPY
- `/gold` - Menu GOLD
- `/btc` - Menu BTC/USD
- `/eth` - Menu ETH/USD

### Par Devise - Menu Complet

```
🇪🇺 EUR/USD

Magic Number: 666001
Type: FOREX

[📊 Stats]        [📈 Positions]
[✅ Start]        [❌ Stop]
[🔍 Analyse]      [📅 News]

[⬅️ Retour]
```

Chaque devise a:
- **📊 Stats** - Performance en temps réel
- **📈 Positions** - Positions ouvertes
- **✅ Start** - Activer le bot
- **❌ Stop** - Désactiver le bot
- **🔍 Analyse** - Confluence + Certitude actuels
- **📅 News** - Calendrier économique

---

## 🎯 ARCHITECTURE SYSTÈME

### Structure

```
6 Bots Spécialisés MT5
    ↓
Guardian FOREX (port 5000)
Guardian CRYPTO (port 5001)
    ↓
Telegram Bot Pro (Interface)
    ↓
YOU (Contrôle total depuis mobile)
```

### Stratégie Complète

✅ **EMA Crossover** (Golden/Death Cross 20×200)
✅ **Smart Money Concepts** (Order Blocks, FVG, BOS, CHoCH)
✅ **Confluence Scoring** /100
✅ **Certainty Percentage** pour chaque trade
✅ **Dynamic ATR SL/TP** (NO fixed %)
✅ **Triple TP** (50%/30%/20% partial closes)
✅ **Break Even** automatique (50% to TP1)
✅ **Trailing Stop** ATR-based (après TP1)
✅ **Economic Calendar** Forex Factory scraping

### Paramètres par Devise

| Devise | ATR Mult | SL Range | Risque | Confluence Min | Guardian |
|--------|----------|----------|--------|----------------|----------|
| **EUR** | ×1.5 | 50-80 pips | 0.3% | 90% | :5000 |
| **GBP** | ×1.8 | 80-120 pips | 0.3% | 90% | :5000 |
| **JPY** | ×1.3 | 40-60 pips | 0.3% | 90% | :5000 |
| **GOLD** | ×2.5 | 200-800 pips | **0.25%** | 90% | :5000 |
| **BTC** | ×2.0 | 500-1500 pips | 0.3% | **85%** | :5001 |
| **ETH** | ×2.0 | 80-200 pips | 0.3% | **85%** | :5001 |

**Chaque bot adapté à la volatilité de sa paire!**

---

## 📁 STRUCTURE FICHIERS

```
LaBete/
│
├── FOREX/                   # Système Forex
│   ├── La_Bete_EUR.mq5     # Bot EUR/USD (1073 lignes)
│   ├── La_Bete_GBP.mq5     # Bot GBP/USD
│   ├── La_Bete_JPY.mq5     # Bot USD/JPY
│   ├── La_Bete_GOLD.mq5    # Bot XAU/USD
│   └── guardian_forex.py   # Guardian API (port 5000)
│
├── CRYPTO/                  # Système Crypto
│   ├── La_Bete_BTC.mq5     # Bot BTC/USD
│   ├── La_Bete_ETH.mq5     # Bot ETH/USD
│   └── guardian_crypto.py  # Guardian API (port 5001)
│
├── CORE/                    # Core System
│   └── telegram_bot_pro.py # Bot Telegram organisé par devise
│
├── SHARED/                  # Modules partagés
│   ├── config.py           # Configuration globale
│   ├── economic_calendar.py # Forex Factory scraping
│   └── telegram_bot.py     # Ancien bot (backup)
│
├── LOGS/                    # Logs automatiques
│   ├── FOREX/
│   └── CRYPTO/
│
├── START_SYSTEM.bat        # Démarrage automatique Windows
├── GUIDE_PROP_FIRM.md      # Guide complet (détails)
└── README.md               # Ce fichier
```

---

## 🔧 INSTALLATION

### 1. Prérequis

```bash
# Python 3.12+
python --version

# Installer dépendances
pip install python-telegram-bot requests beautifulsoup4 lxml pytz flask
```

### 2. Configuration MT5

**Dans MT5 > Outils > Options > Expert Advisors:**

Ajouter aux URLs autorisées:
```
http://localhost:5000
http://localhost:5001
https://www.forexfactory.com
```

✅ Cocher "Autoriser WebRequest pour les URLs listées"

### 3. Configuration Telegram

**Éditer:** `SHARED/config.py`

```python
TELEGRAM_BOT_TOKEN = "VOTRE_TOKEN_ICI"
TELEGRAM_CHAT_ID = "VOTRE_CHAT_ID_ICI"
```

**Obtenir token:**
1. Parler à [@BotFather](https://t.me/BotFather) sur Telegram
2. Créer nouveau bot avec `/newbot`
3. Copier le token

**Obtenir chat_id:**
1. Parler à [@userinfobot](https://t.me/userinfobot)
2. Copier votre ID

### 4. Compiler les Bots

**Dans MetaEditor MT5:**
1. Ouvrir chaque fichier `.mq5`
2. Compiler (F7)
3. Vérifier 0 erreur, 0 warning

---

## 🚀 DÉMARRAGE

### Option 1: Automatique (RECOMMANDÉ)

**Double-cliquer:** `START_SYSTEM.bat`

Choisir **[4] TOUT**

✅ Démarre:
- Guardian FOREX (port 5000)
- Guardian CRYPTO (port 5001)
- Telegram Bot Pro

### Option 2: Manuel

**Terminal 1:**
```bash
cd LaBete/FOREX
python guardian_forex.py
```

**Terminal 2:**
```bash
cd LaBete/CRYPTO
python guardian_crypto.py
```

**Terminal 3:**
```bash
cd LaBete/CORE
python telegram_bot_pro.py
```

### 3. Charger sur MT5

**Pour chaque paire, glisser le bot sur graphique M30:**

- EURUSD M30 → `La_Bete_EUR.mq5`
- GBPUSD M30 → `La_Bete_GBP.mq5`
- USDJPY M30 → `La_Bete_JPY.mq5`
- XAUUSD M30 → `La_Bete_GOLD.mq5`
- BTCUSD M30 → `La_Bete_BTC.mq5`
- ETHUSD M30 → `La_Bete_ETH.mq5`

✅ Vérifier dans l'onglet Expert que tout est actif!

---

## 📊 UTILISATION TELEGRAM

### Vue Globale

**Bouton:** `📊 Vue Globale`

```
📊 VUE GLOBALE - LA BÊTE

🐺 FOREX:
  Trades: 45
  Win Rate: 68.9%
  P&L: +2,450.50€
  Positions: 2

💰 CRYPTO:
  Trades: 18
  Win Rate: 72.2%
  P&L: +1,850.00$
  Positions: 1

💎 TOTAL P&L: +4,300.50€
```

### Contrôle Total

**Bouton:** `⚙️ Contrôle Total`

```
⚙️ CONTRÔLE GLOBAL

⚠️ Actions groupées:

[✅ Start All FOREX]
[❌ Stop All FOREX]

[✅ Start All CRYPTO]
[❌ Stop All CRYPTO]

[🔒 Fermer Toutes Positions]
```

**⚠️ Utilisez avec précaution!**

### Exemple: Gérer EUR/USD

1. Taper `/eur` ou cliquer `🇪🇺 EUR/USD`
2. Voir menu EUR
3. Cliquer **📊 Stats** → Voir performance
4. Cliquer **📈 Positions** → Voir positions en cours
5. Cliquer **🔍 Analyse** → Confluence + Certitude actuels
6. Cliquer **📅 News** → Vérifier calendrier économique
7. Cliquer **✅ Start** / **❌ Stop** → Activer/Désactiver

**Tout depuis votre mobile!**

---

## 🔔 NOTIFICATIONS AUTOMATIQUES

Le bot vous notifie automatiquement:

✅ **Signal détecté** (Confluence + Certitude)
📈 **Position ouverte** (Entry, SL, TP1/2/3)
🎯 **TP atteint** (TP1, TP2, TP3 + % fermé)
🛡️ **Break Even activé** (SL → Entry +10 pips)
🔄 **Trailing activé** (après TP1)
❌ **Stop Loss touché**
⚠️ **News HIGH IMPACT proche** (2h avant)
🚨 **Kill Switch activé** (si limites dépassées)

**Vous êtes toujours dans la boucle!**

---

## 🎓 PROP FIRM COMPLIANCE

### FTMO 40K Challenge

✅ **Risk Management:**
- Max 0.3% par trade (0.25% GOLD)
- Max 2% combiné tous bots
- Stop journalier si -2%
- Max 1 trade simultané par devise

✅ **Règles FTMO:**
- Max 1% loss daily
- Max 10% loss total
- Pas de trading pendant news HIGH
- Confluence minimum respecté
- Guardian API validation obligatoire

✅ **Contrôle Telegram:**
- Surveillance temps réel
- Stats par devise
- Vue globale P&L
- Stop/Start à distance

### Conseils

**DO:**
- ✅ Utiliser Vue Globale pour suivre drawdown
- ✅ Stop manuellement si approche limite
- ✅ Privilégier certitude >70%
- ✅ Respecter calendrier économique
- ✅ Surveiller notifications Telegram

**DON'T:**
- ❌ Ne jamais désactiver Guardian
- ❌ Ne jamais trader pendant news HIGH IMPACT
- ❌ Ne jamais forcer trades (confluence minimum)
- ❌ Ne jamais modifier SL/TP manuellement

---

## 🎯 WORKFLOW JOURNALIER

### Matin (Avant Session)

1. **Double-clic** `START_SYSTEM.bat` → [4]
2. Ouvrir **MT5**, charger les 6 bots
3. Ouvrir **Telegram**, `/start`
4. Vérifier **Vue Globale**
5. Consulter **📅 News** pour chaque devise active

### Pendant Session

**Telegram uniquement!**

- Surveiller notifications
- Vérifier stats via `/eur`, `/gbp`, etc.
- Ajuster si news importantes (Stop bot si nécessaire)
- Utiliser **🔍 Analyse** pour voir confluence actuel

### Soir (Après Session)

1. Vérifier **📊 Vue Globale**
2. Analyser **📊 Stats** par devise
3. Fermer positions si weekend (bouton **🔒**)
4. Vérifier logs si besoin

---

## 📚 DOCUMENTATION

### Guides Disponibles

- **README.md** (ce fichier) - Vue d'ensemble
- **GUIDE_PROP_FIRM.md** - Guide détaillé complet
  - Installation pas à pas
  - Utilisation Telegram
  - Dépannage
  - Conseils FTMO
  - Exemples concrets

### API Endpoints

**Guardian FOREX (localhost:5000):**
- `GET /stats` - Stats globales Forex
- `GET /bot/{currency}/stats` - Stats par devise
- `GET /bot/{currency}/positions` - Positions par devise
- `POST /bot/{currency}/enable` - Activer bot
- `POST /bot/{currency}/disable` - Désactiver bot
- `GET /analyze/{pair}` - Analyser une paire

**Guardian CRYPTO (localhost:5001):**
- Mêmes endpoints pour crypto

---

## ❓ DÉPANNAGE

### Guardian ne démarre pas

```bash
# Vérifier ports disponibles
netstat -an | findstr :5000
netstat -an | findstr :5001

# Si occupé, tuer processus
taskkill /F /IM python.exe
```

### MT5 refuse connexion

**Vérifier MT5 > Options > Expert Advisors:**

✅ `http://localhost:5000` autorisé
✅ `http://localhost:5001` autorisé
✅ "Autoriser WebRequest" coché

### Telegram ne répond pas

```bash
# Tester token
curl https://api.telegram.org/bot<TOKEN>/getMe

# Vérifier config.py
TELEGRAM_BOT_TOKEN = "..."
```

### Bot ne trade pas

1. ✅ Bot **ACTIF** (bouton ✅ Start vert)
2. 🔍 Consulter **Analyse** → Voir confluence actuel
3. 📅 Vérifier **News** → Peut bloquer si proche
4. Confluence doit être ≥90% (Forex) ou ≥85% (Crypto)

---

## 📈 STATISTIQUES SYSTÈME

### Fichiers Code

- **6 Bots MT5** - 1,072-1,073 lignes chacun
- **2 Guardians Python** - 776 lignes chacun
- **Telegram Bot Pro** - 700+ lignes
- **Economic Calendar** - 260 lignes
- **Total:** ~9,000 lignes de code

### Fonctionnalités

✅ EMA Crossover Detection
✅ Order Blocks Detection
✅ Fair Value Gaps Detection
✅ BOS/CHoCH Detection
✅ Confluence Scoring /100
✅ Certainty Calculation %
✅ Dynamic ATR SL/TP
✅ Triple TP Management
✅ Break Even Automation
✅ Trailing Stop
✅ Forex Factory Scraping
✅ Telegram Control per Currency
✅ Guardian API Validation
✅ Kill Switches
✅ Prop Firm Compliance

---

## 🏆 AVANTAGES

### Vs Autres Systèmes

✅ **Organisation par Devise**
- Chaque bot spécialisé
- Paramètres adaptés à volatilité
- Contrôle indépendant

✅ **Telegram Interface**
- Menu graphique intuitif
- Contrôle total mobile
- Notifications temps réel
- Pas besoin MT5 ouvert

✅ **Prop Firm Ready**
- Règles FTMO intégrées
- Risk management strict
- Economic calendar
- Guardian validation

✅ **Code Complet**
- Pas de TODO
- Pas de placeholder
- Production ready
- 0 erreur compilation

---

## 📞 SUPPORT

**Logs:**
```
LOGS/FOREX/    # Logs Guardian Forex
LOGS/CRYPTO/   # Logs Guardian Crypto
```

**En cas de problème:**
1. Consulter logs
2. Vérifier connexions API (`netstat`)
3. Redémarrer système (`START_SYSTEM.bat`)
4. Lire `GUIDE_PROP_FIRM.md`

---

## 🔒 LICENCE

**Système Privé - Usage Personnel**

⚠️ **NE PAS DISTRIBUER** sans autorisation

---

## ✨ VERSION

**LA BÊTE V8 Ultimate**

- EMA Crossover Strategy
- Smart Money Concepts
- Economic Calendar
- Telegram Control per Currency
- 6 Specialized Bots
- Prop Firm Optimized

---

**🐺 Créé pour réussir les challenges FTMO 40K**

_Système professionnel organisé par devise avec contrôle Telegram complet_

🚀 **Démarrez maintenant:** `START_SYSTEM.bat` → [4] TOUT → `/start`

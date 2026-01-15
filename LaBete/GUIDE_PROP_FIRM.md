# 🐺 LA BÊTE - SYSTÈME PROP FIRM PROFESSIONNEL

## 📋 TABLE DES MATIÈRES

1. [Installation](#installation)
2. [Démarrage](#démarrage)
3. [Contrôle Telegram](#contrôle-telegram)
4. [Gestion par Devise](#gestion-par-devise)
5. [Structure des Fichiers](#structure)
6. [Paramètres](#paramètres)

---

## 🚀 INSTALLATION

### 1. Prérequis

```bash
# Python 3.12+
python --version

# Installer les dépendances
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

### 3. Configuration Telegram

**Fichier: `SHARED/config.py`**

```python
TELEGRAM_BOT_TOKEN = "VOTRE_TOKEN_BOT"
TELEGRAM_CHAT_ID = "VOTRE_CHAT_ID"
```

---

## 🎯 DÉMARRAGE

### Méthode 1: Script Automatique (RECOMMANDÉ)

**Double-cliquez sur:** `START_SYSTEM.bat`

Choisissez option **[4] TOUT**

✅ Démarre:
- Guardian FOREX (port 5000)
- Guardian CRYPTO (port 5001)
- Bot Telegram Pro

### Méthode 2: Manuel

**Terminal 1 - Guardian FOREX:**
```bash
cd LaBete/FOREX
python guardian_forex.py
```

**Terminal 2 - Guardian CRYPTO:**
```bash
cd LaBete/CRYPTO
python guardian_crypto.py
```

**Terminal 3 - Telegram Bot:**
```bash
cd LaBete/CORE
python telegram_bot_pro.py
```

### 3. Charger les Bots MT5

Ouvrir MT5 et charger sur les graphiques M30:

| Bot | Paire | Graphique | Magic |
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

Tapez `/start` dans Telegram pour ouvrir le menu:

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

### Navigation

**Cliquer sur une devise** ouvre son menu:

```
🇪🇺 EUR/USD

Magic Number: 666001
Type: FOREX

[📊 Stats]        [📈 Positions]
[✅ Start]        [❌ Stop]
[🔍 Analyse]      [📅 News]

[⬅️ Retour]
```

---

## 💱 GESTION PAR DEVISE

### 🇪🇺 EUR/USD

**Commande rapide:** `/eur`

**Paramètres:**
- ATR × 1.5
- SL: 50-80 pips
- Risque: 0.3%
- Confluence min: 90%

**Menu Telegram:**
- **📊 Stats** - Trades, Win Rate, P&L
- **📈 Positions** - Positions ouvertes en temps réel
- **✅ Start** - Activer le bot
- **❌ Stop** - Désactiver le bot
- **🔍 Analyse** - Confluence + Certitude actuels
- **📅 News** - Calendrier économique EUR

### 🇬🇧 GBP/USD

**Commande rapide:** `/gbp`

**Paramètres:**
- ATR × 1.8 (volatilité plus forte)
- SL: 80-120 pips
- Risque: 0.3%
- Confluence min: 90%

**Actions identiques à EUR**

### 🇯🇵 USD/JPY

**Commande rapide:** `/jpy`

**Paramètres:**
- ATR × 1.3 (volatilité plus faible)
- SL: 40-60 pips
- Risque: 0.3%
- Confluence min: 90%

### 🥇 GOLD (XAU/USD)

**Commande rapide:** `/gold`

**Paramètres:**
- ATR × 2.5 (haute volatilité)
- SL: 200-800 pips
- Risque: **0.25%** (réduit)
- Confluence min: 90%

### ₿ BTC/USD

**Commande rapide:** `/btc`

**Paramètres:**
- ATR × 2.0
- SL: 500-1500 pips
- Risque: 0.3%
- Confluence min: **85%** (crypto)
- Guardian: port 5001

### Ξ ETH/USD

**Commande rapide:** `/eth`

**Paramètres:**
- ATR × 2.0
- SL: 80-200 pips
- Risque: 0.3%
- Confluence min: **85%** (crypto)
- Guardian: port 5001

---

## 📊 VUE GLOBALE

**Bouton:** `📊 Vue Globale`

Affiche:
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

---

## ⚙️ CONTRÔLE TOTAL

**Bouton:** `⚙️ Contrôle Total`

Actions groupées:

```
⚙️ CONTRÔLE GLOBAL

⚠️ Actions groupées:

[✅ Start All FOREX]   [❌ Stop All FOREX]
[✅ Start All CRYPTO]  [❌ Stop All CRYPTO]

[🔒 Fermer Toutes Positions]

[⬅️ Retour]
```

**Utilisez avec précaution!**

---

## 📁 STRUCTURE DES FICHIERS

```
LaBete/
│
├── FOREX/
│   ├── La_Bete_EUR.mq5      # Bot EUR/USD
│   ├── La_Bete_GBP.mq5      # Bot GBP/USD
│   ├── La_Bete_JPY.mq5      # Bot USD/JPY
│   ├── La_Bete_GOLD.mq5     # Bot XAU/USD
│   └── guardian_forex.py    # Guardian FOREX (port 5000)
│
├── CRYPTO/
│   ├── La_Bete_BTC.mq5      # Bot BTC/USD
│   ├── La_Bete_ETH.mq5      # Bot ETH/USD
│   └── guardian_crypto.py   # Guardian CRYPTO (port 5001)
│
├── CORE/
│   └── telegram_bot_pro.py  # Bot Telegram organisé par devise
│
├── SHARED/
│   ├── config.py            # Configuration globale
│   ├── economic_calendar.py # Forex Factory scraping
│   └── telegram_bot.py      # Ancien bot (backup)
│
├── LOGS/                    # Logs automatiques
│   ├── FOREX/
│   └── CRYPTO/
│
├── START_SYSTEM.bat         # Démarrage automatique
└── GUIDE_PROP_FIRM.md      # Ce fichier
```

---

## 🎛️ PARAMÈTRES

### Par Devise

| Devise | ATR Mult | SL Range | Risque | Confluence | Guardian |
|--------|----------|----------|--------|------------|----------|
| EUR | 1.5 | 50-80 | 0.3% | 90% | :5000 |
| GBP | 1.8 | 80-120 | 0.3% | 90% | :5000 |
| JPY | 1.3 | 40-60 | 0.3% | 90% | :5000 |
| GOLD | 2.5 | 200-800 | 0.25% | 90% | :5000 |
| BTC | 2.0 | 500-1500 | 0.3% | 85% | :5001 |
| ETH | 2.0 | 80-200 | 0.3% | 85% | :5001 |

### Triple TP

**Tous les bots:**
- TP1 (1:2) → Fermer 50%
- TP2 (1:3) → Fermer 30%
- TP3 (1:5) → Fermer 20%

### Break Even

- Activation: 50% du chemin vers TP1
- Offset: +10 pips

### Trailing Stop

- Après TP1
- Distance: ATR × 0.5

---

## 🎯 WORKFLOW RECOMMANDÉ

### Matin (Avant NYSE Open)

1. **Double-cliquer** `START_SYSTEM.bat`
2. Choisir **[4] TOUT**
3. Ouvrir **MT5** et charger les 6 bots
4. Ouvrir **Telegram** et taper `/start`
5. Vérifier **Vue Globale**
6. Consulter **News** pour chaque devise active

### Pendant la Session

**Telegram uniquement!**

- Surveiller notifications automatiques
- Vérifier stats par `/eur`, `/gbp`, etc.
- Ajuster si news importantes
- Stop/Start selon conditions

### Soir (Après Session)

1. Vérifier **Vue Globale**
2. Analyser **Performance** par devise
3. Fermer positions si weekend
4. Sauvegarder logs

---

## 🔔 NOTIFICATIONS AUTOMATIQUES

Le bot Telegram vous notifie:

✅ **Signal détecté** (avec confluence + certitude)
📈 **Position ouverte** (entry, SL, TP)
🎯 **TP atteint** (TP1, TP2, TP3)
🛡️ **Break Even activé**
🔄 **Trailing activé**
❌ **Stop Loss touché**
⚠️ **News HIGH IMPACT proche**
🚨 **Kill Switch activé**

---

## ❓ DÉPANNAGE

### Guardian ne démarre pas

```bash
# Vérifier que le port est libre
netstat -an | findstr :5000
netstat -an | findstr :5001

# Fermer processus si occupé
taskkill /F /IM python.exe
```

### MT5 refuse connexion Guardian

**Vérifier dans MT5 > Options > Expert Advisors:**

✅ `http://localhost:5000` est autorisé
✅ `http://localhost:5001` est autorisé

### Telegram ne répond pas

```bash
# Vérifier token dans config.py
TELEGRAM_BOT_TOKEN = "..."

# Vérifier connexion
curl https://api.telegram.org/bot<TOKEN>/getMe
```

### Bot ne prend pas de trades

1. Vérifier que le bot est **ACTIF** (bouton ✅ Start)
2. Consulter **🔍 Analyse** pour voir confluence actuel
3. Vérifier **📅 News** (peut bloquer si news proche)
4. Minimum confluence: 90% Forex, 85% Crypto

---

## 🎓 CONSEILS PROP FIRM

### FTMO 40K Challenge

✅ **DO:**
- Utiliser Vue Globale pour suivre drawdown
- Stop manuellement si approche 4% journalier
- Privilégier certitude >70%
- Respecter calendrier économique

❌ **DON'T:**
- Ne jamais désactiver Guardian
- Ne jamais trader pendant news HIGH IMPACT
- Ne jamais forcer trades (respecter confluence min)
- Ne jamais modifier SL/TP manuellement

### Risk Management

**Par devise:**
- EUR/GBP/JPY/BTC/ETH: 0.3% max
- GOLD: 0.25% max (volatilité)

**Global:**
- Max 2% tous bots combinés
- Max 1 trade simultané par devise
- Stop journalier si -2%

---

## 📞 SUPPORT

**Logs:**
- FOREX: `LOGS/FOREX/`
- CRYPTO: `LOGS/CRYPTO/`

**En cas de problème:**
1. Consulter les logs
2. Vérifier connexions API
3. Redémarrer système complet

---

**🐺 LA BÊTE - Système Prop Firm Professionnel V8**

_Bonne chance avec le challenge FTMO!_ 🚀

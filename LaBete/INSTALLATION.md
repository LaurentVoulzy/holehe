# 🐺 LA BÊTE - GUIDE D'INSTALLATION COMPLET

## Système Dual Forex + Crypto Ultra-Sécurisé pour Prop Firm

**Version:** 6.0 Ultimate
**Auteur:** Yann
**Python:** 3.12+
**Plateformes:** Windows (MT5)

---

## 📋 TABLE DES MATIÈRES

1. [Prérequis](#prérequis)
2. [Installation Python](#installation-python)
3. [Installation MT5](#installation-mt5)
4. [Configuration](#configuration)
5. [Lancement du Système](#lancement-du-système)
6. [Vérifications](#vérifications)
7. [Commandes Telegram](#commandes-telegram)
8. [Troubleshooting](#troubleshooting)

---

## ✅ PRÉREQUIS

### Logiciels nécessaires:
- ✅ **Python 3.12+** (vous avez déjà 3.12.8)
- ✅ **MetaTrader 5** (pour Forex et Crypto)
- ✅ **Telegram** (sur mobile ou desktop)
- ✅ **Compte Prop Firm** (FTMO, RaiseMyFunds, etc.)

### Comptes:
- Token Bot Telegram: `8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE`
- Chat ID Telegram: `1981386789`
- Email: `kykylou30@gmail.com`

---

## 🐍 INSTALLATION PYTHON

### 1. Vérifier Python

Ouvrez **CMD** et tapez:

```cmd
python --version
```

Résultat attendu: `Python 3.12.8` (ou supérieur)

### 2. Installer les dépendances

```cmd
cd C:\Trading\LaBete
pip install -r requirements.txt
```

**Important:** Si erreur "pip not found", utilisez:
```cmd
python -m pip install -r requirements.txt
```

### 3. Vérifier l'installation

```cmd
python -c "import flask, telegram; print('✅ OK')"
```

---

## 📊 INSTALLATION MT5

### 1. Télécharger MetaTrader 5

- Site officiel: https://www.metatrader5.com/
- Ou via votre broker (FTMO, RaiseMyFunds)

### 2. Installer 2 instances MT5

**Instance 1: FOREX**
- Installation: `C:\Program Files\MetaTrader 5 Forex\`
- Compte: FTMO 40K€ (ou RaiseMyFunds 50K$)
- Paires: EURUSD, GBPUSD, USDJPY

**Instance 2: CRYPTO**
- Installation: `C:\Program Files\MetaTrader 5 Crypto\`
- Compte: Crypto broker
- Paires: BTCUSD, ETHUSD

### 3. Copier les fichiers .mq5

**Pour FOREX:**
```
Copier: C:\Trading\LaBete\FOREX\La_Bete_FOREX_V6_Ultimate.mq5
Vers: C:\Program Files\MetaTrader 5 Forex\MQL5\Experts\
```

**Pour CRYPTO:**
```
Copier: C:\Trading\LaBete\CRYPTO\La_Bete_CRYPTO_V6_Ultimate.mq5
Vers: C:\Program Files\MetaTrader 5 Crypto\MQL5\Experts\
```

### 4. Compiler les fichiers

Dans MT5:
1. Ouvrir **MetaEditor** (F4)
2. Ouvrir le fichier `.mq5`
3. Cliquer sur **Compile** (F7)
4. Vérifier: **0 errors**

---

## ⚙️ CONFIGURATION

### 1. Configurer config.py

Ouvrir: `C:\Trading\LaBete\SHARED\config.py`

Vérifier/Modifier:

```python
# Vos identifiants (déjà configurés)
TELEGRAM_BOT_TOKEN = "8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE"
TELEGRAM_CHAT_ID = "1981386789"

# Capital FOREX
FOREX_CONFIG = {
    "account_balance": 40000,  # Votre challenge FTMO 40K€
    "risk_per_trade": 0.003,   # 0.3%
    # ...
}

# Capital CRYPTO
CRYPTO_CONFIG = {
    "account_balance": 50000,  # RaiseMyFunds 50K$
    "risk_per_trade": 0.002,   # 0.2%
    # ...
}
```

### 2. Autoriser WebRequest dans MT5

**CRITICAL:** MT5 doit pouvoir envoyer des requêtes HTTP aux Guardians.

Dans MT5:
1. **Outils** → **Options** → **Expert Advisors**
2. Cocher: ✅ **Autoriser WebRequest pour les URLs suivantes:**
   ```
   http://localhost:5000
   http://localhost:5001
   http://127.0.0.1:5000
   http://127.0.0.1:5001
   ```
3. Cliquer **OK**

### 3. Configurer les fichiers .mq5

Ouvrir les fichiers MT5 et vérifier:

```cpp
// Dans La_Bete_FOREX_V6_Ultimate.mq5
string GUARDIAN_API_URL = "http://localhost:5000/validate_signal";

// Dans La_Bete_CRYPTO_V6_Ultimate.mq5
string GUARDIAN_API_URL = "http://localhost:5001/validate_signal";
```

---

## 🚀 LANCEMENT DU SYSTÈME

### Méthode 1: Manuelle (Recommandée pour débuter)

**Ouvrir 3 fenêtres CMD** (en tant qu'Administrateur):

**Fenêtre 1 - Guardian FOREX:**
```cmd
cd C:\Trading\LaBete\FOREX
python guardian_forex.py
```

**Fenêtre 2 - Guardian CRYPTO:**
```cmd
cd C:\Trading\LaBete\CRYPTO
python guardian_crypto.py
```

**Fenêtre 3 - Bot Telegram:**
```cmd
cd C:\Trading\LaBete\SHARED
python telegram_bot.py
```

✅ **Résultats attendus:**
- Fenêtre 1: `🐺 Forex Guardian démarré sur port 5000`
- Fenêtre 2: `💰 Crypto Guardian démarré sur port 5001`
- Fenêtre 3: `🤖 Bot Telegram La Bête démarré!`

### Méthode 2: Script de lancement (Avancé)

Créer `START_LA_BETE.bat`:

```batch
@echo off
echo 🐺 Lancement de LA BETE...

start "Guardian FOREX" cmd /k "cd C:\Trading\LaBete\FOREX && python guardian_forex.py"
timeout /t 2

start "Guardian CRYPTO" cmd /k "cd C:\Trading\LaBete\CRYPTO && python guardian_crypto.py"
timeout /t 2

start "Bot Telegram" cmd /k "cd C:\Trading\LaBete\SHARED && python telegram_bot.py"

echo ✅ Système démarré!
pause
```

Double-cliquer sur `START_LA_BETE.bat`

### Lancer les bots MT5

**MT5 Instance FOREX:**
1. Ouvrir graphique **EURUSD M30**
2. Navigateur → Experts → `La_Bete_FOREX_V6_Ultimate`
3. Glisser-déposer sur le graphique
4. Paramètres:
   - ✅ Autoriser le trading automatique
   - ✅ Autoriser WebRequest
5. Cliquer **OK**

**MT5 Instance CRYPTO:**
1. Ouvrir graphique **BTCUSD M30**
2. Navigateur → Experts → `La_Bete_CRYPTO_V6_Ultimate`
3. Glisser-déposer sur le graphique
4. Paramètres:
   - ✅ Autoriser le trading automatique
   - ✅ Autoriser WebRequest
5. Cliquer **OK**

---

## ✅ VÉRIFICATIONS

### 1. Vérifier les Guardians

**Test Guardian FOREX:**
```cmd
curl http://localhost:5000/health
```

Résultat attendu:
```json
{
  "status": "OK",
  "system": "FOREX",
  "kill_switch_active": false,
  "timestamp": "2025-01-08T..."
}
```

**Test Guardian CRYPTO:**
```cmd
curl http://localhost:5001/health
```

### 2. Vérifier le Bot Telegram

Ouvrir **Telegram** et chercher votre bot:

Envoyer: `/start`

Réponse attendue:
```
🐺 LA BÊTE - Trading System 🐺
Version 6.0 Ultimate
...
📱 COMMANDES DISPONIBLES:
...
```

### 3. Vérifier MT5

Dans MT5, onglet **Experts**:

✅ Logs attendus:
```
[FOREX] La Bête V6 démarrée
[FOREX] Guardian API: http://localhost:5000/validate_signal
[FOREX] Système opérationnel ✅
```

### 4. Test complet

Envoyer dans Telegram:
```
/stats
```

Réponse attendue:
```
📊 STATISTIQUES GLOBALES - LA BÊTE

🐺 FOREX:
  Trades: 0
  P&L: 0.00€
  ...

💰 CRYPTO:
  Trades: 0
  P&L: 0.00$
  ...
```

---

## 📱 COMMANDES TELEGRAM

### Commandes FOREX

| Commande | Description |
|----------|-------------|
| `/forex_stats` | Statistiques Forex |
| `/forex_positions` | Positions ouvertes Forex |
| `/forex_stop` | Arrêter le bot Forex (Kill Switch) |
| `/forex_start` | Démarrer le bot Forex |
| `/forex_today` | Résumé de la journée Forex |

### Commandes CRYPTO

| Commande | Description |
|----------|-------------|
| `/crypto_stats` | Statistiques Crypto |
| `/crypto_positions` | Positions ouvertes Crypto |
| `/crypto_stop` | Arrêter le bot Crypto (Kill Switch) |
| `/crypto_start` | Démarrer le bot Crypto |
| `/crypto_today` | Résumé de la journée Crypto |

### Commandes GLOBALES

| Commande | Description |
|----------|-------------|
| `/start` | Démarrer le bot / Aide |
| `/help` | Afficher l'aide |
| `/stats` | Stats Forex + Crypto |
| `/stopall` | Arrêter tout (urgence) |
| `/startall` | Démarrer tout |
| `/report` | Rapport complet |
| `/risk` | Niveau de risque global |

---

## 🔧 TROUBLESHOOTING

### Problème: "Module not found"

**Solution:**
```cmd
pip install flask python-telegram-bot requests
```

### Problème: "Port already in use"

**Cause:** Guardian déjà lancé

**Solution:**
```cmd
# Tuer le processus
taskkill /F /IM python.exe

# Relancer
python guardian_forex.py
```

### Problème: MT5 ne se connecte pas au Guardian

**Vérifications:**
1. ✅ Guardian lancé? (`curl http://localhost:5000/health`)
2. ✅ WebRequest autorisé dans MT5?
3. ✅ URL correcte dans le code MT5?
4. ✅ Pare-feu Windows bloque Python?

**Solution pare-feu:**
```
Panneau de configuration → Système et sécurité → Pare-feu Windows
→ Autoriser une application → Python.exe
```

### Problème: Bot Telegram ne répond pas

**Vérifications:**
1. ✅ Token correct? (vérifier config.py)
2. ✅ Internet connecté?
3. ✅ Fenêtre CMD bot_telegram.py ouverte?

**Test token:**
```
https://api.telegram.org/bot8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE/getMe
```

### Problème: Aucun signal détecté

**Causes possibles:**
- Période interdite (Noël, weekend, etc.)
- Confluence score < 90 (Forex) ou < 85 (Crypto)
- Kill Switch actif
- News High Impact proche

**Solution:**
1. Vérifier logs MT5 (onglet Experts)
2. Vérifier logs Guardian (fenêtre CMD)
3. Envoyer `/forex_stats` dans Telegram

### Problème: Kill Switch ne se désactive pas

**Solution manuelle:**
```cmd
curl -X POST http://localhost:5000/kill_switch/deactivate
curl -X POST http://localhost:5001/kill_switch/deactivate
```

Ou via Telegram:
```
/forex_start
/crypto_start
```

---

## 🎯 CHECKLIST AVANT TRADING

Avant de laisser le système trader:

- [ ] ✅ Les 3 fenêtres CMD sont ouvertes (Forex, Crypto, Telegram)
- [ ] ✅ Les 2 bots MT5 sont actifs (graphiques M30)
- [ ] ✅ AutoTrading activé dans MT5 (bouton vert)
- [ ] ✅ WebRequest autorisé
- [ ] ✅ Bot Telegram répond (`/start`)
- [ ] ✅ Pas de période interdite (`is_trading_allowed()`)
- [ ] ✅ Capital configuré correctement (40K€ Forex, 50K$ Crypto)
- [ ] ✅ Risque 0.3% Forex / 0.2% Crypto
- [ ] ✅ Kill Switch désactivé
- [ ] ✅ Notifications Telegram actives

---

## 📊 SURVEILLANCE QUOTIDIENNE

### À faire chaque jour:

**Matin (avant ouverture):**
1. Vérifier `/stats` - Aucune perte anormale hier
2. Vérifier calendrier économique (news aujourd'hui?)
3. S'assurer Kill Switch désactivé
4. Vérifier solde comptes prop firm

**Pendant la journée:**
1. Surveiller notifications Telegram
2. Vérifier positions ouvertes toutes les 2h
3. Analyser les rejets de signaux (logs)

**Soir (18h):**
1. Lire le rapport quotidien automatique
2. Analyser P&L du jour
3. Vérifier win rate
4. Préparer demain (news économiques?)

**Vendredi:**
1. Lire rapport hebdomadaire
2. Analyser performance semaine
3. Ajuster paramètres si nécessaire

---

## ⚠️ RÈGLES STRICTES

### 🚫 NE JAMAIS:

1. ❌ Trader pendant périodes interdites (24 déc - 3 jan, Pâques, etc.)
2. ❌ Désactiver le Kill Switch si déclenché (attendre lendemain)
3. ❌ Augmenter le risque au-delà de 0.3% (Forex) / 0.2% (Crypto)
4. ❌ Forcer un trade si confluence < 90 (Forex) / 85 (Crypto)
5. ❌ Trader après 2 pertes consécutives manuellement
6. ❌ Modifier le code sans sauvegarder l'original
7. ❌ Laisser tourner sans surveiller les 2 premières semaines

### ✅ TOUJOURS:

1. ✅ Surveiller les 3 fenêtres CMD
2. ✅ Répondre aux alertes Telegram
3. ✅ Sauvegarder les bases de données (forex_trades.db, crypto_trades.db)
4. ✅ Tester sur compte démo AVANT prop firm
5. ✅ Respecter les règles prop firm (max daily loss, max total loss)
6. ✅ Analyser CHAQUE trade fermé (pourquoi win? pourquoi loss?)
7. ✅ Garder un journal de trading

---

## 📁 STRUCTURE DES FICHIERS

```
C:\Trading\LaBete\
│
├── FOREX\
│   ├── guardian_forex.py          ← Guardian Forex
│   ├── La_Bete_FOREX_V6_Ultimate.mq5  ← Bot MT5 Forex
│   ├── forex_trades.db            ← Base de données Forex
│   └── logs\
│       └── guardian_forex.log
│
├── CRYPTO\
│   ├── guardian_crypto.py         ← Guardian Crypto
│   ├── La_Bete_CRYPTO_V6_Ultimate.mq5 ← Bot MT5 Crypto
│   ├── crypto_trades.db           ← Base de données Crypto
│   └── logs\
│       └── guardian_crypto.log
│
├── SHARED\
│   ├── config.py                  ← Configuration globale
│   ├── telegram_bot.py            ← Bot Telegram
│   └── utils.py                   ← Utilitaires
│
├── requirements.txt               ← Dépendances Python
├── INSTALLATION.md                ← Ce fichier
├── README.md                      ← Documentation principale
└── START_LA_BETE.bat             ← Script de lancement

```

---

## 🆘 SUPPORT

### Problèmes techniques:
- Vérifier les logs: `C:\Trading\LaBete\FOREX\logs\guardian_forex.log`
- Vérifier MT5 onglet **Journal**
- Envoyer `/stats` dans Telegram

### Ressources:
- Documentation MT5: https://www.mql5.com/en/docs
- Flask API: https://flask.palletsprojects.com/
- Python Telegram Bot: https://python-telegram-bot.org/

---

## ✅ C'EST PARTI !

Une fois tout configuré:

1. Lancer les 3 scripts Python
2. Activer les 2 bots MT5
3. Envoyer `/start` dans Telegram
4. Vérifier `/stats`
5. **SURVEILLER** pendant 2-3 jours avant de laisser autonome

**Bon trading ma couille ! 💎🐺**

---

*Guide créé le 08/01/2025*
*La Bête V6 Ultimate - Système Dual Forex + Crypto*

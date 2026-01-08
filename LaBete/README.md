# 🐺 LA BÊTE - Système Trading Dual Forex + Crypto

## **Version 6.0 Ultimate - Ultra-Sécurisé pour Prop Firm Challenges**

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![MT5](https://img.shields.io/badge/MT5-5.0-green.svg)
![License](https://img.shields.io/badge/license-Private-red.svg)

---

## 📖 PRÉSENTATION

**La Bête** est un système de trading automatisé **dual** (Forex + Crypto) conçu spécifiquement pour **réussir les challenges prop firm** (FTMO, RaiseMyFunds, The5ers, etc.) avec un niveau de sécurité maximum pour éviter de "cramer" les comptes.

### ✨ Pourquoi "La Bête" ?

Après avoir échoué un challenge FTMO 40K€ le 30 décembre 2024 avec une perte de -3,229€ en une soirée pendant une période morte, ce système a été créé pour **NE PLUS JAMAIS revivre ça**.

### 🎯 Objectif

**Trader de manière ultra-sécurisée** en respectant strictement les règles prop firm et en évitant TOUS les pièges psychologiques (revenge trading, overtrading, périodes dangereuses, etc.).

---

## 🚀 FONCTIONNALITÉS PRINCIPALES

### 📊 Analyse Technique Avancée

#### Smart Money Concepts (SMC)
- ✅ **Order Blocks** (OB+ et OB-) avec validation 3 pips
- ✅ **Fair Value Gaps** (FVG+ et FVG-)
- ✅ **Break of Structure** (BOS)
- ✅ **Change of Character** (CHoCH)
- ✅ **Liquidity Sweeps** detection
- ✅ **Market Structure** analysis temps réel

#### Indicateurs Multi-Timeframe
- ✅ **EMA** 20/50/200 sur M30, H1, H4
- ✅ **RSI 14** avec détection divergences
- ✅ **MACD** (12,26,9) avec crossovers
- ✅ **ATR** pour volatilité dynamique
- ✅ **Support/Resistance** automatiques
- ✅ **Previous High/Low** tracking

#### Pattern Recognition
- ✅ **Patterns chartistes**: double top/bottom, H&S, triangles, flags, wedges
- ✅ **Patterns candlestick**: engulfing, pin bar, doji, morning/evening star
- ✅ **Score de fiabilité** pour chaque pattern

---

### 🎯 SYSTÈME DE CONFLUENCE (100 POINTS)

Chaque signal est noté sur **100 points** avant validation:

| Catégorie | Points Max | Critères |
|-----------|------------|----------|
| **Structure SMC** | 40 pts | Prix dans OB (20), FVG aligné (10), BOS+CHoCH (10) |
| **Multi-Timeframe** | 25 pts | Alignement M30+H1+H4 (15), Trend strength (10) |
| **Indicateurs** | 20 pts | EMA alignées (8), RSI favorable (6), MACD crossover (6) |
| **Support/Resistance** | 10 pts | Bounce sur S/R (5), Previous High/Low (5) |
| **Pattern** | 5 pts | Pattern détecté et validé (5) |

**Confluence minimum requis:**
- **Forex**: 90/100 ⚡
- **Crypto**: 85/100 ⚡

---

### 🛡️ 7 NIVEAUX DE PROTECTION ANTI-CRAMAGE

#### **Niveau 1: Stop Loss Dynamique**
- Basé sur ATR × 1.5 (Forex) / × 2.0 (Crypto)
- Positionné sous/sur dernier swing
- Sous/sur Order Block le plus proche
- **Limites**: 50-150 pips (Forex), 200-1000$ BTC, 20-100$ ETH

#### **Niveau 2: Triple Take Profit**
- **TP1**: Risk:Reward 1:2 → Ferme **50%** de la position
- **TP2**: Risk:Reward 1:3 → Ferme **30%** de la position
- **TP3**: Risk:Reward 1:5 → Ferme **20%** de la position
- Ajusté selon structure Support/Resistance

#### **Niveau 3: Break Even Intelligent**
- Activé à **50%** du chemin vers TP1
- SL déplacé à Entry + 10 pips (Forex) / +0.5% (Crypto)
- Protection profit **immédiate**

#### **Niveau 4: Trailing Stop Structurel**
- Activé **après TP1** atteint
- Trail **50% de l'ATR** derrière swing low/high
- **Jamais de recul** du SL

#### **Niveau 5: Filtre News Économiques**
- **ARRÊT 2h avant/après** news High Impact:
  - FOMC, NFP, CPI, GDP, Interest Rate
  - ECB, BOE, BOJ decisions
  - Retail Sales, Employment data
- API calendrier économique intégré
- Détection automatique événements majeurs

#### **Niveau 6: Anti-Revenge Trading**
- Détection: **2 pertes** + trade **< 10 minutes**
- **Kill Switch automatique** activé
- **Pause forcée de 2 heures**
- Notification Telegram immédiate

#### **Niveau 7: Kill Switch Ultimate Multi-Triggers**

Activation automatique si:
- ❌ Perte journalière ≥ **-400€** (Forex) / **-500$** (Crypto)
- ❌ Drawdown ≥ **-3,000€** (Forex) / **-3,500$** (Crypto)
- ❌ Win rate < **35%** (Forex) / **40%** (Crypto) sur 15+ trades
- ❌ **3 pertes consécutives**
- ❌ **8+ trades/jour** (overtrading)
- ❌ News High Impact dans **2h**
- ❌ **Période morte** détectée
- ❌ **Volatilité extrême** anormale

---

### 🚫 PÉRIODES STRICTEMENT INTERDITES

#### Calendrier Strict:
- ❌ **24 déc - 3 jan** (Noël/Nouvel An) **← CRITICAL!**
- ❌ **Pâques** (4 jours)
- ❌ Jours fériés majeurs **US/UK/EU**
- ❌ **Vendredi après 16h**
- ❌ **Dimanche avant 23h**
- ❌ **Avant/pendant/après news 🔴 High Impact**

> ⚠️ **Leçon apprise:** Challenge FTMO cramé le 30 déc (période morte) = -3,229€ en une soirée.

---

### 💰 SPÉCIFICITÉS CRYPTO

Protections supplémentaires pour crypto:

#### Volatilité
- **ATR × 2** pour SL (vs × 1.5 forex)
- **SL min/max**: BTC 200-1000$, ETH 20-100$
- **Risque réduit**: 0.2% par trade (vs 0.3% forex)

#### Filtres Spécifiques
- 🐋 **Whale Activity Detection**: Volume > 300% moyenne
- 📅 **Weekend Gap Protection**: Vendredi 20h - Dimanche 22h
- 😱 **Fear & Greed Index** integration
- 💸 **Funding Rate Analysis** (futures)
- ₿ **BTC Dominance Check** (40-70%)

#### Limites
- **Max 2 trades/jour** (vs 3 forex)
- **Risk:Reward min 1:3** (vs 1:2 forex)
- **1 position max** ouverte simultanée

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Structure du Système

```
LA BÊTE
├─ FOREX (🐺)
│  ├─ Bot MT5 (La_Bete_FOREX_V6_Ultimate.mq5)
│  │  └─ Analyse SMC + Confluence → Signal
│  │
│  └─ Guardian Python (guardian_forex.py)
│     ├─ API Flask :5000
│     ├─ Validation signal (7 niveaux)
│     ├─ Kill Switch monitoring
│     └─ Database SQLite
│
├─ CRYPTO (💰)
│  ├─ Bot MT5 (La_Bete_CRYPTO_V6_Ultimate.mq5)
│  │  └─ Analyse SMC + Confluence → Signal
│  │
│  └─ Guardian Python (guardian_crypto.py)
│     ├─ API Flask :5001
│     ├─ Validation signal + filtres crypto
│     ├─ Whale/Weekend/Funding checks
│     └─ Database SQLite
│
└─ SHARED (🤖)
   ├─ config.py (Configuration centrale)
   ├─ telegram_bot.py (Contrôle dual)
   └─ utils.py (Utilitaires)
```

### Flux de Trading

```
1. MT5 détecte setup (SMC + Confluence ≥ 90/100)
                ↓
2. MT5 calcule Signal (Entry, SL, TP1/2/3, Lot Size)
                ↓
3. MT5 envoie Signal → Guardian Python (HTTP POST)
                ↓
4. Guardian valide (7 niveaux protection)
                ↓
5a. ✅ APPROUVÉ → MT5 ouvre position
5b. ❌ REJETÉ → MT5 ignore, log raison
                ↓
6. MT5 gère position (BE, Trailing, TP partiel)
                ↓
7. Fermeture → Guardian update stats → Check Kill Switch
                ↓
8. Notification Telegram (résultat + stats)
```

---

## 📱 BOT TELEGRAM - CONTRÔLE DUAL

### Commandes Forex

| Commande | Description |
|----------|-------------|
| `/forex_stats` | Statistiques Forex |
| `/forex_positions` | Positions ouvertes Forex |
| `/forex_stop` | Arrêter bot Forex (Kill Switch) |
| `/forex_start` | Démarrer bot Forex |
| `/forex_today` | Résumé journée Forex |

### Commandes Crypto

| Commande | Description |
|----------|-------------|
| `/crypto_stats` | Statistiques Crypto |
| `/crypto_positions` | Positions ouvertes Crypto |
| `/crypto_stop` | Arrêter bot Crypto (Kill Switch) |
| `/crypto_start` | Démarrer bot Crypto |
| `/crypto_today` | Résumé journée Crypto |

### Commandes Globales

| Commande | Description |
|----------|-------------|
| `/start` | Démarrer / Aide |
| `/help` | Afficher l'aide complète |
| `/stats` | Stats Forex + Crypto combinées |
| `/stopall` | ⛔ ARRÊT D'URGENCE TOTAL |
| `/startall` | Démarrer les 2 systèmes |
| `/report` | Rapport complet détaillé |
| `/risk` | Niveau de risque global |
| `/closeall` | Fermer toutes positions |

### Notifications Automatiques

Le bot Telegram vous alerte automatiquement pour:

- 🎯 **Nouveau signal détecté** (avec détails setup)
- ✅ **Position ouverte** (Entry, SL, TPs)
- 💰 **TP1/TP2/TP3 atteints** (+profit)
- ⚠️ **Perte** (avec analyse pourquoi)
- 🔴 **News proche** (2h avant)
- 🚨 **Limites approchées** (drawdown, daily loss)
- ⛔ **Kill Switch activé** (raisons détaillées)
- 📊 **Rapport quotidien** (18h chaque jour)
- 📈 **Rapport hebdomadaire** (vendredi soir)

---

## ⚙️ CONFIGURATION

### Comptes Prop Firm

**FOREX:**
- **Broker**: FTMO
- **Challenge**: 40,000€
- **Risque**: 0.3% par trade
- **Max Daily Loss**: 400€
- **Max Total Drawdown**: 3,000€

**CRYPTO:**
- **Broker**: RaiseMyFunds
- **Compte**: 50,000$ (Account 1038450)
- **Risque**: 0.2% par trade
- **Max Daily Loss**: 500$
- **Max Total Drawdown**: 3,500$

### Paires Tradées

**FOREX:**
- ✅ EURUSD (principal)
- ✅ GBPUSD
- ✅ USDJPY

**CRYPTO:**
- ✅ BTCUSD
- ✅ ETHUSD

### Timeframes

- **Principal**: M30 (analyse principale)
- **Confirmation**: H1 + H4 (alignement)

---

## 🚀 INSTALLATION

### 📋 **[GUIDE COMPLET → INSTALLATION.md](INSTALLATION.md)**

**Résumé rapide:**

1. ✅ **Python 3.12+** installé
2. ✅ **MT5** installé (2 instances: Forex + Crypto)
3. ✅ Installer dépendances: `pip install -r requirements.txt`
4. ✅ Configurer `config.py` (tokens, capital)
5. ✅ Copier fichiers `.mq5` dans MT5
6. ✅ Autoriser WebRequest dans MT5
7. ✅ Lancer:
   - `python guardian_forex.py`
   - `python guardian_crypto.py`
   - `python telegram_bot.py`
8. ✅ Activer bots MT5 sur graphiques M30
9. ✅ Tester avec `/start` dans Telegram

---

## 📊 STATISTIQUES & MONITORING

### Base de Données SQLite

Chaque système maintient sa propre DB:

**Tables:**
- `trades`: Tous les trades (entry, exit, P&L, metadata)
- `signals`: Tous les signaux (approuvés + rejetés avec raison)
- `daily_stats`: Stats quotidiennes agrégées
- `economic_news`: Calendrier économique

### Métriques Trackées

- ✅ Win Rate
- ✅ Profit Factor
- ✅ Max Drawdown
- ✅ Average Win / Average Loss
- ✅ Nombre de trades (jour/semaine/mois)
- ✅ Trades par heure (détection overtrading)
- ✅ Pertes consécutives
- ✅ Temps entre trades
- ✅ Confluence score moyen
- ✅ Rejection reasons stats

---

## ⚠️ RÈGLES STRICTES - À RESPECTER

### 🚫 NE JAMAIS:

1. ❌ Trader pendant **périodes interdites** (24 déc - 3 jan!)
2. ❌ Désactiver **Kill Switch** si déclenché (attendre lendemain)
3. ❌ Augmenter risque **> 0.3%** (Forex) / **0.2%** (Crypto)
4. ❌ Forcer trade si **confluence < 90** (Forex) / **85** (Crypto)
5. ❌ Trader après **2 pertes** consécutives (revenge trading)
6. ❌ Modifier code **sans backup**
7. ❌ Laisser tourner **sans surveillance** (2 premières semaines)

### ✅ TOUJOURS:

1. ✅ Surveiller les **3 fenêtres CMD** (Guardians + Telegram)
2. ✅ Répondre aux **alertes Telegram**
3. ✅ Sauvegarder les **databases** chaque jour
4. ✅ Tester sur **compte démo** avant prop firm
5. ✅ Respecter les **règles prop firm** (max losses)
6. ✅ Analyser **CHAQUE trade** fermé (win/loss pourquoi?)
7. ✅ Tenir un **journal de trading**

---

## 💻 ENVIRONNEMENT TECHNIQUE

### Prérequis

- **OS**: Windows 10/11
- **Python**: 3.12+ (vous avez 3.12.8 ✅)
- **MT5**: Version 5.0+
- **RAM**: 8 GB minimum
- **Internet**: Connexion stable

### Dépendances Python

```
Flask==3.0.0
python-telegram-bot==20.7
requests==2.31.0
python-dateutil==2.8.2
colorlog==6.8.0
python-dotenv==1.0.0
```

Installation:
```bash
pip install -r requirements.txt
```

---

## 📁 FICHIERS DU PROJET

```
LaBete/
│
├── FOREX/
│   ├── guardian_forex.py               ← Guardian Forex (API Flask :5000)
│   ├── La_Bete_FOREX_V6_Ultimate.mq5   ← Bot MT5 Forex
│   ├── La_Bete_FOREX_V6_Template.mq5   ← Template commenté
│   ├── forex_trades.db                 ← Database Forex
│   └── logs/
│       └── guardian_forex.log
│
├── CRYPTO/
│   ├── guardian_crypto.py              ← Guardian Crypto (API Flask :5001)
│   ├── La_Bete_CRYPTO_V6_Ultimate.mq5  ← Bot MT5 Crypto
│   ├── crypto_trades.db                ← Database Crypto
│   └── logs/
│       └── guardian_crypto.log
│
├── SHARED/
│   ├── config.py                       ← Configuration centrale ⚙️
│   ├── telegram_bot.py                 ← Bot Telegram dual
│   ├── utils.py                        ← Utilitaires
│   └── models/                         ← ML models (optionnel)
│
├── requirements.txt                    ← Dépendances Python
├── INSTALLATION.md                     ← Guide installation complet
├── README.md                           ← Ce fichier
└── START_LA_BETE.bat                  ← Script de lancement Windows
```

---

## 🆘 SUPPORT & TROUBLESHOOTING

### Problèmes Fréquents

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Port already in use"**
```bash
taskkill /F /IM python.exe
```

**MT5 ne se connecte pas au Guardian**
- ✅ Vérifier Guardian lancé (`curl http://localhost:5000/health`)
- ✅ Vérifier WebRequest autorisé dans MT5
- ✅ Vérifier pare-feu Windows

**Bot Telegram ne répond pas**
- ✅ Vérifier token dans `config.py`
- ✅ Vérifier internet connecté
- ✅ Vérifier `telegram_bot.py` lancé

### Logs

- **Guardian Forex**: `LaBete/FOREX/logs/guardian_forex.log`
- **Guardian Crypto**: `LaBete/CRYPTO/logs/guardian_crypto.log`
- **MT5**: Onglet **Experts** dans MT5

---

## 📈 ROADMAP

### Version Actuelle: 6.0 Ultimate

**Implémenté:**
- ✅ Smart Money Concepts complet
- ✅ Système de confluence 100 points
- ✅ 7 niveaux de protection
- ✅ Kill Switch multi-triggers
- ✅ Bot Telegram dual control
- ✅ Guardians Python Flask API
- ✅ Filtres crypto spécifiques
- ✅ Anti-revenge trading
- ✅ Périodes interdites
- ✅ Database SQLite tracking

### Version Future: 6.1+

**Prévu:**
- [ ] Machine Learning pour filtrage signaux
- [ ] Dashboard Web temps réel
- [ ] Backtesting automatisé
- [ ] Optimisation paramètres génétique
- [ ] Support multi-broker
- [ ] Support TradingView alerts
- [ ] API calendrier économique avancée
- [ ] Analyse sentiment market
- [ ] Copy trading entre comptes
- [ ] Mobile app (iOS/Android)

---

## 📝 LICENSE

**Privé** - Usage personnel uniquement

Créé par **Yann** pour usage avec prop firm challenges.

**Disclaimer:** Ce système est un outil d'aide à la décision. Aucune garantie de profit. Le trading comporte des risques de perte en capital. À utiliser avec précaution.

---

## 🙏 REMERCIEMENTS

- **FTMO** pour les challenges prop firm
- **RaiseMyFunds** pour le compte actif
- **Communauté SMC** pour les concepts Smart Money
- **Python-Telegram-Bot** pour l'API Telegram
- **Flask** pour l'API REST
- **MetaQuotes** pour MT5

---

## 📞 CONTACT

- **Email**: kykylou30@gmail.com
- **Telegram Bot Token**: `8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE`
- **Telegram Chat ID**: `1981386789`

---

## ✅ PRÊT À TRADER

Une fois installé:

1. ✅ Lancer les 3 Guardians (Forex, Crypto, Telegram)
2. ✅ Activer les 2 bots MT5
3. ✅ Envoyer `/start` dans Telegram
4. ✅ Vérifier `/stats` → Tout à 0
5. ✅ **SURVEILLER** pendant 48h minimum
6. ✅ Analyser chaque signal/trade
7. ✅ **Laisser le système travailler**

---

**🐺 BON TRADING MA COUILLE ! 💎**

**Que La Bête soit avec toi ! ⚡**

---

*Créé le 08/01/2025*
*La Bête V6 Ultimate - Never Cramer Again*

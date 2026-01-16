# 🚀 DÉMARRAGE RAPIDE - LA BÊTE

**⏰ TEMPS TOTAL: 25 MINUTES**

---

## ⚡ ÉTAPES RAPIDES

### 1️⃣ INSTALLER PYTHON (5 min)
```bash
pip install python-telegram-bot requests beautifulsoup4 lxml pytz flask
```

### 2️⃣ CONFIGURER MT5 (5 min)
**Tools → Options → Expert Advisors**
- ✅ Cocher "Allow WebRequest for listed URL"
- ✅ Ajouter: `http://localhost:5000`
- ✅ Ajouter: `http://localhost:5001`

### 3️⃣ COMPILER BOTS (5 min)
Ouvrir MetaEditor et compiler:
- `FOREX/La_Bete_EUR.mq5`
- `FOREX/La_Bete_GBP.mq5`
- `FOREX/La_Bete_JPY.mq5`
- `FOREX/La_Bete_GOLD.mq5`
- `CRYPTO/La_Bete_BTC.mq5`
- `CRYPTO/La_Bete_ETH.mq5`

### 4️⃣ DÉMARRER SYSTÈME (3 min)
Double-clic: `START_SYSTEM.bat`
Choisir: **[4] TOUT**

Vérifier 3 fenêtres ouvertes:
- ✅ Guardian FOREX (port 5000)
- ✅ Guardian CRYPTO (port 5001)
- ✅ Telegram Bot Pro

### 5️⃣ CHARGER BOTS MT5 (5 min)
Sur MT5, M30:
- EUR/USD → La_Bete_EUR
- GBP/USD → La_Bete_GBP
- USD/JPY → La_Bete_JPY
- XAU/USD → La_Bete_GOLD
- BTC/USD → La_Bete_BTC
- ETH/USD → La_Bete_ETH

### 6️⃣ TESTER TELEGRAM (2 min)
Sur Telegram, envoyer: `/start`

Vérifier menu avec boutons:
```
🇪🇺 EUR/USD    🇬🇧 GBP/USD
🇯🇵 USD/JPY    🥇 GOLD
₿ BTC/USD     Ξ ETH/USD
📊 Vue Globale  ⚙️ Contrôle Total
```

---

## ✅ VÉRIFICATIONS RAPIDES

### Système Démarré?
```bash
# Voir les processus Guardian
http://localhost:5000  → doit afficher page Guardian Forex
http://localhost:5001  → doit afficher page Guardian Crypto
```

### Bots MT5 Actifs?
MT5 → Expert → Journal:
- Chercher: "🐺 LA BÊTE"
- Vérifier: "Guardian API: http://localhost:5000" (ou 5001)

### Telegram Fonctionne?
- `/start` → Menu graphique ✅
- Clic sur "🇪🇺 EUR/USD" → Menu EUR ✅
- Clic sur "📊 Stats" → Stats bot EUR ✅

---

## 🎯 STATUT SYSTÈME

**Tout est prêt:**
- ✅ 6 bots (10,346 lignes de code)
- ✅ Telegram déjà configuré
- ✅ Magic numbers: 666001-666004, 777001-777002
- ✅ Guardian ports: 5000 (Forex), 5001 (Crypto)

**Documents détaillés:**
- `CHECKLIST_DEMAIN_MIDI.md` - Version détaillée
- `VERIFICATION_SYSTEME.md` - Vérifications techniques
- `TEST_VERIFICATION_COMPLET.md` - Tests complets
- `README.md` - Guide complet

---

## 🏆 C'EST PARTI!

**Système LA BÊTE - Version 8 Ultimate**
**100% Prêt pour FTMO 40K** ✅

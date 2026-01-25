# 🤖 CONFIGURATION BOT TELEGRAM

## ÉTAPE 1: Créer le Bot Telegram (5 minutes)

### 1️⃣ Ouvrir Telegram et chercher **@BotFather**

### 2️⃣ Créer le bot:
```
/newbot
```

### 3️⃣ Donner un nom au bot:
```
La Bete Trading Bot
```

### 4️⃣ Donner un username (doit finir par "bot"):
```
labete_trading_bot
```

### 5️⃣ **COPIER LE TOKEN**
Tu vas recevoir un message comme:
```
Done! Congratulations on your new bot...
Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

**⚠️ GARDE CE TOKEN SECRET!**

---

## ÉTAPE 2: Obtenir ton Chat ID (2 minutes)

### 1️⃣ Chercher ton bot dans Telegram
- Cherche: `@labete_trading_bot` (ton username)

### 2️⃣ Démarrer une conversation
```
/start
```

### 3️⃣ Chercher **@userinfobot** dans Telegram

### 4️⃣ Envoyer `/start` à @userinfobot

### 5️⃣ **COPIER TON CHAT ID**
Tu vas recevoir:
```
Id: 123456789
```

---

## ÉTAPE 3: Configurer MT5 (1 minute)

### 1️⃣ Dans MT5 → **Outils > Options > Expert Advisors**

### 2️⃣ Cocher ✅ **Autoriser WebRequest pour les URL suivantes**

### 3️⃣ Ajouter cette URL:
```
https://api.telegram.org
```

### 4️⃣ Cliquer **OK**

---

## ÉTAPE 4: Configurer les Bots (30 secondes)

Quand tu attaches le bot sur le graphique, configure:

### Paramètres Telegram:
- **TelegramBotToken**: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` (ton token)
- **TelegramChatID**: `123456789` (ton chat ID)
- **EnableTelegramNotifications**: `true` ✅

---

## 📱 NOTIFICATIONS QUE TU RECEVRAS:

✅ **Démarrage du bot**
```
🚀 BOT DÉMARRÉ
🤖 Bot: La Bete BTC V12
📊 Paire: BTCUSD
💰 Balance: 100000.00 EUR
```

✅ **Position ouverte**
```
🟢 POSITION OUVERTE
📊 Paire: BTCUSD
📈 Direction: BUY
💰 Volume: 0.50 lots
🎯 Prix: 45250.00
🛑 SL: 45100.00
✅ TP: 45550.00
```

✅ **Position fermée**
```
✅ POSITION FERMÉE
📊 Paire: BTCUSD
📈 Direction: BUY
💚 Profit: +150.00 EUR
📌 Raison: Take Profit
```

✅ **Résumé quotidien** (chaque jour à 23:59)
```
📊 RÉSUMÉ QUOTIDIEN
📈 Paire: BTCUSD
🔢 Trades: 12
✅ Gagnants: 8
❌ Perdants: 4
📊 Win Rate: 66.7%
💚 Profit: +450.00 EUR
```

---

## ⚠️ SÉCURITÉ:

- ❌ **NE PARTAGE JAMAIS** ton Bot Token
- ❌ **NE PUBLIE JAMAIS** ton Chat ID
- ✅ Si tu perds le token → Créer un nouveau bot
- ✅ Seul TOI recevras les notifications (ton Chat ID)

---

## 🧪 TEST:

Une fois configuré, le bot enverra un message au démarrage:
```
🚀 BOT DÉMARRÉ
```

Si tu reçois ce message → ✅ Telegram fonctionne!

# 📱 TELEGRAM SIGNAL COPIER

Copiez automatiquement vos signaux Telegram vers MT5!

## 🎯 FONCTIONNALITÉS

- ✅ **Parse automatiquement** les signaux de Telegram
- ✅ **Envoie à MT5** pour exécution immédiate
- ✅ **Risk management** géré par le bot MT5 (calcul auto du lot size)
- ✅ **Multi-TP** support (jusqu'à 3 TPs)
- ✅ **Validation** des signaux avant envoi
- ✅ **Statistiques** et monitoring en temps réel

---

## 📋 FORMAT DE SIGNAL SUPPORTÉ

### Format standard:
```
XAUUSD BUY NOW 5082
SL 5070
TP 5090
TP 5100
TP 5135
```

### Format avec @:
```
BTCUSD SELL @ 95000
SL 96000
TP 94000
TP 93000
```

### Avec alias:
```
GOLD BUY 5082
SL 5070
TP 5090
TP 5100
```

---

## 🔧 INSTALLATION

### 1️⃣ **Installation Python (Windows)**

```bash
# Installer les dépendances
pip install -r requirements.txt
```

### 2️⃣ **Configuration**

Éditer `config.json`:
```json
{
  "telegram": {
    "bot_token": "VOTRE_TOKEN_BOT",
    "authorized_chat_id": "VOTRE_CHAT_ID"
  },
  "mt5": {
    "signals_folder": "C:/Trading/LaBete/SIGNALS"
  }
}
```

**Obtenir votre Bot Token:**
1. Ouvrir Telegram
2. Chercher `@BotFather`
3. `/newbot` → Suivre instructions
4. Copier le token

**Obtenir votre Chat ID:**
1. Chercher `@userinfobot` sur Telegram
2. `/start`
3. Copier votre Chat ID

### 3️⃣ **Créer le dossier signaux**

```
C:\Trading\LaBete\SIGNALS\
```

Le bot Python écrira les signaux ici.
Le bot MT5 les lira de ce dossier.

### 4️⃣ **Installation du bot MT5**

1. Copier `SignalReader_V13.mq5` dans:
   ```
   C:\Users\[USER]\AppData\Roaming\MetaQuotes\Terminal\[ID]\MQL5\Experts\
   ```

2. Compiler dans MetaEditor (F7)

3. Attacher sur un graphique M1 (n'importe quel symbole)

4. Configurer:
   - `SignalsFolder` = `C:\Trading\LaBete\SIGNALS\`
   - `RiskPercent` = `0.5` (ou votre risque préféré)
   - `EnableTelegram` = `true` (pour confirmations)

---

## 🚀 UTILISATION

### 1️⃣ **Démarrer le bot Python**

```bash
python signal_copier.py
```

Vous verrez:
```
🚀 DÉMARRAGE DU BOT TELEGRAM SIGNAL COPIER
✅ Bot connecté!
📱 En écoute des messages de Chat ID: 1981386789
⌛ Bot en attente de signaux...
```

### 2️⃣ **Démarrer le bot MT5**

1. Ouvrir MT5
2. Attacher `SignalReader_V13` sur un graphique
3. Activer AutoTrading (bouton dans MT5)

### 3️⃣ **Envoyer un signal**

Sur Telegram, envoyer au bot:
```
XAUUSD BUY NOW 5082
SL 5070
TP 5090
TP 5100
TP 5135
```

Le bot répondra:
```
📊 SIGNAL DÉTECTÉ
🎯 Symbole: XAUUSD
📈 Direction: BUY
💰 Entrée: 5082.00
🛡️ SL: 5070.00 (12.0 pts)
🎯 Take Profits:
   TP1: 5090.00 (+8.0 pts, R:R 1:0.7)
   TP2: 5100.00 (+18.0 pts, R:R 1:1.5)
   TP3: 5135.00 (+53.0 pts, R:R 1:4.4)

✅ Signal envoyé au bot MT5!
```

### 4️⃣ **Le bot MT5 exécute**

- ✅ Lit le fichier signal JSON
- ✅ Calcule lot size automatiquement (selon RiskPercent)
- ✅ Ouvre position avec SL
- ✅ Place 3 TPs (fermetures partielles)
- ✅ Envoie confirmation Telegram

---

## 📊 COMMANDES TELEGRAM

| Commande | Description |
|----------|-------------|
| `/start` | Afficher message de bienvenue |
| `/status` | Voir status bot + signaux MT5 |
| `/stats` | Voir statistiques session |
| `/help` | Aide et exemples |

---

## 🎯 SYMBOLES SUPPORTÉS

| Alias | Symbole MT5 |
|-------|-------------|
| `GOLD` | XAUUSD |
| `BTC` | BTCUSD |
| `ETH` | ETHUSD |
| `EUR` | EURUSD |
| `GBP` | GBPUSD |
| `JPY` | USDJPY |

---

## ⚙️ WORKFLOW COMPLET

```
┌─────────────┐
│   TELEGRAM  │  "XAUUSD BUY NOW 5082..."
│   (TOI)     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  PYTHON BOT     │  • Parse signal
│  signal_copier  │  • Valide format
│                 │  • Crée fichier JSON
└──────┬──────────┘
       │
       ▼
┌──────────────────────┐
│  FICHIER JSON        │
│  C:/Trading/LaBete/  │
│  SIGNALS/            │
│  signal_XAUUSD_...   │
└──────┬───────────────┘
       │
       ▼
┌─────────────────────┐
│  MT5 BOT            │  • Lit JSON
│  SignalReader_V13   │  • Calcule lot size
│                     │  • Ouvre trade
│                     │  • Place SL/TPs
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│  TELEGRAM   │  "✅ GOLD BUY ouvert @ 5082"
│  (TOI)      │
└─────────────┘
```

---

## 🛡️ SÉCURITÉ

- ✅ **Chat ID autorisé** - Seul votre Chat ID peut envoyer signaux
- ✅ **Validation signaux** - Format vérifié avant envoi
- ✅ **Risk management** - Lot size calculé automatiquement
- ✅ **Protection FTMO** - Limites de drawdown respectées

---

## 📝 FICHIERS

```
TelegramSignalCopier/
├── signal_copier.py       # Bot Telegram principal
├── signal_parser.py       # Parser de signaux
├── mt5_executor.py        # Envoi vers MT5
├── config.json            # Configuration
├── requirements.txt       # Dépendances Python
├── README.md              # Ce fichier
└── SignalReader_V13.mq5   # Bot MT5 (à venir)
```

---

## ❓ FAQ

**Q: Le bot MT5 calcule le lot size comment?**
A: Basé sur `RiskPercent` (par défaut 0.5% du compte) et la distance SL.

**Q: Que se passe-t-il si le signal est invalide?**
A: Le bot Python répond avec erreur. Rien n'est envoyé à MT5.

**Q: Combien de TPs maximum?**
A: 3 TPs maximum. Si plus, seuls les 3 premiers sont utilisés.

**Q: Le bot fonctionne 24/7?**
A: Oui, tant que le bot Python tourne et MT5 est ouvert.

**Q: Puis-je envoyer plusieurs signaux en même temps?**
A: Oui! Envoyez-les un par un. Chaque signal est traité indépendamment.

---

## 🚨 DÉPANNAGE

**Problème: Bot Python ne démarre pas**
```bash
# Vérifier installation
pip install -r requirements.txt

# Vérifier config.json existe et est valide
cat config.json
```

**Problème: Signal pas exécuté sur MT5**
- ✅ Vérifier que `SignalReader_V13` est attaché sur graphique
- ✅ Vérifier AutoTrading activé (bouton vert dans MT5)
- ✅ Vérifier dossier `C:/Trading/LaBete/SIGNALS/` existe
- ✅ Vérifier fichier JSON créé dans le dossier

**Problème: Bot Telegram ne répond pas**
- ✅ Vérifier `bot_token` correct dans config.json
- ✅ Vérifier `authorized_chat_id` correct
- ✅ Envoyer `/start` au bot sur Telegram

---

## 📞 SUPPORT

Pour questions ou problèmes:
1. Vérifier ce README
2. Tester avec `/help` sur le bot
3. Vérifier les logs du bot Python

---

**🎉 BON TRADING!**

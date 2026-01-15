# ✅ CHECKLIST DÉMARRAGE - DEMAIN MIDI

**Date: 16 Janvier 2025 - 12:00**

---

## 📋 ORDRE D'EXÉCUTION (30 MINUTES)

### ⏰ **12:00 - ÉTAPE 1: INSTALLATION PYTHON (5 min)**

```bash
# Ouvrir CMD en Administrateur
pip install python-telegram-bot requests beautifulsoup4 lxml pytz flask

# Vérifier installation
pip list | findstr telegram
pip list | findstr beautifulsoup4
```

✅ **Résultat attendu:** Toutes les librairies installées

---

### ⏰ **12:05 - ÉTAPE 2: CONFIGURATION MT5 (5 min)**

1. **Ouvrir MT5**
2. **Aller à:** Outils > Options > Expert Advisors
3. **Cocher:** "Autoriser WebRequest pour les URLs listées"
4. **Ajouter ces URLs:**
   ```
   http://localhost:5000
   http://localhost:5001
   https://www.forexfactory.com
   ```
5. **Cliquer:** OK

✅ **Résultat attendu:** 3 URLs dans la liste blanche

---

### ⏰ **12:10 - ÉTAPE 3: CONFIGURATION TELEGRAM (5 min)**

1. **Ouvrir:** `LaBete/SHARED/config.py`

2. **Modifier ces lignes:**
   ```python
   TELEGRAM_BOT_TOKEN = "VOTRE_TOKEN_ICI"
   TELEGRAM_CHAT_ID = "VOTRE_CHAT_ID_ICI"
   ```

3. **Comment obtenir le token:**
   - Ouvrir Telegram
   - Parler à @BotFather
   - Taper `/newbot`
   - Suivre instructions
   - Copier le token

4. **Comment obtenir chat_id:**
   - Parler à @userinfobot
   - Copier votre ID

✅ **Résultat attendu:** Token et Chat ID configurés

---

### ⏰ **12:15 - ÉTAPE 4: COMPILER LES BOTS (5 min)**

1. **Ouvrir MetaEditor** (depuis MT5)

2. **Ouvrir et compiler CHAQUE fichier** (F7):
   ```
   ☐ LaBete/FOREX/La_Bete_EUR.mq5
   ☐ LaBete/FOREX/La_Bete_GBP.mq5
   ☐ LaBete/FOREX/La_Bete_JPY.mq5
   ☐ LaBete/FOREX/La_Bete_GOLD.mq5
   ☐ LaBete/CRYPTO/La_Bete_BTC.mq5
   ☐ LaBete/CRYPTO/La_Bete_ETH.mq5
   ```

3. **Vérifier:** 0 erreur, 0 warning pour chaque

✅ **Résultat attendu:** 6 fichiers .ex5 créés

---

### ⏰ **12:20 - ÉTAPE 5: DÉMARRER LE SYSTÈME (3 min)**

1. **Double-cliquer:** `LaBete/START_SYSTEM.bat`

2. **Choisir:** `[4] TOUT`

3. **Vérifier 3 fenêtres CMD ouvertes:**
   ```
   ☐ Guardian FOREX (port 5000)
   ☐ Guardian CRYPTO (port 5001)
   ☐ Telegram Bot Pro
   ```

4. **Vérifier messages dans chaque fenêtre:**
   - "✅ Guardian démarré"
   - "✅ Bot Telegram opérationnel"

✅ **Résultat attendu:** 3 fenêtres actives sans erreur

---

### ⏰ **12:23 - ÉTAPE 6: CHARGER BOTS MT5 (5 min)**

**Pour CHAQUE paire, glisser le bot sur graphique M30:**

```
☐ EURUSD M30  → Glisser La_Bete_EUR.mq5
☐ GBPUSD M30  → Glisser La_Bete_GBP.mq5
☐ USDJPY M30  → Glisser La_Bete_JPY.mq5
☐ XAUUSD M30  → Glisser La_Bete_GOLD.mq5
☐ BTCUSD M30  → Glisser La_Bete_BTC.mq5
☐ ETHUSD M30  → Glisser La_Bete_ETH.mq5
```

**Vérifier dans l'onglet "Expert":**
- 6 bots actifs
- Tous affichent "Système initialisé avec succès"

✅ **Résultat attendu:** 6 bots tournent sur MT5

---

### ⏰ **12:28 - ÉTAPE 7: TESTER TELEGRAM (2 min)**

1. **Ouvrir Telegram**

2. **Chercher votre bot** (nom donné à BotFather)

3. **Taper:** `/start`

4. **Vérifier que tu vois:**
   ```
   ╔════════════════════════════════════╗
   ║   🐺 LA BÊTE - PROP FIRM SYSTEM   ║
   ╚════════════════════════════════════╝

   [🇪🇺 EUR/USD]  [🇬🇧 GBP/USD]
   [🇯🇵 USD/JPY]  [🥇 GOLD]
   [₿ BTC/USD]    [Ξ ETH/USD]

   [📊 Vue Globale]  [⚙️ Contrôle Total]
   ```

5. **Tester:** Cliquer sur `🇪🇺 EUR/USD`

6. **Vérifier menu EUR:**
   ```
   [📊 Stats]        [📈 Positions]
   [✅ Start]        [❌ Stop]
   [🔍 Analyse]      [📅 News]
   ```

✅ **Résultat attendu:** Telegram répond avec boutons

---

### ⏰ **12:30 - ÉTAPE 8: VÉRIFICATION FINALE (2 min)**

**Checklist finale:**

```
☐ 3 fenêtres CMD actives (Guardian Forex, Crypto, Telegram)
☐ MT5 ouvert avec 6 graphiques M30
☐ 6 bots actifs dans onglet Expert MT5
☐ Telegram répond aux commandes
☐ Aucune erreur dans les logs
```

**Tester une commande:**
```
/eur → Clique 📊 Stats
```

Tu dois voir les stats EUR/USD!

✅ **SYSTÈME OPÉRATIONNEL!**

---

## 🚨 EN CAS DE PROBLÈME

### Problème 1: Guardian ne démarre pas

```bash
# Vérifier ports libres
netstat -an | findstr :5000
netstat -an | findstr :5001

# Si occupé
taskkill /F /IM python.exe

# Redémarrer
START_SYSTEM.bat → [4]
```

### Problème 2: MT5 refuse connexion

**Vérifier dans MT5 > Options > Expert Advisors:**
- ✅ WebRequest activé
- ✅ localhost:5000 dans la liste
- ✅ localhost:5001 dans la liste

### Problème 3: Telegram ne répond pas

```bash
# Tester le token
curl https://api.telegram.org/bot<TON_TOKEN>/getMe
```

Si erreur → Revérifier token dans config.py

### Problème 4: Bot ne compile pas

**Erreurs courantes:**
- Vérifier que MT5 est à jour
- Redémarrer MetaEditor
- Vérifier syntaxe du code

---

## 📱 COMMANDES TELEGRAM UTILES

**Après démarrage:**

```
/start     → Menu principal
/eur       → Menu EUR/USD
/gbp       → Menu GBP/USD
/jpy       → Menu USD/JPY
/gold      → Menu GOLD
/btc       → Menu BTC/USD
/eth       → Menu ETH/USD
```

**Dans chaque menu:**
- 📊 Stats → Performance
- 📈 Positions → Trades en cours
- 🔍 Analyse → Confluence actuel
- 📅 News → Calendrier économique
- ✅ Start → Activer bot
- ❌ Stop → Désactiver bot

---

## ⏰ TEMPS TOTAL: ~30 MINUTES

**Répartition:**
- Installation Python: 5 min
- Config MT5: 5 min
- Config Telegram: 5 min
- Compilation bots: 5 min
- Démarrage système: 3 min
- Chargement MT5: 5 min
- Test Telegram: 2 min

---

## ✅ APRÈS DÉMARRAGE

**Telegram deviendra ton tableau de bord:**

1. **Surveillance:** Recevoir notifications automatiques
2. **Contrôle:** Start/Stop bots individuellement
3. **Stats:** Voir performance en temps réel
4. **Positions:** Suivre trades en cours
5. **News:** Vérifier calendrier économique

**Plus besoin d'ouvrir MT5 constamment!**

---

## 📞 SUPPORT

**Si bloqué:**

1. Consulter `GUIDE_PROP_FIRM.md` (guide détaillé)
2. Regarder les logs dans `LOGS/`
3. Vérifier connexions (netstat)

---

**🐺 SYSTÈME PRÊT POUR FTMO 40K!**

_Checklist créée le 15/01/2025 - Prête pour démarrage 16/01/2025 12:00_

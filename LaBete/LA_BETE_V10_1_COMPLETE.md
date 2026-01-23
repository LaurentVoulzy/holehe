# 🐺 LA BÊTE V10 - DOCUMENTATION COMPLÈTE

## 📋 VUE D'ENSEMBLE

**Version :** 10.00
**Date :** 23 Janvier 2026
**Statut :** ✅ COMPLET - 6 bots créés et testables

---

## 🎯 BOTS CRÉÉS (6 au total)

### FOREX (4 bots)
1. **La_Bete_EUR_V10.mq5** - EUR/USD
2. **La_Bete_GBP_V10.mq5** - GBP/USD
3. **La_Bete_JPY_V10.mq5** - USD/JPY
4. **La_Bete_GOLD_V10.mq5** - XAU/USD (Or)

### CRYPTO (2 bots)
5. **La_Bete_BTC_V10.mq5** - BTC/USD
6. **La_Bete_ETH_V10.mq5** - ETH/USD

---

## 🚀 NOUVEAUTÉS V10 vs V9

### ❌ V9 - Problèmes identifiés
- Signal : EMA 20 × EMA 200 (1-2 trades par MOIS)
- Confluence : 85/100 (trop strict)
- Certitude : 50% (trop strict)
- **Résultat : AUCUN TRADE**

### ✅ V10 - Solutions apportées
- Signal : **MA 2 × MA 12** (5-10 trades par SEMAINE)
- Confluence : **35-40/100** (plus permissif)
- Certitude : **30-35%** (plus permissif)
- **Support/Résistance** : Détection H1 + Buy/Sell Limit
- **Résultat attendu : 5-10 trades/semaine avec Win Rate 50-60%**

---

## 📊 STRATÉGIE COMPLÈTE

### 1. SIGNAL D'ENTRÉE (MA2 × MA12)

```
🟢 BUY : MA2 croise MA12 à la HAUSSE
🔴 SELL : MA2 croise MA12 à la BAISSE

Fréquence attendue : 5-10 signaux par semaine
```

### 2. SUPPORT & RÉSISTANCE (H1)

**Détection automatique :**
- Swing Highs = **Résistances** (lignes rouges)
- Swing Lows = **Supports** (lignes vertes)
- Affichage sur graphique MT5

**Ordres Limites automatiques :**
- **Buy Limit** placé sur SUPPORT
  - Entry : 5 pips AU-DESSUS du support
  - SL : 10 pips EN-DESSOUS du support
  - TP : SL × 2.0 (Risk:Reward 1:2)

- **Sell Limit** placé sur RÉSISTANCE
  - Entry : 5 pips EN-DESSOUS de la résistance
  - SL : 10 pips AU-DESSUS de la résistance
  - TP : SL × 2.0 (Risk:Reward 1:2)

**Gestion intelligente :**
- Max 3 ordres limites simultanés
- Annulation automatique si S/R cassé
- Expiration après 240 minutes (optionnel)

### 3. SL/TP DYNAMIQUES (ATR)

**Stop Loss :**
```
SL = ATR × Multiplicateur
```
- FOREX : ATR × 2.0 (min 30 pips, max 100 pips)
- CRYPTO : ATR × 2.5 (min 50 pips, max 200 pips)
- GOLD : ATR × 2.0 (min 30 pips, max 150 pips)

**Take Profits multiples :**
```
TP1 = Entry + (SL × 2.0) → Fermer 50% de la position
TP2 = Entry + (SL × 3.0) → Fermer 30% de la position
TP3 = Entry + (SL × 5.0) → Fermer 20% de la position
```

**Trailing Stop :**
- Activé après TP1
- Distance = ATR × 0.5

### 4. PROTECTION FTMO

**Limites strictes :**
```
Daily Loss Max : -€2,000
Drawdown Total Max : -€4,000
Trades Max/jour : 20
```

**Alertes progressives :**
```
-€1,700 daily → Alerte + Réduction lots 50%
-€3,500 drawdown → Alerte + Réduction lots 30%
-€2,000 daily → ARRÊT TOTAL
-€4,000 drawdown → ARRÊT TOTAL
```

### 5. FILTRE NEWS (FOREX uniquement)

**Source :** ForexFactory.com
**Filtrage :** HIGH IMPACT uniquement

**Devise spécifique :**
- EUR bot → News EUR uniquement
- GBP bot → News GBP uniquement
- JPY bot → News JPY uniquement
- GOLD bot → News USD uniquement

**Actions :**
- 15min AVANT news : Réduction lots 50%
- 15min APRÈS news : Retour normal

---

## ⚙️ PARAMÈTRES PAR DEVISE

| Devise | Magic# | Risque | SL Min/Max | ATR Mult | News | Port Guardian |
|--------|--------|--------|------------|----------|------|---------------|
| **EUR** | 777100 | 0.3% | 30-100 pips | 2.0 | EUR | 5000 |
| **GBP** | 777101 | 0.25% | 30-100 pips | 2.0 | GBP | 5000 |
| **JPY** | 777102 | 0.3% | 30-100 pips | 2.0 | JPY | 5000 |
| **GOLD** | 777103 | 0.2% | 30-150 pips | 2.0 | USD | 5000 |
| **BTC** | 777001 | 0.25% | 50-200 pips | 2.5 | - | 5001 |
| **ETH** | 777002 | 0.25% | 50-200 pips | 2.5 | - | 5001 |

---

## 📝 INSTALLATION MT5

### Étape 1 : Copier les fichiers

**Sur votre PC Windows :**
```
C:\Users\Utilisateur\Documents\GitHub\kylou\LaBete\
├── FOREX\
│   ├── La_Bete_EUR_V10.mq5
│   ├── La_Bete_GBP_V10.mq5
│   ├── La_Bete_JPY_V10.mq5
│   └── La_Bete_GOLD_V10.mq5
└── CRYPTO\
    ├── La_Bete_BTC_V10.mq5
    └── La_Bete_ETH_V10.mq5
```

**Copier vers MT5 :**
```
C:\Users\Utilisateur\AppData\Roaming\MetaQuotes\Terminal\[ID]\MQL5\Experts\
```

### Étape 2 : Compiler dans MetaEditor

1. Ouvrir MetaEditor (F4 dans MT5)
2. Ouvrir chaque fichier .mq5
3. Compiler (F7 ou bouton "Compile")
4. Vérifier qu'il génère un .ex5

### Étape 3 : Configurer MT5

**Autoriser WebRequest :**
```
MT5 → Outils → Options → Expert Advisors → Onglet "Expert Consultants"
Cocher "Autoriser WebRequest pour les URL listées"
Ajouter :
- http://127.0.0.1:5000
- http://127.0.0.1:5001
```

### Étape 4 : Lancer les Guardians

**Sur Windows (CMD) :**
```
cd C:\Users\Utilisateur\Documents\GitHub\kylou\LaBete
START_LA_BETE.bat
```

Vérifier que 3 fenêtres CMD s'ouvrent :
- Guardian FOREX (port 5000)
- Guardian CRYPTO (port 5001)
- Bot Telegram Ultra V10

### Étape 5 : Charger les bots sur MT5

**Pour chaque paire :**
1. Ouvrir chart (M30 recommandé)
2. Glisser-déposer le bot depuis Navigator
3. Configurer si besoin (ou laisser défaut)
4. Activer "Algo Trading" (bouton vert en haut)

**Charts à créer :**
- EUR/USD M30 → La_Bete_EUR_V10
- GBP/USD M30 → La_Bete_GBP_V10
- USD/JPY M30 → La_Bete_JPY_V10
- XAU/USD M30 → La_Bete_GOLD_V10
- BTC/USD M30 → La_Bete_BTC_V10
- ETH/USD M30 → La_Bete_ETH_V10

---

## 🎨 VISUALISATION SUR MT5

**Lignes S/R automatiques :**
- **Lignes VERTES** = Supports
- **Lignes ROUGES** = Résistances
- **Labels** avec prix exact

**Ordres en attente visibles :**
- Buy Limit sur supports (flèche verte ↗)
- Sell Limit sur résistances (flèche rouge ↘)

---

## 📊 MONITORING TELEGRAM

**Commandes disponibles :**
```
/status        - État de tous les bots
/dashboard     - Dashboard FTMO complet
/daily         - Rapport quotidien
/pnl           - Profit & Loss
/params        - Voir paramètres actuels

/eur_params 60 45  - Modifier EUR (confluence 60, certitude 45)
/btc_params 55 42  - Modifier BTC

/emergency_stop    - Arrêt d'urgence
/close_losing      - Fermer trades perdants
/secure_profits    - Sécuriser profits
```

---

## 🧪 TESTS RECOMMANDÉS

### Phase 1 : DEMO (2-3 semaines)
1. Lancer sur compte DEMO
2. Vérifier que des trades s'ouvrent
3. Observer Win Rate et fréquence
4. Ajuster paramètres si besoin

### Phase 2 : Validation
**Objectifs :**
- 5-10 trades par semaine minimum
- Win Rate > 45%
- Respect limites FTMO

**Si problèmes :**
- Trop de trades → Augmenter confluence/certitude
- Pas assez → Baisser confluence/certitude
- Win Rate trop bas → Augmenter confluence

### Phase 3 : LIVE (si validation OK)
1. Passer sur compte FTMO
2. Commencer avec 1-2 bots seulement
3. Étendre progressivement

---

## ⚠️ AVERTISSEMENTS IMPORTANTS

### 1. NE PAS trader si :
- Guardian APIs ne sont pas lancés
- URLs WebRequest pas autorisées dans MT5
- Compte proche des limites FTMO

### 2. Vérifications quotidiennes :
```
✅ Guardian APIs actifs (3 fenêtres CMD)
✅ Bots MT5 avec visage souriant 😊
✅ "Algo Trading" activé (bouton vert)
✅ Lignes S/R visibles sur charts
✅ Daily Loss < -€1,500
```

### 3. En cas de perte série :
- Vérifier les logs MT5 (onglet "Experts")
- Checker Telegram /daily
- Augmenter confluence si < 40% Win Rate
- Arrêter manuellement si besoin

---

## 📈 RÉSULTATS ATTENDUS

**Avec paramètres par défaut :**
```
Trades par semaine : 5-10 (par bot)
Win Rate cible : 50-60%
Risk:Reward moyen : 1:2 à 1:3
Profit hebdo cible : +€800 (objectif FTMO)
```

**Scénario réaliste (6 bots actifs) :**
```
Semaine 1 : 30-50 trades total
  - 15-25 wins (50% WR)
  - Profit : +€500 à +€1,200

Mois 1 : 120-200 trades total
  - Objectif FTMO : +€2,000 ✅
```

---

## 🛠️ DÉPANNAGE

### Problème : Aucun trade
**Solutions :**
1. Vérifier qu'il y a eu au moins 1 crossover MA2×12 récent
2. Baisser confluence à 30, certitude à 25
3. Vérifier logs "Experts" pour erreurs

### Problème : Ordres limites ne se placent pas
**Solutions :**
1. Vérifier que ShowSR = true
2. Vérifier que UseLimitOrders = true
3. Vérifier que des S/R ont été détectés (lignes visibles)
4. Check logs pour erreurs placement

### Problème : Bot "Offline" dans Telegram
**Normal !** Le statut se met à jour au prochain trade ou heartbeat.

### Problème : Guardian API ne répond pas
**Solutions :**
1. Relancer START_LA_BETE.bat
2. Vérifier ports 5000 et 5001 disponibles
3. Check firewall Windows

---

## 📞 SUPPORT

**En cas de problème :**
1. Vérifier ce document
2. Lire logs MT5 (onglet "Experts" et "Journal")
3. Vérifier Telegram /status
4. Fournir screenshots si aide nécessaire

---

## 🎯 PROCHAINES ÉTAPES

**Maintenant, vous devez :**
1. ✅ Pull les changements GitHub Desktop
2. ✅ Compiler les 6 bots dans MetaEditor
3. ✅ Lancer START_LA_BETE.bat
4. ✅ Charger les bots sur MT5
5. ✅ Tester sur DEMO pendant 2 semaines
6. ✅ Analyser résultats
7. ✅ Passer en LIVE si validation OK

---

**🐺 BON TRADING AVEC LA BÊTE V10 ! 🚀**

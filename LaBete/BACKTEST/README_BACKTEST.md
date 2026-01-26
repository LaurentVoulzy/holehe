# 📊 GUIDE BACKTEST - LA BETE V12

## 📁 FICHIERS .SET DISPONIBLES

### 1️⃣ `La_Bete_BTC_V12_BACKTEST.set` (RECOMMANDÉ)
**Paramètres par défaut:**
- MinConfluenceScore: 85
- MinCertaintyPercent: 80
- Très sélectif, haute qualité

### 2️⃣ `La_Bete_BTC_V12_AGGRESSIVE.set`
**Plus de trades:**
- MinConfluenceScore: 70
- MinCertaintyPercent: 65
- Moins sélectif, plus de trades

---

## 🚀 COMMENT UTILISER LES FICHIERS .SET

### ÉTAPE 1: COPIER LES FICHIERS .SET

**Windows:**
```
Copier de: C:\Users\Utilisateur\Documents\GitHub\kylou\LaBete\BACKTEST\*.set
Copier vers: C:\Users\Utilisateur\AppData\Roaming\MetaQuotes\Terminal\[ID_TERMINAL]\MQL5\Profiles\Tester\
```

**OU plus simple:**
Dans MT5, ouvrir Strategy Tester → Onglet "Paramètres" → Bouton "Charger" → Parcourir vers le dossier BACKTEST

---

### ÉTAPE 2: OUVRIR STRATEGY TESTER

**Dans MT5:**
- Menu: Affichage → Strategy Tester
- Ou: CTRL + R

---

### ÉTAPE 3: CONFIGURATION

| Paramètre | Valeur |
|-----------|--------|
| **Expert Advisor** | La_Bete_BTC_V12 |
| **Symbole** | BTCUSD |
| **Période** | M30 |
| **Date début** | 01/12/2025 |
| **Date fin** | 26/01/2026 |
| **Dépôt** | 39649 (ton solde) |
| **Effet de levier** | 1:100 |
| **Modèle** | Tous les ticks |

---

### ÉTAPE 4: CHARGER LE FICHIER .SET

**Dans Strategy Tester:**
1. Onglet **"Paramètres"**
2. Bouton **"Charger"** (en haut à droite)
3. Sélectionner: `La_Bete_BTC_V12_BACKTEST.set`
4. Vérifier que les paramètres sont chargés

**Paramètres importants automatiquement configurés:**
- ✅ EnableTelegramNotifications = false
- ✅ RequireApproval = false
- ✅ CheckEconomicNews = false
- ✅ MinConfluenceScore = 85
- ✅ MinCertaintyPercent = 80

---

### ÉTAPE 5: LANCER LE TEST

Cliquer sur **"Démarrer"**

---

## 📈 RÉSULTATS À ANALYSER

### ✅ INDICATEURS CLÉS:

**Performance:**
- **Profit total** → Doit être positif
- **Profit factor** → > 1.5 = excellent
- **Drawdown max** → < €4000 (limite FTMO)
- **Win rate** → Cible: 55-65%

**Risque:**
- **Plus grosse perte** → < €2000 (daily loss FTMO)
- **Consecutive losses** → Max 3-4 acceptable
- **Recovery factor** → > 3 = bon

**Volume:**
- **Total trades** → 15-30 trades sur 2 mois = bon
- **Trades/jour** → < 2 (conforme MaxTradesPerDay)

---

## 🧪 SCÉNARIOS DE TEST

### Test 1️⃣ - BASELINE (2 mois)
```
Fichier: La_Bete_BTC_V12_BACKTEST.set
Période: 01/12/2025 - 26/01/2026
But: Validation fonctionnelle
```

### Test 2️⃣ - AGRESSIF (2 mois)
```
Fichier: La_Bete_BTC_V12_AGGRESSIVE.set
Période: 01/12/2025 - 26/01/2026
But: Plus de trades, comparaison
```

### Test 3️⃣ - LONG TERME (6 mois)
```
Fichier: La_Bete_BTC_V12_BACKTEST.set
Période: 01/08/2025 - 26/01/2026
But: Validation robustesse
```

---

## ⚠️ IMPORTANT - LIMITATIONS DU BACKTEST

### ❌ NE FONCTIONNERA PAS:
- Telegram (WebRequest désactivé en backtest)
- Guardian Python (API externe)
- News économiques (pas de données)

### ✅ FONCTIONNERA:
- Stratégie MA20 × MA50 ✅
- VWAP H1 + Bandes SD ✅
- ATR dynamic SL/TP ✅
- Triple TP (TP1/TP2/TP3) ✅
- Break Even ✅
- Trailing Stop ✅
- Protection FTMO ✅

---

## 🎯 OPTIMISATION (AVANCÉ)

**Pour trouver les meilleurs paramètres:**

1. Ouvrir Strategy Tester
2. Cocher: **"Optimisation"**
3. Sélectionner paramètres à optimiser:
   - MinConfluenceScore (65-95, step 5)
   - MinCertaintyPercent (60-90, step 5)
   - ATR_Multiplier_SL (1.5-3.0, step 0.5)
   - TP1_RR (1.5-3.0, step 0.5)
4. Critère d'optimisation: **"Profit Factor"**
5. Lancer (⚠️ Peut prendre plusieurs heures!)

---

## 📊 COMPARAISON DES PROFILS

| Profil | Trades/2mois | Win Rate | Profit Factor | Drawdown |
|--------|--------------|----------|---------------|----------|
| **BACKTEST** | 15-20 | 60-70% | 2.0-2.5 | Faible |
| **AGGRESSIVE** | 25-35 | 55-65% | 1.5-2.0 | Moyen |

**Recommandation:** Commencer avec BACKTEST (plus sûr)

---

## 🚀 APRÈS LE BACKTEST

**Si résultats positifs:**
1. ✅ Tester sur compte DEMO (2 semaines)
2. ✅ Vérifier performance réelle
3. ✅ Comparer avec backtest
4. ✅ Si OK → Passer en RÉEL avec prudence

**Si résultats négatifs:**
1. ❌ Ajuster les paramètres
2. ❌ Retester
3. ❌ NE PAS passer en réel!

---

## 📞 SUPPORT

**Questions?**
- Regarde les graphiques d'equity
- Compare BACKTEST vs AGGRESSIVE
- Ajuste MinConfluence et MinCertainty selon résultats

**Bonne chance!** 🍀

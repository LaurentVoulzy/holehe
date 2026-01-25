# 🚀 LA BÊTE V12 - VWAP QUALITY STRATEGY

## 📊 NOUVEAUTÉS V12

### **Changements Majeurs:**

1. **MA2×MA12 → MA20×MA50**
   - MA rapide: 2 → 20 périodes
   - MA lente: 12 → 50 périodes
   - **Résultat:** Moins de signaux, MEILLEURE qualité
   - Win rate attendu: **55-65%** (vs 28% en V11)

2. **Swing High/Low → VWAP Zones**
   - Support/Résistance basés sur **VOLUME** (pas juste prix)
   - VWAP H1 avec bandes Standard Deviation (±1σ, ±2σ)
   - Zones institutionnelles = vraie liquidité
   - **Nouveau:** Indicateur VWAP_V12.mq5 custom créé

3. **Timeframe Recommandé: M30**
   - Stratégie: MA20×MA50 sur **M30**
   - Zones S/R: VWAP sur **H1**
   - 2-4 trades/jour de haute qualité

---

## 📦 FICHIERS MODIFIÉS

### **Bots MT5 (V11 → V12):**
✅ `FOREX/La_Bete_EUR_V12.mq5`
✅ `FOREX/La_Bete_GBP_V12.mq5`
✅ `FOREX/La_Bete_JPY_V12.mq5`
✅ `FOREX/La_Bete_GOLD_V12.mq5`
✅ `CRYPTO/La_Bete_BTC_V12.mq5`
✅ `CRYPTO/La_Bete_ETH_V12.mq5`

### **Nouvel Indicateur:**
✅ `SHARED/VWAP_V12.mq5` - Indicateur VWAP Daily avec bandes SD

### **Telegram Bot:**
✅ `CORE/telegram_bot_ultra.py` - Version 12.0

---

## 🎯 STRATÉGIE COMPLÈTE V12

### **1. Signal d'Entrée:**
```
BUY:
✓ MA20 croise MA50 vers le HAUT
✓ Prix dans zone VWAP -1σ (support)
✓ RSI entre 30-70
✓ Confluence ≥ 85/100
✓ Certitude ≥ 80%

SELL:
✓ MA20 croise MA50 vers le BAS
✓ Prix dans zone VWAP +1σ (résistance)
✓ RSI entre 30-70
✓ Confluence ≥ 85/100
✓ Certitude ≥ 80%
```

### **2. VWAP Zones (H1):**
```
+2σ  ← Résistance extrême (vente agressive)
+1σ  ← Résistance forte (SELL signals)
VWAP ← Ligne centrale (équilibre)
-1σ  ← Support fort (BUY signals)
-2σ  ← Support extrême (achat agressif)
```

### **3. Gestion de Position:**
```
SL:  ATR × 2.0 (30-100 pips FOREX, 50-150 pips CRYPTO)
TP1: 1:2 → Ferme 50%
TP2: 1:3 → Ferme 30%
TP3: 1:5 → Ferme 20%
BE:  À 50% vers TP1 (SL → Entry +10 pips)
Trailing: ATR × 0.5 après TP1
```

---

## 🔧 INSTALLATION V12

### **1. Copier les fichiers:**
```bash
# Pull depuis GitHub
git pull origin claude/create-bot-6rxu1
```

### **2. Compiler l'indicateur VWAP:**
```
1. Ouvrir MetaEditor (MT5)
2. Naviguer: File → Open Data Folder
3. Copier VWAP_V12.mq5 dans: MQL5/Indicators/
4. Compiler VWAP_V12.mq5 (F7)
5. Vérifier: Aucune erreur
```

### **3. Compiler les 6 bots V12:**
```
1. Ouvrir chaque bot V12 dans MetaEditor
2. Compiler (F7)
3. Vérifier: Aucune erreur
4. Si erreur "VWAP not found":
   → Vérifier que VWAP_V12.mq5 est compilé dans Indicators/
```

### **4. Attacher les bots:**
```
1. Ouvrir graphique M30 pour chaque paire:
   - EUR/USD → M30
   - GBP/USD → M30
   - USD/JPY → M30
   - XAU/USD → M30
   - BTC/USD → M30
   - ETH/USD → M30

2. D'abord attacher indicateur VWAP sur graphique H1:
   - Ouvrir graphique H1 de la même paire
   - Insert → Indicators → Custom → VWAP
   - Vérifier: 5 lignes affichées (VWAP + 4 bandes)

3. Ensuite attacher bot V12 sur graphique M30:
   - Drag & Drop bot V12 sur graphique M30
   - Paramètres:
     * MA_Fast = 20 ✓
     * MA_Slow = 50 ✓
     * UseVWAP = true ✓
     * MinConfluenceScore = 85 ✓
     * MinCertaintyPercent = 80 ✓
     * MaxTradesPerDay = 2 ✓
   - Autoriser AutoTrading
```

### **5. Vérifier logs:**
```
MT5 Terminal → Experts Tab

Logs attendus:
✅ "LA BÊTE EUR - V12 VWAP QUALITY TRADE"
✅ "Signaux: MA20 × MA50 Crossover (M30 recommandé)"
✅ "S/R: ✅ VWAP H1 + Bandes SD"
✅ "VWAP H1 Zones: Upper1 (+1σ): X.XXXXX ← Résistance"

Si erreur:
❌ "Impossible d'initialiser VWAP"
→ Indicateur VWAP_V12.mq5 pas compilé correctement
```

---

## 📈 RÉSULTATS ATTENDUS V12

| Métrique | V11 (Échec) | V12 (Objectif) |
|----------|-------------|----------------|
| **Win Rate** | 28% | 55-65% |
| **Trades/jour** | 10-20 | 2-4 |
| **Faux signaux** | Élevé | Faible |
| **Overtrading** | Oui | Non |
| **Confluence** | Faible | Forte (MA+VWAP+Volume) |
| **Adapté FTMO** | Non | Oui |

---

## ⚠️ POINTS IMPORTANTS

1. **VWAP H1 requis:**
   - Le bot M30 LIT le VWAP depuis H1
   - Sans VWAP H1 attaché: bot utilise uniquement MA20×MA50
   - **Solution:** Toujours avoir graphique H1 ouvert avec VWAP

2. **Graphique M30 recommandé:**
   - MA20×MA50 fonctionne MIEUX sur M30
   - Trop rapide sur M5/M15 (faux signaux)
   - Trop lent sur H1 (rate opportunités)

3. **Max 2 trades/jour:**
   - Filtre ultra-sélectif activé
   - Qualité > Quantité
   - Respect limites FTMO

4. **Guardian + MT5 Reader:**
   - Guardian FOREX: Port 5000
   - Guardian CRYPTO: Port 5001
   - MT5 Reader: Données réelles FTMO (toutes les heures)

---

## 🎯 STRATÉGIE EN RÉSUMÉ

```
🕐 TIMEFRAME:
   M30 pour signaux (attacher bot ici)
   H1 pour VWAP zones

📊 INDICATEURS:
   MA20, MA50 (M30)
   RSI 14 (M30)
   ATR 14 (M30)
   VWAP + Bandes SD (H1)

🎯 SIGNAL BUY:
   MA20 > MA50 + Prix près VWAP -1σ + Confluence 85+

🎯 SIGNAL SELL:
   MA20 < MA50 + Prix près VWAP +1σ + Confluence 85+

💰 GESTION:
   SL: ATR × 2.0
   TP: 1:2, 1:3, 1:5 (fermetures partielles)
   BE + Trailing après TP1

🛡️ PROTECTION FTMO:
   Daily: -2000€ max
   Total: -4000€ max
   Trades: 2 max/jour
```

---

## 📞 SUPPORT

En cas de problème:
1. Vérifier VWAP_V12.mq5 compilé
2. Vérifier graphique H1 avec VWAP ouvert
3. Vérifier graphique M30 avec bot V12
4. Consulter logs MT5 (Experts tab)

**Version:** V12.0
**Date:** 2025-01-25
**Auteur:** Yann - La Bête 🐺

# 🔧 INTÉGRATION TELEGRAM DANS LES BOTS V12

## 📋 MODIFICATIONS À FAIRE (5 minutes par bot)

### ✅ ÉTAPE 1: Ajouter l'include en haut du fichier

**Ligne ~22** (après `#include <Trade\AccountInfo.mqh>`):
```mql5
#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>
#include <Trade\AccountInfo.mqh>
#include "../SHARED/TelegramNotify.mqh"  // ← AJOUTER CETTE LIGNE
```

---

### ✅ ÉTAPE 2: Ajouter les paramètres Telegram

**Ligne ~98** (après les paramètres FTMO):
```mql5
input group "=== NOTIFICATIONS TELEGRAM ==="
input string   TelegramBotToken = "";           // Token du bot Telegram
input string   TelegramChatID = "";             // Chat ID Telegram
input bool     EnableTelegramNotifications = false; // Activer notifications Telegram
```

---

### ✅ ÉTAPE 3: Notification au démarrage (OnInit)

**Dans la fonction `OnInit()`, ligne ~180** (à la fin, avant `return(INIT_SUCCEEDED);`):
```mql5
    Print("✅ La Bête BTC V12 initialisé avec succès!");

    // Notification Telegram démarrage
    if(EnableTelegramNotifications)
    {
        NotifyBotStarted(_Symbol, "La Bete BTC V12", "12.00");
    }

    return(INIT_SUCCEEDED);
```

---

### ✅ ÉTAPE 4: Notification d'ouverture de position

**Dans la fonction `OpenPosition()`, ligne ~1544** (remplacer `SendTelegramAlert(alert);`):
```mql5
    if(success)
    {
        Print("✅ Position ouverte avec succès!");
        tradesCountToday++;

        // Notification Telegram
        if(EnableTelegramNotifications)
        {
            ENUM_ORDER_TYPE orderType = (signal.direction == "BUY") ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
            NotifyPositionOpened(_Symbol, orderType, signal.lot_size, signal.entry_price,
                                signal.sl_price, signal.tp1_price, "MA20×MA50 + VWAP");
        }
    }
```

---

### ✅ ÉTAPE 5: Notification de fermeture de position

**Dans la fonction `ManageOpenPositions()`, ligne ~1600** (après chaque `PositionModify` ou `PositionClose`):

**Pour TP1:**
```mql5
                        if(!TP1_Hit && currentPrice >= tp1_price)
                        {
                            TP1_Hit = true;
                            Print("🎯 TP1 atteint!");
                            ClosePartialPosition(TP1_ClosePercent);

                            // Notification Telegram TP1
                            if(EnableTelegramNotifications)
                            {
                                double profit = position.Profit();
                                NotifyPositionClosed(_Symbol, position.Type(), position.Volume(),
                                                    position.PriceOpen(), currentPrice, profit, "TP1 (50%)");
                            }
                        }
```

**Pour TP2:**
```mql5
                        if(TP1_Hit && !TP2_Hit && currentPrice >= tp2_price)
                        {
                            TP2_Hit = true;
                            Print("🎯 TP2 atteint!");
                            ClosePartialPosition(TP2_ClosePercent);

                            // Notification Telegram TP2
                            if(EnableTelegramNotifications)
                            {
                                double profit = position.Profit();
                                NotifyPositionClosed(_Symbol, position.Type(), position.Volume(),
                                                    position.PriceOpen(), currentPrice, profit, "TP2 (30%)");
                            }
                        }
```

**Pour TP3:**
```mql5
                        if(TP2_Hit && !TP3_Hit && currentPrice >= tp3_price)
                        {
                            TP3_Hit = true;
                            Print("🎯 TP3 atteint!");
                            ClosePartialPosition(TP3_ClosePercent);

                            // Notification Telegram TP3
                            if(EnableTelegramNotifications)
                            {
                                double profit = position.Profit();
                                NotifyPositionClosed(_Symbol, position.Type(), position.Volume(),
                                                    position.PriceOpen(), currentPrice, profit, "TP3 (20%)");
                            }
                        }
```

**Pour SL (Stop Loss):**
Chercher dans le code où il y a fermeture au SL et ajouter:
```mql5
                            // Notification Telegram SL
                            if(EnableTelegramNotifications)
                            {
                                double profit = position.Profit();
                                NotifyPositionClosed(_Symbol, position.Type(), position.Volume(),
                                                    position.PriceOpen(), currentPrice, profit, "Stop Loss");
                            }
```

**Pour BE (Break Even):**
```mql5
                        if(trade.PositionModify(position.Ticket(), newSL, tp))
                        {
                            BE_Activated = true;
                            Print("✅ Break Even activé à ", newSL);

                            // Notification Telegram BE
                            if(EnableTelegramNotifications)
                            {
                                SendTelegramMessage("🔒 <b>BREAK EVEN ACTIVÉ</b>\n\n📊 Paire: " + _Symbol +
                                                   "\n🛡️ Nouveau SL: " + DoubleToString(newSL, _Digits));
                            }
                        }
```

---

### ✅ ÉTAPE 6: Notification d'ordre limite placé

**Dans la fonction `PlaceLimitOrdersOnSR()`, après `OrderOpen()` réussi:**
```mql5
        if(success)
        {
            Print("✅ Buy Limit placé à ", buyPrice);

            // Notification Telegram
            if(EnableTelegramNotifications)
            {
                NotifyLimitOrderPlaced(_Symbol, ORDER_TYPE_BUY_LIMIT, lotSize,
                                      buyPrice, sl, tp);
            }
        }
```

---

## 📝 RÉSUMÉ DES FICHIERS À MODIFIER

Pour intégrer Telegram dans tous les 6 bots:

1. ✅ `/LaBete/CRYPTO/La_Bete_BTC_V12.mq5`
2. ✅ `/LaBete/CRYPTO/La_Bete_ETH_V12.mq5`
3. ✅ `/LaBete/FOREX/La_Bete_EUR_V12.mq5`
4. ✅ `/LaBete/FOREX/La_Bete_GBP_V12.mq5`
5. ✅ `/LaBete/FOREX/La_Bete_JPY_V12.mq5`
6. ✅ `/LaBete/FOREX/La_Bete_GOLD_V12.mq5`

---

## 🧪 TEST RAPIDE

1. Modifier 1 bot (BTC par exemple)
2. Compiler (F7)
3. Configurer les paramètres Telegram dans MT5
4. Attacher sur graphique M30
5. Tu dois recevoir: **🚀 BOT DÉMARRÉ**

---

## ⚠️ IMPORTANT

- **NE PAS** supprimer la fonction `SendTelegramAlert()` existante (elle est utilisée par Guardian)
- Les notifications Telegram sont **EN PLUS** de Guardian
- Tu peux activer les deux ou juste Telegram

---

## 🎯 ALTERNATIVE RAPIDE

Si tu veux que je modifie directement les 6 bots, dis-moi et je fais les modifications automatiquement!

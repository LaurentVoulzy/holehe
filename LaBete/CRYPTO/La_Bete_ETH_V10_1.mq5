//+------------------------------------------------------------------+
//|                                           La_Bete_ETH_V10_1.mq5     |
//|                                    Copyright 2025, Yann - La Bête  |
//|                                                                      |
//| BOT SPÉCIALISÉ ETH/USD V10_1 - POWER TRADE STRATEGY                  |
//| - MA2 × MA12 Crossover (High Frequency Trading)                   |
//| - Support/Resistance Detection & Visualization                     |
//| - Dynamic ATR-based SL/TP (Multiple Take Profits)                 |
//| - Triple TP (50% / 30% / 20%) + BE + Trailing                     |
//| - ForexFactory High Impact News (15min pause)                     |
//| - FTMO Protection (Daily -€2K, Total -€4K)                        |
//+------------------------------------------------------------------+

#property copyright "Yann - La Bête"
#property version   "10.10"
#property strict

//+------------------------------------------------------------------+
//| INCLUDES                                                          |
//+------------------------------------------------------------------+
#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>
#include <Trade\AccountInfo.mqh>

//+------------------------------------------------------------------+
//| PARAMÈTRES INPUTS                                                 |
//+------------------------------------------------------------------+
input group "=== CONFIGURATION ETH/USD V10 ==="
input double   RiskPercent = 0.25;           // Risque par trade (%)
input int      MagicNumber = 777002;         // Magic Number ETH
input string   TradeComment = "LaBete_ETH_V10_1"; // Commentaire

input group "=== STRATÉGIE MA2 × MA12 ==="
input int      MA_Fast = 2;                  // MA rapide (ultra court terme)
input int      MA_Slow = 12;                 // MA lente (court terme)
input int      MinConfluenceScore = 85;      // Score confluence minimum (/100)
input int      MinCertaintyPercent = 80;     // Certitude minimum (%)

input group "=== STOP LOSS / TAKE PROFIT (ATR) ==="
input int      SL_MinPips = 50;              // SL minimum CRYPTO (pips)
input int      SL_MaxPips = 200;             // SL maximum CRYPTO (pips)
input double   ATR_Multiplier_SL = 2.5;      // ATR × 2.5 pour CRYPTO
input double   TP1_RR = 2.0;                 // TP1 Risk:Reward 1:2
input double   TP2_RR = 3.0;                 // TP2 Risk:Reward 1:3
input double   TP3_RR = 5.0;                 // TP3 Risk:Reward 1:5

input group "=== PARTIAL CLOSES ==="
input double   TP1_ClosePercent = 50.0;      // Fermer 50% à TP1
input double   TP2_ClosePercent = 30.0;      // Fermer 30% à TP2
input double   TP3_ClosePercent = 20.0;      // Fermer 20% à TP3

input group "=== BREAK EVEN & TRAILING ==="
input double   BE_ActivationPercent = 50.0;  // Activation BE (50% vers TP1)
input int      BE_OffsetPips = 10;           // Offset BE (pips)
input bool     TrailingAfterTP1 = true;      // Activer trailing après TP1
input double   Trailing_ATR_Multiplier = 0.5; // Trailing = ATR × 0.5

input group "=== INDICATEURS ==="
input int      RSI_Period = 14;              // Période RSI
input int      ATR_Period = 14;              // Période ATR
input bool     CheckRSI = true;              // Éviter zones extrêmes RSI

input group "=== SUPPORT / RÉSISTANCE ==="
input bool     ShowSR = true;                // Afficher S/R sur graphique
input ENUM_TIMEFRAMES SR_Timeframe = PERIOD_H1; // Timeframe pour S/R (H1 recommandé)
input int      SR_Lookback = 50;             // Barres pour détecter S/R
input int      SR_Strength = 2;              // Force S/R (nb touches min)
input color    SupportColor = clrLime;       // Couleur Support
input color    ResistanceColor = clrRed;     // Couleur Résistance

input group "=== ORDRES LIMITES SUR S/R ==="
input bool     UseLimitOrders = false;        // Activer Buy/Sell Limit sur S/R
input int      MaxLimitOrders = 3;           // Max ordres limites simultanés
input double   LimitOrderOffset = 25.0;      // Distance du S/R (pips) - marché respire
input double   LimitSL_ATR_Multiplier = 1.5; // SL = ATR H1 × 1.5 (dynamique)
input double   LimitSL_MinPips = 70.0;       // SL minimum CRYPTO (pips)
input double   LimitSL_MaxPips = 180.0;      // SL maximum CRYPTO (pips)
input double   LimitTP_RR = 3.0;             // TP = SL × 3.0 pour ordres limites
input int      LimitOrderExpiry = 240;       // Expiration ordres (min, 0=jamais)

input group "=== API PYTHON GUARDIAN ==="
input string   GuardianURL = "http://localhost:5001/validate_signal";
input bool     RequireApproval = true;       // Requiert approbation Guardian
input int      API_Timeout = 5000;           // Timeout API (ms)

input group "=== NEWS ÉCONOMIQUES (CRYPTO = OFF) ==="
input bool     CheckEconomicNews = false;    // Crypto = 24/7 (pas de news)
input int      NewsBufferMinutes = 15;       // 15min avant/après (si activé)

input group "=== PROTECTION FTMO ==="
input double   MaxDailyLoss = 2000;          // Limite daily loss (€)
input double   MaxDrawdown = 4000;           // Limite drawdown total (€)
input double   AlertDailyLoss = 1700;        // Alerte à 1700€
input double   AlertDrawdown = 3500;         // Alerte à 3500€
input int      MaxTradesPerDay = 2;         // Limite trades/jour

//+------------------------------------------------------------------+
//| VARIABLES GLOBALES                                                |
//+------------------------------------------------------------------+
CTrade         trade;
CPositionInfo  position;
CAccountInfo   account;

// Handles indicateurs
int handleMA_Fast, handleMA_Slow;
int handleRSI, handleATR;

// Handles pour S/R sur H1
int handleATR_H1;

// Buffers
double lastMA_Fast[], lastMA_Slow[];
double lastRSI[], lastATR[];
double lastHigh[], lastLow[], lastClose[], lastOpen[];

// Buffers H1 pour S/R
double lastHigh_H1[], lastLow_H1[], lastClose_H1[], lastATR_H1[];

// État du système
bool systemInitialized = false;
datetime lastBarTime = 0;

// Gestion des TP partiels
bool TP1_Hit = false;
bool TP2_Hit = false;
bool TP3_Hit = false;
bool BE_Activated = false;
bool Trailing_Active = false;

// V10: Support/Résistance
struct SRLevel {
    double price;
    int touches;
    bool is_support;
    datetime last_touch;
    bool is_valid;
};

SRLevel supportLevels[5];
SRLevel resistanceLevels[5];
int supportCount = 0;
int resistanceCount = 0;

// V10: Ordres Limites sur S/R
struct LimitOrderInfo {
    ulong ticket;
    double price;
    bool is_buy;
    double sr_level;
    datetime placed_time;
    bool is_active;
};

LimitOrderInfo activeLimitOrders[10];
int limitOrdersCount = 0;
datetime lastLimitOrderCheck = 0;

// V10: Protection FTMO
double dailyStartBalance = 0;
double dailyPnL = 0;
double totalDrawdown = 0;
int tradesCountToday = 0;
datetime lastDayCheck = 0;
bool tradingAllowed = true;
double riskMultiplier = 1.0;  // Ajustement dynamique du risque

// V10: Gestion news économiques
datetime lastNewsCheck = 0;
datetime nextNewsTime = 0;
bool newsBlockActive = false;
string lastNewsTitle = "";

// Structures
struct SignalData {
    string pair;
    string direction;
    double entry_price;
    double sl_price;
    double sl_pips;
    double tp1_price;
    double tp2_price;
    double tp3_price;
    double lot_size;
    int confluence_score;
    int certainty_percent;
    datetime timestamp;
    string signal_reason;
};

//+------------------------------------------------------------------+
//| Expert initialization function                                     |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("╔══════════════════════════════════════════════════════════╗");
    Print("║          🐺 LA BÊTE ETH V10 POWER TRADE 🐺               ║");
    Print("║     Stratégie MA2 × MA12 - High Frequency Trading        ║");
    Print("║   Support/Résistance + Protection FTMO Renforcée         ║");
    Print("╚══════════════════════════════════════════════════════════╝");

    // Vérifier symbole
    Print("📊 Symbole: ", _Symbol);
    Print("⏰ Timeframe: ", EnumToString(PERIOD_CURRENT));

    // Configuration du trade
    trade.SetExpertMagicNumber(MagicNumber);
    trade.SetDeviationInPoints(10);
    trade.SetTypeFilling(ORDER_FILLING_FOK);
    trade.SetAsyncMode(false);

    // Initialiser les indicateurs (SMA au lieu de EMA)
    handleMA_Fast = iMA(_Symbol, PERIOD_CURRENT, MA_Fast, 0, MODE_SMA, PRICE_CLOSE);
    handleMA_Slow = iMA(_Symbol, PERIOD_CURRENT, MA_Slow, 0, MODE_SMA, PRICE_CLOSE);
    handleRSI = iRSI(_Symbol, PERIOD_CURRENT, RSI_Period, PRICE_CLOSE);
    handleATR = iATR(_Symbol, PERIOD_CURRENT, ATR_Period);

    // Initialiser ATR sur H1 pour S/R
    handleATR_H1 = iATR(_Symbol, SR_Timeframe, ATR_Period);

    // Vérifier les handles
    if(handleMA_Fast == INVALID_HANDLE || handleMA_Slow == INVALID_HANDLE ||
       handleRSI == INVALID_HANDLE || handleATR == INVALID_HANDLE ||
       handleATR_H1 == INVALID_HANDLE)
    {
        Print("❌ ERREUR: Impossible d'initialiser les indicateurs!");
        return(INIT_FAILED);
    }

    // Configurer les arrays
    ArraySetAsSeries(lastMA_Fast, true);
    ArraySetAsSeries(lastMA_Slow, true);
    ArraySetAsSeries(lastRSI, true);
    ArraySetAsSeries(lastATR, true);
    ArraySetAsSeries(lastHigh, true);
    ArraySetAsSeries(lastLow, true);
    ArraySetAsSeries(lastClose, true);
    ArraySetAsSeries(lastOpen, true);

    // Configurer arrays H1
    ArraySetAsSeries(lastHigh_H1, true);
    ArraySetAsSeries(lastLow_H1, true);
    ArraySetAsSeries(lastClose_H1, true);
    ArraySetAsSeries(lastATR_H1, true);

    // Initialiser S/R
    for(int i = 0; i < 5; i++)
    {
        supportLevels[i].is_valid = false;
        resistanceLevels[i].is_valid = false;
    }

    // Initialiser ordres limites
    for(int i = 0; i < 10; i++)
    {
        activeLimitOrders[i].is_active = false;
        activeLimitOrders[i].ticket = 0;
    }
    limitOrdersCount = 0;

    // Initialiser protection FTMO
    dailyStartBalance = account.Balance();

    systemInitialized = true;

    Print("✅ Système ETH V10 initialisé avec succès");
    Print("🔗 Guardian API: ", GuardianURL);
    Print("💰 Risque: ", RiskPercent, "% × ", riskMultiplier);
    Print("🎯 Confluence min: ", MinConfluenceScore, "/100");
    Print("🎲 Certitude min: ", MinCertaintyPercent, "%");
    Print("📏 SL: ATR × ", ATR_Multiplier_SL, " (", SL_MinPips, "-", SL_MaxPips, " pips)");
    Print("🎯 TP: 1:", TP1_RR, " / 1:", TP2_RR, " / 1:", TP3_RR);
    Print("════════════════════════════════════════════════════════");
    Print("🆕 NOUVEAUTÉS V10:");
    Print("📊 Stratégie: MA", MA_Fast, " × MA", MA_Slow, " Crossover");
    Print("📈 S/R: ", (ShowSR ? "✅ ACTIVÉ" : "❌ OFF"), " (", EnumToString(SR_Timeframe), " | Lookback: ", SR_Lookback, " bars)");
    Print("🎯 Ordres Limites: ", (UseLimitOrders ? "✅ ACTIVÉ" : "❌ OFF"),
          (UseLimitOrders ? " (Max: " + IntegerToString(MaxLimitOrders) + " | TP: 1:" + DoubleToString(LimitTP_RR, 1) + ")" : ""));
    Print("🛡️ FTMO: Daily -€", MaxDailyLoss, " | Total -€", MaxDrawdown);
    Print("📰 News: ", (CheckEconomicNews ? "✅ ACTIVÉ" : "❌ OFF (Crypto 24/7)"));
    Print("╚══════════════════════════════════════════════════════════╝");

    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                  |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("🛑 La Bête ETH V10 arrêtée. Raison: ", reason);

    // Annuler tous les ordres limites actifs
    for(int i = 0; i < 10; i++)
    {
        if(activeLimitOrders[i].is_active && activeLimitOrders[i].ticket > 0)
        {
            trade.OrderDelete(activeLimitOrders[i].ticket);
        }
    }

    // Nettoyer les objets graphiques S/R
    DeleteAllSRObjects();

    IndicatorRelease(handleMA_Fast);
    IndicatorRelease(handleMA_Slow);
    IndicatorRelease(handleRSI);
    IndicatorRelease(handleATR);
    IndicatorRelease(handleATR_H1);
}

//+------------------------------------------------------------------+
//| Expert tick function                                               |
//+------------------------------------------------------------------+
void OnTick()
{
    if(!IsNewBar())
        return;

    if(!UpdateIndicators())
        return;

    // V10: Vérifier protection FTMO
    CheckFTMOLimits();

    if(!tradingAllowed)
    {
        Print("🛑 Trading désactivé (limites FTMO)");
        return;
    }

    // V10: Vérifier news économiques (si activé pour crypto)
    if(CheckEconomicNews && !IsEconomicNewsSafe())
    {
        return;
    }

    // V10: Détecter et afficher Support/Résistance
    if(ShowSR)
    {
        DetectSupportResistance();
        DisplaySROnChart();
    }

    // V10: Placer et gérer ordres limites sur S/R
    if(UseLimitOrders && ShowSR)
    {
        PlaceLimitOrdersOnSR();
        ManageLimitOrders();
    }

    // Gérer les positions existantes
    ManageOpenPositions();

    // Chercher nouveau signal si pas de position
    if(!HasOpenPosition())
    {
        // Reset des flags
        TP1_Hit = false;
        TP2_Hit = false;
        TP3_Hit = false;
        BE_Activated = false;
        Trailing_Active = false;

        AnalyzeMarket();
    }
}

//+------------------------------------------------------------------+
//| Détecte une nouvelle barre                                        |
//+------------------------------------------------------------------+
bool IsNewBar()
{
    datetime currentBarTime = iTime(_Symbol, PERIOD_CURRENT, 0);

    if(currentBarTime != lastBarTime)
    {
        lastBarTime = currentBarTime;
        return true;
    }

    return false;
}

//+------------------------------------------------------------------+
//| Met à jour les indicateurs                                        |
//+------------------------------------------------------------------+
bool UpdateIndicators()
{
    if(CopyBuffer(handleMA_Fast, 0, 0, 3, lastMA_Fast) < 0) return false;
    if(CopyBuffer(handleMA_Slow, 0, 0, 3, lastMA_Slow) < 0) return false;
    if(CopyBuffer(handleRSI, 0, 0, 3, lastRSI) < 0) return false;
    if(CopyBuffer(handleATR, 0, 0, 3, lastATR) < 0) return false;

    // Copier les prix
    if(CopyHigh(_Symbol, PERIOD_CURRENT, 0, SR_Lookback, lastHigh) < 0) return false;
    if(CopyLow(_Symbol, PERIOD_CURRENT, 0, SR_Lookback, lastLow) < 0) return false;
    if(CopyClose(_Symbol, PERIOD_CURRENT, 0, SR_Lookback, lastClose) < 0) return false;
    if(CopyOpen(_Symbol, PERIOD_CURRENT, 0, SR_Lookback, lastOpen) < 0) return false;

    return true;
}

//+------------------------------------------------------------------+
//| V10: Vérification Protection FTMO                                 |
//+------------------------------------------------------------------+
void CheckFTMOLimits()
{
    // Réinitialiser compteur quotidien
    MqlDateTime dt;
    TimeToStruct(TimeCurrent(), dt);
    datetime currentDay = StringToTime(IntegerToString(dt.year) + "." +
                                        IntegerToString(dt.mon) + "." +
                                        IntegerToString(dt.day));

    if(currentDay != lastDayCheck)
    {
        lastDayCheck = currentDay;
        dailyStartBalance = account.Balance();
        dailyPnL = 0;
        tradesCountToday = 0;
        Print("📅 Nouveau jour - Reset compteurs FTMO");
    }

    // Calculer P&L du jour
    dailyPnL = account.Balance() - dailyStartBalance;

    // Calculer drawdown total
    totalDrawdown = account.Balance() - account.Equity();

    // 1. LIMITE DAILY LOSS
    if(MathAbs(dailyPnL) >= MaxDailyLoss)
    {
        tradingAllowed = false;
        Print("🛑 LIMITE DAILY LOSS ATTEINTE: ", dailyPnL, "€");
        SendTelegramAlert("🛑 FTMO LIMIT: Daily Loss " + DoubleToString(dailyPnL, 2) + "€");
        return;
    }

    // 2. ALERTE DAILY LOSS
    if(MathAbs(dailyPnL) >= AlertDailyLoss && MathAbs(dailyPnL) < MaxDailyLoss)
    {
        Print("⚠️ ALERTE: Daily Loss proche limite (", dailyPnL, "€ / -", MaxDailyLoss, "€)");

        // Réduire risque à 50%
        riskMultiplier = 0.5;

        SendTelegramAlert("⚠️ Daily Loss: " + DoubleToString(dailyPnL, 2) + "€ (Risque réduit 50%)");
    }

    // 3. LIMITE DRAWDOWN TOTAL
    if(MathAbs(totalDrawdown) >= MaxDrawdown)
    {
        tradingAllowed = false;
        Print("🛑 LIMITE DRAWDOWN TOTAL ATTEINTE: ", totalDrawdown, "€");
        SendTelegramAlert("🛑 FTMO LIMIT: Drawdown " + DoubleToString(totalDrawdown, 2) + "€");
        return;
    }

    // 4. ALERTE DRAWDOWN
    if(MathAbs(totalDrawdown) >= AlertDrawdown && MathAbs(totalDrawdown) < MaxDrawdown)
    {
        Print("⚠️ ALERTE: Drawdown proche limite (", totalDrawdown, "€ / -", MaxDrawdown, "€)");

        // Réduire risque à 30%
        riskMultiplier = 0.3;

        SendTelegramAlert("⚠️ Drawdown: " + DoubleToString(totalDrawdown, 2) + "€ (Risque réduit 30%)");
    }

    // 5. LIMITE TRADES PAR JOUR
    if(tradesCountToday >= MaxTradesPerDay)
    {
        tradingAllowed = false;
        Print("⏸️ LIMITE TRADES/JOUR ATTEINTE: ", tradesCountToday, "/", MaxTradesPerDay);
        return;
    }

    // Si tout OK, risque normal
    if(MathAbs(dailyPnL) < AlertDailyLoss && MathAbs(totalDrawdown) < AlertDrawdown)
    {
        riskMultiplier = 1.0;
    }
}

//+------------------------------------------------------------------+
//| V10: Détection Support/Résistance sur H1                          |
//+------------------------------------------------------------------+
void DetectSupportResistance()
{
    // Copier les données H1
    if(CopyHigh(_Symbol, SR_Timeframe, 0, SR_Lookback, lastHigh_H1) < 0) return;
    if(CopyLow(_Symbol, SR_Timeframe, 0, SR_Lookback, lastLow_H1) < 0) return;
    if(CopyClose(_Symbol, SR_Timeframe, 0, SR_Lookback, lastClose_H1) < 0) return;
    if(CopyBuffer(handleATR_H1, 0, 0, 1, lastATR_H1) < 0) return;

    // Reset
    supportCount = 0;
    resistanceCount = 0;

    for(int i = 0; i < 5; i++)
    {
        supportLevels[i].is_valid = false;
        resistanceLevels[i].is_valid = false;
    }

    // Chercher Swing Highs et Swing Lows sur H1
    for(int i = SR_Strength; i < SR_Lookback - SR_Strength; i++)
    {
        // RESISTANCE = Swing High (plus haut local)
        bool isSwingHigh = true;
        for(int j = 1; j <= SR_Strength; j++)
        {
            if(lastHigh_H1[i] <= lastHigh_H1[i-j] || lastHigh_H1[i] <= lastHigh_H1[i+j])
            {
                isSwingHigh = false;
                break;
            }
        }

        if(isSwingHigh && resistanceCount < 5)
        {
            // Vérifier que ce niveau n'est pas trop proche d'un existant
            bool isDuplicate = false;
            double tolerance = lastATR_H1[0] * 0.5;

            for(int k = 0; k < resistanceCount; k++)
            {
                if(MathAbs(lastHigh_H1[i] - resistanceLevels[k].price) < tolerance)
                {
                    isDuplicate = true;
                    resistanceLevels[k].touches++;
                    break;
                }
            }

            if(!isDuplicate)
            {
                resistanceLevels[resistanceCount].price = lastHigh_H1[i];
                resistanceLevels[resistanceCount].touches = 1;
                resistanceLevels[resistanceCount].is_support = false;
                resistanceLevels[resistanceCount].last_touch = iTime(_Symbol, SR_Timeframe, i);
                resistanceLevels[resistanceCount].is_valid = true;
                resistanceCount++;
            }
        }

        // SUPPORT = Swing Low (plus bas local)
        bool isSwingLow = true;
        for(int j = 1; j <= SR_Strength; j++)
        {
            if(lastLow_H1[i] >= lastLow_H1[i-j] || lastLow_H1[i] >= lastLow_H1[i+j])
            {
                isSwingLow = false;
                break;
            }
        }

        if(isSwingLow && supportCount < 5)
        {
            // Vérifier que ce niveau n'est pas trop proche d'un existant
            bool isDuplicate = false;
            double tolerance = lastATR_H1[0] * 0.5;

            for(int k = 0; k < supportCount; k++)
            {
                if(MathAbs(lastLow_H1[i] - supportLevels[k].price) < tolerance)
                {
                    isDuplicate = true;
                    supportLevels[k].touches++;
                    break;
                }
            }

            if(!isDuplicate)
            {
                supportLevels[supportCount].price = lastLow_H1[i];
                supportLevels[supportCount].touches = 1;
                supportLevels[supportCount].is_support = true;
                supportLevels[supportCount].last_touch = iTime(_Symbol, SR_Timeframe, i);
                supportLevels[supportCount].is_valid = true;
                supportCount++;
            }
        }
    }

    Print("📊 S/R détectés sur ", EnumToString(SR_Timeframe), ": ", supportCount, " Supports | ", resistanceCount, " Résistances");
}

//+------------------------------------------------------------------+
//| V10: Affichage Support/Résistance sur graphique                   |
//+------------------------------------------------------------------+
void DisplaySROnChart()
{
    // Supprimer anciens objets
    DeleteAllSRObjects();

    // Récupérer ATR pour épaisseur des zones
    double atr[];
    ArraySetAsSeries(atr, true);
    if(CopyBuffer(handleATR_H1, 0, 0, 1, atr) <= 0)
        return;

    double zoneThickness = atr[0] * 0.15; // Zone = 15% de l'ATR

    datetime timeNow = TimeCurrent();
    datetime timeStart = timeNow - PeriodSeconds(PERIOD_H1) * 100; // 100 barres avant
    datetime timeEnd = timeNow + PeriodSeconds(PERIOD_H1) * 50;    // 50 barres après

    // Afficher Supports (ZONES rectangulaires)
    for(int i = 0; i < supportCount; i++)
    {
        if(supportLevels[i].is_valid)
        {
            string name = "SupportZone_" + IntegerToString(i);

            double priceHigh = supportLevels[i].price + zoneThickness;
            double priceLow = supportLevels[i].price - zoneThickness;

            // Créer ZONE rectangulaire
            ObjectCreate(0, name, OBJ_RECTANGLE, 0, timeStart, priceHigh, timeEnd, priceLow);
            ObjectSetInteger(0, name, OBJPROP_COLOR, SupportColor);
            ObjectSetInteger(0, name, OBJPROP_FILL, true);
            ObjectSetInteger(0, name, OBJPROP_BACK, true);
            ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
            ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);

            // Label au centre de la zone
            string labelName = "SupportLabel_" + IntegerToString(i);
            ObjectCreate(0, labelName, OBJ_TEXT, 0, timeNow, supportLevels[i].price);
            ObjectSetString(0, labelName, OBJPROP_TEXT, "━━ SUPPORT: " + DoubleToString(supportLevels[i].price, _Digits) + " ━━");
            ObjectSetInteger(0, labelName, OBJPROP_COLOR, SupportColor);
            ObjectSetInteger(0, labelName, OBJPROP_FONTSIZE, 9);
            ObjectSetInteger(0, labelName, OBJPROP_ANCHOR, ANCHOR_LEFT);
        }
    }

    // Afficher Résistances (ZONES rectangulaires)
    for(int i = 0; i < resistanceCount; i++)
    {
        if(resistanceLevels[i].is_valid)
        {
            string name = "ResistanceZone_" + IntegerToString(i);

            double priceHigh = resistanceLevels[i].price + zoneThickness;
            double priceLow = resistanceLevels[i].price - zoneThickness;

            // Créer ZONE rectangulaire
            ObjectCreate(0, name, OBJ_RECTANGLE, 0, timeStart, priceHigh, timeEnd, priceLow);
            ObjectSetInteger(0, name, OBJPROP_COLOR, ResistanceColor);
            ObjectSetInteger(0, name, OBJPROP_FILL, true);
            ObjectSetInteger(0, name, OBJPROP_BACK, true);
            ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
            ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);

            // Label au centre de la zone
            string labelName = "ResistanceLabel_" + IntegerToString(i);
            ObjectCreate(0, labelName, OBJ_TEXT, 0, timeNow, resistanceLevels[i].price);
            ObjectSetString(0, labelName, OBJPROP_TEXT, "━━ RESISTANCE: " + DoubleToString(resistanceLevels[i].price, _Digits) + " ━━");
            ObjectSetInteger(0, labelName, OBJPROP_COLOR, ResistanceColor);
            ObjectSetInteger(0, labelName, OBJPROP_FONTSIZE, 9);
            ObjectSetInteger(0, labelName, OBJPROP_ANCHOR, ANCHOR_LEFT);
        }
    }

    ChartRedraw();
}

//+------------------------------------------------------------------+
//| Supprime tous les objets S/R                                      |
//+------------------------------------------------------------------+
void DeleteAllSRObjects()
{
    for(int i = ObjectsTotal(0, 0, -1) - 1; i >= 0; i--)
    {
        string name = ObjectName(0, i);

        if(StringFind(name, "Support_") >= 0 ||
           StringFind(name, "SupportZone_") >= 0 ||
           StringFind(name, "Resistance_") >= 0 ||
           StringFind(name, "ResistanceZone_") >= 0 ||
           StringFind(name, "SupportLabel_") >= 0 ||
           StringFind(name, "ResistanceLabel_") >= 0)
        {
            ObjectDelete(0, name);
        }
    }
}

//+------------------------------------------------------------------+
//| V10: Place ordres Buy Limit (support) et Sell Limit (résistance) |
//+------------------------------------------------------------------+
void PlaceLimitOrdersOnSR()
{
    if(!UseLimitOrders)
        return;

    if(!tradingAllowed)
        return;

    // Vérifier toutes les 15 minutes
    if(TimeCurrent() - lastLimitOrderCheck < 900)
        return;

    lastLimitOrderCheck = TimeCurrent();

    // Compter ordres actifs
    int activeOrders = 0;
    for(int i = 0; i < 10; i++)
    {
        if(activeLimitOrders[i].is_active)
            activeOrders++;
    }

    if(activeOrders >= MaxLimitOrders)
    {
        Print("⏸️ Max ordres limites atteint (", activeOrders, "/", MaxLimitOrders, ")");
        return;
    }

    double pipValue = _Point * 10;
    double currentPrice = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

    // 1. PLACER BUY LIMIT SUR SUPPORTS
    for(int i = 0; i < supportCount; i++)
    {
        if(!supportLevels[i].is_valid)
            continue;

        if(activeOrders >= MaxLimitOrders)
            break;

        double supportPrice = supportLevels[i].price;

        // Vérifier que le prix actuel est AU-DESSUS du support
        if(currentPrice <= supportPrice)
            continue;

        // Vérifier qu'il n'y a pas déjà un ordre à ce niveau
        bool alreadyPlaced = false;
        for(int j = 0; j < 10; j++)
        {
            if(activeLimitOrders[j].is_active &&
               activeLimitOrders[j].is_buy &&
               MathAbs(activeLimitOrders[j].sr_level - supportPrice) < pipValue * 2)
            {
                alreadyPlaced = true;
                break;
            }
        }

        if(alreadyPlaced)
            continue;

        // Calculer prix d'entrée (légèrement au-dessus du support)
        double entryPrice = supportPrice + (LimitOrderOffset * pipValue);

        // Calculer SL dynamique basé sur ATR H1
        double atrH1 = lastATR_H1[0];
        double slDistance = (atrH1 / _Point / 10) * LimitSL_ATR_Multiplier;
        slDistance = MathMax(LimitSL_MinPips, MathMin(LimitSL_MaxPips, slDistance));
        double slPrice = supportPrice - (slDistance * pipValue);
        double slPips = (entryPrice - slPrice) / pipValue;

        // Calculer TP
        double tpPrice = entryPrice + (slPips * LimitTP_RR * pipValue);

        // Calculer lot size (avec ajustement FTMO)
        double lotSize = CalculateLotSize(slPips, 50); // Certitude fixe 50%

        // Placer Buy Limit
        datetime expiry = 0;
        if(LimitOrderExpiry > 0)
            expiry = TimeCurrent() + (LimitOrderExpiry * 60);

        if(trade.BuyLimit(lotSize, entryPrice, _Symbol, slPrice, tpPrice,
                          ORDER_TIME_SPECIFIED, expiry, TradeComment + "_BuyLimit_S" + IntegerToString(i)))
        {
            // Enregistrer l'ordre
            for(int j = 0; j < 10; j++)
            {
                if(!activeLimitOrders[j].is_active)
                {
                    activeLimitOrders[j].ticket = trade.ResultOrder();
                    activeLimitOrders[j].price = entryPrice;
                    activeLimitOrders[j].is_buy = true;
                    activeLimitOrders[j].sr_level = supportPrice;
                    activeLimitOrders[j].placed_time = TimeCurrent();
                    activeLimitOrders[j].is_active = true;
                    activeOrders++;
                    limitOrdersCount++;

                    Print("✅ BUY LIMIT placé sur Support ", supportPrice, " | Entry: ", entryPrice,
                          " | SL: ", slPrice, " | TP: ", tpPrice, " | Lot: ", lotSize);
                    break;
                }
            }
        }
        else
        {
            Print("❌ Erreur BUY LIMIT: ", trade.ResultRetcodeDescription());
        }
    }

    // 2. PLACER SELL LIMIT SUR RÉSISTANCES
    for(int i = 0; i < resistanceCount; i++)
    {
        if(!resistanceLevels[i].is_valid)
            continue;

        if(activeOrders >= MaxLimitOrders)
            break;

        double resistancePrice = resistanceLevels[i].price;

        // Vérifier que le prix actuel est EN-DESSOUS de la résistance
        if(currentPrice >= resistancePrice)
            continue;

        // Vérifier qu'il n'y a pas déjà un ordre à ce niveau
        bool alreadyPlaced = false;
        for(int j = 0; j < 10; j++)
        {
            if(activeLimitOrders[j].is_active &&
               !activeLimitOrders[j].is_buy &&
               MathAbs(activeLimitOrders[j].sr_level - resistancePrice) < pipValue * 2)
            {
                alreadyPlaced = true;
                break;
            }
        }

        if(alreadyPlaced)
            continue;

        // Calculer prix d'entrée (légèrement en-dessous de la résistance)
        double entryPrice = resistancePrice - (LimitOrderOffset * pipValue);

        // Calculer SL dynamique basé sur ATR H1
        double atrH1 = lastATR_H1[0];
        double slDistance = (atrH1 / _Point / 10) * LimitSL_ATR_Multiplier;
        slDistance = MathMax(LimitSL_MinPips, MathMin(LimitSL_MaxPips, slDistance));
        double slPrice = resistancePrice + (slDistance * pipValue);
        double slPips = (slPrice - entryPrice) / pipValue;

        // Calculer TP
        double tpPrice = entryPrice - (slPips * LimitTP_RR * pipValue);

        // Calculer lot size (avec ajustement FTMO)
        double lotSize = CalculateLotSize(slPips, 50); // Certitude fixe 50%

        // Placer Sell Limit
        datetime expiry = 0;
        if(LimitOrderExpiry > 0)
            expiry = TimeCurrent() + (LimitOrderExpiry * 60);

        if(trade.SellLimit(lotSize, entryPrice, _Symbol, slPrice, tpPrice,
                           ORDER_TIME_SPECIFIED, expiry, TradeComment + "_SellLimit_R" + IntegerToString(i)))
        {
            // Enregistrer l'ordre
            for(int j = 0; j < 10; j++)
            {
                if(!activeLimitOrders[j].is_active)
                {
                    activeLimitOrders[j].ticket = trade.ResultOrder();
                    activeLimitOrders[j].price = entryPrice;
                    activeLimitOrders[j].is_buy = false;
                    activeLimitOrders[j].sr_level = resistancePrice;
                    activeLimitOrders[j].placed_time = TimeCurrent();
                    activeLimitOrders[j].is_active = true;
                    activeOrders++;
                    limitOrdersCount++;

                    Print("✅ SELL LIMIT placé sur Résistance ", resistancePrice, " | Entry: ", entryPrice,
                          " | SL: ", slPrice, " | TP: ", tpPrice, " | Lot: ", lotSize);
                    break;
                }
            }
        }
        else
        {
            Print("❌ Erreur SELL LIMIT: ", trade.ResultRetcodeDescription());
        }
    }
}

//+------------------------------------------------------------------+
//| V10: Gère les ordres limites (vérifier si cassés, expirés)       |
//+------------------------------------------------------------------+
void ManageLimitOrders()
{
    if(!UseLimitOrders)
        return;

    double currentPrice = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
    double pipValue = _Point * 10;

    // 1. PROTECTION FTMO : Annuler TOUS les ordres si proche des limites
    if(MathAbs(dailyPnL) >= 1500 || MathAbs(totalDrawdown) >= 3000)
    {
        Print("🚨 PROTECTION FTMO : Annulation de TOUS les ordres limites");
        Print("   Daily Loss: -€", MathAbs(dailyPnL), " | Drawdown: -€", MathAbs(totalDrawdown));

        for(int i = 0; i < 10; i++)
        {
            if(activeLimitOrders[i].is_active)
            {
                trade.OrderDelete(activeLimitOrders[i].ticket);
                activeLimitOrders[i].is_active = false;
            }
        }
        return;
    }

    // 2. ATR EXPLOSIF : Annuler TOUS si volatilité anormale
    double currentATR_H1 = lastATR_H1[0];
    double avgATR = 0;
    for(int k = 0; k < 20 && k < ArraySize(lastATR_H1); k++)
        avgATR += lastATR_H1[k];
    avgATR /= MathMin(20, ArraySize(lastATR_H1));

    if(currentATR_H1 > avgATR * 1.8)
    {
        Print("🚨 ATR EXPLOSIF : ", currentATR_H1, " > ", avgATR * 1.8, " - Annulation ordres");

        for(int i = 0; i < 10; i++)
        {
            if(activeLimitOrders[i].is_active)
            {
                trade.OrderDelete(activeLimitOrders[i].ticket);
                activeLimitOrders[i].is_active = false;
            }
        }
        return;
    }

    // 3. VÉRIFICATION INDIVIDUELLE DES ORDRES
    for(int i = 0; i < 10; i++)
    {
        if(!activeLimitOrders[i].is_active)
            continue;

        // Vérifier si l'ordre existe toujours (MT5)
        bool orderExists = false;
        for(int j = 0; j < OrdersTotal(); j++)
        {
            ulong ticket = OrderGetTicket(j);
            if(ticket == activeLimitOrders[i].ticket)
            {
                orderExists = true;
                break;
            }
        }

        if(!orderExists)
        {
            // Ordre n'existe plus (exécuté, expiré ou annulé)
            activeLimitOrders[i].is_active = false;
            continue;
        }

        bool cancelOrder = false;
        string cancelReason = "";

        // CONDITION 1 : S/R cassé (±40 pips pour CRYPTO)
        if(activeLimitOrders[i].is_buy)
        {
            if(currentPrice < (activeLimitOrders[i].sr_level - pipValue * 40))
            {
                cancelOrder = true;
                cancelReason = "Support cassé -40 pips";
            }
        }
        else
        {
            if(currentPrice > (activeLimitOrders[i].sr_level + pipValue * 40))
            {
                cancelOrder = true;
                cancelReason = "Résistance cassée +40 pips";
            }
        }

        // CONDITION 2 : Ordre ancien (>3h sans exécution)
        if(TimeCurrent() - activeLimitOrders[i].placed_time > 10800) // 3h
        {
            cancelOrder = true;
            cancelReason = "Ordre ancien (>3h) - S/R obsolète";
        }

        if(cancelOrder)
        {
            Print("⚠️ Annulation ordre limite: ", cancelReason, " | Ticket: ", activeLimitOrders[i].ticket);

            if(trade.OrderDelete(activeLimitOrders[i].ticket))
            {
                Print("✅ Ordre annulé avec succès");
            }

            activeLimitOrders[i].is_active = false;
        }
    }
}

//+------------------------------------------------------------------+
//| V10: Vérifie les news économiques (15min avant/après)             |
//+------------------------------------------------------------------+
bool IsEconomicNewsSafe()
{
    if(!CheckEconomicNews)
        return true;  // Désactivé pour crypto

    // Vérifier toutes les 5 minutes
    if(TimeCurrent() - lastNewsCheck < 300)
    {
        if(newsBlockActive && TimeCurrent() < nextNewsTime)
        {
            return false;
        }
        else if(newsBlockActive && TimeCurrent() >= nextNewsTime)
        {
            newsBlockActive = false;
            riskMultiplier = 1.0;  // Remettre risque normal
            Print("📅 Fin période protection news");
        }
        return !newsBlockActive;
    }

    lastNewsCheck = TimeCurrent();

    // Appel API Guardian pour news HIGH IMPACT uniquement
    string url = StringFormat("%s/calendar/high_impact", StringSubstr(GuardianURL, 0, StringFind(GuardianURL, "/validate")));

    char post[], result[];
    string headers = "Content-Type: application/json\r\n";
    int timeout = 5000;

    int res = WebRequest("GET", url, headers, timeout, post, result, headers);

    if(res == 200)
    {
        string response = CharArrayToString(result);

        if(StringFind(response, "\"upcoming_in_15min\":true") > 0)
        {
            Print("⚠️ NEWS HIGH IMPACT dans 15min! Réduction risque à 50%");
            newsBlockActive = true;
            nextNewsTime = TimeCurrent() + (NewsBufferMinutes * 60);
            riskMultiplier = 0.5;  // Réduire lots à 50%
            return true;  // On continue de trader mais avec moins de risque
        }
    }

    return true;
}

//+------------------------------------------------------------------+
//| ANALYSE COMPLÈTE DU MARCHÉ - MA2 × MA12                          |
//+------------------------------------------------------------------+
void AnalyzeMarket()
{
    Print("🔍 Analyse ETH/USD V10 (MA", MA_Fast, " × MA", MA_Slow, ")...");

    // 1. SIGNAL MA CROSSOVER
    bool crossUp = DetectCrossUp();    // MA2 croise MA12 vers le HAUT
    bool crossDown = DetectCrossDown(); // MA2 croise MA12 vers le BAS

    if(!crossUp && !crossDown)
    {
        // Pas de signal, on continue
        return;
    }

    // 2. DÉTERMINER LA DIRECTION
    string direction = "";
    if(crossUp) direction = "BUY";
    else if(crossDown) direction = "SELL";

    Print("🎯 Signal MA Crossover détecté: ", direction);

    // 3. VALIDATION RSI (éviter zones extrêmes)
    if(CheckRSI)
    {
        if(lastRSI[0] > 80)
        {
            Print("❌ RSI surachat (", DoubleToString(lastRSI[0], 1), ") - Signal ignoré");
            return;
        }

        if(lastRSI[0] < 20)
        {
            Print("❌ RSI survente (", DoubleToString(lastRSI[0], 1), ") - Signal ignoré");
            return;
        }
    }

    // 4. CALCULER CONFLUENCE SCORE
    int confluenceScore = CalculateConfluence(direction);

    Print("📊 Confluence Score: ", confluenceScore, "/100");

    if(confluenceScore < MinConfluenceScore)
    {
        Print("❌ Confluence insuffisante (min: ", MinConfluenceScore, ")");
        return;
    }

    // 5. CALCULER CERTITUDE %
    int certaintyPercent = CalculateCertainty(confluenceScore, direction);

    Print("🎲 Certitude: ", certaintyPercent, "%");

    if(certaintyPercent < MinCertaintyPercent)
    {
        Print("❌ Certitude insuffisante (min: ", MinCertaintyPercent, "%)");
        return;
    }

    // 6. CALCULER SL/TP DYNAMIQUES
    double slPips = CalculateDynamicSL();

    SignalData signal;
    signal.pair = _Symbol;
    signal.direction = direction;
    signal.timestamp = TimeCurrent();
    signal.confluence_score = confluenceScore;
    signal.certainty_percent = certaintyPercent;
    signal.sl_pips = slPips;

    // Prix d'entrée
    if(direction == "BUY")
        signal.entry_price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
    else
        signal.entry_price = SymbolInfoDouble(_Symbol, SYMBOL_BID);

    // Calculer SL et TP
    double pipValue = _Point * 10;

    if(direction == "BUY")
    {
        signal.sl_price = signal.entry_price - (slPips * pipValue);
        signal.tp1_price = signal.entry_price + (slPips * TP1_RR * pipValue);
        signal.tp2_price = signal.entry_price + (slPips * TP2_RR * pipValue);
        signal.tp3_price = signal.entry_price + (slPips * TP3_RR * pipValue);
    }
    else // SELL
    {
        signal.sl_price = signal.entry_price + (slPips * pipValue);
        signal.tp1_price = signal.entry_price - (slPips * TP1_RR * pipValue);
        signal.tp2_price = signal.entry_price - (slPips * TP2_RR * pipValue);
        signal.tp3_price = signal.entry_price - (slPips * TP3_RR * pipValue);
    }

    // Calculer lot size (avec ajustement FTMO)
    signal.lot_size = CalculateLotSize(slPips, certaintyPercent);

    // Générer raison du signal
    signal.signal_reason = GenerateSignalReason(direction, confluenceScore, certaintyPercent);

    Print("🎯 Signal généré: ", direction, " | Entry: ", signal.entry_price,
          " | SL: ", slPips, " pips | Certitude: ", certaintyPercent, "%");

    // 7. ENVOYER AU GUARDIAN
    if(SendSignalToGuardian(signal))
    {
        OpenPosition(signal);
    }
}

//+------------------------------------------------------------------+
//| Détecte MA2 croise MA12 vers le HAUT                             |
//+------------------------------------------------------------------+
bool DetectCrossUp()
{
    // Barre précédente: MA2 <= MA12
    // Barre actuelle: MA2 > MA12

    bool previousBelow = (lastMA_Fast[1] <= lastMA_Slow[1]);
    bool currentAbove = (lastMA_Fast[0] > lastMA_Slow[0]);

    if(previousBelow && currentAbove)
    {
        Print("✅ MA CROSS UP détecté! (MA", MA_Fast, " × MA", MA_Slow, ")");
        return true;
    }

    return false;
}

//+------------------------------------------------------------------+
//| Détecte MA2 croise MA12 vers le BAS                              |
//+------------------------------------------------------------------+
bool DetectCrossDown()
{
    // Barre précédente: MA2 >= MA12
    // Barre actuelle: MA2 < MA12

    bool previousAbove = (lastMA_Fast[1] >= lastMA_Slow[1]);
    bool currentBelow = (lastMA_Fast[0] < lastMA_Slow[0]);

    if(previousAbove && currentBelow)
    {
        Print("✅ MA CROSS DOWN détecté! (MA", MA_Fast, " × MA", MA_Slow, ")");
        return true;
    }

    return false;
}

//+------------------------------------------------------------------+
//| Calcule le score de confluence /100                               |
//+------------------------------------------------------------------+
int CalculateConfluence(string direction)
{
    int score = 0;

    // 1. MA Crossover (TRIGGER) = 30 points
    score += 30;
    Print("   ✓ MA Crossover: +30 pts");

    // 2. RSI dans zone favorable (20 points)
    if(direction == "BUY" && lastRSI[0] < 70 && lastRSI[0] > 30)
    {
        score += 20;
        Print("   ✓ RSI favorable (", DoubleToString(lastRSI[0], 1), "): +20 pts");
    }
    else if(direction == "SELL" && lastRSI[0] > 30 && lastRSI[0] < 70)
    {
        score += 20;
        Print("   ✓ RSI favorable (", DoubleToString(lastRSI[0], 1), "): +20 pts");
    }

    // 3. Prix proche d'un Support (BUY) ou Résistance (SELL) (20 points)
    double currentPrice = (direction == "BUY") ? SymbolInfoDouble(_Symbol, SYMBOL_ASK) : SymbolInfoDouble(_Symbol, SYMBOL_BID);
    double tolerance = lastATR[0] * 0.3;

    if(direction == "BUY")
    {
        for(int i = 0; i < supportCount; i++)
        {
            if(supportLevels[i].is_valid && MathAbs(currentPrice - supportLevels[i].price) < tolerance)
            {
                score += 20;
                Print("   ✓ Prix proche Support: +20 pts");
                break;
            }
        }
    }
    else // SELL
    {
        for(int i = 0; i < resistanceCount; i++)
        {
            if(resistanceLevels[i].is_valid && MathAbs(currentPrice - resistanceLevels[i].price) < tolerance)
            {
                score += 20;
                Print("   ✓ Prix proche Résistance: +20 pts");
                break;
            }
        }
    }

    // 4. Volatilité normale (10 points)
    if(lastATR[0] < lastATR[1] * 1.5)
    {
        score += 10;
        Print("   ✓ Volatilité normale: +10 pts");
    }

    // 5. Momentum (différence MA2-MA12) (10 points)
    double maDiff = MathAbs(lastMA_Fast[0] - lastMA_Slow[0]);
    if(maDiff > lastATR[0] * 0.2)
    {
        score += 10;
        Print("   ✓ Momentum fort: +10 pts");
    }

    return score;
}

//+------------------------------------------------------------------+
//| Calcule le pourcentage de certitude                               |
//+------------------------------------------------------------------+
int CalculateCertainty(int confluenceScore, string direction)
{
    // Base = score de confluence
    int certainty = (int)(confluenceScore * 0.8);

    // BONUS

    // +10% si crossover net
    if(MathAbs(lastMA_Fast[0] - lastMA_Slow[0]) > (lastATR[0] * 0.3))
    {
        certainty += 10;
        Print("   ✓ Crossover net: +10%");
    }

    // +5% si ATR stable
    if(lastATR[0] < lastATR[1] * 1.3)
    {
        certainty += 5;
        Print("   ✓ Volatilité stable: +5%");
    }

    // PÉNALITÉS

    // -10% si volatilité élevée
    if(lastATR[0] > lastATR[1] * 1.8)
    {
        certainty -= 10;
        Print("   ⚠️ Volatilité élevée: -10%");
    }

    // -15% si RSI extrême
    if(lastRSI[0] > 75 || lastRSI[0] < 25)
    {
        certainty -= 15;
        Print("   ⚠️ RSI extrême (", DoubleToString(lastRSI[0], 1), "): -15%");
    }

    // Limiter entre 20% et 95%
    if(certainty > 95) certainty = 95;
    if(certainty < 20) certainty = 20;

    return certainty;
}

//+------------------------------------------------------------------+
//| Calcule le SL dynamique basé sur ATR                              |
//+------------------------------------------------------------------+
double CalculateDynamicSL()
{
    double atrValue = lastATR[0];
    double pipValue = _Point * 10;

    // SL = ATR × Multiplier
    double slPips = (atrValue / pipValue) * ATR_Multiplier_SL;

    // Limiter entre min et max
    if(slPips < SL_MinPips) slPips = SL_MinPips;
    if(slPips > SL_MaxPips) slPips = SL_MaxPips;

    Print("📏 SL Dynamique: ", DoubleToString(slPips, 1), " pips (ATR: ",
          DoubleToString(atrValue / pipValue, 1), " pips × ", ATR_Multiplier_SL, ")");

    return slPips;
}

//+------------------------------------------------------------------+
//| Calcule la taille du lot (ajustée FTMO + certitude)               |
//+------------------------------------------------------------------+
double CalculateLotSize(double slPips, int certaintyPercent)
{
    // Ajuster le risque selon la certitude ET le multiplicateur FTMO
    double adjustedRisk = RiskPercent * riskMultiplier;

    if(certaintyPercent >= 80)
        adjustedRisk = adjustedRisk * 1.0;
    else if(certaintyPercent >= 70)
        adjustedRisk = adjustedRisk * 0.8;
    else if(certaintyPercent >= 60)
        adjustedRisk = adjustedRisk * 0.7;
    else if(certaintyPercent >= 50)
        adjustedRisk = adjustedRisk * 0.6;
    else
        adjustedRisk = adjustedRisk * 0.5;

    double balance = account.Balance();
    double riskAmount = balance * (adjustedRisk / 100.0);

    double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
    double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
    double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);

    double slDistance = slPips * point * 10;
    double lotSize = riskAmount / (slDistance / tickSize * tickValue);

    // Arrondir selon contraintes
    double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
    double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
    double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);

    lotSize = MathFloor(lotSize / stepLot) * stepLot;
    lotSize = MathMax(lotSize, minLot);
    lotSize = MathMin(lotSize, maxLot);

    Print("💰 Lot ajusté: ", lotSize, " (Risque: ", DoubleToString(adjustedRisk, 2),
          "% | Mult FTMO: ", riskMultiplier, " | Certitude: ", certaintyPercent, "%)");

    return lotSize;
}

//+------------------------------------------------------------------+
//| Génère la raison du signal                                        |
//+------------------------------------------------------------------+
string GenerateSignalReason(string direction, int confluence, int certainty)
{
    string reason = "";

    if(direction == "BUY")
        reason = "MA" + IntegerToString(MA_Fast) + " croise MA" + IntegerToString(MA_Slow) + " à la HAUSSE";
    else
        reason = "MA" + IntegerToString(MA_Fast) + " croise MA" + IntegerToString(MA_Slow) + " à la BAISSE";

    reason += " | Confluence: " + IntegerToString(confluence) + "/100";
    reason += " | Certitude: " + IntegerToString(certainty) + "%";

    return reason;
}

//+------------------------------------------------------------------+
//| Envoie le signal au Guardian Python                               |
//+------------------------------------------------------------------+
bool SendSignalToGuardian(SignalData &signal)
{
    if(!RequireApproval)
        return true;

    // Construire le JSON
    string json = StringFormat(
        "{\"pair\":\"%s\",\"direction\":\"%s\",\"entry_price\":%.5f,\"sl_price\":%.5f,\"sl_pips\":%.1f,"
        "\"tp1_price\":%.5f,\"tp2_price\":%.5f,\"tp3_price\":%.5f,\"lot_size\":%.2f,"
        "\"confluence_score\":%d,\"certainty_percent\":%d,\"signal_reason\":\"%s\"}",
        signal.pair, signal.direction, signal.entry_price, signal.sl_price, signal.sl_pips,
        signal.tp1_price, signal.tp2_price, signal.tp3_price, signal.lot_size,
        signal.confluence_score, signal.certainty_percent, signal.signal_reason
    );

    char post[], result[];
    string headers = "Content-Type: application/json\r\n";
    StringToCharArray(json, post, 0, WHOLE_ARRAY);

    int timeout = API_Timeout;
    int res = WebRequest("POST", GuardianURL, headers, timeout, post, result, headers);

    if(res == -1)
    {
        Print("❌ Erreur WebRequest: ", GetLastError());
        Print("⚠️ Vérifiez que ", GuardianURL, " est autorisé dans MT5");
        return false;
    }

    string response = CharArrayToString(result);
    Print("📥 Réponse Guardian: ", response);

    if(StringFind(response, "\"approved\":true") >= 0 || StringFind(response, "\"approved\": true") >= 0)
    {
        Print("✅ Signal APPROUVÉ par Guardian");
        return true;
    }
    else
    {
        Print("❌ Signal REJETÉ par Guardian");
        return false;
    }
}

//+------------------------------------------------------------------+
//| Ouvre une position                                                 |
//+------------------------------------------------------------------+
void OpenPosition(SignalData &signal)
{
    Print("════════════════════════════════════════");
    Print("📈 OUVERTURE POSITION ETH/USD V10");
    Print("════════════════════════════════════════");
    Print("Direction: ", signal.direction);
    Print("Entry: ", signal.entry_price);
    Print("SL: ", signal.sl_price, " (", signal.sl_pips, " pips)");
    Print("TP1: ", signal.tp1_price, " (1:", TP1_RR, ") → Fermer ", TP1_ClosePercent, "%");
    Print("TP2: ", signal.tp2_price, " (1:", TP2_RR, ") → Fermer ", TP2_ClosePercent, "%");
    Print("TP3: ", signal.tp3_price, " (1:", TP3_RR, ") → Fermer ", TP3_ClosePercent, "%");
    Print("Lot: ", signal.lot_size);
    Print("Confluence: ", signal.confluence_score, "/100");
    Print("Certitude: ", signal.certainty_percent, "%");
    Print("Raison: ", signal.signal_reason);
    Print("════════════════════════════════════════");

    bool success = false;

    if(signal.direction == "BUY")
    {
        success = trade.Buy(signal.lot_size, signal.pair, signal.entry_price,
                           signal.sl_price, signal.tp1_price, TradeComment);
    }
    else if(signal.direction == "SELL")
    {
        success = trade.Sell(signal.lot_size, signal.pair, signal.entry_price,
                            signal.sl_price, signal.tp1_price, TradeComment);
    }

    if(success)
    {
        Print("✅ Position ouverte avec succès!");
        tradesCountToday++;

        // Notification Telegram STYLÉE
        string emoji = (signal.direction == "BUY") ? "🟢" : "🔴";
        string alert = "╔═══════════════════════════════╗\n";
        alert += "║  🎯 NOUVELLE POSITION OUVERTE  ║\n";
        alert += "╚═══════════════════════════════╝\n\n";
        alert += emoji + " *" + signal.direction + " " + signal.pair + "*\n\n";
        alert += "💰 Entry: `" + DoubleToString(signal.entry_price, _Digits) + "`\n";
        alert += "🛡️ SL: `" + DoubleToString(signal.sl_price, _Digits) + "` (" + DoubleToString(signal.sl_pips, 1) + " pips)\n";
        alert += "🎯 TP1: `" + DoubleToString(signal.tp1_price, _Digits) + "` (1:" + DoubleToString(TP1_RR, 1) + ")\n";
        alert += "🎯 TP2: `" + DoubleToString(signal.tp2_price, _Digits) + "` (1:" + DoubleToString(TP2_RR, 1) + ")\n";
        alert += "🎯 TP3: `" + DoubleToString(signal.tp3_price, _Digits) + "` (1:" + DoubleToString(TP3_RR, 1) + ")\n\n";
        alert += "📊 Lot: `" + DoubleToString(signal.lot_size, 2) + "`\n";
        alert += "📈 Confluence: *" + IntegerToString(signal.confluence_score) + "/100*\n";
        alert += "🎲 Certitude: *" + IntegerToString(signal.certainty_percent) + "%*\n\n";
        alert += "💡 " + signal.signal_reason + "\n\n";
        alert += "━━━━━━━━━━━━━━━━━━━━━━━\n";
        alert += "✅ Position active - Good luck! 🚀";

        SendTelegramAlert(alert);
    }
    else
    {
        Print("❌ Erreur ouverture: ", trade.ResultRetcodeDescription());
    }
}

//+------------------------------------------------------------------+
//| Gère les positions ouvertes (BE, Trailing, TP partiels)          |
//+------------------------------------------------------------------+
void ManageOpenPositions()
{
    for(int i = PositionsTotal() - 1; i >= 0; i--)
    {
        if(position.SelectByIndex(i))
        {
            if(position.Symbol() == _Symbol && position.Magic() == MagicNumber)
            {
                double openPrice = position.PriceOpen();
                double currentPrice = position.PriceCurrent();
                double sl = position.StopLoss();
                double tp = position.TakeProfit();

                bool isBuy = (position.Type() == POSITION_TYPE_BUY);

                // Calculer les distances
                double pipValue = _Point * 10;
                double slPips = MathAbs(openPrice - sl) / pipValue;

                // Calculer les niveaux TP
                double tp1_price, tp2_price, tp3_price;
                if(isBuy)
                {
                    tp1_price = openPrice + (slPips * TP1_RR * pipValue);
                    tp2_price = openPrice + (slPips * TP2_RR * pipValue);
                    tp3_price = openPrice + (slPips * TP3_RR * pipValue);
                }
                else
                {
                    tp1_price = openPrice - (slPips * TP1_RR * pipValue);
                    tp2_price = openPrice - (slPips * TP2_RR * pipValue);
                    tp3_price = openPrice - (slPips * TP3_RR * pipValue);
                }

                // 1. GESTION BREAK EVEN
                if(!BE_Activated)
                {
                    double distanceToTP1 = isBuy ? (tp1_price - openPrice) : (openPrice - tp1_price);
                    double currentDistance = isBuy ? (currentPrice - openPrice) : (openPrice - currentPrice);
                    double percentToTP1 = (currentDistance / distanceToTP1) * 100.0;

                    if(percentToTP1 >= BE_ActivationPercent)
                    {
                        double newSL = openPrice + (BE_OffsetPips * pipValue * (isBuy ? 1 : -1));

                        if(trade.PositionModify(position.Ticket(), newSL, tp))
                        {
                            BE_Activated = true;
                            Print("🛡️ BREAK EVEN activé @ ", newSL, " (", percentToTP1, "% vers TP1)");

// Notification Telegram Break Even
                            string beAlert = "🛡️ *BREAK EVEN ACTIVÉ*

";
                            beAlert += "Position sécurisée à BE!
";
                            beAlert += "SL déplacé: `" + DoubleToString(newSL, _Digits) + "`

";
                            beAlert += "📊 Progression: " + DoubleToString(percentToTP1, 1) + "% vers TP1
";
                            beAlert += "✅ Plus de risque - Trade protégé!";
                            SendTelegramAlert(beAlert);
                        }
                        }
                    }
                }

                // 2. GESTION TP PARTIELS

                // TP3 atteint
                if(!TP3_Hit)
                {
                    bool tp3Reached = isBuy ? (currentPrice >= tp3_price) : (currentPrice <= tp3_price);
                    if(tp3Reached)
                    {
                        ClosePartialPosition(position.Ticket(), TP3_ClosePercent);
                        TP3_Hit = true;
                        Print("🎯 TP3 ATTEINT! (1:", TP3_RR, ") → Fermé ", TP3_ClosePercent, "%");

// Notification Telegram TP3 - MEGA WIN!
                        string tp3Alert = "╔═══════════════════════════════╗
";
                        tp3Alert += "║  🚀 TP3 ATTEINT - MEGA WIN! 🚀 ║
";
                        tp3Alert += "╚═══════════════════════════════╝

";
                        tp3Alert += "🎉🎉🎉 *FÉLICITATIONS!* 🎉🎉🎉

";
                        tp3Alert += "💰 Take Profit 3 touché!
";
                        tp3Alert += "📊 Ratio: *1:" + DoubleToString(TP3_RR, 1) + "*
";
                        tp3Alert += "✅ Fermé " + DoubleToString(TP3_ClosePercent, 0) + "% de la position

";
                        tp3Alert += "███████████████████ 100%

";
                        tp3Alert += "🏆 TRADE PARFAIT - GG!
";
                        tp3Alert += "💎 Maximum profit sécurisé! 💎";
                        SendTelegramAlert(tp3Alert);
                    }
                    }
                }

                // TP2 atteint
                if(!TP2_Hit && TP3_Hit == false)
                {
                    bool tp2Reached = isBuy ? (currentPrice >= tp2_price) : (currentPrice <= tp2_price);
                    if(tp2Reached)
                    {
                        ClosePartialPosition(position.Ticket(), TP2_ClosePercent);
                        TP2_Hit = true;
                        Print("🎯 TP2 ATTEINT! (1:", TP2_RR, ") → Fermé ", TP2_ClosePercent, "%");

// Notification Telegram TP2 - EXCELLENT!
                        string tp2Alert = "╔═══════════════════════════════╗
";
                        tp2Alert += "║   🎯 TP2 ATTEINT - EXCELLENT!  ║
";
                        tp2Alert += "╚═══════════════════════════════╝

";
                        tp2Alert += "🎊 *SUPER TRADE!* 🎊

";
                        tp2Alert += "💰 Take Profit 2 touché!
";
                        tp2Alert += "📊 Ratio: *1:" + DoubleToString(TP2_RR, 1) + "*
";
                        tp2Alert += "✅ Fermé " + DoubleToString(TP2_ClosePercent, 0) + "% de la position

";
                        tp2Alert += "█████████████░░░░░░ 70%

";
                        tp2Alert += "📈 Reste 20% pour TP3!
";
                        tp2Alert += "🚀 Let it run! 💰";
                        SendTelegramAlert(tp2Alert);
                    }
                    }
                }

                // TP1 atteint
                if(!TP1_Hit && TP2_Hit == false)
                {
                    bool tp1Reached = isBuy ? (currentPrice >= tp1_price) : (currentPrice <= tp1_price);
                    if(tp1Reached)
                    {
                        ClosePartialPosition(position.Ticket(), TP1_ClosePercent);
                        TP1_Hit = true;
                        Print("🎯 TP1 ATTEINT! (1:", TP1_RR, ") → Fermé ", TP1_ClosePercent, "%");

// Notification Telegram TP1 - NICE!
                        string tp1Alert = "╔═══════════════════════════════╗
";
                        tp1Alert += "║    💰 TP1 ATTEINT - NICE! 💰   ║
";
                        tp1Alert += "╚═══════════════════════════════╝

";
                        tp1Alert += "✅ *PREMIER TAKE PROFIT!* ✅

";
                        tp1Alert += "🎯 Take Profit 1 touché!
";
                        tp1Alert += "📊 Ratio: *1:" + DoubleToString(TP1_RR, 1) + "*
";
                        tp1Alert += "✅ Fermé " + DoubleToString(TP1_ClosePercent, 0) + "% de la position

";
                        tp1Alert += "██████░░░░░░░░░░░░░ 30%

";
                        tp1Alert += "📈 Reste 70% en course!
";
                        tp1Alert += "🎯 Objectif TP2 & TP3!
";
                        if(TrailingAfterTP1)
                            tp1Alert += "🔄 Trailing activé - Let's go! 🚀";
                        SendTelegramAlert(tp1Alert);

                        // Activer trailing après TP1
                        if(TrailingAfterTP1)
                        {
                            Trailing_Active = true;
                            Print("🔄 TRAILING activé après TP1");

                        // Activer trailing après TP1
                        if(TrailingAfterTP1)
                        {
                            Trailing_Active = true;
                            Print("🔄 TRAILING activé après TP1");
                        }
                    }
                }

                // 3. GESTION TRAILING STOP
                if(Trailing_Active && TP1_Hit)
                {
                    double trailingDistance = lastATR[0] * Trailing_ATR_Multiplier;
                    double newSL;

                    if(isBuy)
                    {
                        newSL = currentPrice - trailingDistance;
                        if(newSL > sl && newSL > openPrice)
                        {
                            if(trade.PositionModify(position.Ticket(), newSL, tp))
                            {
                                Print("🔄 TRAILING ajusté: SL → ", newSL, " (ATR × ", Trailing_ATR_Multiplier, ")");
                            }
                        }
                    }
                    else // SELL
                    {
                        newSL = currentPrice + trailingDistance;
                        if(newSL < sl && newSL < openPrice)
                        {
                            if(trade.PositionModify(position.Ticket(), newSL, tp))
                            {
                                Print("🔄 TRAILING ajusté: SL → ", newSL, " (ATR × ", Trailing_ATR_Multiplier, ")");
                            }
                        }
                    }
                }
            }
        }
    }
}

//+------------------------------------------------------------------+
//| Ferme une position partiellement                                  |
//+------------------------------------------------------------------+
void ClosePartialPosition(ulong ticket, double percent)
{
    if(position.SelectByTicket(ticket))
    {
        double currentVolume = position.Volume();
        double volumeToClose = currentVolume * (percent / 100.0);

        // Arrondir selon step
        double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
        volumeToClose = MathFloor(volumeToClose / stepLot) * stepLot;

        // Minimum
        double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
        if(volumeToClose < minLot)
            volumeToClose = minLot;

        // Ne pas fermer plus que disponible
        if(volumeToClose > currentVolume)
            volumeToClose = currentVolume;

        if(trade.PositionClosePartial(ticket, volumeToClose))
        {
            Print("✅ Fermeture partielle: ", volumeToClose, " lots (", percent, "%)");
        }
        else
        {
            Print("❌ Erreur fermeture partielle: ", trade.ResultRetcodeDescription());
        }
    }
}

//+------------------------------------------------------------------+
//| Vérifie si une position est ouverte                               |
//+------------------------------------------------------------------+
bool HasOpenPosition()
{
    for(int i = 0; i < PositionsTotal(); i++)
    {
        if(position.SelectByIndex(i))
        {
            if(position.Symbol() == _Symbol && position.Magic() == MagicNumber)
                return true;
        }
    }
    return false;
}

//+------------------------------------------------------------------+
//| Envoie alerte Telegram (via Guardian)                             |
//+------------------------------------------------------------------+
void SendTelegramAlert(string message)
{
    string url = StringFormat("%s/telegram/alert", StringSubstr(GuardianURL, 0, StringFind(GuardianURL, "/validate")));

    string json = "{\"message\":\"" + message + "\"}";

    char post[], result[];
    string headers = "Content-Type: application/json\r\n";
    StringToCharArray(json, post, 0, WHOLE_ARRAY);

    WebRequest("POST", url, headers, 5000, post, result, headers);
}

//+------------------------------------------------------------------+

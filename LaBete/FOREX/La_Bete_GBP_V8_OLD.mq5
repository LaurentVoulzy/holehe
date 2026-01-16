//+------------------------------------------------------------------+
//|                                           La_Bete_GBP.mq5         |
//|                                    Copyright 2025, Yann - La Bête  |
//|                                                                      |
//| BOT SPÉCIALISÉ GBP/USD - PROP FIRM COMPLIANT                       |
//| - EMA Crossover Strategy (Golden/Death Cross)                      |
//| - Smart Money Concepts (OB, FVG, BOS, CHoCH)                       |
//| - Confluence Scoring /100 + Certainty %                            |
//| - Dynamic ATR-based SL/TP (NO FIXED %)                            |
//| - Triple TP (50% / 30% / 20%) + BE + Trailing                     |
//| - Economic Calendar Integration                                    |
//+------------------------------------------------------------------+

#property copyright "Yann - La Bête"
#property version   "8.00"
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
input group "=== CONFIGURATION GBP/USD ==="
input double   RiskPercent = 0.3;           // Risque par trade (%)
input int      MagicNumber = 666002;        // Magic Number EUR
input string   TradeComment = "LaBete_GBP"; // Commentaire

input group "=== CONFLUENCE & SMC ==="
input int      MinConfluenceScore = 90;     // Score confluence minimum (/100)
input int      MinCertaintyPercent = 50;    // Certitude minimum (%)
input int      OB_Lookback = 50;            // Barres pour Order Blocks
input int      FVG_MinSize = 15;            // Taille min FVG (pips)
input double   OB_TolerancePips = 3.0;      // Tolérance prix dans OB (pips)

input group "=== STOP LOSS / TAKE PROFIT (ATR) ==="
input int      SL_MinPips = 80;             // SL minimum EUR (pips)
input int      SL_MaxPips = 120;             // SL maximum EUR (pips)
input double   ATR_Multiplier_SL = 1.8;     // ATR × 1.5 pour EUR
input double   TP1_RR = 2.0;                // TP1 Risk:Reward 1:2
input double   TP2_RR = 3.0;                // TP2 Risk:Reward 1:3
input double   TP3_RR = 5.0;                // TP3 Risk:Reward 1:5

input group "=== PARTIAL CLOSES ==="
input double   TP1_ClosePercent = 50.0;     // Fermer 50% à TP1
input double   TP2_ClosePercent = 30.0;     // Fermer 30% à TP2
input double   TP3_ClosePercent = 20.0;     // Fermer 20% à TP3

input group "=== BREAK EVEN & TRAILING ==="
input double   BE_ActivationPercent = 50.0; // Activation BE (50% vers TP1)
input int      BE_OffsetPips = 10;          // Offset BE (pips)
input bool     TrailingAfterTP1 = true;     // Activer trailing après TP1
input double   Trailing_ATR_Multiplier = 0.5; // Trailing = ATR × 0.5

input group "=== INDICATEURS EMA ==="
input int      EMA_Fast = 20;               // EMA rapide (Golden/Death Cross)
input int      EMA_Medium = 50;             // EMA moyenne
input int      EMA_Slow = 200;              // EMA lente (trigger principal)
input int      RSI_Period = 14;             // Période RSI
input int      ATR_Period = 14;             // Période ATR

input group "=== API PYTHON GUARDIAN ==="
input string   GuardianURL = "http://localhost:5000/validate_signal";
input bool     RequireApproval = true;      // Requiert approbation Guardian
input int      API_Timeout = 5000;          // Timeout API (ms)

//+------------------------------------------------------------------+
//| VARIABLES GLOBALES                                                |
//+------------------------------------------------------------------+
CTrade         trade;
CPositionInfo  position;
CAccountInfo   account;

// Handles indicateurs
int handleEMA_Fast, handleEMA_Medium, handleEMA_Slow;
int handleRSI, handleATR;

// Buffers
double lastEMA_Fast[], lastEMA_Medium[], lastEMA_Slow[];
double lastRSI[], lastATR[];
double lastHigh[], lastLow[], lastClose[], lastOpen[];

// État du système
bool systemInitialized = false;
datetime lastBarTime = 0;

// Gestion des TP partiels
bool TP1_Hit = false;
bool TP2_Hit = false;
bool TP3_Hit = false;
bool BE_Activated = false;
bool Trailing_Active = false;

// Structures
struct OrderBlock {
    double price_top;
    double price_bottom;
    datetime time;
    bool is_bullish;
    bool is_valid;
};

struct FairValueGap {
    double gap_top;
    double gap_bottom;
    datetime time;
    bool is_bullish;
    bool is_valid;
};

struct MarketStructure {
    bool bos_bullish;
    bool bos_bearish;
    bool choch_bullish;
    bool choch_bearish;
    double last_high;
    double last_low;
};

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

OrderBlock currentOB;
FairValueGap currentFVG;
MarketStructure marketStruct;

//+------------------------------------------------------------------+
//| Expert initialization function                                     |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("╔══════════════════════════════════════════════════════════╗");
    Print("║          🐺 LA BÊTE EUR V8 ULTIMATE 🐺                   ║");
    Print("║     Système Spécialisé GBP/USD - Prop Firm Ready         ║");
    Print("║   EMA Crossover + SMC + ATR Dynamic SL/TP                ║");
    Print("╚══════════════════════════════════════════════════════════╝");

    // Vérifier qu'on est sur GBP/USD
    if(_Symbol != "GBPUSD")
    {
        Print("⚠️ ATTENTION: Ce bot est optimisé pour GBP/USD uniquement!");
        Print("   Symbole actuel: ", _Symbol);
    }

    // Configuration du trade
    trade.SetExpertMagicNumber(MagicNumber);
    trade.SetDeviationInPoints(10);
    trade.SetTypeFilling(ORDER_FILLING_FOK);
    trade.SetAsyncMode(false);

    // Initialiser les indicateurs
    handleEMA_Fast = iMA(_Symbol, PERIOD_CURRENT, EMA_Fast, 0, MODE_EMA, PRICE_CLOSE);
    handleEMA_Medium = iMA(_Symbol, PERIOD_CURRENT, EMA_Medium, 0, MODE_EMA, PRICE_CLOSE);
    handleEMA_Slow = iMA(_Symbol, PERIOD_CURRENT, EMA_Slow, 0, MODE_EMA, PRICE_CLOSE);
    handleRSI = iRSI(_Symbol, PERIOD_CURRENT, RSI_Period, PRICE_CLOSE);
    handleATR = iATR(_Symbol, PERIOD_CURRENT, ATR_Period);

    // Vérifier les handles
    if(handleEMA_Fast == INVALID_HANDLE || handleEMA_Medium == INVALID_HANDLE ||
       handleEMA_Slow == INVALID_HANDLE || handleRSI == INVALID_HANDLE ||
       handleATR == INVALID_HANDLE)
    {
        Print("❌ ERREUR: Impossible d'initialiser les indicateurs!");
        return(INIT_FAILED);
    }

    // Configurer les arrays
    ArraySetAsSeries(lastEMA_Fast, true);
    ArraySetAsSeries(lastEMA_Medium, true);
    ArraySetAsSeries(lastEMA_Slow, true);
    ArraySetAsSeries(lastRSI, true);
    ArraySetAsSeries(lastATR, true);
    ArraySetAsSeries(lastHigh, true);
    ArraySetAsSeries(lastLow, true);
    ArraySetAsSeries(lastClose, true);
    ArraySetAsSeries(lastOpen, true);

    // Initialiser structures
    currentOB.is_valid = false;
    currentFVG.is_valid = false;
    marketStruct.last_high = 0;
    marketStruct.last_low = 0;

    systemInitialized = true;

    Print("✅ Système EUR initialisé avec succès");
    Print("🔗 Guardian API: ", GuardianURL);
    Print("📊 Paire: ", _Symbol);
    Print("⏰ Timeframe: ", EnumToString(PERIOD_CURRENT));
    Print("💰 Risque: ", RiskPercent, "%");
    Print("🎯 Confluence min: ", MinConfluenceScore, "/100");
    Print("🎲 Certitude min: ", MinCertaintyPercent, "%");
    Print("📏 SL: ATR × ", ATR_Multiplier_SL, " (", SL_MinPips, "-", SL_MaxPips, " pips)");
    Print("🎯 TP: 1:", TP1_RR, " / 1:", TP2_RR, " / 1:", TP3_RR);

    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                  |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("🛑 La Bête EUR arrêtée. Raison: ", reason);

    IndicatorRelease(handleEMA_Fast);
    IndicatorRelease(handleEMA_Medium);
    IndicatorRelease(handleEMA_Slow);
    IndicatorRelease(handleRSI);
    IndicatorRelease(handleATR);
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
    if(CopyBuffer(handleEMA_Fast, 0, 0, 3, lastEMA_Fast) < 0) return false;
    if(CopyBuffer(handleEMA_Medium, 0, 0, 3, lastEMA_Medium) < 0) return false;
    if(CopyBuffer(handleEMA_Slow, 0, 0, 3, lastEMA_Slow) < 0) return false;
    if(CopyBuffer(handleRSI, 0, 0, 3, lastRSI) < 0) return false;
    if(CopyBuffer(handleATR, 0, 0, 3, lastATR) < 0) return false;

    // Copier les prix
    if(CopyHigh(_Symbol, PERIOD_CURRENT, 0, OB_Lookback, lastHigh) < 0) return false;
    if(CopyLow(_Symbol, PERIOD_CURRENT, 0, OB_Lookback, lastLow) < 0) return false;
    if(CopyClose(_Symbol, PERIOD_CURRENT, 0, OB_Lookback, lastClose) < 0) return false;
    if(CopyOpen(_Symbol, PERIOD_CURRENT, 0, OB_Lookback, lastOpen) < 0) return false;

    return true;
}

//+------------------------------------------------------------------+
//| ANALYSE COMPLÈTE DU MARCHÉ                                        |
//+------------------------------------------------------------------+
void AnalyzeMarket()
{
    Print("🔍 Analyse GBP/USD en cours...");

    // 1. VÉRIFIER EMA CROSSOVER (TRIGGER PRINCIPAL)
    bool goldenCross = DetectGoldenCross();
    bool deathCross = DetectDeathCross();

    if(!goldenCross && !deathCross)
    {
        // Pas de signal EMA, pas besoin de continuer
        return;
    }

    // 2. DÉTECTER SMC PATTERNS
    DetectOrderBlocks();
    DetectFairValueGaps();
    DetectMarketStructure();

    // 3. DÉTERMINER LA DIRECTION
    string direction = "";
    if(goldenCross) direction = "BUY";
    else if(deathCross) direction = "SELL";

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

    // Calculer lot size
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
//| Détecte Golden Cross (EMA Fast croise au-dessus EMA Slow)        |
//+------------------------------------------------------------------+
bool DetectGoldenCross()
{
    // Barre précédente: EMA Fast <= EMA Slow
    // Barre actuelle: EMA Fast > EMA Slow

    bool previousBelow = (lastEMA_Fast[1] <= lastEMA_Slow[1]);
    bool currentAbove = (lastEMA_Fast[0] > lastEMA_Slow[0]);

    if(previousBelow && currentAbove)
    {
        Print("✅ GOLDEN CROSS détecté! (EMA", EMA_Fast, " × EMA", EMA_Slow, ")");
        return true;
    }

    return false;
}

//+------------------------------------------------------------------+
//| Détecte Death Cross (EMA Fast croise en-dessous EMA Slow)        |
//+------------------------------------------------------------------+
bool DetectDeathCross()
{
    // Barre précédente: EMA Fast >= EMA Slow
    // Barre actuelle: EMA Fast < EMA Slow

    bool previousAbove = (lastEMA_Fast[1] >= lastEMA_Slow[1]);
    bool currentBelow = (lastEMA_Fast[0] < lastEMA_Slow[0]);

    if(previousAbove && currentBelow)
    {
        Print("✅ DEATH CROSS détecté! (EMA", EMA_Fast, " × EMA", EMA_Slow, ")");
        return true;
    }

    return false;
}

//+------------------------------------------------------------------+
//| Détecte Order Blocks                                              |
//+------------------------------------------------------------------+
void DetectOrderBlocks()
{
    currentOB.is_valid = false;

    // Chercher OB+ (bullish): dernière bougie baissière avant fort mouvement haussier
    // Chercher OB- (bearish): dernière bougie haussière avant fort mouvement baissier

    for(int i = 3; i < OB_Lookback - 2; i++)
    {
        // OB+ Bullish
        bool isBearishCandle = (lastClose[i] < lastOpen[i]);
        bool strongBullishMove = (lastClose[i-1] > lastHigh[i]) && (lastClose[i-2] > lastClose[i-1]);

        if(isBearishCandle && strongBullishMove)
        {
            currentOB.is_bullish = true;
            currentOB.price_top = lastHigh[i];
            currentOB.price_bottom = lastLow[i];
            currentOB.time = iTime(_Symbol, PERIOD_CURRENT, i);
            currentOB.is_valid = true;

            Print("🟢 Order Block BULLISH détecté @ ", currentOB.price_bottom, " - ", currentOB.price_top);
            break;
        }

        // OB- Bearish
        bool isBullishCandle = (lastClose[i] > lastOpen[i]);
        bool strongBearishMove = (lastClose[i-1] < lastLow[i]) && (lastClose[i-2] < lastClose[i-1]);

        if(isBullishCandle && strongBearishMove)
        {
            currentOB.is_bullish = false;
            currentOB.price_top = lastHigh[i];
            currentOB.price_bottom = lastLow[i];
            currentOB.time = iTime(_Symbol, PERIOD_CURRENT, i);
            currentOB.is_valid = true;

            Print("🔴 Order Block BEARISH détecté @ ", currentOB.price_bottom, " - ", currentOB.price_top);
            break;
        }
    }
}

//+------------------------------------------------------------------+
//| Détecte Fair Value Gaps                                           |
//+------------------------------------------------------------------+
void DetectFairValueGaps()
{
    currentFVG.is_valid = false;

    // FVG Bullish: lastHigh[2] < lastLow[0] (gap entre barre 2 et barre 0)
    // FVG Bearish: lastLow[2] > lastHigh[0]

    double pipValue = _Point * 10;

    // Bullish FVG
    if(lastHigh[2] < lastLow[0])
    {
        double gapSize = (lastLow[0] - lastHigh[2]) / pipValue;

        if(gapSize >= FVG_MinSize)
        {
            currentFVG.is_bullish = true;
            currentFVG.gap_bottom = lastHigh[2];
            currentFVG.gap_top = lastLow[0];
            currentFVG.time = iTime(_Symbol, PERIOD_CURRENT, 1);
            currentFVG.is_valid = true;

            Print("🟢 FVG BULLISH détecté: ", gapSize, " pips (", currentFVG.gap_bottom, " - ", currentFVG.gap_top, ")");
        }
    }

    // Bearish FVG
    if(lastLow[2] > lastHigh[0])
    {
        double gapSize = (lastLow[2] - lastHigh[0]) / pipValue;

        if(gapSize >= FVG_MinSize)
        {
            currentFVG.is_bullish = false;
            currentFVG.gap_bottom = lastHigh[0];
            currentFVG.gap_top = lastLow[2];
            currentFVG.time = iTime(_Symbol, PERIOD_CURRENT, 1);
            currentFVG.is_valid = true;

            Print("🔴 FVG BEARISH détecté: ", gapSize, " pips (", currentFVG.gap_bottom, " - ", currentFVG.gap_top, ")");
        }
    }
}

//+------------------------------------------------------------------+
//| Détecte Market Structure (BOS / CHoCH)                            |
//+------------------------------------------------------------------+
void DetectMarketStructure()
{
    marketStruct.bos_bullish = false;
    marketStruct.bos_bearish = false;
    marketStruct.choch_bullish = false;
    marketStruct.choch_bearish = false;

    // Trouver le dernier plus haut et plus bas significatifs
    double recentHigh = lastHigh[ArrayMaximum(lastHigh, 0, 20)];
    double recentLow = lastLow[ArrayMinimum(lastLow, 0, 20)];

    // BOS Bullish: prix casse le dernier plus haut
    if(lastClose[0] > marketStruct.last_high && marketStruct.last_high > 0)
    {
        marketStruct.bos_bullish = true;
        Print("🟢 BOS BULLISH: Cassure ", marketStruct.last_high);
    }

    // BOS Bearish: prix casse le dernier plus bas
    if(lastClose[0] < marketStruct.last_low && marketStruct.last_low > 0)
    {
        marketStruct.bos_bearish = true;
        Print("🔴 BOS BEARISH: Cassure ", marketStruct.last_low);
    }

    // Mettre à jour les niveaux
    if(recentHigh > marketStruct.last_high)
        marketStruct.last_high = recentHigh;

    if(recentLow < marketStruct.last_low || marketStruct.last_low == 0)
        marketStruct.last_low = recentLow;
}

//+------------------------------------------------------------------+
//| Calcule le score de confluence /100                               |
//+------------------------------------------------------------------+
int CalculateConfluence(string direction)
{
    int score = 0;

    // 1. EMA Crossover (TRIGGER) = 25 points
    score += 25;
    Print("   ✓ EMA Crossover: +25 pts");

    // 2. Alignement des 3 EMAs (15 points)
    if(direction == "BUY")
    {
        if(lastEMA_Fast[0] > lastEMA_Medium[0] && lastEMA_Medium[0] > lastEMA_Slow[0])
        {
            score += 15;
            Print("   ✓ EMAs alignées (haussier): +15 pts");
        }
    }
    else // SELL
    {
        if(lastEMA_Fast[0] < lastEMA_Medium[0] && lastEMA_Medium[0] < lastEMA_Slow[0])
        {
            score += 15;
            Print("   ✓ EMAs alignées (baissier): +15 pts");
        }
    }

    // 3. Order Block aligné (20 points)
    if(currentOB.is_valid)
    {
        double currentPrice = (direction == "BUY") ? SymbolInfoDouble(_Symbol, SYMBOL_ASK) : SymbolInfoDouble(_Symbol, SYMBOL_BID);
        double tolerance = OB_TolerancePips * _Point * 10;

        if(direction == "BUY" && currentOB.is_bullish)
        {
            if(currentPrice >= currentOB.price_bottom - tolerance && currentPrice <= currentOB.price_top + tolerance)
            {
                score += 20;
                Print("   ✓ Prix dans OB+ (±3 pips): +20 pts");
            }
        }
        else if(direction == "SELL" && !currentOB.is_bullish)
        {
            if(currentPrice >= currentOB.price_bottom - tolerance && currentPrice <= currentOB.price_top + tolerance)
            {
                score += 20;
                Print("   ✓ Prix dans OB- (±3 pips): +20 pts");
            }
        }
    }

    // 4. Fair Value Gap aligné (15 points)
    if(currentFVG.is_valid)
    {
        if((direction == "BUY" && currentFVG.is_bullish) || (direction == "SELL" && !currentFVG.is_bullish))
        {
            score += 15;
            Print("   ✓ FVG aligné: +15 pts");
        }
    }

    // 5. Break of Structure (15 points)
    if((direction == "BUY" && marketStruct.bos_bullish) || (direction == "SELL" && marketStruct.bos_bearish))
    {
        score += 15;
        Print("   ✓ BOS aligné: +15 pts");
    }

    // 6. RSI dans zone favorable (10 points)
    if(direction == "BUY" && lastRSI[0] < 70 && lastRSI[0] > 30)
    {
        score += 10;
        Print("   ✓ RSI favorable (", DoubleToString(lastRSI[0], 1), "): +10 pts");
    }
    else if(direction == "SELL" && lastRSI[0] > 30 && lastRSI[0] < 70)
    {
        score += 10;
        Print("   ✓ RSI favorable (", DoubleToString(lastRSI[0], 1), "): +10 pts");
    }

    return score;
}

//+------------------------------------------------------------------+
//| Calcule le pourcentage de certitude                               |
//+------------------------------------------------------------------+
int CalculateCertainty(int confluenceScore, string direction)
{
    // Base = score de confluence
    int certainty = (int)(confluenceScore * 0.8); // 80% du score = base certitude

    // BONUS

    // +10% si Golden/Death Cross net
    if(MathAbs(lastEMA_Fast[0] - lastEMA_Slow[0]) > (lastATR[0] * 0.5))
    {
        certainty += 10;
        Print("   ✓ Crossover net: +10%");
    }

    // +8% si toutes les EMAs alignées
    bool allAligned = false;
    if(direction == "BUY")
        allAligned = (lastEMA_Fast[0] > lastEMA_Medium[0] && lastEMA_Medium[0] > lastEMA_Slow[0]);
    else
        allAligned = (lastEMA_Fast[0] < lastEMA_Medium[0] && lastEMA_Medium[0] < lastEMA_Slow[0]);

    if(allAligned)
    {
        certainty += 8;
        Print("   ✓ EMAs toutes alignées: +8%");
    }

    // +5% si ATR stable (pas de volatilité extrême)
    if(lastATR[0] < lastATR[1] * 1.5)
    {
        certainty += 5;
        Print("   ✓ Volatilité stable: +5%");
    }

    // PÉNALITÉS

    // -10% si volatilité extrême
    if(lastATR[0] > lastATR[1] * 2.0)
    {
        certainty -= 10;
        Print("   ⚠️ Volatilité extrême: -10%");
    }

    // -15% si RSI en zone de surachat/survente extrême
    if(lastRSI[0] > 80 || lastRSI[0] < 20)
    {
        certainty -= 15;
        Print("   ⚠️ RSI extrême (", DoubleToString(lastRSI[0], 1), "): -15%");
    }

    // Limiter entre 30% et 95%
    if(certainty > 95) certainty = 95;
    if(certainty < 30) certainty = 30;

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
//| Calcule la taille du lot (ajustée selon certitude)                |
//+------------------------------------------------------------------+
double CalculateLotSize(double slPips, int certaintyPercent)
{
    // Ajuster le risque selon la certitude
    double adjustedRisk = RiskPercent;

    if(certaintyPercent >= 80)
        adjustedRisk = RiskPercent; // 0.3% si excellente certitude
    else if(certaintyPercent >= 70)
        adjustedRisk = RiskPercent * 0.833; // 0.25% si bonne certitude
    else if(certaintyPercent >= 60)
        adjustedRisk = RiskPercent * 0.667; // 0.2% si certitude moyenne
    else
        adjustedRisk = RiskPercent * 0.5; // 0.15% si certitude faible

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

    Print("💰 Lot ajusté: ", lotSize, " (Risque: ", DoubleToString(adjustedRisk, 2), "% selon certitude ", certaintyPercent, "%)");

    return lotSize;
}

//+------------------------------------------------------------------+
//| Génère la raison du signal                                        |
//+------------------------------------------------------------------+
string GenerateSignalReason(string direction, int confluence, int certainty)
{
    string reason = "";

    if(direction == "BUY")
        reason = "GOLDEN CROSS détecté (EMA" + IntegerToString(EMA_Fast) + " × EMA" + IntegerToString(EMA_Slow) + ")";
    else
        reason = "DEATH CROSS détecté (EMA" + IntegerToString(EMA_Fast) + " × EMA" + IntegerToString(EMA_Slow) + ")";

    if(currentOB.is_valid)
        reason += " + Order Block aligné";

    if(currentFVG.is_valid)
        reason += " + FVG";

    if((direction == "BUY" && marketStruct.bos_bullish) || (direction == "SELL" && marketStruct.bos_bearish))
        reason += " + BOS";

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

    // Construire le JSON avec certitude
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
    Print("📈 OUVERTURE POSITION GBP/USD");
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

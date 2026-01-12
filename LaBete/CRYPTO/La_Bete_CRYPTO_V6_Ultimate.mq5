//+------------------------------------------------------------------+
//|                                La_Bete_CRYPTO_V6_Ultimate.mq5     |
//|                                    Copyright 2025, Yann - La Bête  |
//|                                                                      |
//| SYSTÈME CRYPTO ULTRA-SÉCURISÉ POUR PROP FIRM                        |
//| - Smart Money Concepts (OB, FVG, BOS, CHoCH)                        |
//| - Confluence Scoring 100pts                                         |
//| - 7 Niveaux de Protection Anti-Cramage + Protections Crypto        |
//| - API Python Guardian                                                |
//| - Triple TP / Trailing / Break Even                                 |
//| - Whale Detection / Funding Rate / Weekend Protection               |
//+------------------------------------------------------------------+

#property copyright "Yann - La Bête"
#property version   "6.00"
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
input group "=== CONFIGURATION GÉNÉRALE ==="
input double   RiskPercent = 0.2;           // Risque par trade (%)
input int      MagicNumber = 777777;        // Magic Number
input string   TradeComment = "LaBete_CRYPTO"; // Commentaire

input group "=== CONFLUENCE & SMC ==="
input int      MinConfluenceScore = 85;     // Score confluence minimum (/100)
input int      OB_Lookback = 50;            // Barres pour Order Blocks
input int      FVG_MinSize = 100;           // Taille min FVG ($)
input double   OB_TolerancePercent = 0.3;   // Tolérance prix dans OB (%)

input group "=== STOP LOSS / TAKE PROFIT ==="
input int      SL_MinDollars = 200;         // SL minimum ($) pour BTC
input int      SL_MaxDollars = 1000;        // SL maximum ($) pour BTC
input double   ATR_Multiplier_SL = 2.0;     // Multiplicateur ATR pour SL
input double   TP1_RR = 3.0;                // TP1 Risk:Reward
input double   TP2_RR = 4.0;                // TP2 Risk:Reward
input double   TP3_RR = 6.0;                // TP3 Risk:Reward

input group "=== BREAK EVEN & TRAILING ==="
input double   BE_ActivationPercent = 40.0; // Activation BE (% vers TP1)
input double   BE_OffsetPercent = 0.5;      // Offset BE (%)
input bool     TrailingAfterTP1 = true;     // Activer trailing après TP1
input double   Trailing_ATR_Percent = 60.0; // Trailing (% de l'ATR)

input group "=== INDICATEURS ==="
input int      EMA_Fast = 20;               // EMA rapide
input int      EMA_Medium = 50;             // EMA moyenne
input int      EMA_Slow = 200;              // EMA lente
input int      RSI_Period = 14;             // Période RSI
input int      MACD_Fast = 12;              // MACD rapide
input int      MACD_Slow = 26;              // MACD lent
input int      MACD_Signal = 9;             // MACD signal
input int      ATR_Period = 14;             // Période ATR

input group "=== PROTECTIONS CRYPTO ==="
input bool     CheckWhaleActivity = true;   // Vérifier activité des baleines
input double   WhaleThreshold = 3.0;        // Seuil volume baleines (x moyenne)
input bool     CheckWeekendGap = true;      // Protection weekend gap
input bool     CheckFundingRate = true;     // Vérifier funding rate
input double   MaxFundingRate = 0.01;       // Funding rate max (1%)

input group "=== API PYTHON GUARDIAN ==="
input string   GuardianURL = "http://localhost:5001/validate_signal";  // URL Guardian
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
int handleRSI, handleMACD, handleATR;

// Dernières valeurs
double lastEMA_Fast[], lastEMA_Medium[], lastEMA_Slow[];
double lastRSI[], lastMACD_Main[], lastMACD_Signal[];
double lastATR[];

// État du système
bool systemInitialized = false;
datetime lastBarTime = 0;

// Structure pour signal
struct SignalData {
    string pair;
    string direction;       // "BUY" ou "SELL"
    double entry_price;
    double sl_price;
    double sl_dollars;
    double tp1_price;
    double tp2_price;
    double tp3_price;
    double lot_size;
    int confluence_score;
    datetime timestamp;
};

//+------------------------------------------------------------------+
//| Expert initialization function                                     |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("╔══════════════════════════════════════════════════════════╗");
    Print("║          💰 LA BÊTE CRYPTO V6 ULTIMATE 💰                ║");
    Print("║     Système Ultra-Sécurisé pour Prop Firm Challenges     ║");
    Print("║         + Whale Detection + Weekend Protection           ║");
    Print("╚══════════════════════════════════════════════════════════╝");

    // Configuration du trade
    trade.SetExpertMagicNumber(MagicNumber);
    trade.SetDeviationInPoints(50);  // Plus large pour crypto
    trade.SetTypeFilling(ORDER_FILLING_FOK);
    trade.SetAsyncMode(false);

    // Initialiser les indicateurs
    handleEMA_Fast = iMA(_Symbol, PERIOD_CURRENT, EMA_Fast, 0, MODE_EMA, PRICE_CLOSE);
    handleEMA_Medium = iMA(_Symbol, PERIOD_CURRENT, EMA_Medium, 0, MODE_EMA, PRICE_CLOSE);
    handleEMA_Slow = iMA(_Symbol, PERIOD_CURRENT, EMA_Slow, 0, MODE_EMA, PRICE_CLOSE);
    handleRSI = iRSI(_Symbol, PERIOD_CURRENT, RSI_Period, PRICE_CLOSE);
    handleMACD = iMACD(_Symbol, PERIOD_CURRENT, MACD_Fast, MACD_Slow, MACD_Signal, PRICE_CLOSE);
    handleATR = iATR(_Symbol, PERIOD_CURRENT, ATR_Period);

    // Vérifier les handles
    if(handleEMA_Fast == INVALID_HANDLE || handleEMA_Medium == INVALID_HANDLE ||
       handleEMA_Slow == INVALID_HANDLE || handleRSI == INVALID_HANDLE ||
       handleMACD == INVALID_HANDLE || handleATR == INVALID_HANDLE)
    {
        Print("❌ ERREUR: Impossible d'initialiser les indicateurs!");
        return(INIT_FAILED);
    }

    // Redimensionner les arrays
    ArraySetAsSeries(lastEMA_Fast, true);
    ArraySetAsSeries(lastEMA_Medium, true);
    ArraySetAsSeries(lastEMA_Slow, true);
    ArraySetAsSeries(lastRSI, true);
    ArraySetAsSeries(lastMACD_Main, true);
    ArraySetAsSeries(lastMACD_Signal, true);
    ArraySetAsSeries(lastATR, true);

    systemInitialized = true;

    Print("✅ Système initialisé avec succès");
    Print("🔗 Guardian API: ", GuardianURL);
    Print("📊 Paire: ", _Symbol);
    Print("⏰ Timeframe: ", EnumToString(PERIOD_CURRENT));
    Print("💰 Risque: ", RiskPercent, "%");
    Print("🎯 Confluence min: ", MinConfluenceScore, "/100");
    Print("🐋 Whale detection: ", (CheckWhaleActivity ? "ACTIVÉE" : "DÉSACTIVÉE"));
    Print("🌙 Weekend protection: ", (CheckWeekendGap ? "ACTIVÉE" : "DÉSACTIVÉE"));

    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                  |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("🛑 La Bête Crypto arrêtée. Raison: ", reason);

    // Libérer les indicateurs
    IndicatorRelease(handleEMA_Fast);
    IndicatorRelease(handleEMA_Medium);
    IndicatorRelease(handleEMA_Slow);
    IndicatorRelease(handleRSI);
    IndicatorRelease(handleMACD);
    IndicatorRelease(handleATR);
}

//+------------------------------------------------------------------+
//| Expert tick function                                               |
//+------------------------------------------------------------------+
void OnTick()
{
    // Vérifier nouvelle barre
    if(!IsNewBar())
        return;

    // Mettre à jour les indicateurs
    if(!UpdateIndicators())
        return;

    // Gérer les positions existantes
    ManageOpenPositions();

    // Chercher nouveau signal
    if(!HasOpenPosition())
    {
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
    // Copier les valeurs
    if(CopyBuffer(handleEMA_Fast, 0, 0, 3, lastEMA_Fast) < 0) return false;
    if(CopyBuffer(handleEMA_Medium, 0, 0, 3, lastEMA_Medium) < 0) return false;
    if(CopyBuffer(handleEMA_Slow, 0, 0, 3, lastEMA_Slow) < 0) return false;
    if(CopyBuffer(handleRSI, 0, 0, 3, lastRSI) < 0) return false;
    if(CopyBuffer(handleMACD, 0, 0, 3, lastMACD_Main) < 0) return false;
    if(CopyBuffer(handleMACD, 1, 0, 3, lastMACD_Signal) < 0) return false;
    if(CopyBuffer(handleATR, 0, 0, 3, lastATR) < 0) return false;

    return true;
}

//+------------------------------------------------------------------+
//| Analyse le marché et cherche des signaux                          |
//+------------------------------------------------------------------+
void AnalyzeMarket()
{
    // Vérifications crypto spécifiques
    if(CheckWhaleActivity && IsWhaleActivityDetected())
    {
        Print("🐋 Activité de baleines détectée - Trade suspendu");
        return;
    }

    if(CheckWeekendGap && IsWeekend())
    {
        Print("🌙 Weekend - Trade suspendu");
        return;
    }

    // TODO: Implémenter l'analyse complète
    // 1. Détecter Order Blocks
    // 2. Détecter Fair Value Gaps
    // 3. Identifier BOS / CHoCH
    // 4. Calculer le score de confluence
    // 5. Si confluence >= MinConfluenceScore, créer signal
    // 6. Envoyer signal au Guardian Python
    // 7. Si approuvé, ouvrir position

    Print("🔍 Analyse crypto en cours...");

    // Exemple de structure (à compléter)
    /*
    SignalData signal;
    signal.pair = _Symbol;
    signal.direction = "BUY";  // Ou "SELL"
    signal.entry_price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
    signal.sl_dollars = CalculateSL_Crypto();
    signal.sl_price = signal.entry_price - (signal.sl_dollars / signal.entry_price);
    signal.tp1_price = signal.entry_price + (signal.sl_dollars * TP1_RR / signal.entry_price);
    signal.tp2_price = signal.entry_price + (signal.sl_dollars * TP2_RR / signal.entry_price);
    signal.tp3_price = signal.entry_price + (signal.sl_dollars * TP3_RR / signal.entry_price);
    signal.lot_size = CalculateLotSize_Crypto(signal.sl_dollars);
    signal.confluence_score = CalculateConfluence();
    signal.timestamp = TimeCurrent();

    if(signal.confluence_score >= MinConfluenceScore)
    {
        if(SendSignalToGuardian(signal))
        {
            // Approuvé, ouvrir position
            OpenPosition(signal);
        }
    }
    */
}

//+------------------------------------------------------------------+
//| Détecte activité des baleines (volume anormal)                    |
//+------------------------------------------------------------------+
bool IsWhaleActivityDetected()
{
    // TODO: Implémenter détection volume anormal
    // Comparer volume actuel vs moyenne des 50 dernières barres
    // Si volume > (moyenne * WhaleThreshold), retourner true

    return false;  // Placeholder
}

//+------------------------------------------------------------------+
//| Vérifie si c'est le weekend                                       |
//+------------------------------------------------------------------+
bool IsWeekend()
{
    MqlDateTime dt;
    TimeCurrent(dt);

    // Samedi ou Dimanche
    if(dt.day_of_week == 0 || dt.day_of_week == 6)
        return true;

    // Vendredi après 20h
    if(dt.day_of_week == 5 && dt.hour >= 20)
        return true;

    // Dimanche avant 22h
    if(dt.day_of_week == 0 && dt.hour < 22)
        return true;

    return false;
}

//+------------------------------------------------------------------+
//| Envoie le signal au Guardian Python pour validation               |
//+------------------------------------------------------------------+
bool SendSignalToGuardian(SignalData &signal)
{
    if(!RequireApproval)
        return true;  // Pas de validation requise

    // Construire le JSON
    string json = StringFormat(
        "{\"pair\":\"%s\",\"direction\":\"%s\",\"entry_price\":%.2f,\"sl_price\":%.2f,\"sl_dollars\":%.0f,"
        "\"tp1_price\":%.2f,\"tp2_price\":%.2f,\"tp3_price\":%.2f,\"lot_size\":%.2f,\"confluence_score\":%d}",
        signal.pair, signal.direction, signal.entry_price, signal.sl_price, signal.sl_dollars,
        signal.tp1_price, signal.tp2_price, signal.tp3_price, signal.lot_size, signal.confluence_score
    );

    // Envoyer au Guardian
    char post[], result[];
    string headers = "Content-Type: application/json\r\n";
    StringToCharArray(json, post, 0, WHOLE_ARRAY);

    int timeout = API_Timeout;
    int res = WebRequest("POST", GuardianURL, headers, timeout, post, result, headers);

    if(res == -1)
    {
        Print("❌ Erreur WebRequest: ", GetLastError());
        Print("⚠️ Vérifiez que ", GuardianURL, " est autorisé dans MT5 (Outils > Options > Expert Advisors)");
        return false;
    }

    // Parser la réponse
    string response = CharArrayToString(result);
    Print("📥 Réponse Guardian: ", response);

    // Vérifier si approuvé (parsing basique)
    if(StringFind(response, "\"approved\":true") >= 0 || StringFind(response, "\"approved\": true") >= 0)
    {
        Print("✅ Signal APPROUVÉ par Guardian");
        return true;
    }
    else
    {
        Print("❌ Signal REJETÉ par Guardian");
        // Extraire la raison si possible
        int reasonPos = StringFind(response, "\"reason\":\"");
        if(reasonPos >= 0)
        {
            reasonPos += 10;
            int endPos = StringFind(response, "\"", reasonPos);
            if(endPos > reasonPos)
            {
                string reason = StringSubstr(response, reasonPos, endPos - reasonPos);
                Print("   Raison: ", reason);
            }
        }
        return false;
    }
}

//+------------------------------------------------------------------+
//| Calcule la taille du lot selon le risque (CRYPTO)                 |
//+------------------------------------------------------------------+
double CalculateLotSize_Crypto(double slDollars)
{
    double balance = account.Balance();
    double riskAmount = balance * (RiskPercent / 100.0);

    double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
    double price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

    double lotSize = riskAmount / slDollars;

    // Arrondir selon les contraintes du broker
    double minLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
    double maxLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
    double stepLot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);

    lotSize = MathFloor(lotSize / stepLot) * stepLot;
    lotSize = MathMax(lotSize, minLot);
    lotSize = MathMin(lotSize, maxLot);

    return lotSize;
}

//+------------------------------------------------------------------+
//| Ouvre une position                                                 |
//+------------------------------------------------------------------+
void OpenPosition(SignalData &signal)
{
    Print("📈 Ouverture position: ", signal.direction, " ", signal.pair);

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
        Print("   Lot: ", signal.lot_size);
        Print("   Entry: ", signal.entry_price);
        Print("   SL: ", signal.sl_price, " ($", signal.sl_dollars, ")");
        Print("   TP1: ", signal.tp1_price, " (R:R 1:", TP1_RR, ")");
    }
    else
    {
        Print("❌ Erreur ouverture position: ", trade.ResultRetcodeDescription());
    }
}

//+------------------------------------------------------------------+
//| Gère les positions ouvertes (BE, Trailing, TP partiel)            |
//+------------------------------------------------------------------+
void ManageOpenPositions()
{
    for(int i = PositionsTotal() - 1; i >= 0; i--)
    {
        if(position.SelectByIndex(i))
        {
            if(position.Symbol() == _Symbol && position.Magic() == MagicNumber)
            {
                // TODO: Implémenter
                // 1. Vérifier si BE doit être activé
                // 2. Vérifier si Trailing doit être activé
                // 3. Gérer les TP partiels (TP1 50%, TP2 30%, TP3 20%)
            }
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
//| TEMPLATE - À COMPLÉTER                                            |
//+------------------------------------------------------------------+
// TODO: Implémenter les fonctions suivantes:
// - DetectOrderBlocks() : Détecte les OB+ et OB-
// - DetectFVG() : Détecte les Fair Value Gaps
// - DetectBOS() : Détecte les Break of Structure
// - DetectCHoCH() : Détecte les Change of Character
// - CalculateConfluence() : Calcule le score /100
// - IsPriceInOB() : Vérifie si prix dans OB
// - ManageBreakEven() : Gère le déplacement du SL au BE
// - ManageTrailing() : Gère le trailing stop
// - ManagePartialTP() : Gère les TP partiels
// - CheckFundingRate() : Vérifie le funding rate
// - CalculateVolume_Average() : Calcule volume moyen
// - IsTradingAllowed() : Vérifie périodes interdites
//
// IMPORTANT: Ce template doit être complété avec l'implémentation
// complète du système SMC et des protections crypto.
//+------------------------------------------------------------------+

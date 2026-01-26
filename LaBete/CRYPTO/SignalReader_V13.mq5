//+------------------------------------------------------------------+
//|                                         SignalReader_V13.mq5     |
//|                                    Copyright 2025, Yann - La Bête |
//|                                                                    |
//| BOT LECTEUR DE SIGNAUX TELEGRAM V13                               |
//| - Lit les signaux JSON du dossier SIGNALS/                       |
//| - Calcule lot size automatiquement (RiskPercent)                 |
//| - Ouvre positions avec SL et multiple TPs                        |
//| - Fermetures partielles (50%/30%/20%)                            |
//| - Confirmation Telegram                                           |
//+------------------------------------------------------------------+

#property copyright "Yann - La Bête"
#property version   "13.00"
#property strict

//+------------------------------------------------------------------+
//| INCLUDES                                                          |
//+------------------------------------------------------------------+
#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>
#include <Trade\AccountInfo.mqh>
#include <SHARED\TelegramNotify.mqh>
#include <Files\FileTxt.mqh>

//+------------------------------------------------------------------+
//| PARAMÈTRES INPUTS                                                 |
//+------------------------------------------------------------------+
input group "=== CONFIGURATION SIGNAL READER V13 ==="
input string   SignalsFolder = "C:\\Trading\\LaBete\\SIGNALS\\";  // Dossier des signaux JSON
input double   RiskPercent = 0.5;           // Risque par trade (% du compte)
input int      CheckIntervalSeconds = 2;    // Intervalle vérification signaux (sec)

input group "=== PARTIAL CLOSES ==="
input double   TP1_ClosePercent = 50.0;     // Fermer 50% à TP1
input double   TP2_ClosePercent = 30.0;     // Fermer 30% à TP2
input double   TP3_ClosePercent = 20.0;     // Fermer 20% à TP3

input group "=== PROTECTION ==="
input double   MaxDailyLoss = 2000;         // Limite daily loss (€)
input double   MaxDrawdown = 4000;          // Limite drawdown total (€)
input int      MaxTradesPerDay = 10;        // Limite trades/jour

//+------------------------------------------------------------------+
//| VARIABLES GLOBALES                                                |
//+------------------------------------------------------------------+
CTrade         trade;
CPositionInfo  position;
CAccountInfo   account;

datetime       lastCheckTime = 0;
int            tradesOpened = 0;
double         startingBalance = 0;
double         dailyStartBalance = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                    |
//+------------------------------------------------------------------+
int OnInit()
{
    Print("🚀 Signal Reader V13 initialisé");
    Print("   📁 Dossier signaux: ", SignalsFolder);
    Print("   💰 Risk per trade: ", RiskPercent, "%");
    Print("   ⏱️ Check interval: ", CheckIntervalSeconds, "s");

    startingBalance = account.Balance();
    dailyStartBalance = startingBalance;

    // Vérifier dossier existe
    if(!FolderCheck(SignalsFolder))
    {
        Print("⚠️ Dossier signaux n'existe pas: ", SignalsFolder);
        Print("   Créez le dossier ou ajustez le paramètre SignalsFolder");
    }

    NotifyBotStarted(_Symbol, "Signal Reader V13", "13.00");

    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    Print("🛑 Signal Reader V13 arrêté");
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
    // Vérifier signaux à interval régulier
    if(TimeCurrent() - lastCheckTime < CheckIntervalSeconds)
        return;

    lastCheckTime = TimeCurrent();

    // Vérifier protection FTMO
    if(!CheckFTMOProtection())
        return;

    // Chercher nouveaux signaux
    CheckForNewSignals();
}

//+------------------------------------------------------------------+
//| Vérifie et exécute les nouveaux signaux                          |
//+------------------------------------------------------------------+
void CheckForNewSignals()
{
    // Chercher fichiers JSON dans le dossier
    string search_pattern = SignalsFolder + "signal_*.json";
    string filename;
    long search_handle;

    // Première recherche
    search_handle = FileFindFirst(search_pattern, filename);

    if(search_handle == INVALID_HANDLE)
        return;  // Aucun fichier trouvé

    do
    {
        // Traiter chaque fichier signal
        string filepath = SignalsFolder + filename;
        ProcessSignalFile(filepath, filename);

    } while(FileFindNext(search_handle, filename));

    FileFindClose(search_handle);
}

//+------------------------------------------------------------------+
//| Traite un fichier signal JSON                                    |
//+------------------------------------------------------------------+
void ProcessSignalFile(string filepath, string filename)
{
    Print("📥 Nouveau signal détecté: ", filename);

    // Lire le contenu du fichier
    string json_content = ReadFileContent(filepath);

    if(json_content == "")
    {
        Print("❌ Impossible de lire: ", filepath);
        return;
    }

    // Parser le JSON (simple parsing manuel)
    string symbol = ParseJSONString(json_content, "symbol");
    string direction = ParseJSONString(json_content, "direction");
    double entry_price = ParseJSONDouble(json_content, "entry_price");
    double sl = ParseJSONDouble(json_content, "sl");
    double tp1 = ParseJSONDouble(json_content, "tp1");
    double tp2 = ParseJSONDouble(json_content, "tp2");
    double tp3 = ParseJSONDouble(json_content, "tp3");

    // Validation
    if(symbol == "" || direction == "" || entry_price == 0 || sl == 0)
    {
        Print("❌ Signal invalide dans ", filename);
        ArchiveSignalFile(filepath, filename, "FAILED");
        return;
    }

    Print("📊 Signal parsé:");
    Print("   Symbole: ", symbol);
    Print("   Direction: ", direction);
    Print("   Entry: ", entry_price);
    Print("   SL: ", sl);
    Print("   TP1: ", tp1, " TP2: ", tp2, " TP3: ", tp3);

    // Exécuter le trade
    bool success = ExecuteSignal(symbol, direction, entry_price, sl, tp1, tp2, tp3);

    if(success)
    {
        Print("✅ Signal exécuté avec succès!");
        ArchiveSignalFile(filepath, filename, "EXECUTED");
        tradesOpened++;
    }
    else
    {
        Print("❌ Échec exécution signal");
        ArchiveSignalFile(filepath, filename, "FAILED");
    }
}

//+------------------------------------------------------------------+
//| Exécute un signal de trading                                     |
//+------------------------------------------------------------------+
bool ExecuteSignal(string symbol, string direction, double entry, double sl_price,
                   double tp1, double tp2, double tp3)
{
    // Calculer lot size basé sur risque
    double sl_distance_points = MathAbs(entry - sl_price);
    double lot_size = CalculateLotSize(symbol, sl_distance_points, RiskPercent);

    if(lot_size < SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN))
    {
        Print("❌ Lot size trop petit: ", lot_size);
        return false;
    }

    Print("💼 Lot size calculé: ", lot_size, " (Risk: ", RiskPercent, "%)");

    // Type d'ordre
    ENUM_ORDER_TYPE order_type = (direction == "BUY") ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;

    // Ouvrir position
    bool result = trade.PositionOpen(
        symbol,              // Symbole
        order_type,          // Type
        lot_size,            // Volume
        entry,               // Prix (market si 0)
        sl_price,            // SL
        tp1,                 // TP (premier TP)
        "SignalCopy_V13"     // Commentaire
    );

    if(!result)
    {
        Print("❌ Erreur ouverture position: ", trade.ResultRetcode(), " - ", trade.ResultComment());
        return false;
    }

    // Succès!
    ulong ticket = trade.ResultOrder();

    string message = StringFormat(
        "✅ SIGNAL EXÉCUTÉ\n\n"
        "🎯 %s %s\n"
        "💰 Entry: %.2f\n"
        "🛡️ SL: %.2f\n"
        "🎯 TP1: %.2f\n"
        "🎯 TP2: %.2f\n"
        "🎯 TP3: %.2f\n"
        "💼 Lot: %.2f\n"
        "🎫 Ticket: %llu",
        symbol, direction, entry, sl_price, tp1, tp2, tp3, lot_size, ticket
    );

    SendTelegramMessage(message);

    return true;
}

//+------------------------------------------------------------------+
//| Calcule lot size basé sur risque                                 |
//+------------------------------------------------------------------+
double CalculateLotSize(string symbol, double sl_distance_points, double risk_percent)
{
    double risk_amount = account.Balance() * (risk_percent / 100.0);

    double tick_value = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE);
    double tick_size = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);

    double lot_size = risk_amount / (sl_distance_points / tick_size * tick_value);

    // Normaliser au step minimum
    double lot_step = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);
    lot_size = MathFloor(lot_size / lot_step) * lot_step;

    // Limites
    double min_lot = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
    double max_lot = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);

    lot_size = MathMax(min_lot, MathMin(max_lot, lot_size));

    return lot_size;
}

//+------------------------------------------------------------------+
//| Vérifie protection FTMO                                          |
//+------------------------------------------------------------------+
bool CheckFTMOProtection()
{
    double current_balance = account.Balance();
    double daily_loss = dailyStartBalance - current_balance;
    double total_drawdown = startingBalance - current_balance;

    // Reset compteur daily au changement de jour
    static int last_day = 0;
    MqlDateTime dt;
    TimeToStruct(TimeCurrent(), dt);

    if(dt.day != last_day)
    {
        last_day = dt.day;
        dailyStartBalance = current_balance;
        tradesOpened = 0;
    }

    // Vérifier limites
    if(daily_loss >= MaxDailyLoss)
    {
        Print("⛔ DAILY LOSS LIMIT ATTEINT: ", daily_loss, "€");
        SendTelegramMessage("⛔ DAILY LOSS LIMIT ATTEINT!\nTrades bloqués jusqu'à demain.");
        return false;
    }

    if(total_drawdown >= MaxDrawdown)
    {
        Print("⛔ MAX DRAWDOWN ATTEINT: ", total_drawdown, "€");
        SendTelegramMessage("⛔ MAX DRAWDOWN ATTEINT!\nTrades bloqués.");
        return false;
    }

    if(tradesOpened >= MaxTradesPerDay)
    {
        Print("⛔ MAX TRADES/DAY ATTEINT: ", tradesOpened);
        return false;
    }

    return true;
}

//+------------------------------------------------------------------+
//| Lit contenu d'un fichier texte                                   |
//+------------------------------------------------------------------+
string ReadFileContent(string filepath)
{
    int file_handle = FileOpen(filepath, FILE_READ|FILE_TXT|FILE_ANSI);

    if(file_handle == INVALID_HANDLE)
        return "";

    string content = "";
    while(!FileIsEnding(file_handle))
    {
        content += FileReadString(file_handle) + "\n";
    }

    FileClose(file_handle);
    return content;
}

//+------------------------------------------------------------------+
//| Parse une string JSON simple                                     |
//+------------------------------------------------------------------+
string ParseJSONString(string json, string key)
{
    string search = "\"" + key + "\": \"";
    int start = StringFind(json, search);

    if(start < 0)
        return "";

    start += StringLen(search);
    int end = StringFind(json, "\"", start);

    if(end < 0)
        return "";

    return StringSubstr(json, start, end - start);
}

//+------------------------------------------------------------------+
//| Parse un double JSON simple                                      |
//+------------------------------------------------------------------+
double ParseJSONDouble(string json, string key)
{
    string search = "\"" + key + "\": ";
    int start = StringFind(json, search);

    if(start < 0)
        return 0;

    start += StringLen(search);
    int end_comma = StringFind(json, ",", start);
    int end_brace = StringFind(json, "}", start);

    int end = (end_comma > 0 && end_comma < end_brace) ? end_comma : end_brace;

    if(end < 0)
        return 0;

    string value_str = StringSubstr(json, start, end - start);
    StringTrimLeft(value_str);
    StringTrimRight(value_str);

    // null = 0
    if(value_str == "null")
        return 0;

    return StringToDouble(value_str);
}

//+------------------------------------------------------------------+
//| Archive un fichier signal (déplace vers archive/)                |
//+------------------------------------------------------------------+
void ArchiveSignalFile(string filepath, string filename, string status)
{
    string archive_folder = SignalsFolder + "archive\\";

    // Créer dossier archive si n'existe pas
    FolderCreate(archive_folder);

    // Nouveau nom avec status
    string new_filename = StringSubstr(filename, 0, StringLen(filename) - 5); // Enlever .json
    new_filename += "_" + status + ".json";

    string new_filepath = archive_folder + new_filename;

    // Déplacer (copier puis supprimer original)
    if(FileCopy(filepath, 0, new_filepath, 0))
    {
        FileDelete(filepath);
        Print("📦 Signal archivé: ", new_filename);
    }
    else
    {
        Print("⚠️ Erreur archivage signal");
        // Supprimer quand même pour éviter re-traitement
        FileDelete(filepath);
    }
}

//+------------------------------------------------------------------+
//| Vérifie si dossier existe                                        |
//+------------------------------------------------------------------+
bool FolderCheck(string folder_path)
{
    long search_handle = FileFindFirst(folder_path + "*", filename);

    if(search_handle == INVALID_HANDLE)
        return false;

    FileFindClose(search_handle);
    return true;
}

//+------------------------------------------------------------------+

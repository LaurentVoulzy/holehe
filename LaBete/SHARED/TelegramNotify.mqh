//+------------------------------------------------------------------+
//|                                              TelegramNotify.mqh |
//|                                    Librairie notifications Telegram |
//+------------------------------------------------------------------+
#property copyright "La Bete V12"
#property version   "1.00"
#property strict

//+------------------------------------------------------------------+
//| Variables globales Telegram                                      |
//+------------------------------------------------------------------+
input string TelegramBotToken = "";           // Token du bot Telegram
input string TelegramChatID = "";             // Chat ID Telegram
input bool   EnableTelegramNotifications = false; // Activer notifications Telegram

//+------------------------------------------------------------------+
//| Envoie un message Telegram                                       |
//+------------------------------------------------------------------+
bool SendTelegramMessage(string message)
{
    if(!EnableTelegramNotifications || TelegramBotToken == "" || TelegramChatID == "")
        return false;

    string url = "https://api.telegram.org/bot" + TelegramBotToken + "/sendMessage";

    // Encoder le message pour URL
    string encodedMessage = message;
    StringReplace(encodedMessage, "\n", "%0A");
    StringReplace(encodedMessage, " ", "%20");
    StringReplace(encodedMessage, "€", "%E2%82%AC");
    StringReplace(encodedMessage, "$", "%24");

    string params = "chat_id=" + TelegramChatID + "&text=" + encodedMessage + "&parse_mode=HTML";

    char post[];
    char result[];
    string headers;

    ArrayResize(post, StringToCharArray(params, post, 0, WHOLE_ARRAY) - 1);

    int timeout = 5000; // 5 secondes
    int res = WebRequest("POST", url, "", NULL, timeout, post, 0, result, headers);

    if(res == -1)
    {
        Print("❌ Erreur Telegram: ", GetLastError());
        Print("💡 Vérifiez que l'URL est autorisée dans Outils > Options > Expert Advisors");
        Print("💡 Ajoutez: https://api.telegram.org");
        return false;
    }

    if(res == 200)
    {
        Print("✅ Message Telegram envoyé");
        return true;
    }
    else
    {
        Print("⚠️ Erreur HTTP Telegram: ", res);
        return false;
    }
}

//+------------------------------------------------------------------+
//| Notification d'ouverture de position                             |
//+------------------------------------------------------------------+
void NotifyPositionOpened(string symbol, ENUM_ORDER_TYPE type, double lots, double openPrice, double sl, double tp, string strategy)
{
    if(!EnableTelegramNotifications) return;

    string emoji = (type == ORDER_TYPE_BUY) ? "🟢" : "🔴";
    string direction = (type == ORDER_TYPE_BUY) ? "BUY" : "SELL";

    string message = emoji + " <b>POSITION OUVERTE</b>\n\n";
    message += "📊 Paire: <b>" + symbol + "</b>\n";
    message += "📈 Direction: <b>" + direction + "</b>\n";
    message += "💰 Volume: <b>" + DoubleToString(lots, 2) + " lots</b>\n";
    message += "🎯 Prix: <b>" + DoubleToString(openPrice, _Digits) + "</b>\n";
    message += "🛑 SL: <b>" + DoubleToString(sl, _Digits) + "</b>\n";
    message += "✅ TP: <b>" + DoubleToString(tp, _Digits) + "</b>\n";
    message += "🤖 Stratégie: <b>" + strategy + "</b>\n";
    message += "⏰ Heure: <b>" + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "</b>";

    SendTelegramMessage(message);
}

//+------------------------------------------------------------------+
//| Notification de fermeture de position                            |
//+------------------------------------------------------------------+
void NotifyPositionClosed(string symbol, ENUM_ORDER_TYPE type, double lots, double openPrice, double closePrice, double profit, string reason)
{
    if(!EnableTelegramNotifications) return;

    string emoji = (profit > 0) ? "✅" : (profit < 0) ? "❌" : "⚪";
    string direction = (type == ORDER_TYPE_BUY) ? "BUY" : "SELL";
    string profitEmoji = (profit > 0) ? "💚" : (profit < 0) ? "💔" : "⚪";

    string message = emoji + " <b>POSITION FERMÉE</b>\n\n";
    message += "📊 Paire: <b>" + symbol + "</b>\n";
    message += "📈 Direction: <b>" + direction + "</b>\n";
    message += "💰 Volume: <b>" + DoubleToString(lots, 2) + " lots</b>\n";
    message += "🔵 Ouverture: <b>" + DoubleToString(openPrice, _Digits) + "</b>\n";
    message += "🔴 Fermeture: <b>" + DoubleToString(closePrice, _Digits) + "</b>\n";
    message += profitEmoji + " Profit: <b>" + DoubleToString(profit, 2) + " " + AccountInfoString(ACCOUNT_CURRENCY) + "</b>\n";
    message += "📌 Raison: <b>" + reason + "</b>\n";
    message += "⏰ Heure: <b>" + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "</b>";

    SendTelegramMessage(message);
}

//+------------------------------------------------------------------+
//| Notification d'ordre limite placé                                |
//+------------------------------------------------------------------+
void NotifyLimitOrderPlaced(string symbol, ENUM_ORDER_TYPE type, double lots, double price, double sl, double tp)
{
    if(!EnableTelegramNotifications) return;

    string emoji = (type == ORDER_TYPE_BUY_LIMIT) ? "🟦" : "🟥";
    string direction = (type == ORDER_TYPE_BUY_LIMIT) ? "BUY LIMIT" : "SELL LIMIT";

    string message = emoji + " <b>ORDRE LIMITE PLACÉ</b>\n\n";
    message += "📊 Paire: <b>" + symbol + "</b>\n";
    message += "📈 Type: <b>" + direction + "</b>\n";
    message += "💰 Volume: <b>" + DoubleToString(lots, 2) + " lots</b>\n";
    message += "🎯 Prix: <b>" + DoubleToString(price, _Digits) + "</b>\n";
    message += "🛑 SL: <b>" + DoubleToString(sl, _Digits) + "</b>\n";
    message += "✅ TP: <b>" + DoubleToString(tp, _Digits) + "</b>\n";
    message += "⏰ Heure: <b>" + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "</b>";

    SendTelegramMessage(message);
}

//+------------------------------------------------------------------+
//| Notification d'erreur                                            |
//+------------------------------------------------------------------+
void NotifyError(string symbol, string errorMessage)
{
    if(!EnableTelegramNotifications) return;

    string message = "⚠️ <b>ERREUR</b>\n\n";
    message += "📊 Paire: <b>" + symbol + "</b>\n";
    message += "❌ Message: <b>" + errorMessage + "</b>\n";
    message += "⏰ Heure: <b>" + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "</b>";

    SendTelegramMessage(message);
}

//+------------------------------------------------------------------+
//| Notification de démarrage du bot                                 |
//+------------------------------------------------------------------+
void NotifyBotStarted(string symbol, string botName, string version)
{
    if(!EnableTelegramNotifications) return;

    string message = "🚀 <b>BOT DÉMARRÉ</b>\n\n";
    message += "🤖 Bot: <b>" + botName + "</b>\n";
    message += "📊 Paire: <b>" + symbol + "</b>\n";
    message += "📌 Version: <b>" + version + "</b>\n";
    message += "💰 Balance: <b>" + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2) + " " + AccountInfoString(ACCOUNT_CURRENCY) + "</b>\n";
    message += "⏰ Heure: <b>" + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "</b>";

    SendTelegramMessage(message);
}

//+------------------------------------------------------------------+
//| Résumé quotidien                                                 |
//+------------------------------------------------------------------+
void NotifyDailySummary(string symbol, int totalTrades, int wins, int losses, double totalProfit)
{
    if(!EnableTelegramNotifications) return;

    double winRate = (totalTrades > 0) ? (wins * 100.0 / totalTrades) : 0;
    string profitEmoji = (totalProfit > 0) ? "💚" : (totalProfit < 0) ? "💔" : "⚪";

    string message = "📊 <b>RÉSUMÉ QUOTIDIEN</b>\n\n";
    message += "📈 Paire: <b>" + symbol + "</b>\n";
    message += "🔢 Trades: <b>" + IntegerToString(totalTrades) + "</b>\n";
    message += "✅ Gagnants: <b>" + IntegerToString(wins) + "</b>\n";
    message += "❌ Perdants: <b>" + IntegerToString(losses) + "</b>\n";
    message += "📊 Win Rate: <b>" + DoubleToString(winRate, 1) + "%</b>\n";
    message += profitEmoji + " Profit: <b>" + DoubleToString(totalProfit, 2) + " " + AccountInfoString(ACCOUNT_CURRENCY) + "</b>\n";
    message += "💰 Balance: <b>" + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2) + " " + AccountInfoString(ACCOUNT_CURRENCY) + "</b>\n";
    message += "⏰ Date: <b>" + TimeToString(TimeCurrent(), TIME_DATE) + "</b>";

    SendTelegramMessage(message);
}

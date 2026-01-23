@echo off
cls

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║          🐺 LA BÊTE V10_1 - SYSTÈME COMPLET 🐺          ║
echo ║                                                        ║
echo ║        Démarrage Guardian FOREX + CRYPTO + Telegram   ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé!
    echo    Téléchargez Python 3.12+ sur python.org
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

REM Créer dossiers LOGS
if not exist "LOGS" mkdir LOGS
if not exist "LOGS\FOREX" mkdir LOGS\FOREX
if not exist "LOGS\CRYPTO" mkdir LOGS\CRYPTO

echo.
echo 🚀 DÉMARRAGE LA BÊTE V10_1...
echo.

echo [1/3] 🐺 Guardian FOREX (port 5000)...
cd FOREX
start "Guardian FOREX V10_1" cmd /k "python guardian_forex.py"
cd ..
timeout /t 2 /nobreak >nul
echo ✅ Guardian FOREX OK

echo [2/3] 💰 Guardian CRYPTO (port 5001)...
cd CRYPTO
start "Guardian CRYPTO V10_1" cmd /k "python guardian_crypto.py"
cd ..
timeout /t 2 /nobreak >nul
echo ✅ Guardian CRYPTO OK

echo [3/3] 📱 Bot Telegram Ultra V10_1...
cd CORE
start "Telegram Bot Ultra V10_1" cmd /k "python telegram_bot_ultra.py"
cd ..
timeout /t 2 /nobreak >nul
echo ✅ Bot Telegram Ultra V10_1 OK

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║          ✅ LA BÊTE V10_1 DÉMARRÉE AVEC SUCCÈS ✅        ║
echo ║                                                        ║
echo ║  🐺 Guardian FOREX : http://localhost:5000            ║
echo ║  💰 Guardian CRYPTO: http://localhost:5001            ║
echo ║  📱 Telegram Bot   : Tapez /start dans votre bot      ║
echo ║                                                        ║
echo ║  NOUVEAUTÉS V10_1:                                       ║
echo ║  • Stratégie MA2×MA12 (5-10 trades/semaine)           ║
echo ║  • Support/Résistance auto H1 (lignes visibles)       ║
echo ║  • Buy/Sell Limit sur S/R avec SL intelligent         ║
echo ║  • TP multiples: TP1/TP2/TP3 + Trailing Stop          ║
echo ║  • Protection FTMO: -€2K daily, -€4K total            ║
echo ║                                                        ║
echo ║  📊 PROCHAINES ÉTAPES:                                 ║
echo ║  1. Ouvrir MT5                                         ║
echo ║  2. Charger les bots V10_1 sur charts M30:              ║
echo ║     - La_Bete_EUR_V10_1.mq5 sur EURUSD                  ║
echo ║     - La_Bete_GBP_V10_1.mq5 sur GBPUSD                  ║
echo ║     - La_Bete_JPY_V10_1.mq5 sur USDJPY                  ║
echo ║     - La_Bete_GOLD_V10_1.mq5 sur XAUUSD                 ║
echo ║     - La_Bete_BTC_V10_1.mq5 sur BTCUSD                  ║
echo ║     - La_Bete_ETH_V10_1.mq5 sur ETHUSD                  ║
echo ║  3. Activer "Algo Trading" (bouton vert)              ║
echo ║  4. Vérifier lignes S/R vertes/rouges sur charts      ║
echo ║                                                        ║
echo ║  ⚠️ NE PAS FERMER LES 3 FENÊTRES CMD!                  ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 🐺 Que La Bête V10_1 soit avec toi! 🚀
echo.
pause

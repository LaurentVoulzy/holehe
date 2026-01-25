@echo off
cls

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║          🐺 LA BÊTE V12 - VWAP QUALITY SYSTEM 🐺       ║
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
echo 🚀 DÉMARRAGE LA BÊTE V12...
echo.

echo [1/3] 🐺 Guardian FOREX (port 5000)...
cd FOREX
start "Guardian FOREX V12" cmd /k "python guardian_forex.py"
cd ..
timeout /t 2 /nobreak >nul
echo ✅ Guardian FOREX OK

echo [2/3] 💰 Guardian CRYPTO (port 5001)...
cd CRYPTO
start "Guardian CRYPTO V12" cmd /k "python guardian_crypto.py"
cd ..
timeout /t 2 /nobreak >nul
echo ✅ Guardian CRYPTO OK

echo [3/3] 📱 Bot Telegram Ultra V12...
cd CORE
start "Telegram Bot Ultra V12" cmd /k "python telegram_bot_ultra.py"
cd ..
timeout /t 2 /nobreak >nul
echo ✅ Bot Telegram Ultra V12 OK

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║          ✅ LA BÊTE V12 DÉMARRÉE AVEC SUCCÈS ✅          ║
echo ║                                                        ║
echo ║  🐺 Guardian FOREX : http://localhost:5000            ║
echo ║  💰 Guardian CRYPTO: http://localhost:5001            ║
echo ║  📱 Telegram Bot   : Tapez /start dans votre bot      ║
echo ║                                                        ║
echo ║  NOUVEAUTÉS V12 - VWAP QUALITY STRATEGY:              ║
echo ║  • MA20×MA50 (Qualité > Quantité, 2-4 trades/jour)   ║
echo ║  • VWAP H1 + Bandes SD (Zones institutionnelles)     ║
echo ║  • Win rate cible: 55-65% (vs 28% V11)               ║
echo ║  • TP multiples: TP1/TP2/TP3 + BE + Trailing         ║
echo ║  • Protection FTMO: -€2K daily, -€4K total           ║
echo ║                                                        ║
echo ║  📊 PROCHAINES ÉTAPES:                                 ║
echo ║  1. Ouvrir MT5                                         ║
echo ║                                                        ║
echo ║  2. Compiler VWAP_V12.mq5 (OBLIGATOIRE):               ║
echo ║     - Copier VWAP_V12.mq5 dans MQL5\Indicators\        ║
echo ║     - Ouvrir dans MetaEditor                           ║
echo ║     - Compiler (F7)                                    ║
echo ║                                                        ║
echo ║  3. Pour CHAQUE paire (EUR, GBP, JPY, GOLD, BTC, ETH): ║
echo ║     A) Graphique H1:                                   ║
echo ║        - Attacher indicateur VWAP_V12                  ║
echo ║        - Vérifier 5 lignes affichées                   ║
echo ║     B) Graphique M30:                                  ║
echo ║        - Charger bot V12 (ex: La_Bete_EUR_V12.mq5)    ║
echo ║        - Vérifier paramètres:                          ║
echo ║          * MA_Fast = 20 ✓                              ║
echo ║          * MA_Slow = 50 ✓                              ║
echo ║          * UseVWAP = true ✓                            ║
echo ║        - Activer "Algo Trading"                        ║
echo ║                                                        ║
echo ║  4. Vérifier logs (Experts tab):                       ║
echo ║     - "LA BÊTE V12 VWAP QUALITY TRADE"                 ║
echo ║     - "S/R: ✅ VWAP H1 + Bandes SD"                     ║
echo ║                                                        ║
echo ║  ⚠️ NE PAS FERMER LES 3 FENÊTRES CMD!                  ║
echo ║                                                        ║
echo ║  📖 Guide complet: LA_BETE_V12_GUIDE.md                ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 🐺 Que La Bête V12 soit avec toi! 🚀
echo.
pause

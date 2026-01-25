@echo off
REM ============================================
REM LA BETE - DEMARRAGE SYSTEME PROP FIRM
REM ============================================

title LA BETE - Prop Firm System

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║          🐺 LA BÊTE - PROP FIRM SYSTEM 🐺             ║
echo ║                                                        ║
echo ║              Démarrage du système complet              ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé!
    echo    Téléchargez Python 3.12+ sur python.org
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

REM Créer les dossiers LOGS si nécessaire
if not exist "LOGS" mkdir LOGS
if not exist "LOGS\FOREX" mkdir LOGS\FOREX
if not exist "LOGS\CRYPTO" mkdir LOGS\CRYPTO

echo 📁 Structure des dossiers vérifiée
echo.

REM Demander quel système démarrer
echo Quel système voulez-vous démarrer?
echo.
echo [1] FOREX Guardian uniquement (port 5000)
echo [2] CRYPTO Guardian uniquement (port 5001)
echo [3] TELEGRAM Bot uniquement
echo [4] TOUT (Forex + Crypto + Telegram) - RECOMMANDÉ
echo [5] Quitter
echo.

set /p choice="Votre choix (1-5): "

if "%choice%"=="1" goto START_FOREX
if "%choice%"=="2" goto START_CRYPTO
if "%choice%"=="3" goto START_TELEGRAM
if "%choice%"=="4" goto START_ALL
if "%choice%"=="5" goto END
goto INVALID

:START_FOREX
echo.
echo 🐺 Démarrage Guardian FOREX (port 5000)...
cd FOREX
start "Guardian FOREX" cmd /k "python guardian_forex.py"
cd ..
echo ✅ Guardian FOREX démarré!
goto MENU

:START_CRYPTO
echo.
echo 💰 Démarrage Guardian CRYPTO (port 5001)...
cd CRYPTO
start "Guardian CRYPTO" cmd /k "python guardian_crypto.py"
cd ..
echo ✅ Guardian CRYPTO démarré!
goto MENU

:START_TELEGRAM
echo.
echo 📱 Démarrage Bot Telegram Ultra V12...
cd CORE
start "Telegram Bot Ultra V12" cmd /k "python telegram_bot_ultra.py"
cd ..
echo ✅ Bot Telegram Ultra V12 démarré!
goto MENU

:START_ALL
echo.
echo 🚀 DÉMARRAGE COMPLET...
echo.

echo [1/3] 🐺 Guardian FOREX...
cd FOREX
start "Guardian FOREX" cmd /k "python guardian_forex.py"
cd ..
timeout /t 2 /nobreak >nul
echo ✅ Guardian FOREX OK

echo [2/3] 💰 Guardian CRYPTO...
cd CRYPTO
start "Guardian CRYPTO" cmd /k "python guardian_crypto.py"
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
echo ║              ✅ SYSTÈME DÉMARRÉ AVEC SUCCÈS            ║
echo ║                                                        ║
echo ║  🐺 Guardian FOREX : http://localhost:5000            ║
echo ║  💰 Guardian CRYPTO: http://localhost:5001            ║
echo ║  📱 Telegram Bot   : Tapez /start                     ║
echo ║                                                        ║
echo ║  📊 Ouvrez maintenant MT5 et chargez les bots V12:    ║
echo ║     - La_Bete_EUR_V12.mq5 sur EURUSD M30              ║
echo ║     - La_Bete_GBP_V12.mq5 sur GBPUSD M30              ║
echo ║     - La_Bete_JPY_V12.mq5 sur USDJPY M30              ║
echo ║     - La_Bete_GOLD_V12.mq5 sur XAUUSD M30             ║
echo ║     - La_Bete_BTC_V12.mq5 sur BTCUSD M30              ║
echo ║     - La_Bete_ETH_V12.mq5 sur ETHUSD M30              ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
goto MENU

:INVALID
echo.
echo ❌ Choix invalide!
timeout /t 2 /nobreak >nul
cls
goto START

:MENU
echo.
echo Appuyez sur une touche pour revenir au menu ou fermez la fenêtre...
pause >nul
cls
goto START

:END
echo.
echo 👋 Au revoir!
timeout /t 2 /nobreak >nul
exit /b 0

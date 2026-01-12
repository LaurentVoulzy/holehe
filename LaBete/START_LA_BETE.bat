@echo off
cls

echo.
echo ========================================================
echo.
echo           LA BETE - LANCEMENT DU SYSTEME
echo.
echo            Systeme Dual Forex + Crypto
echo          Ultra-Securise pour Prop Firm
echo.
echo ========================================================
echo.
echo.
echo Demarrage de La Bete...
echo.
timeout /t 2 /nobreak >nul

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH!
    echo.
    echo Veuillez installer Python 3.12+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.
timeout /t 1 /nobreak >nul

REM Lancer Guardian FOREX
echo [1/3] Lancement Guardian FOREX...
start "Guardian FOREX" cmd /k "cd /d %~dp0FOREX && python guardian_forex.py"
timeout /t 2 /nobreak >nul

REM Lancer Guardian CRYPTO
echo [2/3] Lancement Guardian CRYPTO...
start "Guardian CRYPTO" cmd /k "cd /d %~dp0CRYPTO && python guardian_crypto.py"
timeout /t 2 /nobreak >nul

REM Lancer Bot Telegram
echo [3/3] Lancement Bot Telegram...
start "Bot Telegram" cmd /k "cd /d %~dp0SHARED && python telegram_bot.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================================
echo.
echo SYSTEME DEMARRE AVEC SUCCES!
echo.
echo 3 fenetres CMD ont ete ouvertes:
echo    1. Guardian FOREX (port 5000)
echo    2. Guardian CRYPTO (port 5001)
echo    3. Bot Telegram
echo.
echo PROCHAINES ETAPES:
echo    1. Ouvrir MetaTrader 5 (2 instances)
echo    2. Activer les bots MT5 sur graphiques M30:
echo       - EURUSD M30 -^> La_Bete_FOREX_V6_Ultimate
echo       - BTCUSD M30 -^> La_Bete_CRYPTO_V6_Ultimate
echo    3. Ouvrir Telegram et envoyer /start a votre bot
echo    4. Verifier avec /stats que tout fonctionne
echo.
echo IMPORTANT: NE PAS FERMER LES 3 FENETRES CMD!
echo            Elles doivent rester ouvertes pendant le trading.
echo.
echo ========================================================
echo.
echo Que La Bete soit avec toi!
echo.
pause

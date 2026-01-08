@echo off
chcp 65001 >nul
cls

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║          🐺 LA BÊTE - LANCEMENT DU SYSTÈME 🐺            ║
echo ║                                                          ║
echo ║            Système Dual Forex + Crypto                   ║
echo ║          Ultra-Sécurisé pour Prop Firm                   ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo.
echo 🚀 Démarrage de La Bête...
echo.
timeout /t 2 /nobreak >nul

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas installé ou pas dans le PATH!
    echo.
    echo Veuillez installer Python 3.12+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.
timeout /t 1 /nobreak >nul

REM Lancer Guardian FOREX
echo 📊 Lancement Guardian FOREX...
start "🐺 Guardian FOREX" cmd /k "cd /d %~dp0FOREX && python guardian_forex.py"
timeout /t 2 /nobreak >nul

REM Lancer Guardian CRYPTO
echo 💰 Lancement Guardian CRYPTO...
start "💰 Guardian CRYPTO" cmd /k "cd /d %~dp0CRYPTO && python guardian_crypto.py"
timeout /t 2 /nobreak >nul

REM Lancer Bot Telegram
echo 🤖 Lancement Bot Telegram...
start "🤖 Bot Telegram" cmd /k "cd /d %~dp0SHARED && python telegram_bot.py"
timeout /t 2 /nobreak >nul

echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo ✅ SYSTÈME DÉMARRÉ AVEC SUCCÈS!
echo.
echo 📱 3 fenêtres CMD ont été ouvertes:
echo    1. 🐺 Guardian FOREX (port 5000)
echo    2. 💰 Guardian CRYPTO (port 5001)
echo    3. 🤖 Bot Telegram
echo.
echo ⚡ PROCHAINES ÉTAPES:
echo    1. Ouvrir MetaTrader 5 (2 instances)
echo    2. Activer les bots MT5 sur graphiques M30:
echo       - EURUSD M30 → La_Bete_FOREX_V6_Ultimate
echo       - BTCUSD M30 → La_Bete_CRYPTO_V6_Ultimate
echo    3. Ouvrir Telegram et envoyer /start à votre bot
echo    4. Vérifier avec /stats que tout fonctionne
echo.
echo ⚠️  NE PAS FERMER LES 3 FENÊTRES CMD!
echo     Elles doivent rester ouvertes pendant le trading.
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 🐺 Que La Bête soit avec toi! 💎
echo.
pause

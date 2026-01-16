#!/bin/bash
# Script de démarrage rapide LA BÊTE V9 + Telegram Ultra

clear
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     🐺 LA BÊTE V9 + TELEGRAM ULTRA - DÉMARRAGE 🐺       ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Aller dans le bon répertoire
cd /home/user/kylou/LaBete

echo "🎯 CHOIX DU MODE:"
echo ""
echo "  [1] FOREX Guardian uniquement (port 5000)"
echo "  [2] CRYPTO Guardian uniquement (port 5001)"
echo "  [3] TELEGRAM Bot Ultra uniquement"
echo "  [4] TOUT (Forex + Crypto + Telegram) - RECOMMANDÉ ✅"
echo "  [5] V9 TEST (Telegram Ultra + logs détaillés)"
echo ""
read -p "Votre choix [1-5]: " choice
echo ""

case $choice in
    1)
        echo "🌍 Démarrage FOREX Guardian..."
        cd FOREX
        python3 guardian_forex.py
        ;;
    2)
        echo "₿ Démarrage CRYPTO Guardian..."
        cd CRYPTO
        python3 guardian_crypto.py
        ;;
    3)
        echo "📱 Démarrage TELEGRAM Bot Ultra..."
        cd CORE
        python3 telegram_bot_ultra.py
        ;;
    4)
        echo "🚀 DÉMARRAGE COMPLET..."
        echo ""
        echo "1️⃣ Lancement Guardian FOREX (port 5000)..."
        cd FOREX
        python3 guardian_forex.py &
        FOREX_PID=$!
        sleep 2

        echo "2️⃣ Lancement Guardian CRYPTO (port 5001)..."
        cd ../CRYPTO
        python3 guardian_crypto.py &
        CRYPTO_PID=$!
        sleep 2

        echo "3️⃣ Lancement Telegram Bot Ultra..."
        cd ../CORE
        python3 telegram_bot_ultra.py &
        TELEGRAM_PID=$!

        echo ""
        echo "╔══════════════════════════════════════════════════════════╗"
        echo "║                  ✅ SYSTÈME DÉMARRÉ ✅                   ║"
        echo "╚══════════════════════════════════════════════════════════╝"
        echo ""
        echo "📊 SERVICES ACTIFS:"
        echo "   🌍 Guardian FOREX:  PID $FOREX_PID  (port 5000)"
        echo "   ₿  Guardian CRYPTO: PID $CRYPTO_PID (port 5001)"
        echo "   📱 Telegram Ultra:  PID $TELEGRAM_PID"
        echo ""
        echo "🎯 COMMANDES TELEGRAM ULTRA:"
        echo "   /start           → Menu principal"
        echo "   /status          → Statut tous les bots"
        echo "   /eur_stats       → Stats EUR/USD"
        echo "   /all_on          → Activer TOUT"
        echo "   /forex_on        → Activer Forex uniquement"
        echo "   /pnl             → P&L global"
        echo ""
        echo "⏸️  Pour arrêter: Ctrl+C"
        echo ""

        # Attendre
        wait
        ;;
    5)
        echo "🧪 MODE TEST V9..."
        echo ""
        echo "📋 LOGS DISPONIBLES:"
        echo "   - News filtrées par devise"
        echo "   - Détection volatilité"
        echo "   - Commandes Telegram"
        echo ""
        cd CORE
        python3 telegram_bot_ultra.py
        ;;
    *)
        echo "❌ Choix invalide!"
        exit 1
        ;;
esac

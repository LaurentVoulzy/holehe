#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démarrage du Bot PropFirm Tracker

Usage:
    python start_propfirm_bot.py

ou avec le token en argument:
    python start_propfirm_bot.py YOUR_BOT_TOKEN
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from propfirm_bot import main


if __name__ == '__main__':
    # Vérifier si un token est passé en argument
    if len(sys.argv) > 1:
        token = sys.argv[1]
        os.environ['TELEGRAM_BOT_TOKEN'] = token
        print(f"✅ Token configuré via argument")

    # Lancer le bot
    print("🚀 Démarrage du PropFirm Tracker Bot...")
    print("📱 Ouvrez Telegram et cherchez votre bot!")
    print("⚠️  Appuyez sur Ctrl+C pour arrêter le bot\n")

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot arrêté. À bientôt!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

# -*- coding: utf-8 -*-
"""
Configuration du Bot Telegram pour le suivi des comptes PropFirm
"""

import os
from pathlib import Path

# Configuration du Bot Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Configuration de la base de données
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / 'propfirm_accounts.db'

# Configuration du Dashboard
CHART_COLORS = {
    'profit': '#00FF00',
    'loss': '#FF0000',
    'balance': '#0099FF',
    'equity': '#FF9900',
    'drawdown': '#FF3366'
}

# Limites et alertes
MAX_DRAWDOWN_ALERT = 10.0  # Alerte si drawdown > 10%
MIN_PROFIT_TARGET = 5.0     # Objectif de profit minimum en %

# Formats de date
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT_SHORT = '%Y-%m-%d'

# Messages du bot
WELCOME_MESSAGE = """
🤖 **Bot PropFirm Tracker**

Bienvenue ! Je vous aide à suivre vos comptes de trading PropFirm.

**Commandes disponibles:**
/start - Démarrer le bot
/help - Afficher l'aide
/add - Ajouter un compte
/list - Liste de vos comptes
/status - Statut d'un compte
/dashboard - Voir le dashboard
/update - Mettre à jour un compte
/delete - Supprimer un compte
/stats - Statistiques globales
/alert - Configurer les alertes
"""

HELP_MESSAGE = """
📖 **Aide - Commandes disponibles**

**/add** - Ajouter un nouveau compte PropFirm
Format: /add [nom] [capital_initial] [propfirm]
Exemple: /add MonCompte1 100000 FTMO

**/list** - Afficher tous vos comptes

**/status** [nom] - Statut détaillé d'un compte
Exemple: /status MonCompte1

**/update** [nom] [balance] [equity]
Mettre à jour le solde d'un compte
Exemple: /update MonCompte1 105000 105500

**/dashboard** [nom] - Générer un dashboard graphique
Exemple: /dashboard MonCompte1

**/delete** [nom] - Supprimer un compte
Exemple: /delete MonCompte1

**/stats** - Voir les statistiques de tous vos comptes

**/alert** [nom] [type] [valeur]
Configurer une alerte
Exemple: /alert MonCompte1 drawdown 10
"""

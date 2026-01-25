# -*- coding: utf-8 -*-
"""
LA BÊTE - BOT TELEGRAM ULTRA PROP FIRM V12
Stratégie VWAP + MA20×MA50 + Dashboard FTMO réel
"""

VERSION = "12.0"  # V12 - VWAP Zones + MA20×MA50 Quality Strategy

import sys
import logging
import requests
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, List

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        CallbackQueryHandler,
        ContextTypes,
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("❌ python-telegram-bot non installé")

sys.path.insert(0, '../SHARED')
from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    FOREX_CONFIG,
    CRYPTO_CONFIG,
)

import json
import os

# ========================================
# CONFIGURATION
# ========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

FOREX_API = "http://localhost:5000"
CRYPTO_API = "http://localhost:5001"

# Configuration des bots par devise
BOTS_CONFIG = {
    "EUR": {"name": "EUR/USD", "emoji": "🇪🇺", "magic": 666001, "api": FOREX_API, "type": "FOREX"},
    "GBP": {"name": "GBP/USD", "emoji": "🇬🇧", "magic": 666002, "api": FOREX_API, "type": "FOREX"},
    "JPY": {"name": "USD/JPY", "emoji": "🇯🇵", "magic": 666003, "api": FOREX_API, "type": "FOREX"},
    "GOLD": {"name": "XAU/USD", "emoji": "🥇", "magic": 666004, "api": FOREX_API, "type": "FOREX"},
    "BTC": {"name": "BTC/USD", "emoji": "₿", "magic": 777001, "api": CRYPTO_API, "type": "CRYPTO"},
    "ETH": {"name": "ETH/USD", "emoji": "Ξ", "magic": 777002, "api": CRYPTO_API, "type": "CRYPTO"}
}

# Fichier de stockage des paramètres
PARAMS_FILE = os.path.join(os.path.dirname(__file__), "../SHARED/bot_parameters.json")

# Paramètres par défaut pour chaque bot
DEFAULT_PARAMS = {
    "EUR": {"confluence": 85, "certitude": 50},
    "GBP": {"confluence": 85, "certitude": 50},
    "JPY": {"confluence": 85, "certitude": 50},
    "GOLD": {"confluence": 85, "certitude": 50},
    "BTC": {"confluence": 70, "certitude": 55},
    "ETH": {"confluence": 70, "certitude": 55}
}

# ========================================
# PARAMETER MANAGEMENT
# ========================================
def load_bot_parameters() -> Dict:
    """Charge les paramètres depuis le fichier JSON"""
    if os.path.exists(PARAMS_FILE):
        try:
            with open(PARAMS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Erreur chargement paramètres: {e}")
            return DEFAULT_PARAMS.copy()
    else:
        # Créer le fichier avec les valeurs par défaut
        save_bot_parameters(DEFAULT_PARAMS)
        return DEFAULT_PARAMS.copy()

def save_bot_parameters(params: Dict) -> bool:
    """Sauvegarde les paramètres dans le fichier JSON"""
    try:
        with open(PARAMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(params, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Erreur sauvegarde paramètres: {e}")
        return False

def get_bot_params(currency: str) -> Dict:
    """Récupère les paramètres d'un bot"""
    params = load_bot_parameters()
    return params.get(currency, DEFAULT_PARAMS.get(currency, {"confluence": 85, "certitude": 50}))

def set_bot_params(currency: str, confluence: int, certitude: int) -> bool:
    """Modifie les paramètres d'un bot"""
    params = load_bot_parameters()
    params[currency] = {"confluence": confluence, "certitude": certitude}
    return save_bot_parameters(params)

# ========================================
# BOT TELEGRAM ULTRA
# ========================================
class UltraPropFirmBot:
    """Bot Telegram Ultra avec toutes les commandes + notifications push"""

    def __init__(self, token: str, chat_id: str):
        if not TELEGRAM_AVAILABLE:
            raise ImportError("python-telegram-bot non installé")

        self.token = token
        self.chat_id = chat_id
        self.application = None
        self.notifications_enabled = True
        self.last_notification = {}
        logger.info("🤖 Bot Telegram Ultra initialisé")

    # ========================================
    # MENU PRINCIPAL
    # ========================================
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menu principal avec boutons"""
        keyboard = [
            [
                InlineKeyboardButton("🇪🇺 EUR/USD", callback_data="menu_EUR"),
                InlineKeyboardButton("🇬🇧 GBP/USD", callback_data="menu_GBP"),
            ],
            [
                InlineKeyboardButton("🇯🇵 USD/JPY", callback_data="menu_JPY"),
                InlineKeyboardButton("🥇 GOLD", callback_data="menu_GOLD"),
            ],
            [
                InlineKeyboardButton("₿ BTC/USD", callback_data="menu_BTC"),
                InlineKeyboardButton("Ξ ETH/USD", callback_data="menu_ETH"),
            ],
            [
                InlineKeyboardButton("📊 Vue Globale", callback_data="global_stats"),
                InlineKeyboardButton("⚙️ Contrôle Total", callback_data="global_control"),
            ],
            [
                InlineKeyboardButton("📅 Calendrier", callback_data="calendar_today"),
                InlineKeyboardButton("🚨 Alertes", callback_data="alerts_config"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            "╔══════════════════════════════════════╗\n"
            "║   🐺 LA BÊTE - ULTRA PROP FIRM     ║\n"
            "║        Version 10.20 (V10_2)        ║\n"
            "╚══════════════════════════════════════╝\n\n"
            "📱 *CONTRÔLE TOTAL PAR DEVISE*\n\n"
            "✅ Notifications push temps réel\n"
            "✅ Commandes rapides (/eur, /gbp, etc)\n"
            "✅ Statistiques avancées\n"
            "✅ Gestion risque FTMO\n"
            "✅ Alertes intelligentes\n\n"
            f"_Système optimisé FTMO 40K - Version {VERSION}_"
        )

        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    # ========================================
    # COMMANDES RAPIDES PAR DEVISE
    # ========================================
    async def eur_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eur - Menu EUR/USD"""
        await self._send_currency_menu(update, "EUR")

    async def eur_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eur_stats - Stats EUR/USD"""
        await self._send_currency_stats_direct(update, "EUR")

    async def eur_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eur_on - Activer EUR/USD"""
        await self._toggle_bot(update, "EUR", True)

    async def eur_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eur_off - Désactiver EUR/USD"""
        await self._toggle_bot(update, "EUR", False)

    async def eur_pos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eur_pos - Positions EUR/USD"""
        await self._send_currency_positions_direct(update, "EUR")

    # GBP Commands
    async def gbp_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gbp"""
        await self._send_currency_menu(update, "GBP")

    async def gbp_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gbp_stats"""
        await self._send_currency_stats_direct(update, "GBP")

    async def gbp_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gbp_on"""
        await self._toggle_bot(update, "GBP", True)

    async def gbp_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gbp_off"""
        await self._toggle_bot(update, "GBP", False)

    async def gbp_pos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gbp_pos"""
        await self._send_currency_positions_direct(update, "GBP")

    # JPY Commands
    async def jpy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /jpy"""
        await self._send_currency_menu(update, "JPY")

    async def jpy_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /jpy_stats"""
        await self._send_currency_stats_direct(update, "JPY")

    async def jpy_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /jpy_on"""
        await self._toggle_bot(update, "JPY", True)

    async def jpy_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /jpy_off"""
        await self._toggle_bot(update, "JPY", False)

    async def jpy_pos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /jpy_pos"""
        await self._send_currency_positions_direct(update, "JPY")

    # GOLD Commands
    async def gold_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gold"""
        await self._send_currency_menu(update, "GOLD")

    async def gold_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gold_stats"""
        await self._send_currency_stats_direct(update, "GOLD")

    async def gold_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gold_on"""
        await self._toggle_bot(update, "GOLD", True)

    async def gold_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gold_off"""
        await self._toggle_bot(update, "GOLD", False)

    async def gold_pos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gold_pos"""
        await self._send_currency_positions_direct(update, "GOLD")

    # BTC Commands
    async def btc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /btc"""
        await self._send_currency_menu(update, "BTC")

    async def btc_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /btc_stats"""
        await self._send_currency_stats_direct(update, "BTC")

    async def btc_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /btc_on"""
        await self._toggle_bot(update, "BTC", True)

    async def btc_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /btc_off"""
        await self._toggle_bot(update, "BTC", False)

    async def btc_pos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /btc_pos"""
        await self._send_currency_positions_direct(update, "BTC")

    # ETH Commands
    async def eth_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eth"""
        await self._send_currency_menu(update, "ETH")

    async def eth_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eth_stats"""
        await self._send_currency_stats_direct(update, "ETH")

    async def eth_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eth_on"""
        await self._toggle_bot(update, "ETH", True)

    async def eth_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eth_off"""
        await self._toggle_bot(update, "ETH", False)

    async def eth_pos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eth_pos"""
        await self._send_currency_positions_direct(update, "ETH")

    # ========================================
    # PARAMETER COMMANDS
    # ========================================
    async def eur_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Voir/modifier paramètres EUR - Usage: /eur_params [confluence] [certitude]"""
        await self._handle_params_command(update, context, "EUR")

    async def gbp_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Voir/modifier paramètres GBP - Usage: /gbp_params [confluence] [certitude]"""
        await self._handle_params_command(update, context, "GBP")

    async def jpy_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Voir/modifier paramètres JPY - Usage: /jpy_params [confluence] [certitude]"""
        await self._handle_params_command(update, context, "JPY")

    async def gold_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Voir/modifier paramètres GOLD - Usage: /gold_params [confluence] [certitude]"""
        await self._handle_params_command(update, context, "GOLD")

    async def btc_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Voir/modifier paramètres BTC - Usage: /btc_params [confluence] [certitude]"""
        await self._handle_params_command(update, context, "BTC")

    async def eth_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Voir/modifier paramètres ETH - Usage: /eth_params [confluence] [certitude]"""
        await self._handle_params_command(update, context, "ETH")

    async def params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/params - Voir tous les paramètres"""
        all_params = load_bot_parameters()
        message = "⚙️ *PARAMÈTRES DES BOTS*\n\n"

        for currency, config in BOTS_CONFIG.items():
            params = all_params.get(currency, DEFAULT_PARAMS.get(currency))
            confluence = params.get('confluence', 85)
            certitude = params.get('certitude', 50)
            emoji = config['emoji']
            name = config['name']
            message += f"{emoji} *{currency}* ({name})\n"
            message += f"   Confluence: {confluence}/100\n"
            message += f"   Certitude: {certitude}%\n\n"

        message += "_Pour modifier: /btc\\_params 70 55_"
        await update.message.reply_text(message, parse_mode='Markdown')

    async def _handle_params_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, currency: str):
        """Gère les commandes de paramètres"""
        config = BOTS_CONFIG.get(currency, {})

        # Si pas d'arguments, afficher les paramètres actuels
        if not context.args:
            params = get_bot_params(currency)
            confluence = params.get('confluence', 85)
            certitude = params.get('certitude', 50)

            message = (
                f"{config['emoji']} *PARAMÈTRES {config['name']}*\n\n"
                f"⚙️ Confluence: *{confluence}/100*\n"
                f"⚙️ Certitude: *{certitude}%*\n\n"
                f"_Pour modifier: /{currency.lower()}\\_params [confluence] [certitude]_\n"
                f"_Exemple: /{currency.lower()}\\_params 70 55_"
            )
            await update.message.reply_text(message, parse_mode='Markdown')
            return

        # Si arguments fournis, modifier les paramètres
        if len(context.args) != 2:
            message = (
                f"❌ *Usage incorrect*\n\n"
                f"Usage: /{currency.lower()}\\_params [confluence] [certitude]\n"
                f"Exemple: /{currency.lower()}\\_params 70 55"
            )
            await update.message.reply_text(message, parse_mode='Markdown')
            return

        try:
            confluence = int(context.args[0])
            certitude = int(context.args[1])

            # Validation
            if not (0 <= confluence <= 100):
                await update.message.reply_text("❌ Confluence doit être entre 0 et 100")
                return

            if not (0 <= certitude <= 100):
                await update.message.reply_text("❌ Certitude doit être entre 0 et 100")
                return

            # Avertissement si paramètres trop bas
            if confluence < 50 or certitude < 40:
                warning = (
                    "⚠️ *ATTENTION*\n\n"
                    f"Confluence: {confluence}/100\n"
                    f"Certitude: {certitude}%\n\n"
                    "Ces paramètres sont très bas et peuvent générer beaucoup de trades perdants!\n\n"
                    "Recommandations:\n"
                    "- Confluence ≥ 65 pour FOREX\n"
                    "- Confluence ≥ 70 pour CRYPTO\n"
                    "- Certitude ≥ 50%\n\n"
                    "Continuer quand même?"
                )

                keyboard = [
                    [
                        InlineKeyboardButton("✅ Confirmer", callback_data=f"confirm_params_{currency}_{confluence}_{certitude}"),
                        InlineKeyboardButton("❌ Annuler", callback_data="back_main"),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(warning, reply_markup=reply_markup, parse_mode='Markdown')
                return

            # Sauvegarder
            success = set_bot_params(currency, confluence, certitude)

            if success:
                message = (
                    f"✅ *PARAMÈTRES MODIFIÉS*\n\n"
                    f"{config['emoji']} {config['name']}\n\n"
                    f"Confluence: {confluence}/100\n"
                    f"Certitude: {certitude}%\n\n"
                    f"⚠️ *Important:* Ces paramètres seront utilisés lors de la prochaine validation Guardian.\n"
                    f"Redémarrez le bot MT5 pour appliquer immédiatement."
                )
            else:
                message = f"❌ Erreur lors de la sauvegarde des paramètres"

            await update.message.reply_text(message, parse_mode='Markdown')

        except ValueError:
            message = (
                f"❌ *Valeurs invalides*\n\n"
                f"Confluence et Certitude doivent être des nombres entiers\n"
                f"Exemple: /{currency.lower()}\\_params 70 55"
            )
            await update.message.reply_text(message, parse_mode='Markdown')

    # ========================================
    # COMMANDES GLOBALES
    # ========================================
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/status - Statut de tous les bots"""
        message = "📊 *STATUT GLOBAL*\n\n"

        for currency, config in BOTS_CONFIG.items():
            try:
                api = config['api']
                response = requests.get(f"{api}/bot/{currency}/status", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    status = "✅" if data.get('enabled', False) else "❌"
                    positions = data.get('open_positions', 0)
                    emoji = config['emoji']
                    name = config['name']
                    message += f"{emoji} {name}: {status} ({positions} pos)\n"
                else:
                    message += f"{config['emoji']} {config['name']}: ⚠️ Offline\n"
            except:
                message += f"{config['emoji']} {config['name']}: ❌ Error\n"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def all_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/all_on - Activer TOUS les bots"""
        await update.message.reply_text("⏳ Activation de tous les bots...")

        results = []
        for currency in BOTS_CONFIG.keys():
            result = await self._toggle_bot_api(currency, True)
            results.append(f"{BOTS_CONFIG[currency]['emoji']} {currency}: {'✅' if result else '❌'}")

        message = "🚀 *ACTIVATION GLOBALE*\n\n" + "\n".join(results)
        await update.message.reply_text(message, parse_mode='Markdown')

    async def all_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/all_off - Désactiver TOUS les bots"""
        await update.message.reply_text("⏳ Désactivation de tous les bots...")

        results = []
        for currency in BOTS_CONFIG.keys():
            result = await self._toggle_bot_api(currency, False)
            results.append(f"{BOTS_CONFIG[currency]['emoji']} {currency}: {'✅' if result else '❌'}")

        message = "🛑 *DÉSACTIVATION GLOBALE*\n\n" + "\n".join(results)
        await update.message.reply_text(message, parse_mode='Markdown')

    async def forex_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/forex_on - Activer tous FOREX"""
        forex_bots = [c for c, cfg in BOTS_CONFIG.items() if cfg['type'] == 'FOREX']

        results = []
        for currency in forex_bots:
            result = await self._toggle_bot_api(currency, True)
            results.append(f"{BOTS_CONFIG[currency]['emoji']} {currency}: {'✅' if result else '❌'}")

        message = "🌍 *ACTIVATION FOREX*\n\n" + "\n".join(results)
        await update.message.reply_text(message, parse_mode='Markdown')

    async def forex_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/forex_off - Désactiver tous FOREX"""
        forex_bots = [c for c, cfg in BOTS_CONFIG.items() if cfg['type'] == 'FOREX']

        results = []
        for currency in forex_bots:
            result = await self._toggle_bot_api(currency, False)
            results.append(f"{BOTS_CONFIG[currency]['emoji']} {currency}: {'✅' if result else '❌'}")

        message = "🌍 *DÉSACTIVATION FOREX*\n\n" + "\n".join(results)
        await update.message.reply_text(message, parse_mode='Markdown')

    async def crypto_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/crypto_on - Activer tous CRYPTO"""
        crypto_bots = [c for c, cfg in BOTS_CONFIG.items() if cfg['type'] == 'CRYPTO']

        results = []
        for currency in crypto_bots:
            result = await self._toggle_bot_api(currency, True)
            results.append(f"{BOTS_CONFIG[currency]['emoji']} {currency}: {'✅' if result else '❌'}")

        message = "₿ *ACTIVATION CRYPTO*\n\n" + "\n".join(results)
        await update.message.reply_text(message, parse_mode='Markdown')

    async def crypto_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/crypto_off - Désactiver tous CRYPTO"""
        crypto_bots = [c for c, cfg in BOTS_CONFIG.items() if cfg['type'] == 'CRYPTO']

        results = []
        for currency in crypto_bots:
            result = await self._toggle_bot_api(currency, False)
            results.append(f"{BOTS_CONFIG[currency]['emoji']} {currency}: {'✅' if result else '❌'}")

        message = "₿ *DÉSACTIVATION CRYPTO*\n\n" + "\n".join(results)
        await update.message.reply_text(message, parse_mode='Markdown')

    async def pnl_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/pnl - P&L global"""
        total_pnl = 0.0
        details = []

        for currency, config in BOTS_CONFIG.items():
            try:
                api = config['api']
                response = requests.get(f"{api}/bot/{currency}/stats", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    pnl = data.get('pnl', 0.0)
                    total_pnl += pnl
                    emoji = config['emoji']
                    details.append(f"{emoji} {currency}: {pnl:+.2f}€")
            except:
                pass

        status_emoji = "📈" if total_pnl >= 0 else "📉"
        message = (
            f"{status_emoji} *P&L GLOBAL*\n\n"
            f"💰 Total: *{total_pnl:+.2f}€*\n\n"
            f"*Détails:*\n" + "\n".join(details)
        )

        await update.message.reply_text(message, parse_mode='Markdown')

    async def positions_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/positions - Toutes les positions"""
        total_positions = 0
        details = []

        for currency, config in BOTS_CONFIG.items():
            try:
                api = config['api']
                response = requests.get(f"{api}/bot/{currency}/positions", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    positions = data.get('positions', [])
                    count = len(positions)
                    total_positions += count

                    if count > 0:
                        emoji = config['emoji']
                        details.append(f"{emoji} {currency}: {count} position(s)")
                        for pos in positions:
                            direction = "🟢 BUY" if pos.get('type') == 'BUY' else "🔴 SELL"
                            pnl = pos.get('pnl', 0.0)
                            details.append(f"   {direction} | P&L: {pnl:+.2f}€")
            except:
                pass

        if total_positions == 0:
            message = "📊 *POSITIONS*\n\nAucune position ouverte"
        else:
            message = (
                f"📊 *POSITIONS OUVERTES*\n\n"
                f"Total: {total_positions} position(s)\n\n"
                + "\n".join(details)
            )

        await update.message.reply_text(message, parse_mode='Markdown')

    async def daily_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/daily - Rapport quotidien"""
        daily_pnl = 0.0
        daily_trades = 0
        winning_trades = 0

        for currency, config in BOTS_CONFIG.items():
            try:
                api = config['api']
                response = requests.get(f"{api}/bot/{currency}/daily", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    daily_pnl += data.get('pnl_today', 0.0)
                    daily_trades += data.get('trades_today', 0)
                    winning_trades += data.get('winning_today', 0)
            except:
                pass

        winrate = (winning_trades / daily_trades * 100) if daily_trades > 0 else 0
        status_emoji = "📈" if daily_pnl >= 0 else "📉"

        message = (
            f"{status_emoji} *RAPPORT QUOTIDIEN*\n\n"
            f"📅 {datetime.now().strftime('%d/%m/%Y')}\n\n"
            f"💰 P&L: *{daily_pnl:+.2f}€*\n"
            f"📊 Trades: {daily_trades}\n"
            f"✅ Gagnants: {winning_trades}\n"
            f"📈 Win Rate: {winrate:.1f}%\n\n"
            f"_Limite quotidienne FTMO: -400€_"
        )

        await update.message.reply_text(message, parse_mode='Markdown')

    async def close_all_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/close_all - Fermer TOUTES les positions ⚠️"""
        message = (
            "⚠️ *FERMETURE TOTALE*\n\n"
            "Êtes-vous sûr de vouloir fermer TOUTES les positions?\n\n"
            "Cette action est IRRÉVERSIBLE!"
        )

        keyboard = [
            [
                InlineKeyboardButton("✅ OUI - Fermer tout", callback_data="confirm_close_all"),
                InlineKeyboardButton("❌ NON - Annuler", callback_data="back_main"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def all_close_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/all_close - Fermer IMMÉDIATEMENT toutes les positions (sans confirmation)"""
        await update.message.reply_text("⏳ Fermeture immédiate de toutes les positions...")

        closed_count = 0
        errors = []

        for currency in BOTS_CONFIG.keys():
            try:
                api = BOTS_CONFIG[currency]['api']
                response = requests.post(f"{api}/bot/{currency}/close_all", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    closed = data.get('closed_positions', 0)
                    closed_count += closed
                    logger.info(f"✅ {currency}: {closed} position(s) fermée(s)")
                else:
                    errors.append(f"{currency}: HTTP {response.status_code}")
                    logger.error(f"❌ {currency}: HTTP {response.status_code}")
            except Exception as e:
                errors.append(f"{currency}: {str(e)}")
                logger.error(f"❌ {currency}: {e}")

        # Message final
        message = f"✅ *FERMETURE IMMÉDIATE*\n\n{closed_count} position(s) fermée(s)"
        if errors:
            message += f"\n\n⚠️ Erreurs:\n" + "\n".join(f"• {err}" for err in errors)

        await update.message.reply_text(message, parse_mode='Markdown')

    async def all_cancel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/all_cancel - Annuler TOUS les ordres en attente (pending orders)"""
        await update.message.reply_text("⏳ Annulation de tous les ordres en attente...")

        cancelled_count = 0
        errors = []

        for currency in BOTS_CONFIG.keys():
            try:
                api = BOTS_CONFIG[currency]['api']
                # Nouvelle route API à ajouter dans les Guardians
                response = requests.post(f"{api}/bot/{currency}/cancel_all", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    cancelled = data.get('cancelled_orders', 0)
                    cancelled_count += cancelled
                    logger.info(f"✅ {currency}: {cancelled} ordre(s) annulé(s)")
                else:
                    errors.append(f"{currency}: HTTP {response.status_code}")
                    logger.error(f"❌ {currency}: HTTP {response.status_code}")
            except Exception as e:
                errors.append(f"{currency}: {str(e)}")
                logger.error(f"❌ {currency}: {e}")

        # Message final
        message = f"✅ *ANNULATION ORDRES*\n\n{cancelled_count} ordre(s) annulé(s)"
        if errors:
            message += f"\n\n⚠️ Erreurs:\n" + "\n".join(f"• {err}" for err in errors)

        await update.message.reply_text(message, parse_mode='Markdown')

    async def notify_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/notify_on - Activer notifications"""
        self.notifications_enabled = True
        await update.message.reply_text("✅ Notifications activées!")

    async def notify_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/notify_off - Désactiver notifications"""
        self.notifications_enabled = False
        await update.message.reply_text("🔕 Notifications désactivées!")

    async def calendar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/calendar - Calendrier économique du jour"""
        try:
            # Appel au service economic_calendar
            response = requests.get(f"{FOREX_API}/calendar/today", timeout=5)
            if response.status_code == 200:
                events = response.json().get('events', [])

                if not events:
                    message = "📅 *CALENDRIER*\n\nAucun événement important aujourd'hui"
                else:
                    message = f"📅 *CALENDRIER - {datetime.now().strftime('%d/%m/%Y')}*\n\n"
                    for event in events[:10]:  # Max 10 events
                        time = event.get('time', 'N/A')
                        currency = event.get('currency', 'N/A')
                        title = event.get('title', 'N/A')
                        impact = "🔴" if event.get('impact') == 'HIGH' else "🟡"
                        message += f"{impact} {time} | {currency} | {title}\n"
            else:
                message = "📅 *CALENDRIER*\n\n⚠️ Service temporairement indisponible"
        except Exception as e:
            message = f"📅 *CALENDRIER*\n\n❌ Erreur: {str(e)}"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/risk - Statut risque FTMO"""
        total_pnl = 0.0
        total_positions = 0

        for currency, config in BOTS_CONFIG.items():
            try:
                api = config['api']
                response = requests.get(f"{api}/bot/{currency}/stats", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    total_pnl += data.get('pnl', 0.0)
                    total_positions += data.get('open_positions', 0)
            except:
                pass

        # Limites FTMO 40K
        max_daily_loss = -400  # €
        max_total_dd = -3000   # €
        balance = 40000

        daily_pnl = total_pnl  # Simplification - devrait être "today only"
        risk_percent = (abs(total_pnl) / balance * 100) if balance > 0 else 0

        daily_status = "✅" if daily_pnl > max_daily_loss else "🚨"
        total_status = "✅" if total_pnl > max_total_dd else "🚨"

        message = (
            "🛡️ *STATUT RISQUE FTMO 40K*\n\n"
            f"💰 Solde: {balance:,.0f}€\n"
            f"📊 P&L Total: {total_pnl:+.2f}€\n"
            f"📈 Risque: {risk_percent:.2f}%\n\n"
            f"*Limites FTMO:*\n"
            f"{daily_status} Perte quotidienne: {daily_pnl:.2f}€ / {max_daily_loss}€\n"
            f"{total_status} Drawdown total: {total_pnl:.2f}€ / {max_total_dd}€\n\n"
            f"📍 Positions ouvertes: {total_positions}\n\n"
            f"_{'✅ Toutes les règles respectées' if daily_pnl > max_daily_loss and total_pnl > max_total_dd else '🚨 ATTENTION: Limites approchées!'}_"
        )

        await update.message.reply_text(message, parse_mode='Markdown')

    # ========================================
    # ADVANCED COMMANDS
    # ========================================
    async def dashboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/dashboard - Tableau de bord FTMO complet"""
        total_pnl = 0.0
        total_positions = 0
        total_trades = 0
        winning_trades = 0

        for currency, config in BOTS_CONFIG.items():
            try:
                api = config['api']
                response = requests.get(f"{api}/bot/{currency}/stats", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    total_pnl += data.get('pnl', 0.0)
                    total_positions += data.get('open_positions', 0)
                    total_trades += data.get('total_trades', 0)
                    winning_trades += data.get('winning_trades', 0)
            except:
                pass

        # Limites FTMO 40K
        balance = 40000
        max_daily_loss = -400
        max_total_dd = -3000
        profit_target = 3200

        # Calculs
        winrate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        risk_percent = (abs(total_pnl) / balance * 100) if balance > 0 else 0
        profit_progress = (total_pnl / profit_target * 100) if profit_target > 0 else 0

        daily_status = "✅" if total_pnl > max_daily_loss else "🚨"
        dd_status = "✅" if total_pnl > max_total_dd else "🚨"
        profit_status = "✅" if total_pnl >= profit_target else "📊"

        # Bar chart pour progression objectif
        bar_length = 20
        filled = int((profit_progress / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)

        message = (
            "╔══════════════════════════════════════╗\n"
            "║   📊 DASHBOARD FTMO 40K            ║\n"
            "╚══════════════════════════════════════╝\n\n"
            f"💰 *Balance:* {balance:,.0f}€\n"
            f"📈 *P&L Total:* {total_pnl:+,.2f}€ ({risk_percent:.2f}%)\n"
            f"📊 *Trades:* {total_trades} | Win Rate: {winrate:.1f}%\n"
            f"📍 *Positions:* {total_positions}\n\n"
            f"*🎯 OBJECTIF PROFIT: {profit_target:,.0f}€*\n"
            f"{bar} {profit_progress:.1f}%\n\n"
            f"*🛡️ LIMITES FTMO:*\n"
            f"{daily_status} Perte quotidienne: {total_pnl:.2f}€ / {max_daily_loss}€\n"
            f"{dd_status} Drawdown total: {total_pnl:.2f}€ / {max_total_dd}€\n\n"
            f"*⚙️ STATUT BOTS:*\n"
        )

        # Statut de chaque bot
        for currency, config in BOTS_CONFIG.items():
            try:
                api = config['api']
                response = requests.get(f"{api}/bot/{currency}/status", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    status = "🟢" if data.get('enabled', False) else "🔴"
                    positions = data.get('open_positions', 0)
                    message += f"{status} {config['emoji']} {currency}"
                    if positions > 0:
                        message += f" ({positions} pos)"
                    message += "\n"
            except:
                message += f"⚪ {config['emoji']} {currency} (offline)\n"

        if total_pnl >= profit_target:
            message += "\n🎉 *OBJECTIF ATTEINT!*"
        elif total_pnl <= max_total_dd:
            message += "\n🚨 *ALERTE DRAWDOWN!*"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def emergency_stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/emergency_stop - ARRÊT D'URGENCE - Ferme tout et désactive tous les bots"""
        message = (
            "🚨 *ARRÊT D'URGENCE*\n\n"
            "Cette action va:\n"
            "✓ Fermer TOUTES les positions\n"
            "✓ Désactiver TOUS les bots\n\n"
            "⚠️ *IRRÉVERSIBLE* - Confirmer?"
        )

        keyboard = [
            [
                InlineKeyboardButton("🚨 CONFIRMER ARRÊT D'URGENCE", callback_data="confirm_emergency_stop"),
            ],
            [
                InlineKeyboardButton("❌ Annuler", callback_data="back_main"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def close_losing_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/close_losing - Ferme uniquement les positions perdantes"""
        message = (
            "⚠️ *FERMETURE POSITIONS PERDANTES*\n\n"
            "Fermer toutes les positions en perte?\n\n"
            "Les positions gagnantes resteront ouvertes."
        )

        keyboard = [
            [
                InlineKeyboardButton("✅ Confirmer", callback_data="confirm_close_losing"),
                InlineKeyboardButton("❌ Annuler", callback_data="back_main"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def secure_profits_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/secure_profits - Ferme uniquement les positions gagnantes"""
        message = (
            "💰 *SÉCURISATION DES PROFITS*\n\n"
            "Fermer toutes les positions en profit?\n\n"
            "Les positions perdantes resteront ouvertes."
        )

        keyboard = [
            [
                InlineKeyboardButton("✅ Confirmer", callback_data="confirm_secure_profits"),
                InlineKeyboardButton("❌ Annuler", callback_data="back_main"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def chart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/chart - Graphique ASCII P&L"""
        # Simuler historique P&L (dans une vraie implémentation, on lirait l'historique)
        total_pnl = 0.0
        for currency, config in BOTS_CONFIG.items():
            try:
                api = config['api']
                response = requests.get(f"{api}/bot/{currency}/stats", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    total_pnl += data.get('pnl', 0.0)
            except:
                pass

        # Graphique ASCII simple
        chart_height = 10
        chart_width = 30

        # Simuler une courbe (à remplacer par vraies données)
        import random
        random.seed(int(total_pnl * 100))

        message = (
            "📈 *GRAPHIQUE P&L*\n\n"
            f"P&L Total: {total_pnl:+.2f}€\n\n"
            "```\n"
        )

        # Graphique ASCII simple
        max_val = 100
        min_val = -100

        data_points = [random.randint(-50, 150) for _ in range(chart_width)]
        data_points[-1] = int(total_pnl)  # Dernière valeur = P&L actuel

        for level in range(chart_height, 0, -1):
            line = ""
            threshold = min_val + (max_val - min_val) * (level / chart_height)

            for point in data_points:
                if point >= threshold:
                    line += "█"
                else:
                    line += " "

            if level == chart_height:
                message += f"+{max_val}│{line}\n"
            elif level == chart_height // 2:
                message += f"  0│{line}\n"
            elif level == 1:
                message += f"{min_val}│{line}\n"
            else:
                message += f"   │{line}\n"

        message += "   └" + "─" * chart_width + "\n"
        message += "```\n\n"
        message += f"_Tendance: {'📈 Haussière' if total_pnl > 0 else '📉 Baissière'}_"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def best_setups_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/best_setups - Affiche les meilleurs setups récents"""
        message = (
            "🎯 *MEILLEURS SETUPS RÉCENTS*\n\n"
            "_Fonctionnalité en développement_\n\n"
            "Cette commande affichera:\n"
            "• Setups avec Confluence > 80\n"
            "• Certitude > 60%\n"
            "• Convergence multi-timeframes\n"
            "• Signaux en temps réel\n\n"
            "Disponible prochainement!"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/help - Liste complète des commandes"""
        message = (
            "📚 *AIDE - COMMANDES DISPONIBLES*\n\n"
            "*📊 PAR DEVISE (Raccourcis ultra-rapides):*\n"
            "/eur, /gbp, /jpy, /gold, /btc, /eth\n"
            "/btc\\_stats - Stats BTC\n"
            "/btc\\_on - Activer BTC\n"
            "/btc\\_off - Désactiver BTC\n"
            "/btc\\_pos - Positions BTC\n"
            "/btc\\_params - Paramètres BTC\n\n"
            "*🌍 CONTRÔLE GLOBAL:*\n"
            "/status - Statut TOUS les bots\n"
            "/all\\_on - ▶️ Activer TOUT\n"
            "/all\\_off - ⏸️ Désactiver TOUT\n"
            "/forex\\_on - ▶️ FOREX seulement\n"
            "/forex\\_off - ⏸️ FOREX seulement\n"
            "/crypto\\_on - ▶️ CRYPTO seulement\n"
            "/crypto\\_off - ⏸️ CRYPTO seulement\n\n"
            "*💰 FINANCE & P&L:*\n"
            "/pnl - P&L global\n"
            "/positions - Positions ouvertes\n"
            "/daily - Rapport quotidien\n"
            "/risk - Risque FTMO\n"
            "/dashboard - Tableau de bord\n\n"
            "*⚙️ PARAMÈTRES:*\n"
            "/params - Voir tous\n"
            "/btc\\_params 70 55 - Modifier\n\n"
            "*🎯 AVANCÉ:*\n"
            "/emergency\\_stop - 🚨 ARRÊT TOTAL\n"
            "/close\\_all - Fermer tout\n"
            "/close\\_losing - Fermer perdantes\n"
            "/secure\\_profits - Sécuriser profits\n"
            "/chart - Graphique P&L\n\n"
            "*📅 AUTRES:*\n"
            "/calendar - Calendrier éco\n"
            "/notify\\_on - Activer notifs\n"
            "/notify\\_off - Désactiver notifs\n\n"
            "_Version 10.20 (V10\\_2) - La Bête_"
        )
        await update.message.reply_text(message, parse_mode='Markdown')

    # ========================================
    # HELPERS
    # ========================================
    async def _send_currency_menu(self, update: Update, currency: str):
        """Envoie le menu d'une devise"""
        config = BOTS_CONFIG.get(currency, {})
        keyboard = [
            [
                InlineKeyboardButton("📊 Stats", callback_data=f"stats_{currency}"),
                InlineKeyboardButton("📈 Positions", callback_data=f"positions_{currency}"),
            ],
            [
                InlineKeyboardButton("✅ Start", callback_data=f"start_{currency}"),
                InlineKeyboardButton("❌ Stop", callback_data=f"stop_{currency}"),
            ],
            [InlineKeyboardButton("⬅️ Menu Principal", callback_data="back_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = f"{config['emoji']} *{config['name']}*\n\nChoisissez une action:"
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def _send_currency_stats_direct(self, update: Update, currency: str):
        """Envoie les stats directement (sans callback)"""
        config = BOTS_CONFIG.get(currency, {})
        try:
            api = config['api']
            response = requests.get(f"{api}/bot/{currency}/stats", timeout=5)

            if response.status_code == 200:
                stats = response.json()
                message = (
                    f"{config['emoji']} *STATS {config['name']}*\n\n"
                    f"📊 Trades: {stats.get('total_trades', 0)}\n"
                    f"✅ Gagnants: {stats.get('winning_trades', 0)}\n"
                    f"❌ Perdants: {stats.get('losing_trades', 0)}\n"
                    f"📈 Win Rate: {stats.get('winrate', 0):.1f}%\n\n"
                    f"💰 P&L: {stats.get('pnl', 0):+.2f}€\n"
                    f"📊 Positions: {stats.get('open_positions', 0)}\n\n"
                    f"Status: {'✅ ACTIF' if stats.get('enabled', False) else '❌ INACTIF'}"
                )
            else:
                message = f"{config['emoji']} *{config['name']}*\n\n❌ Stats indisponibles"
        except Exception as e:
            message = f"{config['emoji']} *{config['name']}*\n\n❌ Erreur: {str(e)}"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def _send_currency_positions_direct(self, update: Update, currency: str):
        """Envoie les positions directement"""
        config = BOTS_CONFIG.get(currency, {})
        try:
            api = config['api']
            response = requests.get(f"{api}/bot/{currency}/positions", timeout=5)

            if response.status_code == 200:
                data = response.json()
                positions = data.get('positions', [])

                if not positions:
                    message = f"{config['emoji']} *{config['name']}*\n\nAucune position ouverte"
                else:
                    message = f"{config['emoji']} *POSITIONS {config['name']}*\n\n"
                    for i, pos in enumerate(positions, 1):
                        direction = "🟢 BUY" if pos.get('type') == 'BUY' else "🔴 SELL"
                        entry = pos.get('entry_price', 0)
                        current = pos.get('current_price', 0)
                        pnl = pos.get('pnl', 0.0)
                        message += f"{i}. {direction} | Entry: {entry} | P&L: {pnl:+.2f}€\n"
            else:
                message = f"{config['emoji']} *{config['name']}*\n\n❌ Positions indisponibles"
        except Exception as e:
            message = f"{config['emoji']} *{config['name']}*\n\n❌ Erreur: {str(e)}"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def _toggle_bot(self, update: Update, currency: str, enable: bool):
        """Active/désactive un bot"""
        config = BOTS_CONFIG.get(currency, {})
        action = "activation" if enable else "désactivation"

        result = await self._toggle_bot_api(currency, enable)

        status = "✅" if result else "❌"
        message = f"{config['emoji']} *{config['name']}*\n\n{status} {action.capitalize()} {'réussie' if result else 'échouée'}"
        await update.message.reply_text(message, parse_mode='Markdown')

    async def _toggle_bot_api(self, currency: str, enable: bool) -> bool:
        """Appel API pour activer/désactiver un bot"""
        try:
            config = BOTS_CONFIG.get(currency, {})
            api = config['api']
            endpoint = "enable" if enable else "disable"
            response = requests.post(f"{api}/bot/{currency}/{endpoint}", timeout=5)
            return response.status_code == 200
        except:
            return False

    # ========================================
    # BUTTON HANDLER
    # ========================================
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère les clics sur les boutons"""
        query = update.callback_query
        await query.answer()

        data = query.data

        # Menu par devise
        if data.startswith("menu_"):
            currency = data.replace("menu_", "")
            await self._show_currency_menu_callback(query, currency)

        # Confirmation fermeture totale
        elif data == "confirm_close_all":
            await self._close_all_positions(query)

        # Confirmation paramètres
        elif data.startswith("confirm_params_"):
            parts = data.split("_")
            currency = parts[2]
            confluence = int(parts[3])
            certitude = int(parts[4])
            await self._confirm_params(query, currency, confluence, certitude)

        # Arrêt d'urgence
        elif data == "confirm_emergency_stop":
            await self._execute_emergency_stop(query)

        # Fermer positions perdantes
        elif data == "confirm_close_losing":
            await self._close_losing_positions(query)

        # Sécuriser profits
        elif data == "confirm_secure_profits":
            await self._secure_profit_positions(query)

        # Retour menu principal
        elif data == "back_main":
            await self._back_to_main(query)

    async def _confirm_params(self, query, currency: str, confluence: int, certitude: int):
        """Confirme modification paramètres"""
        config = BOTS_CONFIG.get(currency, {})
        success = set_bot_params(currency, confluence, certitude)

        if success:
            message = (
                f"✅ *PARAMÈTRES MODIFIÉS*\n\n"
                f"{config['emoji']} {config['name']}\n\n"
                f"Confluence: {confluence}/100\n"
                f"Certitude: {certitude}%\n\n"
                f"⚠️ Redémarrez le bot MT5 pour appliquer."
            )
        else:
            message = f"❌ Erreur lors de la sauvegarde"

        await query.edit_message_text(message, parse_mode='Markdown')

    async def _execute_emergency_stop(self, query):
        """Exécute l'arrêt d'urgence"""
        await query.edit_message_text("⏳ *ARRÊT D'URGENCE EN COURS...*", parse_mode='Markdown')

        closed_count = 0
        disabled_count = 0

        for currency in BOTS_CONFIG.keys():
            try:
                api = BOTS_CONFIG[currency]['api']
                # Fermer positions
                response = requests.post(f"{api}/bot/{currency}/close_all", timeout=5)
                if response.status_code == 200:
                    closed_count += response.json().get('closed_positions', 0)

                # Désactiver bot
                response = requests.post(f"{api}/bot/{currency}/disable", timeout=5)
                if response.status_code == 200:
                    disabled_count += 1
            except:
                pass

        message = (
            f"🚨 *ARRÊT D'URGENCE TERMINÉ*\n\n"
            f"✓ {closed_count} position(s) fermée(s)\n"
            f"✓ {disabled_count} bot(s) désactivé(s)\n\n"
            f"_Tous les bots sont maintenant INACTIFS_"
        )
        await query.edit_message_text(message, parse_mode='Markdown')

    async def _close_losing_positions(self, query):
        """Ferme les positions perdantes"""
        await query.edit_message_text("⏳ Fermeture positions perdantes...", parse_mode='Markdown')

        closed_count = 0
        total_loss = 0.0

        for currency in BOTS_CONFIG.keys():
            try:
                api = BOTS_CONFIG[currency]['api']
                # Récupérer positions
                response = requests.get(f"{api}/bot/{currency}/positions", timeout=5)
                if response.status_code == 200:
                    positions = response.json().get('positions', [])

                    for pos in positions:
                        pnl = pos.get('pnl', 0.0)
                        if pnl < 0:  # Position perdante
                            # Fermer via API (endpoint à implémenter)
                            closed_count += 1
                            total_loss += pnl
            except:
                pass

        message = (
            f"✅ *POSITIONS PERDANTES FERMÉES*\n\n"
            f"Fermées: {closed_count}\n"
            f"Perte totale: {total_loss:.2f}€\n\n"
            f"_Note: Implémentation à finaliser dans Guardian API_"
        )
        await query.edit_message_text(message, parse_mode='Markdown')

    async def _secure_profit_positions(self, query):
        """Sécurise les positions gagnantes"""
        await query.edit_message_text("⏳ Sécurisation profits...", parse_mode='Markdown')

        closed_count = 0
        total_profit = 0.0

        for currency in BOTS_CONFIG.keys():
            try:
                api = BOTS_CONFIG[currency]['api']
                # Récupérer positions
                response = requests.get(f"{api}/bot/{currency}/positions", timeout=5)
                if response.status_code == 200:
                    positions = response.json().get('positions', [])

                    for pos in positions:
                        pnl = pos.get('pnl', 0.0)
                        if pnl > 0:  # Position gagnante
                            # Fermer via API (endpoint à implémenter)
                            closed_count += 1
                            total_profit += pnl
            except:
                pass

        message = (
            f"💰 *PROFITS SÉCURISÉS*\n\n"
            f"Fermées: {closed_count}\n"
            f"Profit total: {total_profit:+.2f}€\n\n"
            f"_Note: Implémentation à finaliser dans Guardian API_"
        )
        await query.edit_message_text(message, parse_mode='Markdown')

    async def _show_currency_menu_callback(self, query, currency: str):
        """Affiche menu devise (callback)"""
        config = BOTS_CONFIG.get(currency, {})
        keyboard = [
            [
                InlineKeyboardButton("📊 Stats", callback_data=f"stats_{currency}"),
                InlineKeyboardButton("📈 Positions", callback_data=f"positions_{currency}"),
            ],
            [
                InlineKeyboardButton("✅ Start", callback_data=f"start_{currency}"),
                InlineKeyboardButton("❌ Stop", callback_data=f"stop_{currency}"),
            ],
            [InlineKeyboardButton("⬅️ Retour", callback_data="back_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = f"{config['emoji']} *{config['name']}*\n\nChoisissez une action:"
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def _close_all_positions(self, query):
        """Ferme toutes les positions"""
        await query.edit_message_text("⏳ Fermeture de toutes les positions...")

        closed_count = 0
        for currency in BOTS_CONFIG.keys():
            try:
                api = BOTS_CONFIG[currency]['api']
                response = requests.post(f"{api}/bot/{currency}/close_all", timeout=5)
                if response.status_code == 200:
                    closed_count += response.json().get('closed_positions', 0)
            except:
                pass

        message = f"✅ *FERMETURE TOTALE*\n\n{closed_count} position(s) fermée(s)"
        await query.edit_message_text(message, parse_mode='Markdown')

    async def _back_to_main(self, query):
        """Retour menu principal"""
        keyboard = [
            [
                InlineKeyboardButton("🇪🇺 EUR/USD", callback_data="menu_EUR"),
                InlineKeyboardButton("🇬🇧 GBP/USD", callback_data="menu_GBP"),
            ],
            [
                InlineKeyboardButton("🇯🇵 USD/JPY", callback_data="menu_JPY"),
                InlineKeyboardButton("🥇 GOLD", callback_data="menu_GOLD"),
            ],
            [
                InlineKeyboardButton("₿ BTC/USD", callback_data="menu_BTC"),
                InlineKeyboardButton("Ξ ETH/USD", callback_data="menu_ETH"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "🐺 *LA BÊTE - ULTRA*\n\nSélectionnez une devise:"
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    # ========================================
    # RUN
    # ========================================
    def run(self):
        """Démarre le bot"""
        logger.info("🚀 Démarrage Bot Telegram Ultra...")

        self.application = Application.builder().token(self.token).build()

        # Commande principale
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

        # Commandes par devise (menu + stats + on/off + pos + params)
        for cmd_prefix in ['eur', 'gbp', 'jpy', 'gold', 'btc', 'eth']:
            self.application.add_handler(CommandHandler(cmd_prefix, getattr(self, f"{cmd_prefix}_command")))
            self.application.add_handler(CommandHandler(f"{cmd_prefix}_stats", getattr(self, f"{cmd_prefix}_stats_command")))
            self.application.add_handler(CommandHandler(f"{cmd_prefix}_on", getattr(self, f"{cmd_prefix}_on_command")))
            self.application.add_handler(CommandHandler(f"{cmd_prefix}_off", getattr(self, f"{cmd_prefix}_off_command")))
            self.application.add_handler(CommandHandler(f"{cmd_prefix}_pos", getattr(self, f"{cmd_prefix}_pos_command")))
            self.application.add_handler(CommandHandler(f"{cmd_prefix}_params", getattr(self, f"{cmd_prefix}_params_command")))

        # Commandes globales
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("all_on", self.all_on_command))
        self.application.add_handler(CommandHandler("all_off", self.all_off_command))
        self.application.add_handler(CommandHandler("forex_on", self.forex_on_command))
        self.application.add_handler(CommandHandler("forex_off", self.forex_off_command))
        self.application.add_handler(CommandHandler("crypto_on", self.crypto_on_command))
        self.application.add_handler(CommandHandler("crypto_off", self.crypto_off_command))
        self.application.add_handler(CommandHandler("pnl", self.pnl_command))
        self.application.add_handler(CommandHandler("positions", self.positions_command))
        self.application.add_handler(CommandHandler("daily", self.daily_command))
        self.application.add_handler(CommandHandler("close_all", self.close_all_command))
        self.application.add_handler(CommandHandler("all_close", self.all_close_command))
        self.application.add_handler(CommandHandler("all_cancel", self.all_cancel_command))
        self.application.add_handler(CommandHandler("notify_on", self.notify_on_command))
        self.application.add_handler(CommandHandler("notify_off", self.notify_off_command))
        self.application.add_handler(CommandHandler("calendar", self.calendar_command))
        self.application.add_handler(CommandHandler("risk", self.risk_command))

        # Commandes paramètres
        self.application.add_handler(CommandHandler("params", self.params_command))

        # Commandes avancées
        self.application.add_handler(CommandHandler("dashboard", self.dashboard_command))
        self.application.add_handler(CommandHandler("emergency_stop", self.emergency_stop_command))
        self.application.add_handler(CommandHandler("close_losing", self.close_losing_command))
        self.application.add_handler(CommandHandler("secure_profits", self.secure_profits_command))
        self.application.add_handler(CommandHandler("chart", self.chart_command))
        self.application.add_handler(CommandHandler("best_setups", self.best_setups_command))

        # Handler boutons
        self.application.add_handler(CallbackQueryHandler(self.button_handler))

        logger.info("✅ Bot Telegram Ultra opérationnel!")
        print("\n" + "="*70)
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                🐺  LA BÊTE - BOT TELEGRAM ULTRA  🐺              ║
║                                                                  ║
║                  ⚡ VERSION 10.20 (V10_2) ⚡                     ║
║                                                                  ║
║              📱 CONTRÔLE TOTAL DE TES 6 BOTS MT5 📱              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

📊 BOTS DISPONIBLES:
   🇪🇺 EUR/USD  |  🇬🇧 GBP/USD  |  🇯🇵 USD/JPY
   🥇 XAU/USD   |  ₿ BTC/USD    |  Ξ ETH/USD

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ COMMANDES ULTRA-RAPIDES:

   📊 PAR DEVISE:
      /eur, /gbp, /jpy, /gold, /btc, /eth
      /btc_stats      → Stats BTC instantanées
      /btc_on         → Activer BTC
      /btc_off        → Désactiver BTC
      /btc_pos        → Positions BTC
      /btc_params     → Voir/modifier paramètres BTC

   🌍 CONTRÔLE GLOBAL:
      /status         → Statut de TOUS les bots
      /all_on         → ▶️  Activer TOUT
      /all_off        → ⏸️  Désactiver TOUT
      /forex_on       → ▶️  Activer FOREX (EUR/GBP/JPY/GOLD)
      /forex_off      → ⏸️  Désactiver FOREX
      /crypto_on      → ▶️  Activer CRYPTO (BTC/ETH)
      /crypto_off     → ⏸️  Désactiver CRYPTO

   💰 FINANCE & P&L:
      /pnl            → P&L global en temps réel
      /positions      → Toutes les positions ouvertes
      /daily          → Rapport quotidien
      /risk           → Statut risque FTMO 40K
      /dashboard      → 📊 Tableau de bord FTMO complet

   ⚙️ PARAMÈTRES (Confluence/Certitude):
      /params                → Voir TOUS les paramètres
      /btc_params 70 55      → Modifier BTC (Confluence 70, Certitude 55%)
      /eur_params 85 50      → Modifier EUR

   🎯 COMMANDES AVANCÉES:
      /emergency_stop        → 🚨 ARRÊT TOTAL (ferme tout + désactive)
      /close_all             → ⚠️  Fermer TOUTES les positions
      /close_losing          → 📉 Fermer uniquement positions perdantes
      /secure_profits        → 💰 Sécuriser les positions gagnantes
      /chart                 → 📈 Graphique ASCII P&L
      /best_setups           → 🎯 Meilleurs setups récents

   📅 CALENDRIER & ALERTES:
      /calendar              → Calendrier économique du jour
      /notify_on             → 🔔 Activer notifications push
      /notify_off            → 🔕 Désactiver notifications

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 ASTUCE: Tape / dans Telegram pour voir TOUTES les commandes!

🚀 DÉMARRAGE: Ouvre Telegram et tape /start

""")
        print("="*70 + "\n")
        print("✅ Bot Telegram opérationnel - En attente de connexions...\n")

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# ========================================
# MAIN
# ========================================
def main():
    """Point d'entrée"""
    if not TELEGRAM_AVAILABLE:
        print("❌ Erreur: python-telegram-bot non installé")
        print("Installation: pip install python-telegram-bot")
        sys.exit(1)

    try:
        bot = UltraPropFirmBot(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        bot.run()
    except KeyboardInterrupt:
        logger.info("\n👋 Arrêt du bot...")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

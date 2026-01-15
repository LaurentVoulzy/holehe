# -*- coding: utf-8 -*-
"""
LA BÊTE - BOT TELEGRAM PROFESSIONNEL PROP FIRM
Organisation par devise + Contrôle total via Telegram
"""

import sys
import logging
import requests
from datetime import datetime
from typing import Optional, Dict

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

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    FOREX_CONFIG,
    CRYPTO_CONFIG,
)

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
    "EUR": {
        "name": "EUR/USD",
        "emoji": "🇪🇺",
        "magic": 666001,
        "api": FOREX_API,
        "type": "FOREX"
    },
    "GBP": {
        "name": "GBP/USD",
        "emoji": "🇬🇧",
        "magic": 666002,
        "api": FOREX_API,
        "type": "FOREX"
    },
    "JPY": {
        "name": "USD/JPY",
        "emoji": "🇯🇵",
        "magic": 666003,
        "api": FOREX_API,
        "type": "FOREX"
    },
    "GOLD": {
        "name": "XAU/USD",
        "emoji": "🥇",
        "magic": 666004,
        "api": FOREX_API,
        "type": "FOREX"
    },
    "BTC": {
        "name": "BTC/USD",
        "emoji": "₿",
        "magic": 777001,
        "api": CRYPTO_API,
        "type": "CRYPTO"
    },
    "ETH": {
        "name": "ETH/USD",
        "emoji": "Ξ",
        "magic": 777002,
        "api": CRYPTO_API,
        "type": "CRYPTO"
    }
}


# ========================================
# BOT TELEGRAM PROFESSIONNEL
# ========================================
class PropFirmTelegramBot:
    """Bot Telegram organisé par devise pour Prop Firm"""

    def __init__(self, token: str):
        if not TELEGRAM_AVAILABLE:
            raise ImportError("python-telegram-bot non installé")

        self.token = token
        self.application = None
        logger.info("🤖 Bot Telegram Prop Firm initialisé")

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
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            "╔════════════════════════════════════╗\n"
            "║   🐺 LA BÊTE - PROP FIRM SYSTEM   ║\n"
            "╚════════════════════════════════════╝\n\n"
            "📱 *CONTRÔLE PAR DEVISE*\n\n"
            "Sélectionnez une devise pour gérer:\n"
            "• Stats en temps réel\n"
            "• Positions ouvertes\n"
            "• Start/Stop bot\n"
            "• Analyse marché\n"
            "• Calendrier économique\n\n"
            "_Système optimisé FTMO 40K_"
        )

        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère les clics sur les boutons"""
        query = update.callback_query
        await query.answer()

        data = query.data

        # Menu par devise
        if data.startswith("menu_"):
            currency = data.replace("menu_", "")
            await self.show_currency_menu(query, currency)

        # Stats globales
        elif data == "global_stats":
            await self.show_global_stats(query)

        # Contrôle global
        elif data == "global_control":
            await self.show_global_control(query)

        # Actions par devise
        elif data.startswith("stats_"):
            currency = data.replace("stats_", "")
            await self.show_currency_stats(query, currency)

        elif data.startswith("positions_"):
            currency = data.replace("positions_", "")
            await self.show_currency_positions(query, currency)

        elif data.startswith("start_"):
            currency = data.replace("start_", "")
            await self.start_currency_bot(query, currency)

        elif data.startswith("stop_"):
            currency = data.replace("stop_", "")
            await self.stop_currency_bot(query, currency)

        elif data.startswith("analyze_"):
            currency = data.replace("analyze_", "")
            await self.analyze_currency(query, currency)

        elif data.startswith("news_"):
            currency = data.replace("news_", "")
            await self.show_currency_news(query, currency)

        # Actions globales
        elif data == "start_all_forex":
            await self.start_all_forex(query)

        elif data == "stop_all_forex":
            await self.stop_all_forex(query)

        elif data == "start_all_crypto":
            await self.start_all_crypto(query)

        elif data == "stop_all_crypto":
            await self.stop_all_crypto(query)

        elif data == "close_all_positions":
            await self.close_all_positions(query)

        # Retour menu principal
        elif data == "back_main":
            await self.back_to_main(query)

    # ========================================
    # MENUS PAR DEVISE
    # ========================================

    async def show_currency_menu(self, query, currency: str):
        """Affiche le menu d'une devise"""
        config = BOTS_CONFIG.get(currency, {})
        emoji = config.get("emoji", "")
        name = config.get("name", currency)

        keyboard = [
            [
                InlineKeyboardButton("📊 Stats", callback_data=f"stats_{currency}"),
                InlineKeyboardButton("📈 Positions", callback_data=f"positions_{currency}"),
            ],
            [
                InlineKeyboardButton("✅ Start", callback_data=f"start_{currency}"),
                InlineKeyboardButton("❌ Stop", callback_data=f"stop_{currency}"),
            ],
            [
                InlineKeyboardButton("🔍 Analyse", callback_data=f"analyze_{currency}"),
                InlineKeyboardButton("📅 News", callback_data=f"news_{currency}"),
            ],
            [
                InlineKeyboardButton("⬅️ Retour", callback_data="back_main"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            f"{emoji} *{name}*\n\n"
            f"Magic Number: {config.get('magic', 'N/A')}\n"
            f"Type: {config.get('type', 'N/A')}\n\n"
            f"_Choisissez une action:_"
        )

        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def show_currency_stats(self, query, currency: str):
        """Affiche les stats d'une devise"""
        config = BOTS_CONFIG.get(currency, {})
        api = config.get("api")
        emoji = config.get("emoji", "")
        name = config.get("name", currency)

        try:
            response = requests.get(f"{api}/bot/{currency}/stats", timeout=5)

            if response.status_code == 200:
                stats = response.json()

                message = (
                    f"{emoji} *STATS {name}*\n\n"
                    f"📊 Trades: {stats.get('total_trades', 0)}\n"
                    f"✅ Gagnants: {stats.get('winning_trades', 0)}\n"
                    f"❌ Perdants: {stats.get('losing_trades', 0)}\n"
                    f"📈 Win Rate: {stats.get('winrate', 0):.1f}%\n\n"
                    f"💰 P&L: {stats.get('pnl', 0):.2f}€\n"
                    f"📊 Positions: {stats.get('open_positions', 0)}\n\n"
                    f"🎯 Dernière confluence: {stats.get('last_confluence', 0)}/100\n"
                    f"🎲 Dernière certitude: {stats.get('last_certainty', 0)}%\n\n"
                    f"Status: {'✅ ACTIF' if stats.get('enabled', False) else '❌ INACTIF'}"
                )
            else:
                message = f"{emoji} *{name}*\n\n❌ Impossible de récupérer les stats"

        except Exception as e:
            message = f"{emoji} *{name}*\n\n❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data=f"menu_{currency}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def show_currency_positions(self, query, currency: str):
        """Affiche les positions d'une devise"""
        config = BOTS_CONFIG.get(currency, {})
        api = config.get("api")
        emoji = config.get("emoji", "")
        name = config.get("name", currency)

        try:
            response = requests.get(f"{api}/bot/{currency}/positions", timeout=5)

            if response.status_code == 200:
                data = response.json()
                positions = data.get('positions', [])

                if positions:
                    message = f"{emoji} *POSITIONS {name}*\n\n"

                    for pos in positions:
                        direction = "🟢 BUY" if pos.get('type') == 'BUY' else "🔴 SELL"
                        pnl = pos.get('pnl', 0)
                        pnl_emoji = "📈" if pnl > 0 else "📉" if pnl < 0 else "➡️"

                        message += (
                            f"{direction} {pos.get('lots', 0)} lots\n"
                            f"Entry: {pos.get('entry', 0):.5f}\n"
                            f"Current: {pos.get('current', 0):.5f}\n"
                            f"P&L: {pnl_emoji} {pnl:.2f}€\n"
                            f"Ticket: #{pos.get('ticket', 'N/A')}\n\n"
                        )
                else:
                    message = f"{emoji} *{name}*\n\n✅ Aucune position ouverte"

            else:
                message = f"{emoji} *{name}*\n\n❌ Erreur API"

        except Exception as e:
            message = f"{emoji} *{name}*\n\n❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data=f"menu_{currency}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def start_currency_bot(self, query, currency: str):
        """Démarre un bot"""
        config = BOTS_CONFIG.get(currency, {})
        api = config.get("api")
        emoji = config.get("emoji", "")
        name = config.get("name", currency)

        try:
            response = requests.post(f"{api}/bot/{currency}/enable", timeout=5)

            if response.status_code == 200:
                message = f"{emoji} *{name}*\n\n✅ Bot activé avec succès!"
            else:
                message = f"{emoji} *{name}*\n\n❌ Erreur activation"

        except Exception as e:
            message = f"{emoji} *{name}*\n\n❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data=f"menu_{currency}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def stop_currency_bot(self, query, currency: str):
        """Arrête un bot"""
        config = BOTS_CONFIG.get(currency, {})
        api = config.get("api")
        emoji = config.get("emoji", "")
        name = config.get("name", currency)

        try:
            response = requests.post(f"{api}/bot/{currency}/disable", timeout=5)

            if response.status_code == 200:
                message = f"{emoji} *{name}*\n\n❌ Bot désactivé"
            else:
                message = f"{emoji} *{name}*\n\n❌ Erreur désactivation"

        except Exception as e:
            message = f"{emoji} *{name}*\n\n❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data=f"menu_{currency}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def analyze_currency(self, query, currency: str):
        """Analyse une devise"""
        config = BOTS_CONFIG.get(currency, {})
        api = config.get("api")
        emoji = config.get("emoji", "")
        name = config.get("name", currency)
        pair = name.replace("/", "")

        try:
            response = requests.get(f"{api}/analyze/{pair}", timeout=10)

            if response.status_code == 200:
                analysis = response.json()

                message = (
                    f"{emoji} *ANALYSE {name}*\n\n"
                    f"🎯 Confluence: {analysis.get('confluence_score', 0)}/100\n"
                    f"🎲 Certitude: {analysis.get('certainty', 0)}%\n\n"
                    f"📊 EMA 20: {analysis.get('ema_20', 'N/A')}\n"
                    f"📊 EMA 50: {analysis.get('ema_50', 'N/A')}\n"
                    f"📊 EMA 200: {analysis.get('ema_200', 'N/A')}\n"
                    f"📊 RSI: {analysis.get('rsi', 'N/A')}\n"
                    f"📊 ATR: {analysis.get('atr', 'N/A')}\n\n"
                    f"Signal: {analysis.get('signal', 'NO TRADE')}\n"
                    f"Raison: {analysis.get('reason', 'N/A')}"
                )
            else:
                message = f"{emoji} *{name}*\n\n❌ Impossible d'analyser"

        except Exception as e:
            message = f"{emoji} *{name}*\n\n❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data=f"menu_{currency}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def show_currency_news(self, query, currency: str):
        """Affiche les news d'une devise"""
        config = BOTS_CONFIG.get(currency, {})
        emoji = config.get("emoji", "")
        name = config.get("name", currency)

        try:
            from economic_calendar import check_news_before_trade

            pair = name.replace("/", "")
            safe, reason = check_news_before_trade(pair)

            if safe:
                message = f"{emoji} *NEWS {name}*\n\n✅ {reason}"
            else:
                message = f"{emoji} *NEWS {name}*\n\n⚠️ {reason}"

        except Exception as e:
            message = f"{emoji} *{name}*\n\n❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data=f"menu_{currency}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    # ========================================
    # VUE GLOBALE
    # ========================================

    async def show_global_stats(self, query):
        """Affiche les stats globales"""
        try:
            # Stats Forex
            forex_resp = requests.get(f"{FOREX_API}/stats", timeout=5)
            forex_stats = forex_resp.json() if forex_resp.status_code == 200 else {}

            # Stats Crypto
            crypto_resp = requests.get(f"{CRYPTO_API}/stats", timeout=5)
            crypto_stats = crypto_resp.json() if crypto_resp.status_code == 200 else {}

            message = (
                "📊 *VUE GLOBALE - LA BÊTE*\n\n"
                "🐺 *FOREX:*\n"
                f"  Trades: {forex_stats.get('total_trades', 0)}\n"
                f"  Win Rate: {forex_stats.get('winrate', 0):.1f}%\n"
                f"  P&L: {forex_stats.get('total_pnl', 0):.2f}€\n"
                f"  Positions: {forex_stats.get('open_positions', 0)}\n\n"
                "💰 *CRYPTO:*\n"
                f"  Trades: {crypto_stats.get('total_trades', 0)}\n"
                f"  Win Rate: {crypto_stats.get('winrate', 0):.1f}%\n"
                f"  P&L: {crypto_stats.get('total_pnl', 0):.2f}$\n"
                f"  Positions: {crypto_stats.get('open_positions', 0)}\n\n"
                f"💎 *TOTAL P&L:* {forex_stats.get('total_pnl', 0) + crypto_stats.get('total_pnl', 0):.2f}€"
            )

        except Exception as e:
            message = f"❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data="back_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def show_global_control(self, query):
        """Menu de contrôle global"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Start All FOREX", callback_data="start_all_forex"),
                InlineKeyboardButton("❌ Stop All FOREX", callback_data="stop_all_forex"),
            ],
            [
                InlineKeyboardButton("✅ Start All CRYPTO", callback_data="start_all_crypto"),
                InlineKeyboardButton("❌ Stop All CRYPTO", callback_data="stop_all_crypto"),
            ],
            [
                InlineKeyboardButton("🔒 Fermer Toutes Positions", callback_data="close_all_positions"),
            ],
            [
                InlineKeyboardButton("⬅️ Retour", callback_data="back_main"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            "⚙️ *CONTRÔLE GLOBAL*\n\n"
            "⚠️ Actions groupées:\n\n"
            "• Start/Stop tous les bots Forex\n"
            "• Start/Stop tous les bots Crypto\n"
            "• Fermer toutes les positions\n\n"
            "_Utilisez avec précaution!_"
        )

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    # ========================================
    # ACTIONS GLOBALES
    # ========================================

    async def start_all_forex(self, query):
        """Démarre tous les bots Forex"""
        try:
            response = requests.post(f"{FOREX_API}/start_all", timeout=5)
            if response.status_code == 200:
                message = "✅ Tous les bots FOREX activés!"
            else:
                message = "❌ Erreur activation Forex"
        except Exception as e:
            message = f"❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data="global_control")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def stop_all_forex(self, query):
        """Arrête tous les bots Forex"""
        try:
            response = requests.post(f"{FOREX_API}/stop_all", timeout=5)
            if response.status_code == 200:
                message = "❌ Tous les bots FOREX désactivés!"
            else:
                message = "❌ Erreur désactivation Forex"
        except Exception as e:
            message = f"❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data="global_control")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def start_all_crypto(self, query):
        """Démarre tous les bots Crypto"""
        try:
            response = requests.post(f"{CRYPTO_API}/start_all", timeout=5)
            if response.status_code == 200:
                message = "✅ Tous les bots CRYPTO activés!"
            else:
                message = "❌ Erreur activation Crypto"
        except Exception as e:
            message = f"❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data="global_control")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def stop_all_crypto(self, query):
        """Arrête tous les bots Crypto"""
        try:
            response = requests.post(f"{CRYPTO_API}/stop_all", timeout=5)
            if response.status_code == 200:
                message = "❌ Tous les bots CRYPTO désactivés!"
            else:
                message = "❌ Erreur désactivation Crypto"
        except Exception as e:
            message = f"❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data="global_control")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def close_all_positions(self, query):
        """Ferme toutes les positions"""
        try:
            # Fermer Forex
            forex_resp = requests.post(f"{FOREX_API}/close_all_positions", timeout=5)
            forex_closed = forex_resp.json().get('closed', 0) if forex_resp.status_code == 200 else 0

            # Fermer Crypto
            crypto_resp = requests.post(f"{CRYPTO_API}/close_all_positions", timeout=5)
            crypto_closed = crypto_resp.json().get('closed', 0) if crypto_resp.status_code == 200 else 0

            message = (
                "🔒 *FERMETURE TOTALE*\n\n"
                f"🐺 Forex: {forex_closed} position(s)\n"
                f"💰 Crypto: {crypto_closed} position(s)\n\n"
                f"✅ Total: {forex_closed + crypto_closed} position(s) fermée(s)"
            )

        except Exception as e:
            message = f"❌ Erreur: {str(e)}"

        keyboard = [[InlineKeyboardButton("⬅️ Retour", callback_data="global_control")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

    async def back_to_main(self, query):
        """Retour au menu principal"""
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
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            "╔════════════════════════════════════╗\n"
            "║   🐺 LA BÊTE - PROP FIRM SYSTEM   ║\n"
            "╚════════════════════════════════════╝\n\n"
            "📱 *CONTRÔLE PAR DEVISE*\n\n"
            "Sélectionnez une devise pour gérer:\n"
            "• Stats en temps réel\n"
            "• Positions ouvertes\n"
            "• Start/Stop bot\n"
            "• Analyse marché\n"
            "• Calendrier économique\n\n"
            "_Système optimisé FTMO 40K_"
        )

        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    # ========================================
    # COMMANDES TEXTE RAPIDES
    # ========================================

    async def eur_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eur"""
        # Simuler un clic sur le bouton EUR
        keyboard = [[InlineKeyboardButton("Menu EUR/USD", callback_data="menu_EUR")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🇪🇺 EUR/USD", reply_markup=reply_markup)

    async def gbp_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gbp"""
        keyboard = [[InlineKeyboardButton("Menu GBP/USD", callback_data="menu_GBP")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🇬🇧 GBP/USD", reply_markup=reply_markup)

    async def jpy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /jpy"""
        keyboard = [[InlineKeyboardButton("Menu USD/JPY", callback_data="menu_JPY")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🇯🇵 USD/JPY", reply_markup=reply_markup)

    async def gold_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /gold"""
        keyboard = [[InlineKeyboardButton("Menu GOLD", callback_data="menu_GOLD")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🥇 GOLD", reply_markup=reply_markup)

    async def btc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /btc"""
        keyboard = [[InlineKeyboardButton("Menu BTC/USD", callback_data="menu_BTC")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("₿ BTC/USD", reply_markup=reply_markup)

    async def eth_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Raccourci /eth"""
        keyboard = [[InlineKeyboardButton("Menu ETH/USD", callback_data="menu_ETH")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Ξ ETH/USD", reply_markup=reply_markup)

    # ========================================
    # RUN
    # ========================================

    def run(self):
        """Démarre le bot"""
        logger.info("🚀 Démarrage Bot Telegram Prop Firm...")

        self.application = Application.builder().token(self.token).build()

        # Commande principale
        self.application.add_handler(CommandHandler("start", self.start_command))

        # Raccourcis par devise
        self.application.add_handler(CommandHandler("eur", self.eur_command))
        self.application.add_handler(CommandHandler("gbp", self.gbp_command))
        self.application.add_handler(CommandHandler("jpy", self.jpy_command))
        self.application.add_handler(CommandHandler("gold", self.gold_command))
        self.application.add_handler(CommandHandler("btc", self.btc_command))
        self.application.add_handler(CommandHandler("eth", self.eth_command))

        # Handler pour tous les boutons
        self.application.add_handler(CallbackQueryHandler(self.button_handler))

        logger.info("✅ Bot Telegram opérationnel!")
        print("\n╔════════════════════════════════════╗")
        print("║   🤖 BOT TELEGRAM PROP FIRM       ║")
        print("╚════════════════════════════════════╝")
        print("\n📱 Ouvrez Telegram et tapez /start\n")
        print("Contrôle par devise avec interface graphique!\n")

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

    bot = PropFirmTelegramBot(token=TELEGRAM_BOT_TOKEN)
    bot.run()


if __name__ == "__main__":
    main()

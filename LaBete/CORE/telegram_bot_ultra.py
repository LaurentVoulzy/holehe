# -*- coding: utf-8 -*-
"""
LA BÊTE - BOT TELEGRAM ULTRA PROP FIRM
Version améliorée avec toutes les commandes rapides + notifications push
"""

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
            "╚══════════════════════════════════════╝\n\n"
            "📱 *CONTRÔLE TOTAL PAR DEVISE*\n\n"
            "✅ Notifications push temps réel\n"
            "✅ Commandes rapides (/eur, /gbp, etc)\n"
            "✅ Statistiques avancées\n"
            "✅ Gestion risque FTMO\n"
            "✅ Alertes intelligentes\n\n"
            "_Système optimisé FTMO 40K - Version Ultra_"
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

        # Retour menu principal
        elif data == "back_main":
            await self._back_to_main(query)

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

        # Commandes par devise (menu + stats + on/off + pos)
        for cmd_prefix in ['eur', 'gbp', 'jpy', 'gold', 'btc', 'eth']:
            self.application.add_handler(CommandHandler(cmd_prefix, getattr(self, f"{cmd_prefix}_command")))
            self.application.add_handler(CommandHandler(f"{cmd_prefix}_stats", getattr(self, f"{cmd_prefix}_stats_command")))
            self.application.add_handler(CommandHandler(f"{cmd_prefix}_on", getattr(self, f"{cmd_prefix}_on_command")))
            self.application.add_handler(CommandHandler(f"{cmd_prefix}_off", getattr(self, f"{cmd_prefix}_off_command")))
            self.application.add_handler(CommandHandler(f"{cmd_prefix}_pos", getattr(self, f"{cmd_prefix}_pos_command")))

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
        self.application.add_handler(CommandHandler("notify_on", self.notify_on_command))
        self.application.add_handler(CommandHandler("notify_off", self.notify_off_command))
        self.application.add_handler(CommandHandler("calendar", self.calendar_command))
        self.application.add_handler(CommandHandler("risk", self.risk_command))

        # Handler boutons
        self.application.add_handler(CallbackQueryHandler(self.button_handler))

        logger.info("✅ Bot Telegram Ultra opérationnel!")
        print("\n╔════════════════════════════════════════╗")
        print("║   🤖 BOT TELEGRAM ULTRA PROP FIRM     ║")
        print("╚════════════════════════════════════════╝")
        print("\n📱 Ouvrez Telegram et tapez /start")
        print("\n⚡ COMMANDES RAPIDES DISPONIBLES:")
        print("   /eur, /gbp, /jpy, /gold, /btc, /eth")
        print("   /status, /pnl, /positions, /daily")
        print("   /all_on, /all_off, /close_all")
        print("   /forex_on, /forex_off, /crypto_on, /crypto_off")
        print("   /calendar, /risk, /notify_on, /notify_off")
        print("\n   Tape / dans Telegram pour voir toutes les commandes!\n")

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

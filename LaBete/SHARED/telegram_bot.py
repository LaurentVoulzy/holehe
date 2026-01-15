# -*- coding: utf-8 -*-
"""
LA BÊTE - Bot Telegram Dual Control
Contrôle centralisé des systèmes Forex + Crypto
Python 3.12+ Compatible
"""

import sys
import logging
from pathlib import Path
import requests
from datetime import datetime
from typing import Optional

try:
    from telegram import Update
    from telegram.ext import (
        Application,
        CommandHandler,
        ContextTypes,
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("❌ python-telegram-bot non installé. Installez avec: pip install python-telegram-bot")

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    FOREX_CONFIG,
    CRYPTO_CONFIG,
    WELCOME_MESSAGE,
)

# ========================================
# CONFIGURATION LOGGING
# ========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# ========================================
# URLS APIs Guardian
# ========================================
FOREX_API = FOREX_CONFIG['guardian_api_url']
CRYPTO_API = CRYPTO_CONFIG['guardian_api_url']


# ========================================
# BOT TELEGRAM CLASS
# ========================================
class LaBeteBot:
    """Bot Telegram pour contrôler La Bête (Forex + Crypto)"""

    def __init__(self, token: str):
        if not TELEGRAM_AVAILABLE:
            raise ImportError("python-telegram-bot non installé")

        self.token = token
        self.application = None

        logger.info("🤖 Bot Telegram La Bête initialisé")

    # ----------------------------------------
    # COMMANDES - GÉNÉRAL
    # ----------------------------------------

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start"""
        await update.message.reply_text(
            WELCOME_MESSAGE +
            "\n\n📱 *COMMANDES DISPONIBLES:*\n\n"
            "*FOREX:*\n"
            "/forex_stats - Stats Forex\n"
            "/forex_positions - Positions ouvertes Forex\n"
            "/forex_stop - Arrêt bot Forex\n"
            "/forex_start - Démarrage bot Forex\n"
            "/forex_today - Résumé journée Forex\n\n"
            "*CRYPTO:*\n"
            "/crypto_stats - Stats Crypto\n"
            "/crypto_positions - Positions ouvertes Crypto\n"
            "/crypto_stop - Arrêt bot Crypto\n"
            "/crypto_start - Démarrage bot Crypto\n"
            "/crypto_today - Résumé journée Crypto\n\n"
            "*GLOBAL:*\n"
            "/stats - Stats des 2 systèmes\n"
            "/stopall - Arrêt total\n"
            "/startall - Démarrage total\n"
            "/report - Rapport complet\n"
            "/risk - Niveau risque global\n"
            "/closeall - Ferme toutes positions\n\n"
            "*ANALYSE:*\n"
            "/analyze EURUSD - Analyse détaillée d'une paire\n"
            "/market_report - Rapport marché complet\n"
            "/why_no_trade - Pourquoi aucun trade pris\n",
            parse_mode='Markdown'
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /help"""
        await update.message.reply_text(
            "📖 *AIDE - LA BÊTE*\n\n"
            "Utilisez /start pour voir toutes les commandes disponibles.\n\n"
            "Le système surveille automatiquement vos trades et vous alerte en cas de:\n"
            "• Signal détecté\n"
            "• Position ouverte/fermée\n"
            "• TP/SL atteint\n"
            "• Limite de risque approchée\n"
            "• News économique proche\n"
            "• Kill Switch activé\n\n"
            "Rapport quotidien automatique à 18h.\n"
            "Rapport hebdomadaire le vendredi.\n",
            parse_mode='Markdown'
        )

    # ----------------------------------------
    # COMMANDES - FOREX
    # ----------------------------------------

    async def forex_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stats Forex"""
        try:
            response = requests.get(f"{FOREX_API}/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                message = self._format_stats(stats, "FOREX")
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Impossible de récupérer les stats Forex")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def forex_positions_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Positions ouvertes Forex"""
        try:
            response = requests.get(f"{FOREX_API}/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                message = f"📊 *POSITIONS OUVERTES - FOREX*\n\n"
                message += f"Positions: {stats.get('open_positions', 0)}\n"
                # TODO: Détailler les positions
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Erreur API Forex")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def forex_stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Arrêter le bot Forex"""
        try:
            response = requests.post(f"{FOREX_API}/kill_switch/activate", timeout=5)
            if response.status_code == 200:
                await update.message.reply_text("✅ Bot Forex arrêté (Kill Switch activé)")
            else:
                await update.message.reply_text("❌ Erreur arrêt bot Forex")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def forex_start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Démarrer le bot Forex"""
        try:
            response = requests.post(f"{FOREX_API}/kill_switch/deactivate", timeout=5)
            if response.status_code == 200:
                await update.message.reply_text("✅ Bot Forex démarré")
            else:
                await update.message.reply_text("❌ Erreur démarrage bot Forex")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def forex_today_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Résumé journée Forex"""
        try:
            response = requests.get(f"{FOREX_API}/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                message = self._format_daily_summary(stats, "FOREX")
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Erreur récupération stats")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    # ----------------------------------------
    # COMMANDES - CRYPTO
    # ----------------------------------------

    async def crypto_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stats Crypto"""
        try:
            response = requests.get(f"{CRYPTO_API}/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                message = self._format_stats(stats, "CRYPTO")
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Impossible de récupérer les stats Crypto")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def crypto_positions_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Positions ouvertes Crypto"""
        try:
            response = requests.get(f"{CRYPTO_API}/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                message = f"💰 *POSITIONS OUVERTES - CRYPTO*\n\n"
                message += f"Positions: {stats.get('open_positions', 0)}\n"
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Erreur API Crypto")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def crypto_stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Arrêter le bot Crypto"""
        try:
            response = requests.post(f"{CRYPTO_API}/kill_switch/activate", timeout=5)
            if response.status_code == 200:
                await update.message.reply_text("✅ Bot Crypto arrêté (Kill Switch activé)")
            else:
                await update.message.reply_text("❌ Erreur arrêt bot Crypto")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def crypto_start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Démarrer le bot Crypto"""
        try:
            response = requests.post(f"{CRYPTO_API}/kill_switch/deactivate", timeout=5)
            if response.status_code == 200:
                await update.message.reply_text("✅ Bot Crypto démarré")
            else:
                await update.message.reply_text("❌ Erreur démarrage bot Crypto")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def crypto_today_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Résumé journée Crypto"""
        try:
            response = requests.get(f"{CRYPTO_API}/stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                message = self._format_daily_summary(stats, "CRYPTO")
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Erreur récupération stats")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    # ----------------------------------------
    # COMMANDES - GLOBAL
    # ----------------------------------------

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stats globales Forex + Crypto"""
        try:
            # Récupérer stats Forex
            forex_response = requests.get(f"{FOREX_API}/stats", timeout=5)
            forex_stats = forex_response.json() if forex_response.status_code == 200 else {}

            # Récupérer stats Crypto
            crypto_response = requests.get(f"{CRYPTO_API}/stats", timeout=5)
            crypto_stats = crypto_response.json() if crypto_response.status_code == 200 else {}

            # Formatter message
            message = "📊 *STATISTIQUES GLOBALES - LA BÊTE*\n\n"

            # Forex
            message += "🐺 *FOREX:*\n"
            message += f"  Trades: {forex_stats.get('total_trades', 0)}\n"
            message += f"  P&L: {forex_stats.get('total_pnl', 0):.2f}€\n"
            message += f"  Win Rate: {self._calculate_winrate(forex_stats):.1f}%\n"
            message += f"  Positions: {forex_stats.get('open_positions', 0)}\n\n"

            # Crypto
            message += "💰 *CRYPTO:*\n"
            message += f"  Trades: {crypto_stats.get('total_trades', 0)}\n"
            message += f"  P&L: {crypto_stats.get('total_pnl', 0):.2f}$\n"
            message += f"  Win Rate: {self._calculate_winrate(crypto_stats):.1f}%\n"
            message += f"  Positions: {crypto_stats.get('open_positions', 0)}\n\n"

            # Total
            total_pnl = forex_stats.get('total_pnl', 0) + crypto_stats.get('total_pnl', 0)
            message += f"💎 *TOTAL P&L:* {total_pnl:.2f}€\n"

            await update.message.reply_text(message, parse_mode='Markdown')

        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def stopall_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Arrêter tout"""
        try:
            # Arrêter Forex
            requests.post(f"{FOREX_API}/kill_switch/activate", timeout=5)
            # Arrêter Crypto
            requests.post(f"{CRYPTO_API}/kill_switch/activate", timeout=5)

            await update.message.reply_text("🛑 *TOUS LES SYSTÈMES ARRÊTÉS*", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def startall_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Démarrer tout"""
        try:
            # Démarrer Forex
            requests.post(f"{FOREX_API}/kill_switch/deactivate", timeout=5)
            # Démarrer Crypto
            requests.post(f"{CRYPTO_API}/kill_switch/deactivate", timeout=5)

            await update.message.reply_text("✅ *TOUS LES SYSTÈMES DÉMARRÉS*", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Rapport complet"""
        # Appeler stats
        await self.stats_command(update, context)

    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Niveau de risque"""
        try:
            forex_response = requests.get(f"{FOREX_API}/stats", timeout=5)
            forex_stats = forex_response.json() if forex_response.status_code == 200 else {}

            crypto_response = requests.get(f"{CRYPTO_API}/stats", timeout=5)
            crypto_stats = crypto_response.json() if crypto_response.status_code == 200 else {}

            message = "⚠️ *ANALYSE DU RISQUE*\n\n"

            # Forex
            forex_risk = self._assess_risk(forex_stats, FOREX_CONFIG)
            message += f"🐺 Forex: {forex_risk}\n"

            # Crypto
            crypto_risk = self._assess_risk(crypto_stats, CRYPTO_CONFIG)
            message += f"💰 Crypto: {crypto_risk}\n"

            await update.message.reply_text(message, parse_mode='Markdown')

        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    # ----------------------------------------
    # HELPERS
    # ----------------------------------------

    def _format_stats(self, stats: dict, system: str) -> str:
        """Formate les stats pour affichage"""
        emoji = "🐺" if system == "FOREX" else "💰"
        currency = "€" if system == "FOREX" else "$"

        message = f"{emoji} *STATS {system}*\n\n"
        message += f"Date: {stats.get('date', 'N/A')}\n"
        message += f"Trades: {stats.get('total_trades', 0)}\n"
        message += f"Gagnants: {stats.get('winning_trades', 0)}\n"
        message += f"Perdants: {stats.get('losing_trades', 0)}\n"
        message += f"Win Rate: {self._calculate_winrate(stats):.1f}%\n"
        message += f"P&L: {stats.get('total_pnl', 0):.2f}{currency}\n"
        message += f"Positions ouvertes: {stats.get('open_positions', 0)}\n"

        if stats.get('kill_switch_active'):
            message += "\n🚨 *KILL SWITCH ACTIF*"

        return message

    def _format_daily_summary(self, stats: dict, system: str) -> str:
        """Résumé quotidien"""
        emoji = "🐺" if system == "FOREX" else "💰"

        message = f"{emoji} *RÉSUMÉ {system} - {stats.get('date')}*\n\n"
        message += f"Trades: {stats.get('total_trades', 0)}\n"
        message += f"✅ Gagnants: {stats.get('winning_trades', 0)}\n"
        message += f"❌ Perdants: {stats.get('losing_trades', 0)}\n"
        message += f"Win Rate: {self._calculate_winrate(stats):.1f}%\n\n"

        pnl = stats.get('total_pnl', 0)
        if pnl > 0:
            message += f"📈 Profit: +{pnl:.2f}\n"
        elif pnl < 0:
            message += f"📉 Perte: {pnl:.2f}\n"
        else:
            message += f"➡️ Breakeven\n"

        return message

    def _calculate_winrate(self, stats: dict) -> float:
        """Calcule le win rate"""
        total = stats.get('total_trades', 0)
        if total == 0:
            return 0.0
        winning = stats.get('winning_trades', 0)
        return (winning / total) * 100

    def _assess_risk(self, stats: dict, config: dict) -> str:
        """Évalue le niveau de risque"""
        pnl = stats.get('total_pnl', 0)
        max_loss = config['kill_switch']['max_daily_loss']

        risk_percent = abs(pnl / max_loss * 100) if pnl < 0 else 0

        if stats.get('kill_switch_active'):
            return "🔴 CRITIQUE (Kill Switch actif)"
        elif risk_percent > 75:
            return "🟠 ÉLEVÉ (>75% limite)"
        elif risk_percent > 50:
            return "🟡 MOYEN (>50% limite)"
        else:
            return "🟢 FAIBLE"

    # ----------------------------------------
    # COMMANDES - ANALYSE
    # ----------------------------------------

    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Analyse détaillée d'une paire"""
        try:
            if not context.args:
                await update.message.reply_text(
                    "❌ Usage: /analyze <PAIR>\n"
                    "Exemples: /analyze EURUSD, /analyze BTCUSD"
                )
                return

            pair = context.args[0].upper()

            # Déterminer si c'est Forex ou Crypto
            forex_pairs = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
            crypto_pairs = ["BTCUSD", "ETHUSD"]

            if pair in forex_pairs:
                api_url = FOREX_API
                system = "FOREX"
            elif pair in crypto_pairs:
                api_url = CRYPTO_API
                system = "CRYPTO"
            else:
                await update.message.reply_text(f"❌ Paire non reconnue: {pair}")
                return

            # Demander l'analyse au Guardian
            response = requests.get(f"{api_url}/analyze/{pair}", timeout=10)

            if response.status_code == 200:
                analysis = response.json()
                message = self._format_analysis(analysis, pair, system)
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                await update.message.reply_text(f"❌ Impossible d'analyser {pair}")

        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def market_report_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Rapport marché complet"""
        try:
            # Récupérer les analyses de toutes les paires
            forex_response = requests.get(f"{FOREX_API}/market_report", timeout=10)
            crypto_response = requests.get(f"{CRYPTO_API}/market_report", timeout=10)

            message = "📊 *RAPPORT MARCHÉ COMPLET*\n\n"

            # Forex
            if forex_response.status_code == 200:
                forex_data = forex_response.json()
                message += "🐺 *FOREX:*\n"
                for pair_data in forex_data.get('pairs', []):
                    score = pair_data.get('confluence_score', 0)
                    emoji = "✅" if score >= 90 else "❌"
                    message += f"  {pair_data['pair']}: {score}/100 {emoji}\n"

                best = forex_data.get('best_opportunity')
                if best:
                    message += f"\n🎯 Meilleure: {best['pair']} ({best['score']}/100)\n"

                message += "\n"

            # Crypto
            if crypto_response.status_code == 200:
                crypto_data = crypto_response.json()
                message += "💰 *CRYPTO:*\n"
                for pair_data in crypto_data.get('pairs', []):
                    score = pair_data.get('confluence_score', 0)
                    emoji = "✅" if score >= 85 else "❌"
                    message += f"  {pair_data['pair']}: {score}/100 {emoji}\n"

            await update.message.reply_text(message, parse_mode='Markdown')

        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    async def why_no_trade_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Pourquoi aucun trade pris"""
        try:
            # Demander l'historique des signaux rejetés
            forex_response = requests.get(f"{FOREX_API}/rejected_signals", timeout=10)
            crypto_response = requests.get(f"{CRYPTO_API}/rejected_signals", timeout=10)

            message = "🤔 *POURQUOI AUCUN TRADE?*\n\n"

            # Forex
            if forex_response.status_code == 200:
                forex_data = forex_response.json()
                recent = forex_data.get('recent_rejections', [])

                if recent:
                    message += "🐺 *FOREX - Dernières analyses:*\n"
                    for rej in recent[:5]:  # Les 5 dernières
                        time_str = rej.get('time', 'N/A')
                        pair = rej.get('pair', 'N/A')
                        score = rej.get('score', 0)
                        reason = rej.get('reason', 'N/A')
                        message += f"  {time_str} {pair}: {score}/100\n"
                        message += f"    → {reason}\n"

                    stats = forex_data.get('stats', {})
                    message += f"\n📊 Stats 24h Forex:\n"
                    message += f"  Signaux analysés: {stats.get('analyzed', 0)}\n"
                    message += f"  Score moyen: {stats.get('avg_score', 0):.1f}/100\n"
                    message += f"  Meilleur: {stats.get('best_score', 0)}/100\n\n"

            # Crypto
            if crypto_response.status_code == 200:
                crypto_data = crypto_response.json()
                recent = crypto_data.get('recent_rejections', [])

                if recent:
                    message += "💰 *CRYPTO - Dernières analyses:*\n"
                    for rej in recent[:5]:
                        time_str = rej.get('time', 'N/A')
                        pair = rej.get('pair', 'N/A')
                        score = rej.get('score', 0)
                        reason = rej.get('reason', 'N/A')
                        message += f"  {time_str} {pair}: {score}/100\n"
                        message += f"    → {reason}\n"

            if len(message.split('\n')) <= 3:
                message += "Aucune analyse récente trouvée.\n"
                message += "Les bots sont peut-être en attente de configurations de marché favorables."

            await update.message.reply_text(message, parse_mode='Markdown')

        except Exception as e:
            await update.message.reply_text(f"❌ Erreur: {str(e)}")

    def _format_analysis(self, analysis: dict, pair: str, system: str) -> str:
        """Formate une analyse détaillée"""
        emoji = "🐺" if system == "FOREX" else "💰"

        message = f"{emoji} *ANALYSE {pair} M30*\n\n"

        # Indicateurs
        indicators = analysis.get('indicators', {})
        message += "🔍 *Indicateurs:*\n"
        message += f"  EMA 20: {indicators.get('ema_20', 'N/A')}\n"
        message += f"  EMA 50: {indicators.get('ema_50', 'N/A')}\n"
        message += f"  EMA 200: {indicators.get('ema_200', 'N/A')}\n"
        message += f"  RSI: {indicators.get('rsi', 'N/A')}\n"
        message += f"  MACD: {indicators.get('macd', 'N/A')}\n"
        message += f"  ATR: {indicators.get('atr', 'N/A')}\n\n"

        # Score de confluence
        score = analysis.get('confluence_score', 0)
        min_score = 90 if system == "FOREX" else 85
        emoji_result = "✅" if score >= min_score else "❌"

        message += f"🎯 *Score Confluence:* {score}/100 {emoji_result}\n"

        breakdown = analysis.get('score_breakdown', {})
        if breakdown:
            message += f"  Structure SMC: {breakdown.get('smc', 0)}/40\n"
            message += f"  Multi-TF: {breakdown.get('timeframe', 0)}/25\n"
            message += f"  Indicateurs: {breakdown.get('indicators', 0)}/20\n"
            message += f"  S/R: {breakdown.get('structure', 0)}/10\n"
            message += f"  Pattern: {breakdown.get('pattern', 0)}/5\n\n"

        # Décision
        decision = analysis.get('decision', 'NO_TRADE')
        if decision == 'BUY' or decision == 'SELL':
            message += f"✅ *SIGNAL {decision} DÉTECTÉ*\n"
        else:
            message += f"❌ *POSITION NON PRISE*\n"
            reason = analysis.get('rejection_reason', 'Score insuffisant')
            message += f"Raison: {reason}\n\n"

        # Détails
        details = analysis.get('details', {})
        if details:
            message += "*Détails:*\n"
            for key, value in details.items():
                emoji_check = "✅" if value else "❌"
                message += f"  {emoji_check} {key}\n"

        return message

    # ----------------------------------------
    # RUN
    # ----------------------------------------

    def run(self):
        """Démarre le bot"""
        logger.info("🚀 Démarrage du bot Telegram La Bête...")

        self.application = Application.builder().token(self.token).build()

        # Commandes générales
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

        # Commandes Forex
        self.application.add_handler(CommandHandler("forex_stats", self.forex_stats_command))
        self.application.add_handler(CommandHandler("forex_positions", self.forex_positions_command))
        self.application.add_handler(CommandHandler("forex_stop", self.forex_stop_command))
        self.application.add_handler(CommandHandler("forex_start", self.forex_start_command))
        self.application.add_handler(CommandHandler("forex_today", self.forex_today_command))

        # Commandes Crypto
        self.application.add_handler(CommandHandler("crypto_stats", self.crypto_stats_command))
        self.application.add_handler(CommandHandler("crypto_positions", self.crypto_positions_command))
        self.application.add_handler(CommandHandler("crypto_stop", self.crypto_stop_command))
        self.application.add_handler(CommandHandler("crypto_start", self.crypto_start_command))
        self.application.add_handler(CommandHandler("crypto_today", self.crypto_today_command))

        # Commandes globales
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("stopall", self.stopall_command))
        self.application.add_handler(CommandHandler("startall", self.startall_command))
        self.application.add_handler(CommandHandler("report", self.report_command))
        self.application.add_handler(CommandHandler("risk", self.risk_command))

        # Commandes d'analyse
        self.application.add_handler(CommandHandler("analyze", self.analyze_command))
        self.application.add_handler(CommandHandler("market_report", self.market_report_command))
        self.application.add_handler(CommandHandler("why_no_trade", self.why_no_trade_command))

        # Démarrer le bot
        logger.info("✅ Bot Telegram opérationnel!")
        print("\n🤖 Bot Telegram La Bête démarré!")
        print("📱 Ouvrez Telegram et cherchez votre bot\n")

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# ========================================
# MAIN
# ========================================
def main():
    """Point d'entrée"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          🤖 BOT TELEGRAM - La Bête (Dual) 🤖             ║
║                                                          ║
║            Contrôle Centralisé Forex + Crypto            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

    if not TELEGRAM_AVAILABLE:
        print("❌ Erreur: python-telegram-bot non installé")
        print("Installation: pip install python-telegram-bot")
        sys.exit(1)

    bot = LaBeteBot(token=TELEGRAM_BOT_TOKEN)
    bot.run()


if __name__ == "__main__":
    main()

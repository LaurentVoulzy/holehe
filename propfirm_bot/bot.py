# -*- coding: utf-8 -*-
"""
Bot Telegram pour le suivi des comptes PropFirm
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application,
        CommandHandler,
        ContextTypes,
        CallbackQueryHandler,
        ConversationHandler,
        MessageHandler,
        filters
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("python-telegram-bot n'est pas installé. Installez-le avec: pip install python-telegram-bot")

from .database import Database
from .models import Account, PropFirmType, AccountStatus
from .dashboard import DashboardGenerator
from .config import (
    TELEGRAM_BOT_TOKEN,
    WELCOME_MESSAGE,
    HELP_MESSAGE,
    MAX_DRAWDOWN_ALERT
)

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# États pour ConversationHandler
(ADD_NAME, ADD_BALANCE, ADD_PROPFIRM, ADD_STATUS,
 UPDATE_NAME, UPDATE_BALANCE, UPDATE_EQUITY) = range(7)


class PropFirmBot:
    """Bot Telegram pour le suivi des comptes PropFirm"""

    def __init__(self, token: str):
        """Initialise le bot"""
        if not TELEGRAM_AVAILABLE:
            raise ImportError("python-telegram-bot n'est pas installé")

        self.token = token
        self.db = Database()
        self.dashboard_gen = DashboardGenerator()
        self.application = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start"""
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) started the bot")

        await update.message.reply_text(
            WELCOME_MESSAGE,
            parse_mode='Markdown'
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /help"""
        await update.message.reply_text(
            HELP_MESSAGE,
            parse_mode='Markdown'
        )

    async def add_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /add - Ajouter un compte"""
        args = context.args

        if len(args) < 3:
            await update.message.reply_text(
                "❌ Usage: /add [nom] [capital_initial] [propfirm]\n"
                "Exemple: /add MonCompte1 100000 FTMO"
            )
            return

        account_name = args[0]
        try:
            initial_balance = float(args[1])
        except ValueError:
            await update.message.reply_text("❌ Le capital initial doit être un nombre valide")
            return

        propfirm_name = args[2].upper()

        # Vérifier si la propfirm existe
        try:
            propfirm = PropFirmType[propfirm_name] if propfirm_name in [e.name for e in PropFirmType] else PropFirmType.OTHER
        except:
            propfirm = PropFirmType.OTHER

        # Créer le compte
        account = Account(
            user_id=update.effective_user.id,
            account_name=account_name,
            propfirm=propfirm,
            initial_balance=initial_balance,
            current_balance=initial_balance,
            current_equity=initial_balance,
            status=AccountStatus.CHALLENGE,
            created_at=datetime.now(),
            last_updated=datetime.now()
        )

        # Ajouter à la base de données
        if self.db.add_account(account):
            await update.message.reply_text(
                f"✅ Compte **{account_name}** créé avec succès!\n\n"
                f"💰 Capital initial: ${initial_balance:,.2f}\n"
                f"🏢 PropFirm: {propfirm.value}\n"
                f"📊 Statut: {AccountStatus.CHALLENGE.value}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                f"❌ Un compte avec le nom **{account_name}** existe déjà!",
                parse_mode='Markdown'
            )

    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /list - Liste des comptes"""
        user_id = update.effective_user.id
        accounts = self.db.get_user_accounts(user_id)

        if not accounts:
            await update.message.reply_text(
                "📋 Vous n'avez aucun compte enregistré.\n"
                "Utilisez /add pour en créer un!"
            )
            return

        message = "📋 **Vos Comptes PropFirm:**\n\n"

        for account in accounts:
            profit_pct = account.get_profit_percentage()
            emoji = "📈" if profit_pct > 0 else "📉" if profit_pct < 0 else "➡️"

            message += (
                f"{account.get_status_emoji()} **{account.account_name}**\n"
                f"   🏢 {account.propfirm.value}\n"
                f"   💰 ${account.current_balance:,.2f}\n"
                f"   {emoji} {profit_pct:+.2f}%\n"
                f"   📉 DD: {account.max_drawdown:.2f}%\n\n"
            )

        await update.message.reply_text(message, parse_mode='Markdown')

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /status - Statut détaillé d'un compte"""
        args = context.args

        if len(args) < 1:
            await update.message.reply_text(
                "❌ Usage: /status [nom_du_compte]\n"
                "Exemple: /status MonCompte1"
            )
            return

        account_name = args[0]
        user_id = update.effective_user.id

        account = self.db.get_account(user_id, account_name)

        if not account:
            await update.message.reply_text(
                f"❌ Compte **{account_name}** non trouvé!",
                parse_mode='Markdown'
            )
            return

        # Envoyer le résumé
        await update.message.reply_text(
            account.get_summary(),
            parse_mode='Markdown'
        )

    async def update_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /update - Mettre à jour un compte"""
        args = context.args

        if len(args) < 3:
            await update.message.reply_text(
                "❌ Usage: /update [nom] [balance] [equity]\n"
                "Exemple: /update MonCompte1 105000 105500"
            )
            return

        account_name = args[0]
        user_id = update.effective_user.id

        try:
            new_balance = float(args[1])
            new_equity = float(args[2])
        except ValueError:
            await update.message.reply_text("❌ Le balance et l'equity doivent être des nombres valides")
            return

        # Récupérer le compte
        account = self.db.get_account(user_id, account_name)

        if not account:
            await update.message.reply_text(
                f"❌ Compte **{account_name}** non trouvé!",
                parse_mode='Markdown'
            )
            return

        # Mettre à jour le compte
        old_balance = account.current_balance
        account.add_history_entry(new_balance, new_equity)

        # Sauvegarder dans la DB
        self.db.update_account(account)
        self.db.add_history_entry(user_id, account_name, account.history[-1])

        profit_loss = new_balance - old_balance
        emoji = "📈" if profit_loss > 0 else "📉" if profit_loss < 0 else "➡️"

        message = (
            f"✅ Compte **{account_name}** mis à jour!\n\n"
            f"💰 Nouvelle Balance: ${new_balance:,.2f}\n"
            f"📊 Equity: ${new_equity:,.2f}\n"
            f"{emoji} P/L: ${profit_loss:+,.2f}\n"
            f"📉 Drawdown: {account.max_drawdown:.2f}%\n"
        )

        # Alerte si drawdown trop élevé
        if account.max_drawdown > MAX_DRAWDOWN_ALERT:
            message += f"\n⚠️ **ATTENTION:** Drawdown élevé ({account.max_drawdown:.2f}%)!"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def dashboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /dashboard - Générer un dashboard"""
        args = context.args

        if len(args) < 1:
            await update.message.reply_text(
                "❌ Usage: /dashboard [nom_du_compte]\n"
                "Exemple: /dashboard MonCompte1"
            )
            return

        account_name = args[0]
        user_id = update.effective_user.id

        account = self.db.get_account(user_id, account_name)

        if not account:
            await update.message.reply_text(
                f"❌ Compte **{account_name}** non trouvé!",
                parse_mode='Markdown'
            )
            return

        # Générer le dashboard
        await update.message.reply_text("📊 Génération du dashboard en cours...")

        try:
            chart_buffer = self.dashboard_gen.generate_account_dashboard(account)

            await update.message.reply_photo(
                photo=chart_buffer,
                caption=f"📊 Dashboard pour **{account_name}**",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error generating dashboard: {e}")
            await update.message.reply_text(
                f"❌ Erreur lors de la génération du dashboard: {str(e)}"
            )

    async def delete_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /delete - Supprimer un compte"""
        args = context.args

        if len(args) < 1:
            await update.message.reply_text(
                "❌ Usage: /delete [nom_du_compte]\n"
                "Exemple: /delete MonCompte1"
            )
            return

        account_name = args[0]
        user_id = update.effective_user.id

        if self.db.delete_account(user_id, account_name):
            await update.message.reply_text(
                f"✅ Compte **{account_name}** supprimé avec succès!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                f"❌ Compte **{account_name}** non trouvé!",
                parse_mode='Markdown'
            )

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /stats - Statistiques globales"""
        user_id = update.effective_user.id
        accounts = self.db.get_user_accounts(user_id)

        if not accounts:
            await update.message.reply_text(
                "📋 Vous n'avez aucun compte enregistré."
            )
            return

        total_initial = sum(acc.initial_balance for acc in accounts)
        total_current = sum(acc.current_balance for acc in accounts)
        total_pl = total_current - total_initial
        total_pl_pct = (total_pl / total_initial * 100) if total_initial > 0 else 0

        active_accounts = len([acc for acc in accounts if acc.status == AccountStatus.ACTIVE or acc.status == AccountStatus.FUNDED])
        in_profit = len([acc for acc in accounts if acc.total_profit_loss > 0])
        in_loss = len([acc for acc in accounts if acc.total_profit_loss < 0])

        emoji = "📈" if total_pl > 0 else "📉" if total_pl < 0 else "➡️"

        message = f"""
📊 **STATISTIQUES GLOBALES**
━━━━━━━━━━━━━━━━━━━━

📋 **Nombre de comptes:** {len(accounts)}
🟢 **Comptes actifs:** {active_accounts}
📈 **En profit:** {in_profit}
📉 **En perte:** {in_loss}

💰 **Capital total initial:** ${total_initial:,.2f}
💵 **Capital total actuel:** ${total_current:,.2f}
{emoji} **P/L Total:** ${total_pl:+,.2f} ({total_pl_pct:+.2f}%)

━━━━━━━━━━━━━━━━━━━━
        """

        await update.message.reply_text(message, parse_mode='Markdown')

        # Générer un graphique de comparaison si plusieurs comptes
        if len(accounts) > 1:
            try:
                chart_buffer = self.dashboard_gen.generate_comparison_chart(accounts)
                await update.message.reply_photo(
                    photo=chart_buffer,
                    caption="📊 Comparaison de vos comptes"
                )
            except Exception as e:
                logger.error(f"Error generating comparison chart: {e}")

    async def alert_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /alert - Configurer une alerte"""
        args = context.args

        if len(args) < 3:
            await update.message.reply_text(
                "❌ Usage: /alert [nom] [type] [valeur]\n"
                "Types: drawdown, profit, loss\n"
                "Exemple: /alert MonCompte1 drawdown 10"
            )
            return

        account_name = args[0]
        alert_type = args[1].lower()
        try:
            threshold = float(args[2])
        except ValueError:
            await update.message.reply_text("❌ La valeur doit être un nombre")
            return

        user_id = update.effective_user.id

        # Vérifier que le compte existe
        account = self.db.get_account(user_id, account_name)
        if not account:
            await update.message.reply_text(
                f"❌ Compte **{account_name}** non trouvé!",
                parse_mode='Markdown'
            )
            return

        # Ajouter l'alerte
        if self.db.add_alert(user_id, account_name, alert_type, threshold):
            await update.message.reply_text(
                f"✅ Alerte configurée pour **{account_name}**\n"
                f"Type: {alert_type}\n"
                f"Seuil: {threshold}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Erreur lors de la création de l'alerte")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gestion des erreurs"""
        logger.error(f"Update {update} caused error {context.error}")

    def run(self):
        """Démarre le bot"""
        logger.info("Starting PropFirm Bot...")

        # Créer l'application
        self.application = Application.builder().token(self.token).build()

        # Ajouter les handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("add", self.add_command))
        self.application.add_handler(CommandHandler("list", self.list_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("update", self.update_command))
        self.application.add_handler(CommandHandler("dashboard", self.dashboard_command))
        self.application.add_handler(CommandHandler("delete", self.delete_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("alert", self.alert_command))

        # Handler d'erreurs
        self.application.add_error_handler(self.error_handler)

        # Démarrer le bot
        logger.info("Bot is running...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Point d'entrée principal"""
    # Vérifier le token
    token = TELEGRAM_BOT_TOKEN

    if token == 'YOUR_BOT_TOKEN_HERE':
        print("❌ ERREUR: Veuillez configurer votre TELEGRAM_BOT_TOKEN")
        print("Vous pouvez le définir via:")
        print("  1. Variable d'environnement: export TELEGRAM_BOT_TOKEN='votre_token'")
        print("  2. Modifier le fichier config.py")
        sys.exit(1)

    # Créer et lancer le bot
    bot = PropFirmBot(token)
    bot.run()


if __name__ == '__main__':
    main()

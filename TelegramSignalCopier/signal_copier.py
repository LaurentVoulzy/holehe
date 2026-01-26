"""
Telegram Signal Copier - Bot Telegram qui copie automatiquement les signaux vers MT5
"""

import os
import json
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from signal_parser import SignalParser
from mt5_executor import MT5Executor


class SignalCopierBot:
    """Bot Telegram qui copie les signaux de trading vers MT5"""

    def __init__(self, config_file: str = 'config.json'):
        """
        Args:
            config_file: Fichier de configuration JSON
        """
        # Charger configuration
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.bot_token = self.config['telegram']['bot_token']
        self.authorized_chat_id = int(self.config['telegram']['authorized_chat_id'])
        self.signals_folder = self.config['mt5']['signals_folder']

        # Initialiser composants
        self.parser = SignalParser()
        self.executor = MT5Executor(signals_folder=self.signals_folder)

        # Statistiques
        self.stats = {
            'signals_received': 0,
            'signals_parsed': 0,
            'signals_sent': 0,
            'signals_failed': 0
        }

        print("🤖 Signal Copier Bot initialisé")
        print(f"   📱 Chat ID autorisé: {self.authorized_chat_id}")
        print(f"   📁 Dossier signaux: {self.signals_folder}")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start"""
        if not self._is_authorized(update):
            return

        welcome_msg = """
🤖 **TELEGRAM SIGNAL COPIER**

✅ Bot actif et prêt à copier vos signaux!

📊 **Format de signal:**
```
XAUUSD BUY NOW 5082
SL 5070
TP 5090
TP 5100
TP 5135
```

🎯 **Commandes disponibles:**
/start - Afficher ce message
/status - Voir status du bot
/stats - Voir statistiques
/help - Aide et exemples

💡 **Envoyez simplement votre signal!**
Le bot le parsera automatiquement et l'enverra à MT5.
"""
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /status"""
        if not self._is_authorized(update):
            return

        # Obtenir status MT5
        mt5_status = self.executor.get_status()

        status_msg = f"""
📊 **STATUS DU BOT**

🟢 Bot actif et en écoute

📂 **Signaux MT5:**
   • En attente: {mt5_status['pending']}
   • Exécutés: {mt5_status['executed']}
   • Échoués: {mt5_status['failed']}
   • Archivés: {mt5_status['archived']}

📈 **Session actuelle:**
   • Signaux reçus: {self.stats['signals_received']}
   • Parsés avec succès: {self.stats['signals_parsed']}
   • Envoyés à MT5: {self.stats['signals_sent']}
   • Échecs: {self.stats['signals_failed']}
"""
        await update.message.reply_text(status_msg, parse_mode='Markdown')

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /stats"""
        if not self._is_authorized(update):
            return

        stats_msg = f"""
📊 **STATISTIQUES**

📥 **Signaux reçus:** {self.stats['signals_received']}
✅ **Parsés:** {self.stats['signals_parsed']}
📤 **Envoyés MT5:** {self.stats['signals_sent']}
❌ **Échecs:** {self.stats['signals_failed']}

📈 **Taux de succès:** {self._success_rate():.1f}%
"""
        await update.message.reply_text(stats_msg, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /help"""
        if not self._is_authorized(update):
            return

        help_msg = """
📚 **AIDE - SIGNAL COPIER**

🎯 **Formats de signaux supportés:**

**Format standard:**
```
XAUUSD BUY NOW 5082
SL 5070
TP 5090
TP 5100
TP 5135
```

**Format avec @:**
```
BTCUSD SELL @ 95000
SL 96000
TP 94000
TP 93000
```

**Avec alias:**
```
GOLD BUY 5082
SL 5070
TP 5090
```

📌 **Symboles supportés:**
   • GOLD / XAUUSD
   • BTC / BTCUSD
   • ETH / ETHUSD
   • EUR / EURUSD
   • GBP / GBPUSD
   • JPY / USDJPY

💡 **Le bot MT5 gère automatiquement:**
   ✅ Calcul du lot size (risk %)
   ✅ Placement SL/TP
   ✅ Fermetures partielles (TP1/TP2/TP3)
   ✅ Protection FTMO

⚠️ **Important:**
   • SL obligatoire
   • Au moins 1 TP requis
   • Maximum 3 TPs
"""
        await update.message.reply_text(help_msg, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Traite les messages texte (signaux potentiels)"""
        if not self._is_authorized(update):
            await update.message.reply_text("❌ Non autorisé. Chat ID inconnu.")
            return

        message_text = update.message.text
        self.stats['signals_received'] += 1

        print(f"\n📩 Message reçu de {update.effective_user.username}:")
        print(f"   {message_text[:100]}...")

        # Parser le signal
        signal = self.parser.parse(message_text)

        if not signal:
            # Pas un signal valide
            self.stats['signals_failed'] += 1
            await update.message.reply_text(
                "❌ Format de signal invalide.\n"
                "Utilisez /help pour voir les formats acceptés."
            )
            return

        # Signal parsé avec succès
        self.stats['signals_parsed'] += 1

        # Afficher résumé du signal
        summary = self.parser.format_signal_summary(signal)
        await update.message.reply_text(summary, parse_mode='Markdown')

        # Envoyer au bot MT5
        success = self.executor.send_signal(signal)

        if success:
            self.stats['signals_sent'] += 1
            await update.message.reply_text(
                "✅ **Signal envoyé au bot MT5!**\n\n"
                "Le bot MT5 va:\n"
                "   • Calculer le lot size automatiquement\n"
                "   • Ouvrir la position\n"
                "   • Placer SL et TPs\n\n"
                "📊 Surveillez MT5 pour confirmation."
            , parse_mode='Markdown')
        else:
            self.stats['signals_failed'] += 1
            await update.message.reply_text(
                "❌ Erreur lors de l'envoi au bot MT5.\n"
                "Vérifiez que le dossier signaux existe."
            )

    def _is_authorized(self, update: Update) -> bool:
        """Vérifie si le chat ID est autorisé"""
        chat_id = update.effective_chat.id
        return chat_id == self.authorized_chat_id

    def _success_rate(self) -> float:
        """Calcule le taux de succès"""
        total = self.stats['signals_received']
        if total == 0:
            return 0.0
        return (self.stats['signals_sent'] / total) * 100

    def run(self):
        """Lance le bot"""
        print("\n" + "=" * 60)
        print("🚀 DÉMARRAGE DU BOT TELEGRAM SIGNAL COPIER")
        print("=" * 60)

        # Créer application
        app = Application.builder().token(self.bot_token).build()

        # Ajouter handlers
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("status", self.status_command))
        app.add_handler(CommandHandler("stats", self.stats_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Lancer le bot
        print(f"✅ Bot connecté!")
        print(f"📱 En écoute des messages de Chat ID: {self.authorized_chat_id}")
        print(f"💡 Envoyez /start pour commencer")
        print("\n⌛ Bot en attente de signaux...\n")

        app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        bot = SignalCopierBot('config.json')
        bot.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Bot arrêté par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()

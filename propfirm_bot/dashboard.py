# -*- coding: utf-8 -*-
"""
Générateur de dashboard graphique pour les comptes PropFirm
"""

import io
from datetime import datetime, timedelta
from typing import List, Optional

try:
    import matplotlib
    matplotlib.use('Agg')  # Backend non-interactif
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from .models import Account, TradeHistory
from .config import CHART_COLORS


class DashboardGenerator:
    """Génère des graphiques de dashboard pour les comptes"""

    def __init__(self):
        """Initialise le générateur de dashboard"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("Matplotlib n'est pas installé. Installez-le avec: pip install matplotlib")

        # Style des graphiques
        plt.style.use('seaborn-v0_8-darkgrid')

    def generate_account_dashboard(self, account: Account) -> io.BytesIO:
        """Génère un dashboard complet pour un compte"""

        # Créer une figure avec plusieurs sous-graphiques
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle(f'Dashboard - {account.account_name} ({account.propfirm.value})',
                     fontsize=16, fontweight='bold')

        # 1. Graphique de l'évolution du balance
        ax1 = plt.subplot(2, 2, 1)
        self._plot_balance_evolution(ax1, account)

        # 2. Graphique du drawdown
        ax2 = plt.subplot(2, 2, 2)
        self._plot_drawdown(ax2, account)

        # 3. Graphique P/L cumulé
        ax3 = plt.subplot(2, 2, 3)
        self._plot_cumulative_pl(ax3, account)

        # 4. Statistiques et métriques
        ax4 = plt.subplot(2, 2, 4)
        self._plot_statistics(ax4, account)

        plt.tight_layout()

        # Sauvegarder dans un buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plt.close(fig)

        return buffer

    def _plot_balance_evolution(self, ax, account: Account):
        """Graphique de l'évolution du balance"""
        if not account.history:
            ax.text(0.5, 0.5, 'Pas de données disponibles',
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Évolution du Balance')
            return

        dates = [entry.timestamp for entry in account.history]
        balances = [entry.balance for entry in account.history]
        equities = [entry.equity for entry in account.history]

        ax.plot(dates, balances, label='Balance', color=CHART_COLORS['balance'],
               linewidth=2, marker='o', markersize=4)
        ax.plot(dates, equities, label='Equity', color=CHART_COLORS['equity'],
               linewidth=2, marker='s', markersize=4, alpha=0.7)

        # Ligne de référence du capital initial
        ax.axhline(y=account.initial_balance, color='gray', linestyle='--',
                  linewidth=1, alpha=0.5, label='Capital Initial')

        ax.set_title('Évolution du Balance et Equity', fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Montant ($)')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        # Format des dates sur l'axe X
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    def _plot_drawdown(self, ax, account: Account):
        """Graphique du drawdown"""
        if not account.history:
            ax.text(0.5, 0.5, 'Pas de données disponibles',
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Drawdown')
            return

        dates = [entry.timestamp for entry in account.history]
        drawdowns = [entry.drawdown for entry in account.history]

        ax.fill_between(dates, drawdowns, 0, color=CHART_COLORS['drawdown'],
                        alpha=0.6, label='Drawdown')
        ax.plot(dates, drawdowns, color=CHART_COLORS['drawdown'],
               linewidth=2, marker='o', markersize=3)

        # Ligne de limite si définie
        if account.max_total_loss:
            max_dd_percent = account.max_total_loss * 100
            ax.axhline(y=max_dd_percent, color='red', linestyle='--',
                      linewidth=2, label=f'Limite Max ({max_dd_percent:.0f}%)')

        ax.set_title('Drawdown (%)', fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Drawdown (%)')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        ax.invert_yaxis()  # Inverser l'axe Y pour que le drawdown soit vers le bas

        # Format des dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    def _plot_cumulative_pl(self, ax, account: Account):
        """Graphique du P/L cumulé"""
        if not account.history:
            ax.text(0.5, 0.5, 'Pas de données disponibles',
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('P/L Cumulé')
            return

        dates = [entry.timestamp for entry in account.history]

        # Calculer le P/L cumulé
        cumulative_pl = []
        total = 0
        for entry in account.history:
            total += entry.profit_loss
            cumulative_pl.append(total)

        # Couleur conditionnelle
        colors = [CHART_COLORS['profit'] if pl >= 0 else CHART_COLORS['loss']
                 for pl in cumulative_pl]

        # Graphique en barres
        bars = ax.bar(dates, cumulative_pl, color=colors, alpha=0.7, width=0.8)

        # Ligne de référence à 0
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)

        # Ligne de tendance
        if len(cumulative_pl) > 1:
            ax.plot(dates, cumulative_pl, color='blue', linewidth=2,
                   marker='o', markersize=3, alpha=0.5, label='Tendance')

        ax.set_title('Profit/Loss Cumulé ($)', fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('P/L Cumulé ($)')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, axis='y')

        # Format des dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    def _plot_statistics(self, ax, account: Account):
        """Affiche les statistiques clés"""
        ax.axis('off')

        # Calculer les statistiques
        profit_pct = account.get_profit_percentage()
        total_pl = account.total_profit_loss

        # Calculer les jours de trading
        if account.history:
            days_trading = (account.last_updated - account.created_at).days
            if days_trading == 0:
                days_trading = 1
        else:
            days_trading = 1

        # Win rate si on a l'historique
        if account.history:
            winning_trades = sum(1 for entry in account.history if entry.profit_loss > 0)
            total_trades = len(account.history)
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        else:
            win_rate = 0
            total_trades = 0

        # Texte des statistiques
        stats_text = f"""
STATISTIQUES DU COMPTE
{'=' * 35}

📊 Statut: {account.status.value}
💰 PropFirm: {account.propfirm.value}

💵 Capital Initial: ${account.initial_balance:,.2f}
💵 Balance Actuelle: ${account.current_balance:,.2f}
📈 Balance Max: ${account.max_balance:,.2f}

{'─' * 35}

📊 P/L Total: ${total_pl:,.2f}
📊 P/L Pourcentage: {profit_pct:+.2f}%
📉 Drawdown Max: {account.max_drawdown:.2f}%

{'─' * 35}

📅 Jours de Trading: {days_trading}
🎯 Nombre de Mises à Jour: {total_trades}
✅ Win Rate: {win_rate:.1f}%

{'─' * 35}

🕐 Créé le: {account.created_at.strftime('%Y-%m-%d')}
🕐 Dernière MAJ: {account.last_updated.strftime('%Y-%m-%d %H:%M')}
        """

        # Couleur du texte selon performance
        text_color = 'green' if profit_pct > 0 else 'red' if profit_pct < 0 else 'black'

        ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               fontfamily='monospace',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        ax.set_title('Métriques de Performance', fontweight='bold', pad=20)

    def generate_comparison_chart(self, accounts: List[Account]) -> io.BytesIO:
        """Génère un graphique de comparaison entre plusieurs comptes"""

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Comparaison des Comptes', fontsize=16, fontweight='bold')

        account_names = [acc.account_name for acc in accounts]
        profit_percentages = [acc.get_profit_percentage() for acc in accounts]
        drawdowns = [acc.max_drawdown for acc in accounts]

        # Graphique 1: Comparaison des profits
        colors1 = [CHART_COLORS['profit'] if p >= 0 else CHART_COLORS['loss']
                  for p in profit_percentages]

        ax1.bar(account_names, profit_percentages, color=colors1, alpha=0.7)
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax1.set_title('Profit/Loss (%)', fontweight='bold')
        ax1.set_ylabel('P/L (%)')
        ax1.grid(True, alpha=0.3, axis='y')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Graphique 2: Comparaison des drawdowns
        ax2.bar(account_names, drawdowns, color=CHART_COLORS['drawdown'], alpha=0.7)
        ax2.set_title('Drawdown Maximum (%)', fontweight='bold')
        ax2.set_ylabel('Drawdown (%)')
        ax2.grid(True, alpha=0.3, axis='y')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()

        # Sauvegarder dans un buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plt.close(fig)

        return buffer

    def generate_simple_chart(self, account: Account) -> io.BytesIO:
        """Génère un graphique simple pour un aperçu rapide"""

        fig, ax = plt.subplots(figsize=(10, 6))

        if account.history:
            dates = [entry.timestamp for entry in account.history]
            balances = [entry.balance for entry in account.history]

            ax.plot(dates, balances, color=CHART_COLORS['balance'],
                   linewidth=3, marker='o', markersize=6)
            ax.axhline(y=account.initial_balance, color='gray', linestyle='--',
                      linewidth=2, alpha=0.5, label='Capital Initial')

            ax.fill_between(dates, balances, account.initial_balance,
                           where=[b >= account.initial_balance for b in balances],
                           color=CHART_COLORS['profit'], alpha=0.3, label='Profit')
            ax.fill_between(dates, balances, account.initial_balance,
                           where=[b < account.initial_balance for b in balances],
                           color=CHART_COLORS['loss'], alpha=0.3, label='Perte')
        else:
            ax.text(0.5, 0.5, 'Pas de données disponibles',
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)

        ax.set_title(f'{account.account_name} - Évolution du Balance',
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Balance ($)', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        if account.history:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.tight_layout()

        # Sauvegarder dans un buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plt.close(fig)

        return buffer

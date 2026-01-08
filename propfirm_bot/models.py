# -*- coding: utf-8 -*-
"""
Modèles de données pour le suivi des comptes PropFirm
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class PropFirmType(Enum):
    """Types de PropFirm supportés"""
    FTMO = "FTMO"
    THE5ERS = "The5ers"
    TOPSTEP = "TopstepTrader"
    ONEUP = "OneUp Trader"
    MYFUNDEDFX = "MyFundedFX"
    FUNDED_NEXT = "Funded Next"
    OTHER = "Autre"


class AccountStatus(Enum):
    """Statuts possibles d'un compte"""
    ACTIVE = "Actif"
    CHALLENGE = "En Challenge"
    VERIFICATION = "En Vérification"
    FUNDED = "Financé"
    FAILED = "Échoué"
    PASSED = "Réussi"
    SUSPENDED = "Suspendu"


@dataclass
class TradeHistory:
    """Historique d'une mise à jour de compte"""
    timestamp: datetime
    balance: float
    equity: float
    profit_loss: float
    drawdown: float
    note: Optional[str] = None


@dataclass
class Account:
    """Modèle de compte PropFirm"""
    user_id: int
    account_name: str
    propfirm: PropFirmType
    initial_balance: float
    current_balance: float
    current_equity: float
    status: AccountStatus
    created_at: datetime
    last_updated: datetime
    history: List[TradeHistory] = field(default_factory=list)
    max_balance: float = 0.0
    max_drawdown: float = 0.0
    total_profit_loss: float = 0.0
    profit_target: Optional[float] = None
    max_daily_loss: Optional[float] = None
    max_total_loss: Optional[float] = None

    def __post_init__(self):
        """Initialisation après création"""
        if self.max_balance == 0.0:
            self.max_balance = self.initial_balance

        self.calculate_metrics()

    def calculate_metrics(self):
        """Calcule les métriques du compte"""
        # Profit/Loss total
        self.total_profit_loss = self.current_balance - self.initial_balance

        # Max balance atteint
        if self.current_balance > self.max_balance:
            self.max_balance = self.current_balance

        # Drawdown actuel
        if self.max_balance > 0:
            self.max_drawdown = ((self.max_balance - self.current_balance) / self.max_balance) * 100
        else:
            self.max_drawdown = 0.0

    def get_profit_percentage(self) -> float:
        """Calcule le pourcentage de profit"""
        if self.initial_balance == 0:
            return 0.0
        return (self.total_profit_loss / self.initial_balance) * 100

    def get_current_drawdown(self) -> float:
        """Retourne le drawdown actuel en pourcentage"""
        return self.max_drawdown

    def is_in_danger(self) -> bool:
        """Vérifie si le compte est en danger"""
        # Vérifier le drawdown maximum
        if self.max_total_loss and self.max_drawdown >= (self.max_total_loss * 100):
            return True

        # Vérifier si le compte est en perte importante
        if self.get_profit_percentage() < -5:
            return True

        return False

    def get_status_emoji(self) -> str:
        """Retourne un emoji basé sur le statut"""
        emoji_map = {
            AccountStatus.ACTIVE: "🟢",
            AccountStatus.CHALLENGE: "🔵",
            AccountStatus.VERIFICATION: "🟡",
            AccountStatus.FUNDED: "💰",
            AccountStatus.FAILED: "🔴",
            AccountStatus.PASSED: "✅",
            AccountStatus.SUSPENDED: "⏸️"
        }
        return emoji_map.get(self.status, "⚪")

    def add_history_entry(self, balance: float, equity: float, note: Optional[str] = None):
        """Ajoute une entrée à l'historique"""
        profit_loss = balance - self.current_balance

        entry = TradeHistory(
            timestamp=datetime.now(),
            balance=balance,
            equity=equity,
            profit_loss=profit_loss,
            drawdown=self.max_drawdown,
            note=note
        )

        self.history.append(entry)
        self.current_balance = balance
        self.current_equity = equity
        self.last_updated = datetime.now()
        self.calculate_metrics()

    def to_dict(self) -> dict:
        """Convertit le compte en dictionnaire"""
        return {
            'user_id': self.user_id,
            'account_name': self.account_name,
            'propfirm': self.propfirm.value,
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'current_equity': self.current_equity,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'last_updated': self.last_updated.isoformat(),
            'max_balance': self.max_balance,
            'max_drawdown': self.max_drawdown,
            'total_profit_loss': self.total_profit_loss,
            'profit_target': self.profit_target,
            'max_daily_loss': self.max_daily_loss,
            'max_total_loss': self.max_total_loss
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Account':
        """Crée un compte depuis un dictionnaire"""
        return cls(
            user_id=data['user_id'],
            account_name=data['account_name'],
            propfirm=PropFirmType(data['propfirm']),
            initial_balance=data['initial_balance'],
            current_balance=data['current_balance'],
            current_equity=data['current_equity'],
            status=AccountStatus(data['status']),
            created_at=datetime.fromisoformat(data['created_at']),
            last_updated=datetime.fromisoformat(data['last_updated']),
            max_balance=data.get('max_balance', 0.0),
            max_drawdown=data.get('max_drawdown', 0.0),
            total_profit_loss=data.get('total_profit_loss', 0.0),
            profit_target=data.get('profit_target'),
            max_daily_loss=data.get('max_daily_loss'),
            max_total_loss=data.get('max_total_loss')
        )

    def get_summary(self) -> str:
        """Retourne un résumé formaté du compte"""
        profit_pct = self.get_profit_percentage()
        profit_emoji = "📈" if profit_pct > 0 else "📉" if profit_pct < 0 else "➡️"

        summary = f"""
{self.get_status_emoji()} **{self.account_name}** ({self.propfirm.value})
━━━━━━━━━━━━━━━━━━━━
💼 **Statut:** {self.status.value}
💰 **Capital Initial:** ${self.initial_balance:,.2f}
💵 **Balance Actuelle:** ${self.current_balance:,.2f}
📊 **Equity:** ${self.current_equity:,.2f}
{profit_emoji} **P/L:** ${self.total_profit_loss:,.2f} ({profit_pct:+.2f}%)
📉 **Drawdown Max:** {self.max_drawdown:.2f}%
📅 **Dernière MAJ:** {self.last_updated.strftime('%Y-%m-%d %H:%M')}
"""

        if self.profit_target:
            progress = (self.total_profit_loss / (self.initial_balance * self.profit_target / 100)) * 100
            summary += f"🎯 **Objectif de profit:** {progress:.1f}% de {self.profit_target}%\n"

        if self.is_in_danger():
            summary += "\n⚠️ **ATTENTION:** Compte en danger!\n"

        return summary

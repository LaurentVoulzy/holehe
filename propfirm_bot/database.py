# -*- coding: utf-8 -*-
"""
Gestion de la base de données SQLite pour le suivi des comptes PropFirm
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from .models import Account, PropFirmType, AccountStatus, TradeHistory
from .config import DATABASE_PATH


class Database:
    """Gestionnaire de base de données pour les comptes PropFirm"""

    def __init__(self, db_path: Path = DATABASE_PATH):
        """Initialise la connexion à la base de données"""
        self.db_path = db_path
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """Crée une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialise les tables de la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Table des comptes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                account_name TEXT NOT NULL,
                propfirm TEXT NOT NULL,
                initial_balance REAL NOT NULL,
                current_balance REAL NOT NULL,
                current_equity REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                max_balance REAL DEFAULT 0.0,
                max_drawdown REAL DEFAULT 0.0,
                total_profit_loss REAL DEFAULT 0.0,
                profit_target REAL,
                max_daily_loss REAL,
                max_total_loss REAL,
                UNIQUE(user_id, account_name)
            )
        ''')

        # Table de l'historique
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                balance REAL NOT NULL,
                equity REAL NOT NULL,
                profit_loss REAL NOT NULL,
                drawdown REAL NOT NULL,
                note TEXT,
                FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE CASCADE
            )
        ''')

        # Table des alertes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                account_name TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                threshold REAL NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def add_account(self, account: Account) -> bool:
        """Ajoute un nouveau compte"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO accounts (
                    user_id, account_name, propfirm, initial_balance,
                    current_balance, current_equity, status, created_at,
                    last_updated, max_balance, max_drawdown, total_profit_loss,
                    profit_target, max_daily_loss, max_total_loss
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                account.user_id,
                account.account_name,
                account.propfirm.value,
                account.initial_balance,
                account.current_balance,
                account.current_equity,
                account.status.value,
                account.created_at.isoformat(),
                account.last_updated.isoformat(),
                account.max_balance,
                account.max_drawdown,
                account.total_profit_loss,
                account.profit_target,
                account.max_daily_loss,
                account.max_total_loss
            ))

            conn.commit()
            conn.close()
            return True

        except sqlite3.IntegrityError:
            return False

    def get_account(self, user_id: int, account_name: str) -> Optional[Account]:
        """Récupère un compte spécifique"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM accounts
            WHERE user_id = ? AND account_name = ?
        ''', (user_id, account_name))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        account = self._row_to_account(row)

        # Charger l'historique
        account.history = self.get_account_history(row['id'])

        return account

    def get_user_accounts(self, user_id: int) -> List[Account]:
        """Récupère tous les comptes d'un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM accounts
            WHERE user_id = ?
            ORDER BY last_updated DESC
        ''', (user_id,))

        rows = cursor.fetchall()
        conn.close()

        accounts = []
        for row in rows:
            account = self._row_to_account(row)
            accounts.append(account)

        return accounts

    def update_account(self, account: Account) -> bool:
        """Met à jour un compte existant"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE accounts
                SET current_balance = ?,
                    current_equity = ?,
                    status = ?,
                    last_updated = ?,
                    max_balance = ?,
                    max_drawdown = ?,
                    total_profit_loss = ?
                WHERE user_id = ? AND account_name = ?
            ''', (
                account.current_balance,
                account.current_equity,
                account.status.value,
                account.last_updated.isoformat(),
                account.max_balance,
                account.max_drawdown,
                account.total_profit_loss,
                account.user_id,
                account.account_name
            ))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error updating account: {e}")
            return False

    def delete_account(self, user_id: int, account_name: str) -> bool:
        """Supprime un compte"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                DELETE FROM accounts
                WHERE user_id = ? AND account_name = ?
            ''', (user_id, account_name))

            conn.commit()
            conn.close()
            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error deleting account: {e}")
            return False

    def add_history_entry(self, user_id: int, account_name: str, entry: TradeHistory) -> bool:
        """Ajoute une entrée à l'historique"""
        try:
            # Récupérer l'ID du compte
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id FROM accounts
                WHERE user_id = ? AND account_name = ?
            ''', (user_id, account_name))

            row = cursor.fetchone()
            if not row:
                return False

            account_id = row['id']

            cursor.execute('''
                INSERT INTO trade_history (
                    account_id, timestamp, balance, equity,
                    profit_loss, drawdown, note
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                account_id,
                entry.timestamp.isoformat(),
                entry.balance,
                entry.equity,
                entry.profit_loss,
                entry.drawdown,
                entry.note
            ))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error adding history entry: {e}")
            return False

    def get_account_history(self, account_id: int, limit: int = 100) -> List[TradeHistory]:
        """Récupère l'historique d'un compte"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM trade_history
            WHERE account_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (account_id, limit))

        rows = cursor.fetchall()
        conn.close()

        history = []
        for row in rows:
            entry = TradeHistory(
                timestamp=datetime.fromisoformat(row['timestamp']),
                balance=row['balance'],
                equity=row['equity'],
                profit_loss=row['profit_loss'],
                drawdown=row['drawdown'],
                note=row['note']
            )
            history.append(entry)

        return list(reversed(history))  # Ordre chronologique

    def _row_to_account(self, row: sqlite3.Row) -> Account:
        """Convertit une ligne de la DB en objet Account"""
        return Account(
            user_id=row['user_id'],
            account_name=row['account_name'],
            propfirm=PropFirmType(row['propfirm']),
            initial_balance=row['initial_balance'],
            current_balance=row['current_balance'],
            current_equity=row['current_equity'],
            status=AccountStatus(row['status']),
            created_at=datetime.fromisoformat(row['created_at']),
            last_updated=datetime.fromisoformat(row['last_updated']),
            max_balance=row['max_balance'],
            max_drawdown=row['max_drawdown'],
            total_profit_loss=row['total_profit_loss'],
            profit_target=row['profit_target'],
            max_daily_loss=row['max_daily_loss'],
            max_total_loss=row['max_total_loss']
        )

    def add_alert(self, user_id: int, account_name: str, alert_type: str, threshold: float) -> bool:
        """Ajoute une alerte"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO alerts (user_id, account_name, alert_type, threshold, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, account_name, alert_type, threshold, datetime.now().isoformat()))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error adding alert: {e}")
            return False

    def get_user_alerts(self, user_id: int) -> List[dict]:
        """Récupère les alertes d'un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM alerts
            WHERE user_id = ? AND is_active = 1
        ''', (user_id,))

        rows = cursor.fetchall()
        conn.close()

        alerts = []
        for row in rows:
            alerts.append({
                'id': row['id'],
                'account_name': row['account_name'],
                'alert_type': row['alert_type'],
                'threshold': row['threshold']
            })

        return alerts

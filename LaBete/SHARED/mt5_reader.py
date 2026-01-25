# -*- coding: utf-8 -*-
"""
LA BÊTE - MT5 Reader
Lit les données MT5 en lecture seule et les stocke dans une DB

IMPORTANT:
- Fonctionne SEULEMENT sur Windows
- MT5 doit être installé et connecté
- Utilise le mot de passe LECTURE SEULE (Investor Password)
"""

import MetaTrader5 as mt5
import schedule
import time
import sqlite3
from datetime import datetime
from pathlib import Path
import logging

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration MT5 (LECTURE SEULE)
MT5_LOGIN = 1512373613
MT5_PASSWORD = "3sHq1786xWD1"  # Mot de passe LECTURE SEULE
MT5_SERVER = "FTMO-Demo"

# Base de données
DB_PATH = Path(__file__).parent / "mt5_account_data.db"


def init_database():
    """Initialise la base de données"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table pour les données du compte
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account_snapshot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            balance REAL NOT NULL,
            equity REAL NOT NULL,
            profit REAL NOT NULL,
            margin REAL NOT NULL,
            margin_free REAL NOT NULL,
            margin_level REAL,
            positions_count INTEGER NOT NULL,
            orders_count INTEGER NOT NULL
        )
    ''')

    # Table pour les positions ouvertes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS open_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ticket INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            type TEXT NOT NULL,
            volume REAL NOT NULL,
            open_price REAL NOT NULL,
            current_price REAL NOT NULL,
            sl REAL,
            tp REAL,
            profit REAL NOT NULL,
            comment TEXT
        )
    ''')

    # Table pour historique des trades (nouveau)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trade_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket INTEGER NOT NULL UNIQUE,
            symbol TEXT NOT NULL,
            type TEXT NOT NULL,
            volume REAL NOT NULL,
            open_time TEXT NOT NULL,
            close_time TEXT NOT NULL,
            open_price REAL NOT NULL,
            close_price REAL NOT NULL,
            sl REAL,
            tp REAL,
            profit REAL NOT NULL,
            commission REAL,
            swap REAL,
            comment TEXT
        )
    ''')

    conn.commit()
    conn.close()
    logger.info("✅ Base de données initialisée")


def connect_mt5():
    """Se connecte à MT5 en lecture seule"""
    if not mt5.initialize():
        logger.error("❌ Échec initialisation MT5")
        return False

    if not mt5.login(MT5_LOGIN, MT5_PASSWORD, MT5_SERVER):
        logger.error(f"❌ Échec login MT5: {mt5.last_error()}")
        mt5.shutdown()
        return False

    logger.info(f"✅ Connecté à MT5: {MT5_LOGIN} @ {MT5_SERVER}")
    return True


def update_account_data():
    """
    Lit les données MT5 et les stocke dans la DB
    Appelée toutes les HEURES
    """
    logger.info("📊 Mise à jour données MT5...")

    if not connect_mt5():
        return

    try:
        # Récupérer infos compte
        account_info = mt5.account_info()
        if account_info is None:
            logger.error("❌ Impossible de récupérer infos compte")
            return

        # Récupérer positions ouvertes
        positions = mt5.positions_get()
        if positions is None:
            positions = ()

        # Récupérer ordres en attente
        orders = mt5.orders_get()
        if orders is None:
            orders = ()

        # Sauvegarder snapshot du compte
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO account_snapshot
            (timestamp, balance, equity, profit, margin, margin_free, margin_level,
             positions_count, orders_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp,
            account_info.balance,
            account_info.equity,
            account_info.profit,
            account_info.margin,
            account_info.margin_free,
            account_info.margin_level if account_info.margin > 0 else 0,
            len(positions),
            len(orders)
        ))

        # Sauvegarder positions ouvertes (remplacer toutes)
        cursor.execute('DELETE FROM open_positions')

        for pos in positions:
            cursor.execute('''
                INSERT INTO open_positions
                (timestamp, ticket, symbol, type, volume, open_price, current_price,
                 sl, tp, profit, comment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                pos.ticket,
                pos.symbol,
                "BUY" if pos.type == 0 else "SELL",
                pos.volume,
                pos.price_open,
                pos.price_current,
                pos.sl,
                pos.tp,
                pos.profit,
                pos.comment
            ))

        # Mettre à jour historique des trades (nouveaux uniquement)
        # Récupérer trades depuis le début du mois
        from_date = datetime(datetime.now().year, datetime.now().month, 1)
        deals = mt5.history_deals_get(from_date, datetime.now())

        if deals:
            for deal in deals:
                # Seulement les OUT (fermetures de positions)
                if deal.entry == 1:  # DEAL_ENTRY_OUT
                    try:
                        cursor.execute('''
                            INSERT OR IGNORE INTO trade_history
                            (ticket, symbol, type, volume, open_time, close_time,
                             open_price, close_price, sl, tp, profit, commission,
                             swap, comment)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            deal.position_id,
                            deal.symbol,
                            "BUY" if deal.type == 0 else "SELL",
                            deal.volume,
                            datetime.fromtimestamp(deal.time).isoformat(),
                            datetime.fromtimestamp(deal.time).isoformat(),
                            deal.price,
                            deal.price,
                            0,  # SL non disponible dans deals
                            0,  # TP non disponible dans deals
                            deal.profit,
                            deal.commission,
                            deal.swap,
                            deal.comment
                        ))
                    except sqlite3.IntegrityError:
                        pass  # Trade déjà en base

        conn.commit()
        conn.close()

        logger.info(f"✅ Données MT5 sauvegardées: Balance={account_info.balance:.2f}€, "
                   f"Equity={account_info.equity:.2f}€, P&L={account_info.profit:.2f}€, "
                   f"Positions={len(positions)}")

    except Exception as e:
        logger.error(f"❌ Erreur mise à jour données: {e}")
    finally:
        mt5.shutdown()


def get_latest_account_data():
    """Récupère les dernières données du compte depuis la DB"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT balance, equity, profit, margin_free, positions_count, orders_count, timestamp
        FROM account_snapshot
        ORDER BY id DESC
        LIMIT 1
    ''')

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "balance": row[0],
            "equity": row[1],
            "profit": row[2],
            "margin_free": row[3],
            "positions_count": row[4],
            "orders_count": row[5],
            "last_update": row[6]
        }
    return None


def get_open_positions():
    """Récupère toutes les positions ouvertes depuis la DB"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT ticket, symbol, type, volume, open_price, current_price, sl, tp, profit, comment
        FROM open_positions
    ''')

    positions = []
    for row in cursor.fetchall():
        positions.append({
            "ticket": row[0],
            "symbol": row[1],
            "type": row[2],
            "volume": row[3],
            "open_price": row[4],
            "current_price": row[5],
            "sl": row[6],
            "tp": row[7],
            "profit": row[8],
            "comment": row[9]
        })

    conn.close()
    return positions


def main():
    """Point d'entrée - Lance la mise à jour toutes les heures"""
    logger.info("🚀 Démarrage MT5 Reader")
    logger.info(f"📊 Login: {MT5_LOGIN} @ {MT5_SERVER}")
    logger.info(f"💾 Base de données: {DB_PATH}")
    logger.info(f"⏱️  Fréquence: Toutes les HEURES")

    # Initialiser la DB
    init_database()

    # Première mise à jour immédiate
    logger.info("📊 Première mise à jour immédiate...")
    update_account_data()

    # Planifier mise à jour toutes les heures
    schedule.every(1).hours.do(update_account_data)

    logger.info("✅ MT5 Reader opérationnel - Mise à jour toutes les heures")

    # Boucle infinie
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check chaque minute


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Arrêt MT5 Reader...")
        mt5.shutdown()
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        mt5.shutdown()

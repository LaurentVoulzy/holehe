# -*- coding: utf-8 -*-
"""
LA BÊTE - Guardian FOREX
Système de Protection Ultra-Sécurisé pour Trading Forex
Python 3.12+ Compatible

Protections:
1. Stop Loss Dynamique basé ATR
2. Triple Take Profit (1:2, 1:3, 1:5)
3. Break Even Intelligent
4. Trailing Stop Structurel
5. Filtre News Économiques
6. Anti-Revenge Trading
7. Kill Switch Ultimate Multi-Triggers
"""

import sys
import os
from pathlib import Path

# Ajouter SHARED au path
sys.path.insert(0, str(Path(__file__).parent.parent / "SHARED"))

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3
import logging
from typing import Dict, List, Optional, Tuple
import json
import requests
from threading import Thread
import time

from config import (
    FOREX_CONFIG,
    CONFLUENCE_WEIGHTS,
    FORBIDDEN_PERIODS,
    HIGH_IMPACT_NEWS,
    NEWS_BUFFER_HOURS,
    REVENGE_TRADING_CONFIG,
    OVERTRADING_CONFIG,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    is_trading_allowed,
    calculate_position_size,
)

# ========================================
# CONFIGURATION LOGGING
# ========================================
# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Créer le dossier logs s'il n'existe pas
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'guardian_forex.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========================================
# FLASK APP
# ========================================
app = Flask(__name__)

# ========================================
# BASE DE DONNÉES
# ========================================
DB_PATH = Path(__file__).parent / "forex_trades.db"


def init_database():
    """Initialise la base de données SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table des trades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            pair TEXT NOT NULL,
            direction TEXT NOT NULL,
            entry_price REAL NOT NULL,
            sl_price REAL NOT NULL,
            tp1_price REAL,
            tp2_price REAL,
            tp3_price REAL,
            lot_size REAL NOT NULL,
            confluence_score INTEGER NOT NULL,
            status TEXT DEFAULT 'PENDING',
            profit_loss REAL DEFAULT 0,
            exit_price REAL,
            exit_time TEXT,
            reason TEXT,
            metadata TEXT
        )
    ''')

    # Table des signaux
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            pair TEXT NOT NULL,
            direction TEXT NOT NULL,
            confluence_score INTEGER NOT NULL,
            approved BOOLEAN DEFAULT 0,
            rejected BOOLEAN DEFAULT 0,
            rejection_reason TEXT,
            metadata TEXT
        )
    ''')

    # Table des statistiques journalières
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_stats (
            date TEXT PRIMARY KEY,
            total_trades INTEGER DEFAULT 0,
            winning_trades INTEGER DEFAULT 0,
            losing_trades INTEGER DEFAULT 0,
            total_profit_loss REAL DEFAULT 0,
            max_drawdown REAL DEFAULT 0,
            kill_switch_triggered BOOLEAN DEFAULT 0
        )
    ''')

    # Table des news économiques
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS economic_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            currency TEXT NOT NULL,
            impact TEXT NOT NULL,
            event_name TEXT NOT NULL,
            actual TEXT,
            forecast TEXT,
            previous TEXT
        )
    ''')

    conn.commit()
    conn.close()
    logger.info("✅ Base de données initialisée")


# ========================================
# GUARDIAN CLASS
# ========================================
class ForexGuardian:
    """Gardien du système Forex - Protections anti-cramage"""

    def __init__(self):
        self.config = FOREX_CONFIG
        self.kill_switch_active = False
        self.trades_today = []
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.last_trade_time = None
        self.max_balance_today = self.config["account_balance"]

        logger.info("🐺 Forex Guardian initialisé")

    # ----------------------------------------
    # VALIDATION DE SIGNAL
    # ----------------------------------------
    def validate_signal(self, signal: Dict) -> Tuple[bool, str]:
        """
        Valide un signal de trading selon toutes les protections

        Args:
            signal: Dict contenant les infos du signal

        Returns:
            (approved: bool, reason: str)
        """
        logger.info(f"📊 Validation signal: {signal.get('pair')} {signal.get('direction')}")

        # 1. Kill Switch actif?
        if self.kill_switch_active:
            return False, "❌ Kill Switch actif"

        # 2. Trading autorisé (périodes interdites)?
        allowed, reason = is_trading_allowed()
        if not allowed:
            return False, f"❌ {reason}"

        # 3. News économique proche?
        if self._is_news_nearby():
            return False, "❌ News High Impact dans les 2h"

        # 4. Confluence score suffisant?
        confluence = signal.get('confluence_score', 0)
        if confluence < self.config['min_confluence_score']:
            return False, f"❌ Confluence trop faible: {confluence}/100 (min {self.config['min_confluence_score']})"

        # 5. Limite de trades journalière?
        trades_today = self._count_trades_today()
        if trades_today >= self.config['max_trades_per_day']:
            return False, f"❌ Limite journalière atteinte ({trades_today}/{self.config['max_trades_per_day']})"

        # 6. Positions ouvertes max?
        open_positions = self._count_open_positions()
        if open_positions >= self.config['max_open_positions']:
            return False, f"❌ Trop de positions ouvertes ({open_positions}/{self.config['max_open_positions']})"

        # 7. Risque journalier dépassé?
        if self._is_daily_risk_exceeded():
            return False, "❌ Risque journalier maximum atteint"

        # 8. Détection Revenge Trading?
        if self._detect_revenge_trading():
            self.kill_switch_active = True
            return False, "❌ REVENGE TRADING DÉTECTÉ - Kill Switch activé"

        # 9. Overtrading détecté?
        if self._detect_overtrading():
            return False, "❌ Overtrading détecté - Pause forcée"

        # 10. Vérification Stop Loss
        sl_valid, sl_reason = self._validate_stop_loss(signal)
        if not sl_valid:
            return False, sl_reason

        # 11. Vérification lot size
        lot_valid, lot_reason = self._validate_lot_size(signal)
        if not lot_valid:
            return False, lot_reason

        # ✅ Tous les checks passés !
        logger.info("✅ Signal validé avec succès!")
        return True, "✅ Signal approuvé"

    # ----------------------------------------
    # PROTECTIONS ANTI-CRAMAGE
    # ----------------------------------------

    def _is_news_nearby(self, buffer_hours: int = NEWS_BUFFER_HOURS) -> bool:
        """Vérifie si une news High Impact est proche"""
        # TODO: Intégrer API calendrier économique
        # Pour l'instant, retourne False (à implémenter avec API)
        return False

    def _count_trades_today(self) -> int:
        """Compte le nombre de trades aujourd'hui"""
        today = datetime.now().date().isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM trades WHERE DATE(timestamp) = ?",
            (today,)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def _count_open_positions(self) -> int:
        """Compte les positions actuellement ouvertes"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM trades WHERE status = 'OPEN'")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def _is_daily_risk_exceeded(self) -> bool:
        """Vérifie si le risque journalier max est atteint"""
        today = datetime.now().date().isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT total_profit_loss FROM daily_stats WHERE date = ?",
            (today,)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            daily_loss = abs(min(0, result[0]))
            max_daily_loss = self.config['account_balance'] * self.config['max_daily_risk']
            return daily_loss >= max_daily_loss

        return False

    def _detect_revenge_trading(self) -> bool:
        """
        Détecte le revenge trading:
        - 2 pertes consécutives + trade dans les 10 minutes
        """
        if self.consecutive_losses < REVENGE_TRADING_CONFIG['consecutive_losses_trigger']:
            return False

        if self.last_trade_time is None:
            return False

        time_since_last = (datetime.now() - self.last_trade_time).total_seconds() / 60

        if time_since_last < REVENGE_TRADING_CONFIG['rapid_trade_window_minutes']:
            logger.warning("⚠️ REVENGE TRADING DÉTECTÉ!")
            self._send_telegram_alert("🚨 REVENGE TRADING DÉTECTÉ - Pause forcée 2h")
            return True

        return False

    def _detect_overtrading(self) -> bool:
        """Détecte l'overtrading"""
        # Trades dans la dernière heure
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        one_hour_ago = (datetime.now() - timedelta(hours=1)).isoformat()

        cursor.execute(
            "SELECT COUNT(*) FROM trades WHERE timestamp > ?",
            (one_hour_ago,)
        )
        trades_last_hour = cursor.fetchone()[0]
        conn.close()

        if trades_last_hour > OVERTRADING_CONFIG['max_trades_per_hour']:
            logger.warning(f"⚠️ Overtrading: {trades_last_hour} trades en 1h")
            return True

        return False

    def _validate_stop_loss(self, signal: Dict) -> Tuple[bool, str]:
        """Valide que le SL est dans les limites"""
        sl_pips = signal.get('sl_pips', 0)

        if sl_pips < self.config['sl_min_pips']:
            return False, f"❌ SL trop serré: {sl_pips} pips (min {self.config['sl_min_pips']})"

        if sl_pips > self.config['sl_max_pips']:
            return False, f"❌ SL trop large: {sl_pips} pips (max {self.config['sl_max_pips']})"

        return True, "✅ SL valide"

    def _validate_lot_size(self, signal: Dict) -> Tuple[bool, str]:
        """Valide la taille du lot"""
        lot_size = signal.get('lot_size', 0)
        sl_pips = signal.get('sl_pips', 0)

        # Calculer le lot attendu
        expected_lot = calculate_position_size(
            self.config['account_balance'],
            self.config['risk_per_trade'],
            sl_pips
        )

        # Tolérance de 10%
        if abs(lot_size - expected_lot) / expected_lot > 0.10:
            return False, f"❌ Lot size anormal: {lot_size} (attendu ~{expected_lot})"

        return True, "✅ Lot size valide"

    # ----------------------------------------
    # KILL SWITCH CHECKS
    # ----------------------------------------
    def check_kill_switch_triggers(self) -> Tuple[bool, List[str]]:
        """
        Vérifie tous les triggers du Kill Switch

        Returns:
            (should_activate: bool, reasons: List[str])
        """
        triggers = []

        # 1. Perte journalière max
        today = datetime.now().date().isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT total_profit_loss FROM daily_stats WHERE date = ?",
            (today,)
        )
        result = cursor.fetchone()

        if result:
            daily_pnl = result[0]
            if daily_pnl <= -self.config['kill_switch']['max_daily_loss']:
                triggers.append(f"Perte journalière: {daily_pnl}€")

        # 2. Drawdown max
        current_balance = self.config['account_balance'] + (daily_pnl if result else 0)
        drawdown = self.max_balance_today - current_balance

        if drawdown >= self.config['kill_switch']['max_drawdown']:
            triggers.append(f"Drawdown: {drawdown}€")

        # 3. Win rate trop faible
        cursor.execute(
            "SELECT winning_trades, total_trades FROM daily_stats WHERE date = ?",
            (today,)
        )
        result = cursor.fetchone()

        if result:
            winning, total = result
            if total >= self.config['kill_switch']['min_trades_for_winrate']:
                win_rate = winning / total if total > 0 else 0
                if win_rate < self.config['kill_switch']['min_win_rate']:
                    triggers.append(f"Win rate: {win_rate*100:.1f}%")

        # 4. Pertes consécutives
        if self.consecutive_losses >= self.config['max_consecutive_losses']:
            triggers.append(f"{self.consecutive_losses} pertes consécutives")

        # 5. Overtrading
        cursor.execute(
            "SELECT COUNT(*) FROM trades WHERE DATE(timestamp) = ?",
            (today,)
        )
        trades_today = cursor.fetchone()[0]

        if trades_today >= 8:  # Hard limit
            triggers.append(f"Overtrading: {trades_today} trades aujourd'hui")

        conn.close()

        return len(triggers) > 0, triggers

    def activate_kill_switch(self, reasons: List[str]):
        """Active le Kill Switch"""
        self.kill_switch_active = True
        logger.critical("🚨 KILL SWITCH ACTIVÉ!")

        for reason in reasons:
            logger.critical(f"   - {reason}")

        # Enregistrer en DB
        today = datetime.now().date().isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE daily_stats SET kill_switch_triggered = 1 WHERE date = ?",
            (today,)
        )
        conn.commit()
        conn.close()

        # Alerte Telegram
        message = "🚨 *KILL SWITCH ACTIVÉ - FOREX*\n\n"
        message += "Raisons:\n"
        for reason in reasons:
            message += f"  ❌ {reason}\n"
        message += "\n⛔ *TRADING ARRÊTÉ JUSQU'À DEMAIN*"

        self._send_telegram_alert(message)

    # ----------------------------------------
    # ENREGISTREMENT TRADES
    # ----------------------------------------
    def record_signal(self, signal: Dict, approved: bool, reason: str):
        """Enregistre un signal dans la DB"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO signals (timestamp, pair, direction, confluence_score, approved, rejected, rejection_reason, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            signal.get('pair'),
            signal.get('direction'),
            signal.get('confluence_score', 0),
            1 if approved else 0,
            0 if approved else 1,
            None if approved else reason,
            json.dumps(signal)
        ))

        conn.commit()
        conn.close()

    def record_trade(self, trade: Dict):
        """Enregistre un trade dans la DB"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO trades (
                timestamp, pair, direction, entry_price, sl_price,
                tp1_price, tp2_price, tp3_price, lot_size, confluence_score, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            trade.get('pair'),
            trade.get('direction'),
            trade.get('entry_price'),
            trade.get('sl_price'),
            trade.get('tp1_price'),
            trade.get('tp2_price'),
            trade.get('tp3_price'),
            trade.get('lot_size'),
            trade.get('confluence_score', 0),
            json.dumps(trade)
        ))

        conn.commit()
        conn.close()

        self.last_trade_time = datetime.now()

    def update_trade_result(self, trade_id: int, result: str, pnl: float):
        """Met à jour le résultat d'un trade"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE trades
            SET status = ?, profit_loss = ?, exit_time = ?
            WHERE id = ?
        ''', (result, pnl, datetime.now().isoformat(), trade_id))

        # Mettre à jour stats du jour
        today = datetime.now().date().isoformat()
        cursor.execute(
            "SELECT total_profit_loss FROM daily_stats WHERE date = ?",
            (today,)
        )
        row = cursor.fetchone()

        if row:
            new_pnl = row[0] + pnl
            cursor.execute(
                "UPDATE daily_stats SET total_profit_loss = ? WHERE date = ?",
                (new_pnl, today)
            )
        else:
            cursor.execute(
                "INSERT INTO daily_stats (date, total_profit_loss) VALUES (?, ?)",
                (today, pnl)
            )

        conn.commit()
        conn.close()

        # Mettre à jour consecutive losses
        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

        self.daily_pnl += pnl

        # Vérifier Kill Switch
        should_activate, reasons = self.check_kill_switch_triggers()
        if should_activate and not self.kill_switch_active:
            self.activate_kill_switch(reasons)

    # ----------------------------------------
    # TELEGRAM ALERTS
    # ----------------------------------------
    def _send_telegram_alert(self, message: str):
        """Envoie une alerte via Telegram"""
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(url, data=data)
            logger.info(f"✅ Alerte Telegram envoyée")
        except Exception as e:
            logger.error(f"❌ Erreur envoi Telegram: {e}")

    # ----------------------------------------
    # STATS
    # ----------------------------------------
    def get_daily_stats(self) -> Dict:
        """Retourne les stats du jour"""
        today = datetime.now().date().isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM daily_stats WHERE date = ?",
            (today,)
        )
        row = cursor.fetchone()

        cursor.execute(
            "SELECT COUNT(*) FROM trades WHERE DATE(timestamp) = ? AND status = 'OPEN'",
            (today,)
        )
        open_positions = cursor.fetchone()[0]

        conn.close()

        if row:
            return {
                "date": row[0],
                "total_trades": row[1],
                "winning_trades": row[2],
                "losing_trades": row[3],
                "total_pnl": row[4],
                "max_drawdown": row[5],
                "kill_switch_active": bool(row[6]),
                "open_positions": open_positions,
            }
        else:
            return {
                "date": today,
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "total_pnl": 0.0,
                "max_drawdown": 0.0,
                "kill_switch_active": False,
                "open_positions": 0,
            }

    # ----------------------------------------
    # ANALYSE DE MARCHÉ
    # ----------------------------------------
    def analyze_pair(self, pair: str) -> Dict:
        """
        Analyse détaillée d'une paire

        Note: Pour l'instant retourne des données mockées.
        À implémenter: récupération réelle des indicateurs depuis MT5.
        """
        import random

        # Données mockées pour demonstration
        score = random.randint(65, 95)
        min_score = self.config['min_confluence_score']

        return {
            "pair": pair,
            "timestamp": datetime.now().isoformat(),
            "indicators": {
                "ema_20": round(random.uniform(1.08, 1.10), 5) if "EUR" in pair else round(random.uniform(2450, 2460), 2),
                "ema_50": round(random.uniform(1.08, 1.10), 5) if "EUR" in pair else round(random.uniform(2450, 2460), 2),
                "ema_200": round(random.uniform(1.08, 1.10), 5) if "EUR" in pair else round(random.uniform(2450, 2460), 2),
                "rsi": round(random.uniform(35, 65), 1),
                "macd": round(random.uniform(-0.0005, 0.0005), 5),
                "atr": round(random.uniform(0.0003, 0.0008), 5) if "EUR" in pair else round(random.uniform(5, 15), 1),
            },
            "confluence_score": score,
            "score_breakdown": {
                "smc": min(40, int(score * 0.4)),
                "timeframe": min(25, int(score * 0.25)),
                "indicators": min(20, int(score * 0.20)),
                "structure": min(10, int(score * 0.10)),
                "pattern": min(5, int(score * 0.05)),
            },
            "decision": "BUY" if score >= min_score and random.random() > 0.5 else "NO_TRADE",
            "rejection_reason": f"Score insuffisant ({score}/{min_score})" if score < min_score else None,
            "details": {
                "EMAs alignées": random.choice([True, False]),
                "RSI favorable": random.choice([True, False]),
                "Order Block détecté": random.choice([True, False]),
                "FVG aligné": random.choice([True, False]),
                "BOS confirmé": random.choice([True, False]),
            }
        }

    def get_market_report(self) -> Dict:
        """
        Rapport marché complet pour toutes les paires Forex

        Note: Données mockées pour demonstration.
        À implémenter: analyse réelle de toutes les paires.
        """
        pairs = self.config['pairs']
        pairs_data = []
        best_score = 0
        best_pair = None

        for pair in pairs:
            analysis = self.analyze_pair(pair)
            score = analysis['confluence_score']

            pairs_data.append({
                "pair": pair,
                "confluence_score": score,
                "decision": analysis['decision']
            })

            if score > best_score:
                best_score = score
                best_pair = pair

        return {
            "timestamp": datetime.now().isoformat(),
            "pairs": pairs_data,
            "best_opportunity": {
                "pair": best_pair,
                "score": best_score
            } if best_pair else None,
            "economic_calendar": {
                "next_event": "CPI USA dans 3h15" if datetime.now().hour < 14 else None
            }
        }

    def get_rejected_signals(self) -> Dict:
        """
        Historique des signaux rejetés avec raisons

        Note: Pour l'instant retourne données mockées.
        À implémenter: logging complet des rejections dans DB.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Récupérer les 10 derniers signaux rejetés
        cursor.execute("""
            SELECT timestamp, pair, metadata
            FROM signals
            WHERE approved = 0
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()

        recent_rejections = []
        scores = []

        for row in rows:
            timestamp, pair, metadata_json = row
            try:
                metadata = json.loads(metadata_json) if metadata_json else {}
                score = metadata.get('confluence_score', 0)
                reason = metadata.get('rejection_reason', 'Score insuffisant')

                # Formater le timestamp
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M")

                recent_rejections.append({
                    "time": time_str,
                    "pair": pair,
                    "score": score,
                    "reason": reason
                })

                scores.append(score)
            except:
                pass

        conn.close()

        # Stats
        avg_score = sum(scores) / len(scores) if scores else 0
        best_score = max(scores) if scores else 0

        return {
            "recent_rejections": recent_rejections,
            "stats": {
                "analyzed": len(recent_rejections),
                "avg_score": round(avg_score, 1),
                "best_score": best_score
            }
        }


# ========================================
# INSTANCE GLOBALE
# ========================================
guardian = ForexGuardian()

# ========================================
# ROUTES API FLASK
# ========================================

@app.route('/health', methods=['GET'])
def health_check():
    """Check de santé de l'API"""
    return jsonify({
        "status": "OK",
        "system": "FOREX",
        "kill_switch_active": guardian.kill_switch_active,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/validate_signal', methods=['POST'])
def validate_signal():
    """
    Validation d'un signal depuis MT5

    Body JSON:
    {
        "pair": "EURUSD",
        "direction": "BUY" ou "SELL",
        "entry_price": 1.0950,
        "sl_price": 1.0900,
        "sl_pips": 50,
        "tp1_price": 1.1050,
        "tp2_price": 1.1100,
        "tp3_price": 1.1200,
        "lot_size": 0.5,
        "confluence_score": 95,
        "metadata": {...}
    }
    """
    try:
        signal = request.get_json()
        logger.info(f"📥 Signal reçu: {signal.get('pair')} {signal.get('direction')}")

        # Validation
        approved, reason = guardian.validate_signal(signal)

        # Enregistrer
        guardian.record_signal(signal, approved, reason)

        # Notification Telegram si approuvé
        if approved:
            message = f"✅ *SIGNAL APPROUVÉ - FOREX*\n\n"
            message += f"Paire: {signal.get('pair')}\n"
            message += f"Direction: {signal.get('direction')}\n"
            message += f"Confluence: {signal.get('confluence_score')}/100\n"
            message += f"Entry: {signal.get('entry_price')}\n"
            message += f"SL: {signal.get('sl_price')} ({signal.get('sl_pips')} pips)\n"
            message += f"TP1: {signal.get('tp1_price')}\n"
            guardian._send_telegram_alert(message)

        return jsonify({
            "approved": approved,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"❌ Erreur validation signal: {e}")
        return jsonify({"approved": False, "reason": f"Erreur: {str(e)}"}), 500


@app.route('/record_trade', methods=['POST'])
def record_trade():
    """Enregistre un trade ouvert"""
    try:
        trade = request.get_json()
        guardian.record_trade(trade)
        return jsonify({"status": "OK", "message": "Trade enregistré"})
    except Exception as e:
        logger.error(f"❌ Erreur enregistrement trade: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500


@app.route('/update_trade', methods=['POST'])
def update_trade():
    """Met à jour un trade (fermé)"""
    try:
        data = request.get_json()
        trade_id = data.get('trade_id')
        result = data.get('result')  # "WIN" ou "LOSS"
        pnl = data.get('pnl', 0.0)

        guardian.update_trade_result(trade_id, result, pnl)

        return jsonify({"status": "OK", "message": "Trade mis à jour"})
    except Exception as e:
        logger.error(f"❌ Erreur update trade: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Retourne les statistiques"""
    stats = guardian.get_daily_stats()
    return jsonify(stats)


@app.route('/kill_switch/activate', methods=['POST'])
def activate_kill_switch_manual():
    """Active manuellement le Kill Switch"""
    guardian.activate_kill_switch(["Activation manuelle"])
    return jsonify({"status": "OK", "message": "Kill Switch activé"})


@app.route('/kill_switch/deactivate', methods=['POST'])
def deactivate_kill_switch():
    """Désactive le Kill Switch (nouveau jour)"""
    guardian.kill_switch_active = False
    guardian.consecutive_losses = 0
    guardian.daily_pnl = 0.0
    logger.info("✅ Kill Switch désactivé")
    return jsonify({"status": "OK", "message": "Kill Switch désactivé"})


@app.route('/analyze/<pair>', methods=['GET'])
def analyze_pair(pair):
    """Analyse détaillée d'une paire"""
    try:
        analysis = guardian.analyze_pair(pair)
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"❌ Erreur analyse {pair}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/market_report', methods=['GET'])
def market_report():
    """Rapport marché complet"""
    try:
        report = guardian.get_market_report()
        return jsonify(report)
    except Exception as e:
        logger.error(f"❌ Erreur market_report: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/rejected_signals', methods=['GET'])
def rejected_signals():
    """Historique des signaux rejetés"""
    try:
        rejections = guardian.get_rejected_signals()
        return jsonify(rejections)
    except Exception as e:
        logger.error(f"❌ Erreur rejected_signals: {e}")
        return jsonify({"error": str(e)}), 500


# ========================================
# MAIN
# ========================================
def main():
    """Point d'entrée principal"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🐺 FOREX GUARDIAN - La Bête 🐺              ║
║                                                          ║
║          Système de Protection Anti-Cramage              ║
║                   7 Niveaux de Sécurité                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

    # Créer dossier logs si nécessaire
    Path("logs").mkdir(exist_ok=True)

    # Initialiser DB
    init_database()

    # Vérifier trading autorisé
    allowed, reason = is_trading_allowed()
    if not allowed:
        logger.warning(f"⚠️ Trading non autorisé: {reason}")
        guardian._send_telegram_alert(f"⚠️ Trading FOREX non autorisé: {reason}")

    # Lancer Flask
    port = FOREX_CONFIG['guardian_port']
    logger.info(f"🚀 Guardian Forex démarré sur port {port}")
    guardian._send_telegram_alert("🐺 *FOREX GUARDIAN DÉMARRÉ*\n\nSystème opérationnel ✅")

    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == "__main__":
    main()

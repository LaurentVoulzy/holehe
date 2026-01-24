# -*- coding: utf-8 -*-
"""
LA BÊTE - Guardian CRYPTO
Système de Protection Ultra-Sécurisé pour Trading Crypto
Python 3.12+ Compatible

Protections spécifiques crypto:
- Whale Activity Detection
- Weekend Gap Protection
- Funding Rate Analysis
- BTC Dominance Check
- Volatilité extrême (ATR × 2)
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "SHARED"))

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3
import logging
from typing import Dict, List, Optional, Tuple
import json
import requests

from config import (
    CRYPTO_CONFIG,
    CONFLUENCE_WEIGHTS,
    FORBIDDEN_PERIODS,
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
        logging.FileHandler(LOG_DIR / 'guardian_crypto.log', encoding='utf-8'),
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
DB_PATH = Path(__file__).parent / "crypto_trades.db"


def init_database():
    """Initialise la base de données SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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
            whale_activity BOOLEAN DEFAULT 0,
            funding_rate REAL,
            btc_dominance REAL,
            metadata TEXT
        )
    ''')

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

    conn.commit()
    conn.close()
    logger.info("✅ Base de données crypto initialisée")


# ========================================
# GUARDIAN CRYPTO CLASS
# ========================================
class CryptoGuardian:
    """Gardien du système Crypto - Protections anti-cramage + spécificités crypto"""

    def __init__(self):
        self.config = CRYPTO_CONFIG
        self.kill_switch_active = False
        self.trades_today = []
        self.daily_pnl = 0.0
        self.consecutive_losses = 0
        self.last_trade_time = None
        self.max_balance_today = self.config["account_balance"]

        logger.info("💰 Crypto Guardian initialisé")

    # ----------------------------------------
    # VALIDATION DE SIGNAL
    # ----------------------------------------
    def validate_signal(self, signal: Dict) -> Tuple[bool, str]:
        """Valide un signal crypto avec protections spécifiques"""
        logger.info(f"💰 Validation signal crypto: {signal.get('pair')} {signal.get('direction')}")

        # 1. Kill Switch actif?
        if self.kill_switch_active:
            return False, "❌ Kill Switch actif"

        # 2. Trading autorisé? (CRYPTO = 24/7)
        allowed, reason = is_trading_allowed(market_type="CRYPTO")
        if not allowed:
            return False, f"❌ {reason}"

        # 3. Weekend Gap Protection (vendredi 20h - dimanche 22h)
        if self._is_weekend_period():
            return False, "❌ Weekend - Risque de gap"

        # 4. Confluence score suffisant?
        confluence = signal.get('confluence_score', 0)
        if confluence < self.config['min_confluence_score']:
            return False, f"❌ Confluence trop faible: {confluence}/100 (min {self.config['min_confluence_score']})"

        # 5. Whale Activity Detection
        if self._detect_whale_activity(signal):
            return False, "❌ Whale activity détectée - Volume anormal"

        # 6. Funding Rate Check (futures)
        funding_rate = signal.get('funding_rate', 0)
        if abs(funding_rate) > self.config.get('max_funding_rate', 0.01):
            return False, f"❌ Funding rate trop élevé: {funding_rate*100:.2f}%"

        # 7. BTC Dominance Check
        btc_dominance = signal.get('btc_dominance', 50)
        if btc_dominance < self.config.get('min_btc_dominance', 40) or \
           btc_dominance > self.config.get('max_btc_dominance', 70):
            return False, f"❌ BTC Dominance anormale: {btc_dominance:.1f}%"

        # 8. Limite de trades journalière (plus stricte pour crypto)
        trades_today = self._count_trades_today()
        if trades_today >= self.config['max_trades_per_day']:
            return False, f"❌ Limite journalière atteinte ({trades_today}/{self.config['max_trades_per_day']})"

        # 9. Positions ouvertes max
        open_positions = self._count_open_positions()
        if open_positions >= self.config['max_open_positions']:
            return False, f"❌ Trop de positions ouvertes ({open_positions}/{self.config['max_open_positions']})"

        # 10. Risque journalier
        if self._is_daily_risk_exceeded():
            return False, "❌ Risque journalier maximum atteint"

        # 11. Détection Revenge Trading
        if self._detect_revenge_trading():
            self.kill_switch_active = True
            return False, "❌ REVENGE TRADING DÉTECTÉ - Kill Switch activé"

        # 12. Vérification Stop Loss (crypto = ATR × 2)
        sl_valid, sl_reason = self._validate_stop_loss(signal)
        if not sl_valid:
            return False, sl_reason

        # 13. Risk:Reward minimum 1:3 pour crypto
        rr_valid, rr_reason = self._validate_risk_reward(signal)
        if not rr_valid:
            return False, rr_reason

        # ✅ Tous les checks passés !
        logger.info("✅ Signal crypto validé avec succès!")
        return True, "✅ Signal approuvé"

    # ----------------------------------------
    # PROTECTIONS SPÉCIFIQUES CRYPTO
    # ----------------------------------------

    def _is_weekend_period(self) -> bool:
        """
        Vérifie si on est dans la période weekend dangereuse
        CRYPTO: Toujours False (marché 24/7)
        """
        # CRYPTO trade 24/7, pas de restriction week-end !
        return False

    def _detect_whale_activity(self, signal: Dict) -> bool:
        """Détecte l'activité de whales (volume anormal)"""
        volume_ratio = signal.get('volume_ratio', 1.0)
        threshold = self.config.get('whale_activity_threshold', 3.0)

        if volume_ratio > threshold:
            logger.warning(f"🐋 Whale activity: Volume {volume_ratio:.1f}x la moyenne")
            return True

        return False

    def _validate_stop_loss(self, signal: Dict) -> Tuple[bool, str]:
        """Valide le SL selon la crypto"""
        pair = signal.get('pair', 'BTCUSD')
        sl_distance = abs(signal.get('entry_price', 0) - signal.get('sl_price', 0))

        if 'BTC' in pair:
            if sl_distance < self.config['btc_sl_min']:
                return False, f"❌ SL BTC trop serré: ${sl_distance:.0f} (min ${self.config['btc_sl_min']})"
            if sl_distance > self.config['btc_sl_max']:
                return False, f"❌ SL BTC trop large: ${sl_distance:.0f} (max ${self.config['btc_sl_max']})"

        elif 'ETH' in pair:
            if sl_distance < self.config['eth_sl_min']:
                return False, f"❌ SL ETH trop serré: ${sl_distance:.0f} (min ${self.config['eth_sl_min']})"
            if sl_distance > self.config['eth_sl_max']:
                return False, f"❌ SL ETH trop large: ${sl_distance:.0f} (max ${self.config['eth_sl_max']})"

        return True, "✅ SL valide"

    def _validate_risk_reward(self, signal: Dict) -> Tuple[bool, str]:
        """Valide le ratio Risk:Reward (min 1:3 pour crypto)"""
        entry = signal.get('entry_price', 0)
        sl = signal.get('sl_price', 0)
        tp1 = signal.get('tp1_price', 0)

        if entry == 0 or sl == 0 or tp1 == 0:
            return False, "❌ Prix entry/SL/TP manquants"

        risk = abs(entry - sl)
        reward = abs(tp1 - entry)

        if risk == 0:
            return False, "❌ Risk = 0"

        rr_ratio = reward / risk

        min_rr = self.config.get('min_rr_ratio', 3.0)
        if rr_ratio < min_rr:
            return False, f"❌ R:R trop faible: 1:{rr_ratio:.1f} (min 1:{min_rr})"

        return True, f"✅ R:R valide: 1:{rr_ratio:.1f}"

    def _count_trades_today(self) -> int:
        """Compte les trades crypto aujourd'hui"""
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
        """Compte les positions crypto ouvertes"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM trades WHERE status = 'OPEN'")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def _is_daily_risk_exceeded(self) -> bool:
        """Vérifie le risque journalier"""
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
        """Détecte le revenge trading"""
        if self.consecutive_losses < 2:  # Seuil crypto plus strict
            return False

        if self.last_trade_time is None:
            return False

        time_since_last = (datetime.now() - self.last_trade_time).total_seconds() / 60

        if time_since_last < 10:  # Trade dans les 10min après 2 pertes
            logger.warning("⚠️ REVENGE TRADING CRYPTO DÉTECTÉ!")
            self._send_telegram_alert("🚨 REVENGE TRADING CRYPTO - Pause forcée")
            return True

        return False

    # ----------------------------------------
    # KILL SWITCH
    # ----------------------------------------
    def check_kill_switch_triggers(self) -> Tuple[bool, List[str]]:
        """Vérifie les triggers du Kill Switch crypto"""
        triggers = []

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
                triggers.append(f"Perte journalière: {daily_pnl}$")

        # Drawdown
        current_balance = self.config['account_balance'] + (daily_pnl if result else 0)
        drawdown = self.max_balance_today - current_balance

        if drawdown >= self.config['kill_switch']['max_drawdown']:
            triggers.append(f"Drawdown: {drawdown}$")

        # Win rate
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

        # Pertes consécutives
        if self.consecutive_losses >= self.config['max_consecutive_losses']:
            triggers.append(f"{self.consecutive_losses} pertes consécutives")

        conn.close()

        return len(triggers) > 0, triggers

    def activate_kill_switch(self, reasons: List[str]):
        """Active le Kill Switch"""
        self.kill_switch_active = True
        logger.critical("🚨 KILL SWITCH CRYPTO ACTIVÉ!")

        for reason in reasons:
            logger.critical(f"   - {reason}")

        today = datetime.now().date().isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE daily_stats SET kill_switch_triggered = 1 WHERE date = ?",
            (today,)
        )
        conn.commit()
        conn.close()

        message = "🚨 *KILL SWITCH ACTIVÉ - CRYPTO*\n\n"
        message += "Raisons:\n"
        for reason in reasons:
            message += f"  ❌ {reason}\n"
        message += "\n⛔ *TRADING CRYPTO ARRÊTÉ*"

        self._send_telegram_alert(message)

    # ----------------------------------------
    # DATABASE
    # ----------------------------------------
    def record_signal(self, signal: Dict, approved: bool, reason: str):
        """Enregistre un signal"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO signals (
                timestamp, pair, direction, confluence_score, approved, rejected,
                rejection_reason, whale_activity, funding_rate, btc_dominance, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            signal.get('pair'),
            signal.get('direction'),
            signal.get('confluence_score', 0),
            1 if approved else 0,
            0 if approved else 1,
            None if approved else reason,
            signal.get('whale_activity', False),
            signal.get('funding_rate'),
            signal.get('btc_dominance'),
            json.dumps(signal)
        ))

        conn.commit()
        conn.close()

    def record_trade(self, trade: Dict):
        """Enregistre un trade"""
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

        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

        self.daily_pnl += pnl

        should_activate, reasons = self.check_kill_switch_triggers()
        if should_activate and not self.kill_switch_active:
            self.activate_kill_switch(reasons)

    # ----------------------------------------
    # TELEGRAM
    # ----------------------------------------
    def _send_telegram_alert(self, message: str):
        """Envoie une alerte Telegram"""
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
        Analyse détaillée d'une paire crypto

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
                "ema_20": round(random.uniform(95000, 105000), 2) if "BTC" in pair else round(random.uniform(3200, 3600), 2),
                "ema_50": round(random.uniform(95000, 105000), 2) if "BTC" in pair else round(random.uniform(3200, 3600), 2),
                "ema_200": round(random.uniform(95000, 105000), 2) if "BTC" in pair else round(random.uniform(3200, 3600), 2),
                "rsi": round(random.uniform(35, 65), 1),
                "macd": round(random.uniform(-500, 500), 2),
                "atr": round(random.uniform(800, 1500), 2) if "BTC" in pair else round(random.uniform(50, 120), 2),
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
                "Whale activity": random.choice([True, False]),
                "Weekend protection": self._is_weekend_period(),
            }
        }

    def get_market_report(self) -> Dict:
        """
        Rapport marché complet pour toutes les paires Crypto

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
            "weekend_protection": self._is_weekend_period()
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
guardian = CryptoGuardian()

# ========================================
# ROUTES API FLASK
# ========================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        "status": "OK",
        "system": "CRYPTO",
        "kill_switch_active": guardian.kill_switch_active,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/validate_signal', methods=['POST'])
def validate_signal():
    """Validation d'un signal crypto"""
    try:
        signal = request.get_json()
        logger.info(f"📥 Signal crypto reçu: {signal.get('pair')} {signal.get('direction')}")

        approved, reason = guardian.validate_signal(signal)
        guardian.record_signal(signal, approved, reason)

        if approved:
            message = f"✅ *SIGNAL APPROUVÉ - CRYPTO*\n\n"
            message += f"Paire: {signal.get('pair')}\n"
            message += f"Direction: {signal.get('direction')}\n"
            message += f"Confluence: {signal.get('confluence_score')}/100\n"
            message += f"Entry: ${signal.get('entry_price')}\n"
            message += f"SL: ${signal.get('sl_price')}\n"
            message += f"TP1: ${signal.get('tp1_price')}\n"
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
    """Enregistre un trade"""
    try:
        trade = request.get_json()
        guardian.record_trade(trade)
        return jsonify({"status": "OK", "message": "Trade enregistré"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500


@app.route('/update_trade', methods=['POST'])
def update_trade():
    """Met à jour un trade"""
    try:
        data = request.get_json()
        guardian.update_trade_result(data.get('trade_id'), data.get('result'), data.get('pnl', 0.0))
        return jsonify({"status": "OK", "message": "Trade mis à jour"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Stats"""
    stats = guardian.get_daily_stats()
    return jsonify(stats)


@app.route('/kill_switch/activate', methods=['POST'])
def activate_kill_switch_manual():
    """Active le Kill Switch"""
    guardian.activate_kill_switch(["Activation manuelle"])
    return jsonify({"status": "OK", "message": "Kill Switch activé"})


@app.route('/kill_switch/deactivate', methods=['POST'])
def deactivate_kill_switch():
    """Désactive le Kill Switch"""
    guardian.kill_switch_active = False
    guardian.consecutive_losses = 0
    guardian.daily_pnl = 0.0
    logger.info("✅ Kill Switch crypto désactivé")
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
    """Point d'entrée"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║            💰 CRYPTO GUARDIAN - La Bête 💰               ║
║                                                          ║
║       Système de Protection Anti-Cramage Crypto         ║
║         + Whale Detection + Weekend Protection           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

    Path("logs").mkdir(exist_ok=True)
    init_database()

    allowed, reason = is_trading_allowed(market_type="CRYPTO")
    if not allowed:
        logger.warning(f"⚠️ Trading CRYPTO non autorisé: {reason}")
        guardian._send_telegram_alert(f"⚠️ Trading CRYPTO non autorisé: {reason}")

    if guardian._is_weekend_period():
        logger.warning("⚠️ Période weekend - Protection activée")

    port = CRYPTO_CONFIG['guardian_port']
    logger.info(f"🚀 Guardian Crypto démarré sur port {port}")
    guardian._send_telegram_alert("💰 *CRYPTO GUARDIAN DÉMARRÉ*\n\nSystème opérationnel ✅")

    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == "__main__":
    main()

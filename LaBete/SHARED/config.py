# -*- coding: utf-8 -*-
"""
LA BÊTE - Configuration Globale
Système Dual Forex + Crypto Ultra-Sécurisé pour Prop Firm
Python 3.12+ Compatible
"""

from datetime import datetime
from typing import Dict, List

# ========================================
# IDENTIFIANTS UTILISATEUR
# ========================================
TELEGRAM_BOT_TOKEN = "8530848109:AAE0VkNIWpvDBuqUi0nZeXlluURnEMOHuwE"
TELEGRAM_CHAT_ID = "1981386789"
USER_EMAIL = "kykylou30@gmail.com"

# ========================================
# CONFIGURATION FOREX
# ========================================
FOREX_CONFIG = {
    # Paires tradées
    "pairs": ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
    "primary_pair": "EURUSD",

    # Compte MT5
    "mt5_account": 1512301052,  # Compte FTMO Demo
    "mt5_password": "15x*Js?w@",  # Mot de passe FTMO (lecture seule)
    "mt5_server": "FTMO-Demo",  # Serveur FTMO

    # Capital et risque
    "account_balance": 40000,  # FTMO 40K€
    "currency": "EUR",
    "risk_per_trade": 0.003,  # 0.3% par trade
    "max_daily_risk": 0.01,   # 1% max par jour
    "max_weekly_risk": 0.03,  # 3% max par semaine

    # Timeframes
    "primary_timeframe": "M30",
    "confirmation_timeframes": ["H1", "H4"],

    # Limites de trading
    "max_trades_per_day": 3,
    "max_open_positions": 2,
    "max_consecutive_losses": 3,

    # Stop Loss / Take Profit (Paires Forex standard)
    "sl_min_pips": 50,
    "sl_max_pips": 150,
    "atr_multiplier_sl": 1.5,

    # Stop Loss / Take Profit spécifique XAUUSD (Gold)
    "xauusd_sl_min_pips": 200,     # 200 pips min pour Gold ($20)
    "xauusd_sl_max_pips": 800,     # 800 pips max pour Gold ($80)
    "xauusd_atr_multiplier": 2.0,  # ATR x2 pour Gold (plus volatile)
    "xauusd_risk_percent": 0.0025, # 0.25% pour Gold (légèrement réduit)

    "tp_levels": [
        {"ratio": 2.0, "close_percent": 50},  # TP1: 1:2, ferme 50%
        {"ratio": 3.0, "close_percent": 30},  # TP2: 1:3, ferme 30%
        {"ratio": 5.0, "close_percent": 20},  # TP3: 1:5, ferme 20%
    ],

    # Break Even
    "break_even_activation": 0.5,  # 50% du chemin vers TP1
    "break_even_offset_pips": 10,

    # Trailing Stop
    "trailing_activation_after_tp1": True,
    "trailing_atr_percent": 0.5,  # 50% de l'ATR

    # Confluence minimum
    "min_confluence_score": 90,  # Sur 100

    # Kill Switch
    "kill_switch": {
        "max_daily_loss": 400,  # €
        "max_drawdown": 3000,   # €
        "min_win_rate": 0.35,   # 35%
        "min_trades_for_winrate": 15,
    },

    # Guardian API
    "guardian_api_url": "http://localhost:5000",
    "guardian_port": 5000,
}

# ========================================
# CONFIGURATION CRYPTO
# ========================================
CRYPTO_CONFIG = {
    # Paires tradées
    "pairs": ["BTCUSD", "ETHUSD"],
    "primary_pair": "BTCUSD",

    # Compte MT5
    "mt5_account": 1512301052,  # Compte FTMO Demo (même compte que Forex)
    "mt5_password": "15x*Js?w@",  # Mot de passe FTMO (lecture seule)
    "mt5_server": "FTMO-Demo",  # Serveur FTMO

    # Capital et risque
    "account_balance": 40000,  # FTMO 40K€
    "currency": "EUR",
    "risk_per_trade": 0.002,  # 0.2% par trade (plus volatile)
    "max_daily_risk": 0.008,  # 0.8% max par jour
    "max_weekly_risk": 0.025,  # 2.5% max par semaine

    # Timeframes
    "primary_timeframe": "M30",
    "confirmation_timeframes": ["H1", "H4"],

    # Limites de trading
    "max_trades_per_day": 2,  # Crypto plus risqué
    "max_open_positions": 1,
    "max_consecutive_losses": 2,

    # Stop Loss / Take Profit
    "btc_sl_min": 200,   # $
    "btc_sl_max": 1000,  # $
    "eth_sl_min": 20,    # $
    "eth_sl_max": 100,   # $
    "atr_multiplier_sl": 2.0,  # ATR x2 pour crypto
    "min_rr_ratio": 3.0,  # Minimum 1:3
    "tp_levels": [
        {"ratio": 3.0, "close_percent": 50},  # TP1: 1:3, ferme 50%
        {"ratio": 4.0, "close_percent": 30},  # TP2: 1:4, ferme 30%
        {"ratio": 6.0, "close_percent": 20},  # TP3: 1:6, ferme 20%
    ],

    # Break Even
    "break_even_activation": 0.4,  # 40% du chemin vers TP1
    "break_even_offset_percent": 0.005,  # 0.5%

    # Trailing Stop
    "trailing_activation_after_tp1": True,
    "trailing_atr_percent": 0.6,  # 60% de l'ATR

    # Confluence minimum
    "min_confluence_score": 85,  # Sur 100 (moins strict que forex)

    # Kill Switch
    "kill_switch": {
        "max_daily_loss": 400,  # €
        "max_drawdown": 3000,   # €
        "min_win_rate": 0.40,   # 40%
        "min_trades_for_winrate": 10,
    },

    # Filtres spécifiques crypto
    "whale_activity_threshold": 3.0,  # Volume > 300% moyenne
    "max_funding_rate": 0.01,  # 1%
    "min_btc_dominance": 40,   # %
    "max_btc_dominance": 70,   # %

    # Guardian API
    "guardian_api_url": "http://localhost:5001",
    "guardian_port": 5001,
}

# ========================================
# SYSTÈME DE CONFLUENCE (100 POINTS)
# ========================================
CONFLUENCE_WEIGHTS = {
    # Structure SMC (40 points)
    "smc": {
        "price_in_orderblock": 20,      # Prix dans OB ±3 pips
        "fvg_present": 10,               # FVG présent et aligné
        "bos_choch_confirmed": 10,       # BOS + CHoCH confirmé
    },

    # Multi-Timeframe (25 points)
    "timeframe": {
        "alignment_m30_h1_h4": 15,      # Alignement des 3 TF
        "trend_strength": 10,            # Force de la tendance
    },

    # Indicateurs (20 points)
    "indicators": {
        "ema_alignment": 8,              # EMAs alignées
        "rsi_favorable": 6,              # RSI en zone favorable
        "macd_crossover": 6,             # MACD crossover
    },

    # Support/Resistance (10 points)
    "structure": {
        "sr_bounce": 5,                  # Bounce sur S/R majeur
        "previous_high_low": 5,          # Previous high/low
    },

    # Pattern (5 points)
    "pattern": {
        "pattern_detected": 5,           # Pattern chartiste détecté
    }
}

# ========================================
# PÉRIODES INTERDITES (CRITICAL!)
# ========================================
FORBIDDEN_PERIODS = [
    # Noël / Nouvel An (CRUCIAL - cramage le 30 déc!)
    {"start": "12-24", "end": "01-03", "reason": "Noël/Nouvel An - Période morte"},

    # Autres jours fériés majeurs
    {"start": "04-14", "end": "04-17", "reason": "Pâques"},  # Dates variables

    # Weekends
    {"day": "Friday", "after": "16:00", "reason": "Weekend approaching"},
    {"day": "Sunday", "before": "23:00", "reason": "Weekend - Low liquidity"},
]

# News à éviter absolument
HIGH_IMPACT_NEWS = [
    "FOMC", "NFP", "CPI", "GDP", "ECB", "BOE", "BOJ",
    "Interest Rate", "Employment", "Inflation", "Retail Sales"
]

NEWS_BUFFER_HOURS = 2  # Arrêt 2h avant/après news high impact

# ========================================
# INDICATEURS TECHNIQUES
# ========================================
INDICATORS_CONFIG = {
    # EMAs
    "ema_periods": [20, 50, 200],

    # RSI
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70,
    "rsi_bullish_zone": (40, 60),
    "rsi_bearish_zone": (40, 60),

    # MACD
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,

    # ATR
    "atr_period": 14,

    # Bollinger Bands
    "bb_period": 20,
    "bb_deviation": 2,
}

# ========================================
# SMART MONEY CONCEPTS (SMC)
# ========================================
SMC_CONFIG = {
    # Order Blocks
    "ob_lookback": 50,           # Barres à analyser
    "ob_min_size_pips": 20,      # Taille min OB en pips
    "ob_max_age_bars": 100,      # Age max d'un OB valide
    "ob_tolerance_pips": 3,      # Prix doit être dans OB ±3 pips

    # Fair Value Gaps
    "fvg_min_size_pips": 15,     # Taille min FVG
    "fvg_max_age_bars": 50,      # Age max FVG

    # Break of Structure / Change of Character
    "bos_min_distance_pips": 30,  # Distance min pour valider BOS
    "choch_confirmation_bars": 3,  # Barres de confirmation CHoCH

    # Liquidity
    "liquidity_lookback": 100,    # Barres pour détecter liquidité
    "liquidity_sweep_tolerance": 5,  # Pips pour sweep
}

# ========================================
# PATTERNS CHARTISTES
# ========================================
PATTERNS_CONFIG = {
    # Patterns majeurs
    "patterns": [
        "double_top", "double_bottom",
        "head_shoulders", "inverse_head_shoulders",
        "triangle_ascending", "triangle_descending", "triangle_symmetrical",
        "flag_bull", "flag_bear",
        "wedge_rising", "wedge_falling",
        "channel_ascending", "channel_descending",
    ],

    # Patterns candlestick
    "candlestick_patterns": [
        "engulfing_bull", "engulfing_bear",
        "pin_bar_bull", "pin_bar_bear",
        "doji",
        "morning_star", "evening_star",
        "three_white_soldiers", "three_black_crows",
        "hammer", "shooting_star",
    ],

    # Scoring
    "pattern_min_score": 70,  # Score min pour valider pattern
}

# ========================================
# ANTI-REVENGE TRADING
# ========================================
REVENGE_TRADING_CONFIG = {
    "consecutive_losses_trigger": 2,
    "rapid_trade_window_minutes": 10,
    "forced_pause_hours": 2,
    "psychological_cooldown": True,
}

# ========================================
# OVERTRADING DETECTION
# ========================================
OVERTRADING_CONFIG = {
    "max_trades_per_hour": 2,
    "max_trades_per_4hours": 4,
    "rapid_fire_threshold_minutes": 15,  # < 15min entre trades = suspect
}

# ========================================
# LOGGING & DATABASE
# ========================================
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_forex": "LaBete/FOREX/logs/forex.log",
    "file_crypto": "LaBete/CRYPTO/logs/crypto.log",
    "database": "LaBete/SHARED/labete.db",
    "max_log_size_mb": 50,
    "backup_count": 5,
}

# ========================================
# NOTIFICATIONS TELEGRAM
# ========================================
TELEGRAM_NOTIFICATIONS = {
    "on_signal": True,           # Nouveau signal détecté
    "on_entry": True,            # Position ouverte
    "on_tp_hit": True,           # TP atteint
    "on_sl_hit": True,           # SL touché
    "on_news_alert": True,       # News proche
    "on_limit_approached": True, # Limites approchées
    "on_kill_switch": True,      # Kill switch activé
    "daily_report": True,        # Rapport quotidien 18h
    "weekly_report": True,       # Rapport hebdomadaire vendredi
    "report_time": "18:00",      # Heure rapport quotidien
}

# ========================================
# DASHBOARD WEB
# ========================================
DASHBOARD_CONFIG = {
    "enabled": True,
    "host": "127.0.0.1",
    "port": 8080,
    "auto_refresh_seconds": 5,
    "charts_enabled": True,
}

# ========================================
# VALIDATION MANUELLE
# ========================================
MANUAL_VALIDATION = {
    "enabled": False,  # Si True, demande validation via Telegram
    "timeout_seconds": 300,  # 5 minutes max pour répondre
    "auto_reject_on_timeout": True,
}

# ========================================
# MACHINE LEARNING (Optionnel)
# ========================================
ML_CONFIG = {
    "enabled": False,  # Désactivé par défaut
    "model_path": "LaBete/SHARED/models/",
    "features": [
        "rsi", "macd", "ema_alignment", "atr",
        "volume", "time_of_day", "day_of_week"
    ],
    "prediction_threshold": 0.65,  # 65% confiance min
    "retrain_frequency_days": 30,
}

# ========================================
# CALENDRIER ÉCONOMIQUE API
# ========================================
ECONOMIC_CALENDAR_API = {
    "enabled": True,
    "provider": "forexfactory",  # ou "investing.com"
    "api_key": None,  # Si nécessaire
    "cache_duration_hours": 24,
    "check_interval_minutes": 30,
}

# ========================================
# BACKTESTING
# ========================================
BACKTEST_CONFIG = {
    "enabled": False,
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    "initial_balance": 10000,
    "commission_pips": 0.8,
    "slippage_pips": 0.5,
}

# ========================================
# FONCTIONS UTILITAIRES
# ========================================

def is_trading_allowed(current_time: datetime = None) -> tuple[bool, str]:
    """
    Vérifie si le trading est autorisé à ce moment
    Returns: (allowed: bool, reason: str)
    """
    if current_time is None:
        current_time = datetime.now()

    # Vérifier périodes interdites
    current_date = current_time.strftime("%m-%d")
    current_day = current_time.strftime("%A")
    current_hour = current_time.strftime("%H:%M")

    for period in FORBIDDEN_PERIODS:
        if "start" in period and "end" in period:
            if period["start"] <= current_date <= period["end"]:
                return False, period["reason"]

        if "day" in period:
            if period["day"] == current_day:
                if "after" in period and current_hour >= period["after"]:
                    return False, period["reason"]
                if "before" in period and current_hour <= period["before"]:
                    return False, period["reason"]

    return True, "Trading allowed"


def get_system_config(system: str) -> Dict:
    """
    Retourne la config pour forex ou crypto
    """
    if system.lower() == "forex":
        return FOREX_CONFIG
    elif system.lower() == "crypto":
        return CRYPTO_CONFIG
    else:
        raise ValueError(f"Unknown system: {system}")


def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    sl_pips: float,
    pip_value: float = 10  # Pour lot standard
) -> float:
    """
    Calcule la taille de position basée sur le risque
    """
    risk_amount = account_balance * risk_percent
    position_size = risk_amount / (sl_pips * pip_value)
    return round(position_size, 2)


# ========================================
# CONSTANTES GLOBALES
# ========================================
VERSION = "8.0 Ultimate - Economic Calendar + XAUUSD"
AUTHOR = "Yann - La Bête"
CREATED_DATE = "2025-01-08"
UPDATED_DATE = "2025-01-12"
PYTHON_VERSION = "3.12+"

# Message de bienvenue
WELCOME_MESSAGE = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🐺 LA BÊTE - Trading System 🐺              ║
║                                                          ║
║                   Version {VERSION}                      ║
║              Système Dual Forex + Crypto                 ║
║          Ultra-Sécurisé pour Prop Firm Challenges        ║
║                                                          ║
║  ⚡ Smart Money Concepts (SMC)                           ║
║  ⚡ Confluence Scoring 100pts                            ║
║  ⚡ 7 Niveaux de Protection Anti-Cramage                 ║
║  ⚡ Kill Switch Automatique Multi-Triggers               ║
║  ⚡ Bot Telegram Dual Control                            ║
║  ⚡ Dashboard Web Temps Réel                             ║
║                                                          ║
║  Créé par : {AUTHOR}                                     ║
║  Date : {CREATED_DATE}                                   ║
║  Python : {PYTHON_VERSION}                               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(WELCOME_MESSAGE)
    print("\n✅ Configuration chargée avec succès!\n")

    # Test fonction trading allowed
    allowed, reason = is_trading_allowed()
    print(f"Trading autorisé: {allowed}")
    if not allowed:
        print(f"Raison: {reason}")

    # Afficher configs
    print(f"\n📊 FOREX Config:")
    print(f"  - Paires: {FOREX_CONFIG['pairs']}")
    print(f"  - Risque/trade: {FOREX_CONFIG['risk_per_trade']*100}%")
    print(f"  - Confluence min: {FOREX_CONFIG['min_confluence_score']}/100")

    print(f"\n💰 CRYPTO Config:")
    print(f"  - Paires: {CRYPTO_CONFIG['pairs']}")
    print(f"  - Risque/trade: {CRYPTO_CONFIG['risk_per_trade']*100}%")
    print(f"  - Confluence min: {CRYPTO_CONFIG['min_confluence_score']}/100")

"""
Signal Parser - Parse les signaux Telegram et extrait les informations de trade
Format supporté:
    XAUUSD BUY NOW 5082
    SL 5070
    TP 5090
    TP 5100
    TP 5135
"""

import re
from typing import Dict, List, Optional
from datetime import datetime

class SignalParser:
    """Parse les signaux de trading depuis Telegram"""

    # Symboles supportés
    SUPPORTED_SYMBOLS = [
        'XAUUSD', 'BTCUSD', 'ETHUSD',  # Crypto/Gold
        'EURUSD', 'GBPUSD', 'USDJPY',  # Forex majors
        'GOLD', 'BTC', 'ETH', 'EUR', 'GBP', 'JPY'  # Aliases
    ]

    # Mapping aliases → symboles MT5
    SYMBOL_ALIASES = {
        'GOLD': 'XAUUSD',
        'BTC': 'BTCUSD',
        'ETH': 'ETHUSD',
        'EUR': 'EURUSD',
        'GBP': 'GBPUSD',
        'JPY': 'USDJPY'
    }

    def __init__(self):
        self.last_signal = None

    def parse(self, message: str) -> Optional[Dict]:
        """
        Parse un message de signal Telegram

        Args:
            message: Texte du message Telegram

        Returns:
            Dict avec les infos du trade ou None si invalide
            {
                'symbol': 'XAUUSD',
                'direction': 'BUY' ou 'SELL',
                'entry_price': 5082.0,
                'sl': 5070.0,
                'tps': [5090.0, 5100.0, 5135.0],
                'timestamp': '2026-01-26 14:30:00'
            }
        """
        try:
            # Nettoyer le message
            message = message.upper().strip()
            lines = [line.strip() for line in message.split('\n') if line.strip()]

            if not lines:
                return None

            # Parse première ligne: SYMBOL BUY/SELL NOW price
            first_line = lines[0]

            # Extraire symbole
            symbol = self._extract_symbol(first_line)
            if not symbol:
                return None

            # Extraire direction
            direction = self._extract_direction(first_line)
            if not direction:
                return None

            # Extraire prix d'entrée (peut être sur première ligne ou ligne "Entry")
            entry_price = self._extract_entry_price(first_line)

            # Extraire SL et TPs des lignes suivantes
            sl = None
            tps = []

            for line in lines[1:]:
                # Support formats: "SL 5070" ou "SL : 5070" ou "SL: 5070"
                if line.startswith('SL') or 'SL :' in line or 'SL:' in line:
                    sl = self._extract_price(line)
                # Support formats: "TP 5090" ou "TP1 : 5095" ou "TP1: 5095"
                elif line.startswith('TP') or 'TP1' in line or 'TP2' in line or 'TP3' in line:
                    # Skip si "ouvert" ou "open" (laisser courir)
                    if 'OUVERT' in line or 'OPEN' in line:
                        continue
                    tp = self._extract_price(line)
                    if tp:
                        tps.append(tp)
                # Support format "Entry : 5091 - 5092" (prendre milieu)
                elif 'ENTRY' in line or '👉' in line:
                    # Si on n'a pas encore d'entry_price, mettre à jour
                    entry_from_line = self._extract_entry_range(line)
                    if entry_from_line:
                        entry_price = entry_from_line

            # Si toujours pas d'entry_price, échec
            if not entry_price:
                print("⚠️ Prix d'entrée manquant dans le signal")
                return None

            # Validation
            if not sl:
                print("⚠️ SL manquant dans le signal")
                return None

            if len(tps) == 0:
                print("⚠️ Aucun TP trouvé dans le signal")
                return None

            # Valider que SL est dans la bonne direction
            if direction == 'BUY' and sl >= entry_price:
                print(f"⚠️ SL invalide pour BUY: SL ({sl}) doit être < Entry ({entry_price})")
                return None

            if direction == 'SELL' and sl <= entry_price:
                print(f"⚠️ SL invalide pour SELL: SL ({sl}) doit être > Entry ({entry_price})")
                return None

            # Construire le signal
            signal = {
                'symbol': symbol,
                'direction': direction,
                'entry_price': entry_price,
                'sl': sl,
                'tps': sorted(tps, reverse=(direction == 'SELL')),  # TPs du plus proche au plus loin
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'raw_message': message
            }

            self.last_signal = signal
            return signal

        except Exception as e:
            print(f"❌ Erreur parsing signal: {e}")
            return None

    def _extract_symbol(self, text: str) -> Optional[str]:
        """Extrait le symbole du texte"""
        for symbol in self.SUPPORTED_SYMBOLS:
            if symbol in text:
                # Mapper alias → symbole MT5
                return self.SYMBOL_ALIASES.get(symbol, symbol)
        return None

    def _extract_direction(self, text: str) -> Optional[str]:
        """Extrait BUY ou SELL"""
        if 'BUY' in text or '📈' in text or 'LONG' in text or '🟢' in text:
            return 'BUY'
        elif 'SELL' in text or '📉' in text or 'SHORT' in text or '🔴' in text:
            return 'SELL'
        return None

    def _extract_entry_price(self, text: str) -> Optional[float]:
        """Extrait le prix d'entrée de la première ligne"""
        # Chercher un nombre (peut être avec décimales)
        # Format: "XAUUSD BUY NOW 5082" ou "XAUUSD BUY @ 5082.50"

        # Enlever le symbole et direction
        text = re.sub(r'(XAUUSD|BTCUSD|ETHUSD|EURUSD|GBPUSD|USDJPY|GOLD|BTC|ETH|EUR|GBP|JPY)', '', text)
        text = re.sub(r'(BUY|SELL|LONG|SHORT|NOW|@)', '', text)

        # Chercher le premier nombre
        match = re.search(r'(\d+\.?\d*)', text)
        if match:
            return float(match.group(1))
        return None

    def _extract_price(self, text: str) -> Optional[float]:
        """Extrait un prix d'une ligne SL/TP"""
        # Format: "SL 5070" ou "TP 5090" ou "TP1 : 5095"
        # Enlever le préfixe TP1/TP2/TP3/SL pour éviter de prendre ce nombre
        text_clean = re.sub(r'(TP[123]?|SL)\s*:?\s*', '', text, count=1)

        # Maintenant chercher le nombre (le prix)
        match = re.search(r'(\d+\.?\d*)', text_clean)
        if match:
            return float(match.group(1))
        return None

    def _extract_entry_range(self, text: str) -> Optional[float]:
        """Extrait le prix d'entrée d'un range (prend le milieu)"""
        # Format: "Entry : 5091 - 5092" ou "Entry: 5091-5092"
        # Chercher deux nombres séparés par "-"
        match = re.search(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)', text)
        if match:
            price1 = float(match.group(1))
            price2 = float(match.group(2))
            # Retourner le milieu
            return (price1 + price2) / 2.0

        # Sinon, chercher un seul nombre
        match = re.search(r'(\d+\.?\d*)', text)
        if match:
            return float(match.group(1))

        return None

    def format_signal_summary(self, signal: Dict) -> str:
        """Format un résumé du signal pour affichage"""
        if not signal:
            return "❌ Signal invalide"

        # Calculer distance SL en pips/points
        sl_distance = abs(signal['entry_price'] - signal['sl'])

        # Calculer R:R pour chaque TP
        rr_ratios = []
        for tp in signal['tps']:
            tp_distance = abs(tp - signal['entry_price'])
            rr = tp_distance / sl_distance if sl_distance > 0 else 0
            rr_ratios.append(f"{rr:.1f}")

        summary = f"""
📊 **SIGNAL DÉTECTÉ**

🎯 Symbole: {signal['symbol']}
{'📈' if signal['direction'] == 'BUY' else '📉'} Direction: {signal['direction']}
💰 Entrée: {signal['entry_price']:.2f}

🛡️ SL: {signal['sl']:.2f} ({sl_distance:.1f} pts)

🎯 Take Profits:
"""

        for i, (tp, rr) in enumerate(zip(signal['tps'], rr_ratios), 1):
            tp_distance = abs(tp - signal['entry_price'])
            summary += f"   TP{i}: {tp:.2f} (+{tp_distance:.1f} pts, R:R 1:{rr})\n"

        summary += f"\n⏰ Timestamp: {signal['timestamp']}"

        return summary


if __name__ == '__main__':
    # Test du parser
    parser = SignalParser()

    # Test 1: Signal GOLD
    test_signal_1 = """
XAUUSD BUY NOW 5082
SL 5070
TP 5090
TP 5100
TP 5135
"""

    print("=" * 60)
    print("TEST 1: Signal GOLD BUY")
    print("=" * 60)
    result = parser.parse(test_signal_1)
    if result:
        print("✅ Signal parsé avec succès!")
        print(parser.format_signal_summary(result))
    else:
        print("❌ Échec parsing")

    # Test 2: Signal BTC
    test_signal_2 = """
BTCUSD SELL 95000
SL 96000
TP 94000
TP 93000
"""

    print("\n" + "=" * 60)
    print("TEST 2: Signal BTC SELL")
    print("=" * 60)
    result = parser.parse(test_signal_2)
    if result:
        print("✅ Signal parsé avec succès!")
        print(parser.format_signal_summary(result))
    else:
        print("❌ Échec parsing")

    # Test 3: Format avec @
    test_signal_3 = """
EUR BUY @ 1.0450
SL 1.0420
TP 1.0480
TP 1.0500
"""

    print("\n" + "=" * 60)
    print("TEST 3: Signal EUR avec @")
    print("=" * 60)
    result = parser.parse(test_signal_3)
    if result:
        print("✅ Signal parsé avec succès!")
        print(parser.format_signal_summary(result))
    else:
        print("❌ Échec parsing")

    # Test 4: Format avec emojis et range
    test_signal_4 = """
🟢 BUY XAUUSD

👉Entry : 5091 - 5092
TP1 : 5095
TP2 : 5102
TP3 : ouvert
SL : 5085
"""

    print("\n" + "=" * 60)
    print("TEST 4: Signal GOLD avec emojis et range")
    print("=" * 60)
    result = parser.parse(test_signal_4)
    if result:
        print("✅ Signal parsé avec succès!")
        print(parser.format_signal_summary(result))
    else:
        print("❌ Échec parsing")

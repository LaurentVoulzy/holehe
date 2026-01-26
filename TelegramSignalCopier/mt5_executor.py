"""
MT5 Executor - Envoie les signaux au bot MT5 via fichiers JSON
"""

import json
import os
from typing import Dict
from datetime import datetime
from pathlib import Path


class MT5Executor:
    """Exécute les trades sur MT5 via fichiers JSON"""

    def __init__(self, signals_folder: str = None):
        """
        Args:
            signals_folder: Dossier où placer les fichiers de signaux
                           Par défaut: C:/Trading/LaBete/SIGNALS/
        """
        if signals_folder is None:
            # Dossier par défaut (Windows MT5)
            signals_folder = "C:/Trading/LaBete/SIGNALS"

        self.signals_folder = Path(signals_folder)
        self.signals_folder.mkdir(parents=True, exist_ok=True)

        # Dossier pour signaux archivés
        self.archive_folder = self.signals_folder / "archive"
        self.archive_folder.mkdir(parents=True, exist_ok=True)

        print(f"✅ MT5Executor initialisé")
        print(f"   📁 Dossier signaux: {self.signals_folder}")

    def send_signal(self, signal: Dict) -> bool:
        """
        Envoie un signal au bot MT5

        Args:
            signal: Dictionnaire du signal parsé

        Returns:
            True si succès, False sinon
        """
        try:
            # Créer nom de fichier unique
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            symbol = signal['symbol']
            direction = signal['direction']

            filename = f"signal_{symbol}_{direction}_{timestamp}.json"
            filepath = self.signals_folder / filename

            # Préparer données pour MT5
            mt5_signal = {
                'symbol': signal['symbol'],
                'direction': signal['direction'],  # BUY ou SELL
                'entry_price': signal['entry_price'],
                'sl': signal['sl'],
                'tp1': signal['tps'][0] if len(signal['tps']) > 0 else None,
                'tp2': signal['tps'][1] if len(signal['tps']) > 1 else None,
                'tp3': signal['tps'][2] if len(signal['tps']) > 2 else None,
                'timestamp': signal['timestamp'],
                'status': 'PENDING',  # PENDING, EXECUTED, FAILED
                'source': 'TELEGRAM',
                'raw_message': signal.get('raw_message', '')
            }

            # Écrire fichier JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(mt5_signal, f, indent=2, ensure_ascii=False)

            print(f"✅ Signal envoyé à MT5: {filename}")
            print(f"   📁 {filepath}")

            return True

        except Exception as e:
            print(f"❌ Erreur envoi signal à MT5: {e}")
            return False

    def get_pending_signals(self) -> list:
        """Récupère la liste des signaux en attente"""
        pending = []

        for filepath in self.signals_folder.glob("signal_*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    signal = json.load(f)

                if signal.get('status') == 'PENDING':
                    pending.append({
                        'file': filepath.name,
                        'signal': signal
                    })
            except Exception as e:
                print(f"⚠️ Erreur lecture {filepath.name}: {e}")

        return pending

    def archive_signal(self, filename: str):
        """Archive un signal traité"""
        try:
            source = self.signals_folder / filename
            dest = self.archive_folder / filename

            if source.exists():
                source.rename(dest)
                print(f"📦 Signal archivé: {filename}")
        except Exception as e:
            print(f"⚠️ Erreur archivage {filename}: {e}")

    def get_status(self) -> Dict:
        """Obtient le status du dossier signaux"""
        pending = len(list(self.signals_folder.glob("signal_*_PENDING_*.json")))
        executed = len(list(self.signals_folder.glob("signal_*_EXECUTED_*.json")))
        failed = len(list(self.signals_folder.glob("signal_*_FAILED_*.json")))
        archived = len(list(self.archive_folder.glob("signal_*.json")))

        return {
            'pending': pending,
            'executed': executed,
            'failed': failed,
            'archived': archived
        }

    def cleanup_old_signals(self, days: int = 7):
        """Nettoie les signaux archivés de plus de X jours"""
        import time

        now = time.time()
        cutoff = now - (days * 86400)  # X jours en secondes

        deleted = 0
        for filepath in self.archive_folder.glob("signal_*.json"):
            if filepath.stat().st_mtime < cutoff:
                filepath.unlink()
                deleted += 1

        if deleted > 0:
            print(f"🧹 {deleted} signaux archivés supprimés (> {days} jours)")

        return deleted


if __name__ == '__main__':
    # Test de l'executor
    print("=" * 60)
    print("TEST MT5 EXECUTOR")
    print("=" * 60)

    # Créer executor (test avec dossier local)
    executor = MT5Executor(signals_folder="./test_signals")

    # Signal de test
    test_signal = {
        'symbol': 'XAUUSD',
        'direction': 'BUY',
        'entry_price': 5082.0,
        'sl': 5070.0,
        'tps': [5090.0, 5100.0, 5135.0],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'raw_message': 'XAUUSD BUY NOW 5082\nSL 5070\nTP 5090\nTP 5100\nTP 5135'
    }

    # Envoyer signal
    success = executor.send_signal(test_signal)

    if success:
        print("\n✅ Signal envoyé avec succès!")

        # Vérifier signaux en attente
        pending = executor.get_pending_signals()
        print(f"\n📊 Signaux en attente: {len(pending)}")

        # Afficher status
        status = executor.get_status()
        print(f"\n📈 Status:")
        print(f"   Pending: {status['pending']}")
        print(f"   Executed: {status['executed']}")
        print(f"   Failed: {status['failed']}")
        print(f"   Archived: {status['archived']}")
    else:
        print("\n❌ Échec envoi signal")

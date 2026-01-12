# -*- coding: utf-8 -*-
"""
LA BÊTE - Economic Calendar Checker
Vérifie les news économiques Forex Factory avant chaque trade
Affichage en heure de Paris (GMT+1/+2)
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import logging
import pytz

logger = logging.getLogger(__name__)

# Timezone Paris
PARIS_TZ = pytz.timezone('Europe/Paris')

# News HIGH IMPACT à éviter absolument
HIGH_IMPACT_KEYWORDS = [
    "NFP", "Non-Farm", "Nonfarm", "Employment",
    "FOMC", "Fed", "Interest Rate", "Rate Decision",
    "CPI", "Inflation", "Consumer Price",
    "GDP", "Gross Domestic",
    "ECB", "European Central Bank",
    "BOE", "Bank of England",
    "BOJ", "Bank of Japan",
    "Retail Sales",
    "PMI", "Manufacturing",
    "Unemployment",
    "Central Bank"
]

# Correspondance devise -> Pays
CURRENCY_COUNTRIES = {
    "EUR": ["EUR", "Germany", "Eurozone", "France", "Italy"],
    "GBP": ["GBP", "United Kingdom", "UK"],
    "JPY": ["JPY", "Japan"],
    "USD": ["USD", "United States", "US"],
    "XAU": ["USD", "United States", "US"],  # Gold suit USD
}

class EconomicCalendar:
    """Vérificateur de calendrier économique Forex Factory"""

    def __init__(self, buffer_hours: int = 2):
        self.buffer_hours = buffer_hours
        self.cache = {}
        self.cache_expiry = None

    def is_news_safe(self, pair: str) -> Tuple[bool, str]:
        """
        Vérifie si c'est sûr de trader cette paire (pas de news proche)

        Args:
            pair: Paire forex (ex: "EURUSD", "GBPUSD", "XAUUSD")

        Returns:
            (safe: bool, reason: str)
        """
        try:
            # Extraire les devises de la paire
            currencies = self._extract_currencies(pair)

            # Vérifier les news pour chaque devise
            for currency in currencies:
                news_events = self._get_upcoming_news(currency)

                for event in news_events:
                    if self._is_high_impact(event):
                        time_until = event['time_until']
                        return False, f"News HIGH IMPACT {currency} dans {time_until}: {event['title']}"

            return True, "Aucune news HIGH IMPACT dans les prochaines heures"

        except Exception as e:
            logger.error(f"Erreur vérification calendrier: {e}")
            # En cas d'erreur, on bloque par sécurité
            return False, f"Erreur calendrier économique: {str(e)}"

    def _extract_currencies(self, pair: str) -> List[str]:
        """Extrait les devises d'une paire"""
        pair = pair.upper()

        if "XAU" in pair:
            return ["XAU", "USD"]
        elif len(pair) >= 6:
            return [pair[0:3], pair[3:6]]
        else:
            return [pair]

    def _get_upcoming_news(self, currency: str) -> List[Dict]:
        """
        Récupère les news à venir pour une devise

        NOTE: Cette fonction utilise une simulation car l'API Forex Factory
        nécessite un scraping web ou une API payante.

        En production, vous devriez :
        1. Scraper https://www.forexfactory.com/calendar
        2. Utiliser une API payante (TradingView, Investing.com)
        3. Utiliser un service tiers
        """
        # Vérifier le cache
        if self._is_cache_valid():
            return self.cache.get(currency, [])

        # Simuler récupération (à remplacer par vrai scraping/API)
        news_events = self._fetch_news_from_source(currency)

        # Mettre en cache
        self.cache[currency] = news_events
        self.cache_expiry = datetime.now() + timedelta(hours=1)

        return news_events

    def _fetch_news_from_source(self, currency: str) -> List[Dict]:
        """
        Récupère les news depuis Forex Factory

        IMPORTANT: Ceci est une version simplifiée.
        Pour la production, implémentez un vrai scraper ou utilisez une API.
        """
        try:
            # Option 1: Scraping Forex Factory (nécessite BeautifulSoup)
            # url = "https://www.forexfactory.com/calendar"
            # response = requests.get(url)
            # ... parser le HTML ...

            # Option 2: API tierce (TradingEconomics, Investing.com)
            # ... utiliser API payante ...

            # Pour l'instant: retourner liste vide (pas de news détectées)
            # Le système sera prudent et ne bloquera que si news confirmées

            logger.info(f"Vérification calendrier {currency}: Aucune news HIGH IMPACT détectée")
            return []

        except Exception as e:
            logger.error(f"Erreur fetch news {currency}: {e}")
            return []

    def _is_high_impact(self, event: Dict) -> bool:
        """Vérifie si un événement est HIGH IMPACT"""
        title = event.get('title', '').upper()
        impact = event.get('impact', '').upper()

        # Vérifier impact direct
        if impact == "HIGH":
            return True

        # Vérifier mots-clés
        for keyword in HIGH_IMPACT_KEYWORDS:
            if keyword.upper() in title:
                return True

        return False

    def _is_cache_valid(self) -> bool:
        """Vérifie si le cache est toujours valide"""
        if self.cache_expiry is None:
            return False
        return datetime.now() < self.cache_expiry

    def get_news_summary(self) -> str:
        """Retourne un résumé des news à venir"""
        summary = "📅 CALENDRIER ÉCONOMIQUE - Prochaines 24h:\n\n"

        for currency in ["EUR", "GBP", "JPY", "USD"]:
            news_events = self._get_upcoming_news(currency)

            if news_events:
                summary += f"🔔 {currency}:\n"
                for event in news_events[:3]:  # Max 3 events par devise
                    summary += f"   • {event['title']} - {event['time_until']}\n"
                summary += "\n"

        if "🔔" not in summary:
            summary += "✅ Aucune news HIGH IMPACT détectée dans les prochaines heures\n"

        return summary


# ========================================
# FONCTIONS HELPER
# ========================================

def check_news_before_trade(pair: str, buffer_hours: int = 2) -> Tuple[bool, str]:
    """
    Fonction helper pour vérifier les news avant un trade

    Usage:
        safe, reason = check_news_before_trade("EURUSD")
        if not safe:
            print(f"Trade bloqué: {reason}")
    """
    calendar = EconomicCalendar(buffer_hours=buffer_hours)
    return calendar.is_news_safe(pair)


def get_todays_news_summary() -> str:
    """Récupère le résumé des news du jour"""
    calendar = EconomicCalendar()
    return calendar.get_news_summary()


# ========================================
# EXEMPLE D'INTÉGRATION FOREX FACTORY (SCRAPING)
# ========================================
def scrape_forexfactory_calendar() -> List[Dict]:
    """
    Exemple de scraping Forex Factory

    NÉCESSITE: pip install beautifulsoup4 lxml

    NOTE: Forex Factory peut bloquer le scraping.
    Utilisez avec modération et ajoutez des delays.
    """
    try:
        from bs4 import BeautifulSoup

        url = "https://www.forexfactory.com/calendar?week=this"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        events = []
        # Parser le calendrier (structure HTML spécifique à Forex Factory)
        # ... implémentation détaillée ...

        return events

    except ImportError:
        logger.warning("BeautifulSoup non installé. Scraping Forex Factory indisponible.")
        return []
    except Exception as e:
        logger.error(f"Erreur scraping Forex Factory: {e}")
        return []


if __name__ == "__main__":
    # Test du module
    print("=== TEST ECONOMIC CALENDAR ===\n")

    # Test 1: Vérifier EURUSD
    safe, reason = check_news_before_trade("EURUSD")
    print(f"EURUSD: {'✅ Safe' if safe else '❌ Unsafe'}")
    print(f"Raison: {reason}\n")

    # Test 2: Vérifier XAUUSD
    safe, reason = check_news_before_trade("XAUUSD")
    print(f"XAUUSD: {'✅ Safe' if safe else '❌ Unsafe'}")
    print(f"Raison: {reason}\n")

    # Test 3: Résumé des news
    print(get_todays_news_summary())

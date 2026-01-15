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
        Récupère les news depuis Forex Factory avec scraping BeautifulSoup
        """
        try:
            from bs4 import BeautifulSoup
            import re

            # URL Forex Factory pour aujourd'hui
            url = "https://www.forexfactory.com/calendar?day=today"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                logger.warning(f"Forex Factory HTTP {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            events = []

            # Trouver les pays correspondant à la devise
            target_countries = CURRENCY_COUNTRIES.get(currency, [currency])

            # Parser les lignes du calendrier
            calendar_rows = soup.find_all('tr', class_='calendar__row')

            current_time = datetime.now(PARIS_TZ)

            for row in calendar_rows:
                try:
                    # Récupérer le pays
                    currency_cell = row.find('td', class_='calendar__currency')
                    if not currency_cell:
                        continue

                    event_currency = currency_cell.text.strip()

                    # Vérifier si c'est la bonne devise
                    if event_currency not in target_countries and not any(country in event_currency for country in target_countries):
                        continue

                    # Récupérer l'impact
                    impact_cell = row.find('td', class_='calendar__impact')
                    impact_spans = impact_cell.find_all('span', class_='calendar__impact-icon') if impact_cell else []
                    impact_level = len([s for s in impact_spans if 'calendar__impact-icon--active' in s.get('class', [])])

                    # Seulement les HIGH IMPACT (3 barres rouges)
                    if impact_level < 3:
                        continue

                    # Récupérer le titre
                    title_cell = row.find('td', class_='calendar__event')
                    if not title_cell:
                        continue
                    title = title_cell.text.strip()

                    # Récupérer l'heure
                    time_cell = row.find('td', class_='calendar__time')
                    if not time_cell:
                        continue
                    time_str = time_cell.text.strip()

                    # Parser l'heure (format: "9:30am" ou "All Day")
                    if time_str and time_str != "All Day":
                        try:
                            # Convertir l'heure en datetime
                            event_time = datetime.strptime(time_str, "%I:%M%p").time()
                            event_datetime = datetime.combine(current_time.date(), event_time)
                            event_datetime = PARIS_TZ.localize(event_datetime)

                            # Calculer le temps restant
                            time_until = event_datetime - current_time
                            hours_until = time_until.total_seconds() / 3600

                            # Seulement les news dans les prochaines N heures
                            if 0 <= hours_until <= self.buffer_hours:
                                minutes_until = int(time_until.total_seconds() / 60)

                                if minutes_until < 60:
                                    time_until_str = f"{minutes_until}min"
                                else:
                                    time_until_str = f"{int(hours_until)}h{minutes_until % 60}min"

                                events.append({
                                    'currency': event_currency,
                                    'title': title,
                                    'impact': 'HIGH',
                                    'time': event_datetime.strftime("%H:%M"),
                                    'time_until': time_until_str,
                                    'hours_until': hours_until
                                })

                                logger.warning(f"⚠️ NEWS HIGH IMPACT {event_currency} dans {time_until_str}: {title}")

                        except Exception as e:
                            logger.debug(f"Erreur parsing heure '{time_str}': {e}")
                            continue

                except Exception as e:
                    logger.debug(f"Erreur parsing row: {e}")
                    continue

            if events:
                logger.info(f"Calendrier {currency}: {len(events)} news HIGH IMPACT trouvées")
            else:
                logger.info(f"Calendrier {currency}: Aucune news HIGH IMPACT dans les {self.buffer_hours}h")

            return events

        except ImportError:
            logger.warning("BeautifulSoup4 non installé. Calendrier économique désactivé.")
            logger.warning("Installez avec: pip install beautifulsoup4 lxml")
            return []

        except Exception as e:
            logger.error(f"Erreur scraping Forex Factory pour {currency}: {e}")
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

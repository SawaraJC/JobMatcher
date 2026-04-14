import requests

from parsers.greenhouse import GreenhouseParser
from parsers.lever import LeverParser
from parsers.workday import WorkdayParser
from parsers.generic import GenericParser


# Detect which parser to use
def detect_parser(url):
    url = url.lower()

    if "greenhouse.io" in url:
        return GreenhouseParser()

    elif "lever.co" in url:
        return LeverParser()

    elif "myworkdayjobs.com" in url:
        return WorkdayParser()

    else:
        return GenericParser()


# Shared fetch function (for HTML-based parsers only)
def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"Fetch failed for {url}: {e}")
        return None


# Main scrape function
def scrape(url):
    parser = detect_parser(url)

    try:
        # API-based parsers (no HTML needed)
        if isinstance(parser, (GreenhouseParser, LeverParser, WorkdayParser)):
            return parser.parse(url)

        # HTML-based parser
        html = fetch(url)

        if not html:
            return []

        return parser.parse(html)

    except Exception as e:
        print(f"Scraping failed for {url}: {e}")
        return []
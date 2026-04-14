from bs4 import BeautifulSoup
from parsers.base import BaseParser

class GenericParser(BaseParser):
    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")

        jobs = []
        for job in soup.find_all("a"):
            text = job.get_text().strip()
            if "engineer" in text.lower():
                jobs.append({
                    "title": text,
                    "location": "N/A",
                    "description": "N/A",
                    "company": "unknown"
                })

        return jobs
import requests
from parsers.base import BaseParser

class LeverParser(BaseParser):
    def parse(self, url):
        company = url.split("/")[-1]
        api_url = f"https://api.lever.co/v0/postings/{company}"

        res = requests.get(api_url)
        jobs = res.json()

        result = []
        for job in jobs:
            result.append({
                "title": job["text"],
                "location": job["categories"]["location"],
                "description": job["description"],
                "company": company
            })

        return result
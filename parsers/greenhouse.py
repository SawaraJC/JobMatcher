import requests
from parsers.base import BaseParser

class GreenhouseParser(BaseParser):
    def parse(self, url):
        # Convert careers page → API
        # Example: boards.greenhouse.io/company
        company = url.split("/")[-1]
        api_url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

        res = requests.get(api_url)
        jobs = res.json().get("jobs", [])

        result = []
        for job in jobs:
            result.append({
                "title": job["title"],
                "location": job["location"]["name"],
                "description": job["content"],
                "company": company
            })

        return result
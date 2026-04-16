import requests
from parsers.base import BaseParser


class GreenhouseParser(BaseParser):

    def parse(self, url):
        """
        Parse jobs from Greenhouse boards
        Example:
        https://boards.greenhouse.io/stripe
        """

        company = self.extract_company(url)

        api_url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Greenhouse API failed for {company}: {e}")
            return []

        data = response.json()
        jobs = data.get("jobs", [])

        results = []
        seen_ids = set()

        for job in jobs:
            job_id = job.get("id")

            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            results.append({
                "title": job.get("title"),
                "location": job.get("location", {}).get("name"),
                "description": job.get("content"),
                "job_id": job_id,
                "url": job.get("absolute_url"),
                "company": company
            })

        print(f"Greenhouse ({company}): {len(results)} jobs")

        return results

    def extract_company(self, url):
        """
        Safer extraction of company name
        """
        parts = url.rstrip("/").split("/")
        return parts[-1]
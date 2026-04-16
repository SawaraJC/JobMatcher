import requests
from parsers.base import BaseParser


class LeverParser(BaseParser):

    def parse(self, url):
        """
        Parse jobs from Lever
        Example:
        https://jobs.lever.co/netflix
        """

        company = self.extract_company(url)

        api_url = f"https://api.lever.co/v0/postings/{company}?mode=json"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Lever API failed for {company}: {e}")
            return []

        jobs = response.json()

        results = []
        seen_ids = set()

        for job in jobs:
            job_id = job.get("id")

            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            results.append({
                "title": job.get("text"),
                "location": job.get("categories", {}).get("location"),
                "description": job.get("description"),
                "job_id": job_id,
                "url": job.get("hostedUrl"),
                "company": company
            })

        print(f"Lever ({company}): {len(results)} jobs")

        return results

    def extract_company(self, url):
        """
        Safe company extraction
        """
        parts = url.rstrip("/").split("/")
        return parts[-1]
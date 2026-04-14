import requests
import time
from parsers.util import parse_workday_url, extract_wd_part


class WorkdayParser:

    def __init__(self, delay=1):
        self.delay = delay

    def build_api_url(self, tenant, site, url):
        """
        Construct Workday API endpoint dynamically
        """
        wd_part = extract_wd_part(url)

        if not wd_part:
            raise ValueError("Invalid Workday URL format")

        return f"https://{tenant}.{wd_part}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"

    def fetch_jobs(self, api_url):
        payload = {
            "limit": 20,
            "offset": 0
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        all_jobs = []

        while True:
            response = requests.post(api_url, json=payload, headers=headers)

            if response.status_code != 200:
                print(f"Request failed: {response.status_code}")
                break

            data = response.json()
            jobs = data.get("jobPostings", [])

            if not jobs:
                break

            for job in jobs:
                all_jobs.append({
                    "title": job.get("title"),
                    "location": job.get("locationsText"),
                    "job_id": job.get("externalPath"),
                    "posted_date": job.get("postedOn"),
                    "company": api_url.split("/")[4]
                })

            payload["offset"] += payload["limit"]

            time.sleep(self.delay)

        return all_jobs

    def parse(self, url):
        """
        Main method to scrape jobs from Workday
        """
        config = parse_workday_url(url)

        if not config:
            print("Invalid Workday URL")
            return []

        tenant = config["tenant"]
        site = config["site"]

        api_url = self.build_api_url(tenant, site, url)

        print(f"Fetching from API: {api_url}")

        return self.fetch_jobs(api_url)
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
        seen_jobs = set()  
        total_count = 0

        print("Starting job fetch...\n")

        while True:
            response = requests.post(api_url, json=payload, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Request failed: {response.status_code}")
                break

            data = response.json()
            jobs = data.get("jobPostings", [])

            if not jobs:
                print("No jobs returned, stopping.")
                break

            new_jobs_in_batch = 0

            for job in jobs:
                job_id = job.get("externalPath")

                if job_id in seen_jobs:
                    continue

                seen_jobs.add(job_id)

                all_jobs.append({
                    "title": job.get("title"),
                    "location": job.get("locationsText"),
                    "job_id": job_id,
                    "posted_date": job.get("postedOn"),
                    "company": api_url.split("/")[5]
                })

                total_count += 1
                new_jobs_in_batch += 1

                print(f"Unique jobs collected: {total_count}", end="\r")

            if new_jobs_in_batch == 0:
                print("\nNo new jobs found, stopping pagination.")
                break

            payload["offset"] += payload["limit"]

            time.sleep(self.delay)

        print(f"\n\nFinal Unique Jobs Collected: {total_count}\n")

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

        print(f"Fetching from API:\n{api_url}\n")

        return self.fetch_jobs(api_url)
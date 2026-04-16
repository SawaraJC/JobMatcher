import requests
import time
from parsers.util import parse_oracle_url


class OracleParser:

    def __init__(self, delay=1):
        self.delay = delay

    def build_api_url(self, base_url):
        return f"{base_url}/hcmRestApi/resources/latest/recruitingCEJobRequisitions"

    def fetch_jobs(self, api_url, site):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        offset = 0
        limit = 25

        all_jobs = []
        seen = set()

        print("📡 Fetching Oracle jobs...\n")

        while True:
            params = {
                "onlyData": "true",
                "finder": f"findReqs;siteNumber={site},limit={limit},offset={offset}"
            }

            response = requests.get(api_url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Failed: {response.status_code}")
                break

            data = response.json()
            jobs = data.get("items", [])

            if not jobs:
                print("No more jobs")
                break

            new_count = 0

            for job in jobs:
                job_id = job.get("Id")

                if job_id in seen:
                    continue

                seen.add(job_id)

                all_jobs.append({
                    "title": job.get("Title"),
                    "location": job.get("PrimaryLocation"),
                    "job_id": job_id,
                    "company": api_url.split("/")[2].split(".")[0]
                })

                new_count += 1
                print(f"Jobs collected: {len(all_jobs)}", end="\r")

            if new_count == 0:
                print("\nNo new jobs — stopping")
                break

            offset += limit
            time.sleep(self.delay)

        print(f"\n\nTotal jobs: {len(all_jobs)}\n")

        return all_jobs

    def parse(self, url):
        config = parse_oracle_url(url)

        if not config:
            print("Invalid Oracle URL")
            return []

        api_url = self.build_api_url(config["base_url"])

        print(f"Fetching from API:\n{api_url}\n")

        return self.fetch_jobs(api_url, config["site"])
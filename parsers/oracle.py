import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from parsers.util import parse_oracle_url


class OracleParser:

    def __init__(self, delay=0.2, max_workers=8):
        self.delay = delay
        self.max_workers = max_workers

    def build_api_url(self, base_url):
        return f"{base_url}/hcmRestApi/resources/latest/recruitingCEJobRequisitions"

    def _make_request(self, api_url, site, offset, limit, headers):
        params = {
            "onlyData": "true",
            "expand": "requisitionList.workLocation,requisitionList.secondaryLocations",
            "finder": (
                f"findReqs;"
                f"siteNumber={site},"
                f"facetsList=LOCATIONS;WORK_LOCATIONS;WORKPLACE_TYPES;TITLES;CATEGORIES;ORGANIZATIONS;POSTING_DATES;FLEX_FIELDS,"
                f"limit={limit},"
                f"offset={offset},"
                f"sortBy=POSTING_DATES_DESC"
            )
        }

        response = requests.get(api_url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}")

        return response.json()

    def fetch_jobs(self, api_url, site, config):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        limit = 50

        print(f"\nFetching Oracle jobs for {config['tenant']}...\n")

        # Step 1: Initial request
        initial_data = self._make_request(api_url, site, 0, limit, headers)
        items = initial_data.get("items", [])

        if not items:
            print("No data returned from initial request")
            return []

        total_jobs = items[0].get("TotalJobsCount", 0)
        print(f"Total jobs reported: {total_jobs}")

        offsets = list(range(0, total_jobs, limit))

        all_jobs = []
        seen_ids = set()

        def process_offset(offset):
            try:
                time.sleep(self.delay)

                data = self._make_request(api_url, site, offset, limit, headers)
                batch = []

                items = data.get("items", [])
                for item in items:
                    requisitions = item.get("requisitionList", [])

                    for job in requisitions:
                        job_id = job.get("Id")
                        if not job_id:
                            continue

                        location = (
                            job.get("PrimaryLocation")
                            or job.get("PrimaryLocationCountry")
                            or "Unknown"
                        )

                        batch.append({
                            "title": job.get("Title"),
                            "location": location,
                            "job_id": job_id,
                            "company": config["tenant"],
                            "description": job.get("ShortDescriptionStr"),
                            "url": f"{config['base_url']}/hcmUI/CandidateExperience/en/sites/{site}/job/{job_id}"
                        })

                return batch

            except Exception as e:
                print(f"Error at offset {offset}: {e}")
                return []

        # Step 2: Parallel execution
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(process_offset, offset): offset for offset in offsets}

            for future in as_completed(futures):
                offset = futures[future]

                try:
                    batch = future.result()
                    new_count = 0

                    for job in batch:
                        job_id = job["job_id"]

                        if job_id in seen_ids:
                            continue

                        seen_ids.add(job_id)
                        all_jobs.append(job)
                        new_count += 1

                    print(f"Offset {offset} complete | New jobs: {new_count} | Total: {len(all_jobs)}")

                except Exception as e:
                    print(f"Error processing offset {offset}: {e}")

        print(f"\nFinal Jobs Collected ({config['tenant']}): {len(all_jobs)}\n")

        return all_jobs

    def parse(self, url):
        config = parse_oracle_url(url)

        if not config:
            print("Invalid Oracle URL")
            return []

        api_url = self.build_api_url(config["base_url"])
        site = config["site"]

        print(f"Fetching from API:\n{api_url}\n")

        return self.fetch_jobs(api_url, site, config)
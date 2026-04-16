from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper_engine import scrape
import time

SOURCES = [
    {
        "name": "TransUnion",
        "url": "https://transunion.wd5.myworkdayjobs.com/en-GB/TransUnion"
    },
    {
        "name": "JPMC",
        "url": "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/jobs"
    }
]


def run():
    start_time = time.time()

    all_jobs = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_source = {
            executor.submit(scrape, source["url"]): source
            for source in SOURCES
        }

        for future in as_completed(future_to_source):
            source = future_to_source[future]

            try:
                jobs = future.result()

                if not jobs:
                    print(f"No jobs found for {source['name']}")
                    continue

                print(f"{source['name']}: {len(jobs)} jobs")

                all_jobs.extend(jobs)

            except Exception as e:
                print(f"Error scraping {source['name']}: {e}")

    end_time = time.time()

    print(f"\nTotal Jobs Collected: {len(all_jobs)}")
    print(f"Time Taken: {round(end_time - start_time, 2)} seconds\n")

    for job in all_jobs[:10]:
        print(f"{job.get('title')} - {job.get('company')}")


if __name__ == "__main__":
    run()
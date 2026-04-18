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

    print("\nStarting job scraping...\n")

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
                    print(f"[{source['name']}] No jobs found\n")
                    continue

                print(f"[{source['name']}] Jobs fetched: {len(jobs)}\n")

                all_jobs.extend(jobs)

            except Exception as e:
                print(f"[{source['name']}] Error: {e}\n")

    end_time = time.time()

    print("Scraping complete.\n")
    print(f"Total jobs collected: {len(all_jobs)}")
    print(f"Time taken: {round(end_time - start_time, 2)} seconds\n")

    print("Sample results:\n")

    for idx, job in enumerate(all_jobs[:10], start=1):
        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        print(f"{idx}. {title} - {company}")


if __name__ == "__main__":
    run()
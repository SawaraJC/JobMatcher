import requests

APP_ID = "1c7a3fd4"
APP_KEY = "2ece2451f82cbd8f124f2358533f6bd4"

def fetch_jobs(keyword):
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": keyword
    }

    response = requests.get(url, params=params)
    data = response.json()

    jobs = []
    for job in data.get("results", []):
        jobs.append({
            "title": job["title"],
            "description": job["description"]
        })

    return jobs
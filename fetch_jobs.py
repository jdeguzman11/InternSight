# Justin DeGuzman

# send HTTP requests to websites/APIs
import requests

url = "https://boards-api.greenhouse.io/v1/boards/stripe/jobs"

response = requests.get(url)

data = response.json()

jobs = []

for job in data["jobs"]:
    job_info = {
        "title": job["title"],
        "company": job["company_name"],
        "location": job["location"]["name"],
        "date": job["first_published"],
        "link": job["absolute_url"]
    }

    jobs.append(job_info)


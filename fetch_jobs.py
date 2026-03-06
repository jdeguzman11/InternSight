# Justin DeGuzman

# send HTTP requests to websites/APIs
import requests
# jobs list into a pandas dataframe
import pandas as pd
# HTML cleaner
from bs4 import BeautifulSoup
import html

from extract_skills import extract_skills


def clean_html(html_text):
    decoded = html.unescape(html_text)
    soup = BeautifulSoup(decoded, "html.parser")
    return soup.get_text(separator=" ")


url = "https://boards-api.greenhouse.io/v1/boards/stripe/jobs?content=true"
response = requests.get(url)
data = response.json()

jobs = []

for job in data["jobs"]:
    job_info = {
        "title": job["title"],
        "company": job["company_name"],
        "location": job["location"]["name"],
        "date": job["first_published"],
        "link": job["absolute_url"],
        "content": clean_html(job.get("content", "")),
        "skills": extract_skills(clean_html(job["content"]))
    }

    jobs.append(job_info)

dataframe = pd.DataFrame(jobs)
dataframe.to_csv("data/jobs.csv", index=False)

print(dataframe.head())

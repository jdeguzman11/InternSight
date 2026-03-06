# Justin DeGuzman

# send HTTP requests to websites/APIs
import requests
# jobs list into a pandas dataframe
import pandas as pd
# HTML cleaner
from bs4 import BeautifulSoup
import html
# most common skills
from collections import Counter

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
dataframe = dataframe[
    dataframe["title"].str.contains(
        "engineer|developer|data|machine learning|ai|software|analyst",
        case=False,
        na=False
    )
]

dataframe.to_csv("data/jobs.csv", index=False)

all_skills = []

for skills_list in dataframe["skills"]:
    all_skills.extend(skills_list)

skill_counts = Counter(all_skills)

print("\n Top Skills Across Jobs:\n")

for skill, count in skill_counts.most_common(10):
    print(f"{skill}: {count}")

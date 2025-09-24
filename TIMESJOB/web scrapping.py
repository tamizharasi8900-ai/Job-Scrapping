from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def scrape_timesjobs(skill, location=""):
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={skill}&txtLocation={location}"

    # Run Chrome in headless mode (no window)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  # wait for JS to load

    jobs = []
    job_cards = driver.find_elements(By.CSS_SELECTOR, "li.clearfix.job-bx.wht-shd-bx")

    for job in job_cards:
        try:
            title = job.find_element(By.CSS_SELECTOR, "h2 a").text.strip()
        except:
            title = "N/A"

        try:
            company = job.find_element(By.CSS_SELECTOR, "h3.joblist-comp-name").text.strip()
        except:
            company = "N/A"

        try:
            location_out = job.find_element(By.CSS_SELECTOR, "ul.top-jd-dtl li").text.strip()
        except:
            location_out = "N/A"

        try:
            skills = job.find_element(By.CSS_SELECTOR, "span.srp-skills").text.strip()
        except:
            skills = "N/A"

        try:
            posted = job.find_element(By.CSS_SELECTOR, "span.sim-posted").text.strip()
        except:
            posted = "N/A"

        jobs.append({
            "Title": title,
            "Company": company,
            "Location": location_out,
            "Skills": skills,
            "Posted": posted
        })

    driver.quit()

    if not jobs:
        print("⚠ No jobs found.")
        return

    # Save to CSV
    filename = f"{skill.lower().replace(' ', '_')}_jobs.csv"
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"✅ Saved {len(jobs)} jobs to {filename}")
    print(df.head())

if __name__ == "__main__":
    job_title = input("Enter job title: ")
    job_location = input("Enter location (leave blank for all India): ")
    scrape_timesjobs(job_title, job_location)

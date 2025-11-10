"""
JobSpy Scraper Module
Scans Indeed and LinkedIn by locations (PT, ES, UK, IT, CY, EU, Remote)
Saves raw job listings to JSON.
Fully modular, with logs and filters.
"""
# %%
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import logging

from jobspy import scrape_jobs
import pandas as pd

# ------------------- Logging -------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ------------------- Constants (FINAL) -------------------
DATA_DIR = Path(__file__).parents[2] / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Keywords for search
KEYWORDS = [
    "data analyst", "data science", "junior data", "mid-level data analyst",
    "data scientist", "analytics", "business intelligence", "junior analytics"
]

# YOUR FINAL LIST OF LOCATIONS
LOCATIONS = [
    "Portugal", "Lisbon", "Porto",
    "Spain", "Madrid", "Barcelona",
    "United Kingdom", "UK", "London",
    "Italy", "Rome", "Milan",
    "Cyprus", "Limassol",
    "European Union", "EU",
    "Remote", "remote"
]

RESULTS_WANTED = 25  # more — higher chance to catch in Portugal/Cyprus
ENGLISH_ONLY = True
HOURS_OLD = 72  # only fresh (3 days)

# ------------------- Main function -------------------
def scrape_and_save() -> Path:
    """
    Runs JobSpy, collects jobs, and saves to JSON.
    Returns the file path.
    """
    logger.info(f"Starting scan: {', '.join(KEYWORDS)}")
    logger.info(f"Locations: {', '.join(LOCATIONS)}")

    # JobSpy
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin"],
        search_term=" OR ".join(KEYWORDS),
        location=",".join(LOCATIONS),
        results_wanted=RESULTS_WANTED,
        linkedin_fetch_description=True,
        hours_old=HOURS_OLD,
        verbose=1
    )

    if jobs.empty:
        logger.warning("No jobs found!")
        return None

    # Filter by English language 
    df = jobs.copy()
    if ENGLISH_ONLY:
        mask = (
            df["description"].str.contains(r"\b(english|eng)\b", case=False, na=False) |
            df["title"].str.contains(r"\b(english|eng)\b", case=False, na=False)
        )
        df = df[mask]
        logger.info(f"After English filter: {len(df)} jobs")

    # Convert to list of dicts
    records = df.to_dict(orient="records")
    cleaned_jobs = []

    # Keywords for filtering by location (lowercase)
    location_keywords = [loc.lower() for loc in LOCATIONS]

    for job in records:
        cleaned = {
            "id": job.get("id") or job.get("job_id"),
            "title": job.get("title", "").strip(),
            "company": job.get("company", "").strip(),
            "location": job.get("location", "").strip(),
            "job_url": job.get("job_url", ""),
            "description": job.get("description", "")[:5000],  # truncate
            "date_posted": str(job.get("date_posted")),
            "site": job.get("site"),
            "salary": job.get("salary", ""),
        }

        # Filter: only desired locations
        loc_lower = cleaned["location"].lower()
        if any(kw in loc_lower for kw in location_keywords):
            cleaned_jobs.append(cleaned)

    if not cleaned_jobs:
        logger.warning("After location filter: no jobs found!")
        return None

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = DATA_DIR / f"jobs_{timestamp}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(cleaned_jobs, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved {len(cleaned_jobs)} jobs → {filepath.name}")
    logger.info(f"Sample locations: {[j['location'] for j in cleaned_jobs[:3]]}")
    return filepath


# ------------------- CLI entry point -------------------
if __name__ == "__main__":
    print("AI Job Agent — Scanning jobs...")
    result = scrape_and_save()
    if result:
        print(f"Done! Data saved: {result}")
    else:
        print("Error: no jobs found. Try again later.")

# %%

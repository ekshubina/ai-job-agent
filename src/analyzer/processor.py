"""
Processes raw job listings → adds skills + match %
"""
# %%
import json
from pathlib import Path
from typing import List, Dict
import logging

from . import extract_skills, load_resume_skills, calculate_match

logger = logging.getLogger(__name__)

DATA_RAW = Path("data/raw")
DATA_PROCESSED = Path("data/processed")
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

def process_latest_jobs():
    # Find the latest JSON
    raw_files = list(DATA_RAW.glob("jobs_*.json"))
    if not raw_files:
        logger.error("No raw data! Run Step 1.")
        return

    latest_file = max(raw_files, key=lambda p: p.stat().st_mtime)
    logger.info(f"Processing: {latest_file.name}")

    with open(latest_file, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    # Load your resume
    resume_skills = load_resume_skills()

    processed = []
    for job in jobs:
        desc = job.get("description", "") + " " + job.get("title", "")
        job_skills = extract_skills(desc)
        match_pct = calculate_match(job_skills, resume_skills)

        job_enhanced = job.copy()
        job_enhanced.update({
            "extracted_skills": list(job_skills),
            "match_percentage": match_pct,
            "missing_skills": list(resume_skills - job_skills),
            "extra_skills": list(job_skills - resume_skills)
        })
        processed.append(job_enhanced)

    # Sort by match %
    processed.sort(key=lambda x: x["match_percentage"], reverse=True)

    # Save
    out_file = DATA_PROCESSED / f"matched_{latest_file.stem}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

    logger.info(f"Done! Processed {len(processed)} jobs → {out_file.name}")
    logger.info(f"Top-3 match: {[j['match_percentage'] for j in processed[:3]]}%")

    # Show top-3
    print("\nTOP-3 JOBS:")
    for i, j in enumerate(processed[:3], 1):
        print(f"{i}. {j['title']} | {j['company']} | {j['location']}")
        print(f"   Match: {j['match_percentage']}% | Skills: {', '.join(j['extracted_skills'][:5])}")
        print(f"   → {j['job_url']}\n")

# %%

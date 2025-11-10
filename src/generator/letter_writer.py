"""
Saves cover letters for top-N jobs
"""
# %%
from pathlib import Path
import json
import logging
from . import generate_cover_letter

logger = logging.getLogger(__name__)

LETTERS_DIR = Path("data/letters")
LETTERS_DIR.mkdir(exist_ok=True)

def write_cover_letters(top_n: int = 3):
    processed_files = list(Path("data/processed").glob("matched_*.json"))
    if not processed_files:
        logger.error("No processed job files found!")
        return

    latest = max(processed_files, key=lambda p: p.stat().st_mtime)
    with open(latest, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    # Load your skills
    resume_file = Path("data/resume_skills.json")
    if not resume_file.exists():
        logger.error("Resume not found!")
        return
    with open(resume_file, "r", encoding="utf-8") as f:
        resume_skills = json.load(f)

    # Generate for top-N
    for i, job in enumerate(jobs[:top_n]):
        letter = generate_cover_letter(job, resume_skills)
        
        safe_title = "".join(c if c.isalnum() else "_" for c in job["title"][:50])
        safe_company = "".join(c if c.isalnum() else "_" for c in job["company"][:30])
        filename = LETTERS_DIR / f"letter_{i+1}_{safe_title}_{safe_company}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Job: {job['title']}\n")
            f.write(f"Company: {job['company']} | {job['location']}\n")
            f.write(f"Match: {job['match_percentage']}%\n")
            f.write(f"URL: {job['job_url']}\n")
            f.write("="*60 + "\n\n")
            f.write(letter)
        
        logger.info(f"Letter {i+1} → {filename.name}")
        print(f"Letter {i+1}: {filename.name}")

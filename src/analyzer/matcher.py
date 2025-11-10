"""
Matching my CV with job description → Match %
"""
# %%
from typing import Dict, List, Set
import json
from pathlib import Path

def calculate_match(job_skills: Set[str], resume_skills: Set[str]) -> float:
    if not resume_skills:
        return 0.0
    intersection = job_skills.intersection(resume_skills)
    return round(len(intersection) / len(resume_skills) * 100, 1)

def load_resume_skills() -> Set[str]:
    """
    Requests your skills once.
    Saves to data/resume_skills.json
    """
    resume_file = Path("data/resume_skills.json")
    if resume_file.exists():
        with open(resume_file, "r", encoding="utf-8") as f:
            skills = json.load(f)
        print(f"Loaded resume: {len(skills)} skills")
        return set(skills)

    print("\nEnter your skills (comma separated):")
    print("Example: python, sql, excel, tableau, aws, git")
    user_input = input("→ ").strip().lower()
    skills = {s.strip() for s in user_input.split(",") if s.strip()}
    
    resume_file.parent.mkdir(exist_ok=True)
    with open(resume_file, "w", encoding="utf-8") as f:
        json.dump(list(skills), f, indent=2)
    print(f"Saved {len(skills)} skills to {resume_file}")
    return skills

# %%

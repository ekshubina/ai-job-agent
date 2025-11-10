"""
Generation of cover letter through local distilgpt2
Offline, fast, personalized
"""
# %%
from transformers import pipeline
from pathlib import Path
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Load model once (offline)
try:
    generator = pipeline(
        "text-generation",
        model="distilgpt2",
        max_length=500,
        truncation=True,
        pad_token_id=50256
    )
    logger.info("distilgpt2 loaded (offline)")
except Exception as e:
    logger.error(f"Model loading error: {e}")
    generator = None

def generate_cover_letter(job: dict, resume_skills: list) -> str:
    """
    Generates a cover letter tailored to the job.
    """
    if not generator:
        return "Error: model not loaded."
    title = job.get("title", "Data Analyst")
    company = job.get("company", "the company")
    location = job.get("location", "Remote")
    match = job.get("match_percentage", 0)
    skills = job.get("extracted_skills", [])[:7]  # top-7
    missing = job.get("missing_skills", [])

    # Form prompt
    skills_str = ", ".join(skills)
    prompt = f"""Write a professional cover letter for a {title} position at {company} in {location}.

I am a Data Analyst with strong skills in {skills_str}. My background includes predictive modeling, ETL pipelines, and stakeholder communication.

I am excited to apply because"""
    
    # Generation
    result = generator(prompt, max_new_tokens=250, do_sample=True, temperature=0.7)
    generated = result[0]["generated_text"]
    
    # Trim to end of sentence
    letter = generated.split("I am excited to apply because")[1].strip()
    letter = letter.split("\n\n")[0].strip()
    
    # Add signature
    letter += f"""

Best regards,
[Your Name]
Data Analyst | {len(resume_skills)} key skills | {match}% match
"""
    return letter.strip()

# %%

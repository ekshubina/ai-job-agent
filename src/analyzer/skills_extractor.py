"""
Flair NER — skills extraction from job description
Offline, local model
"""
# %%


from typing import List, Set
from flair.data import Sentence
from flair.models import SequenceTagger
import logging

logger = logging.getLogger(__name__)

# ------------------- Model Loading -------------------
try:
    tagger = SequenceTagger.load("flair/ner-english-large")
    logger.info("Flair NER модель загружена (оффлайн)")
except Exception as e:
    logger.error(f"Ошибка загрузки Flair: {e}")
    tagger = None

# ------------------- Extended Skills List  -------------------
KNOWN_SKILLS = {
    # Data Science & Machine Learning
    "predictive modeling", "regression", "classification", "clustering", "nlp",
    "time-series analysis", "time series", "network analysis", "neural networks",
    "deep learning", "feature engineering", "hyperparameter tuning", "etl pipelines",
    "etl", "ml", "machine learning",

    # Programming & Tools
    "python", "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "sql",
    "jupyter", "tableau", "git", "github copilot", "copilot", "mcp",

    # Data Extraction & Processing
    "api integration", "restful api", "rest api", "web scraping", "data cleaning",
    "data preprocessing", "data enrichment",

    # Statistical Analysis
    "hypothesis testing", "a/b testing", "ab testing", "statistical inference",
    "probability distributions", "bayesian methods", "bayesian",

    # Business Intelligence
    "kpi development", "kpi", "data visualization", "business impact analysis",
    "risk assessment",

    # Soft Skills (often mentioned in job descriptions)
    "problem-solving", "problem solving", "cross-functional collaboration",
    "distributed team", "stakeholder communication", "pitching", "presenting",
    "communication", "collaboration", "teamwork"
}

# ------------------- Extraction Function -------------------
def extract_skills(text: str) -> Set[str]:
    """
    Extracts skills from job description text.
    1. Exact match (based on KNOWN_SKILLS)
    2. NER: ORG/PRODUCT (tools)
    """
    if not tagger or not text:
        return set()

    text_lower = text.lower()
    found = set()

    # 1. Exact match
    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            found.add(skill)

    # 2. NER: look for tools/libraries
    sentence = Sentence(text)
    tagger.predict(sentence)
    for entity in sentence.get_spans('ner'):
        label = entity.tag
        value = entity.text.lower()
        if label in ["ORG", "PRODUCT", "MISC"] and value in KNOWN_SKILLS:
            found.add(value)

    return found
# %%

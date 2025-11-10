
# %%
"""
AI Job Agent — full pipeline
"""
import logging
from src.scraper.jobspy_parser import scrape_and_save
from src.analyzer.processor import process_latest_jobs
from src.generator.letter_writer import write_cover_letters

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("AI Job Agent — Full Pipeline\n")
    
    # Step 1: Scraping
    print("1. Scraping jobs...")
    filepath = scrape_and_save()
    
    if not filepath:
        print("No new jobs found.")
        exit()

    # Step 2: Analysis
    print("\n2. Analysis + Match %...")
    process_latest_jobs()
    
    # Step 3: Cover Letters
    print("\n3. Generating Cover Letters (top-3)...")
    write_cover_letters(top_n=3)
    
    print("\nDONE! Letters are in data/letters/")
    print("You can start sending applications!")
# %%

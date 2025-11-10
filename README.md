# AI Job Agent 🤖

An automated tool that helps streamline your job application process by scraping job postings, analyzing matches with your skills, and generating personalized cover letters.

## Features

- 🔍 **Job Scraping**: Automatically scrapes job postings and saves them locally
- 📊 **Skills Analysis**: Analyzes job requirements and matches them against your resume skills
- ✍️ **Cover Letter Generation**: Automatically generates personalized cover letters for top matching positions
- 💾 **Data Management**: Organizes scraped jobs, processed results, and generated letters in a structured format

## Project Structure

```
.
├── main.py              # Main execution script
├── requirements.txt     # Project dependencies
├── data/               # Data storage
│   ├── resume_skills.json       # Your resume skills
│   ├── letters/               # Generated cover letters
│   ├── processed/            # Processed job matches
│   └── raw/                  # Raw scraped job data
└── src/                # Source code
    ├── analyzer/             # Job analysis modules
    ├── generator/           # Cover letter generation
    ├── scraper/            # Job scraping functionality
    └── utils/              # Utility functions
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ekshubina/ai-job-agent.git
cd ai-job-agent
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the full pipeline with:

```bash
python main.py
```

This will execute:
1. Job scraping to find new positions
2. Analysis and matching with your skills
3. Generation of cover letters for top matches

The generated cover letters will be saved in `data/letters/`.

## Configuration

- Add your skills to `data/resume_skills.json`
- Configure job search parameters in the scraper settings
- Adjust matching thresholds in the analyzer settings

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt
- Internet connection for job scraping

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

[MIT License](LICENSE)

## Author

[ekshubina](https://github.com/ekshubina)

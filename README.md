# AutoApply Tools

This repository contains two approaches to automating job applications:

- **Chrome Extension** – located in the `extension/` directory. It can auto-fill basic web forms directly inside the browser.
- **Python Job Application Agent** – a modular framework found in the `job_bot/` directory for scraping jobs, logging in with Selenium, and preparing cover letters.

## Python Agent

### Setup
1. Copy `.env.example` to `.env` and populate with your credentials (e.g. `LEVER_USERNAME`, `LEVER_PASSWORD`, `RESUME_PATH`).
2. Install dependencies with `pip install -r requirements.txt`.
   The Selenium driver is provisioned automatically via `webdriver-manager` but requires a Chrome/Chromium browser.
3. Run `python job_bot/main.py` to scrape listings, generate cover-letter prompts, attempt applications, and persist status to a local SQLite/CSV store.
   Sites that trigger CAPTCHAs will pause and prompt for manual completion.

### Structure
```
job_bot/
    automation/           # Selenium helpers for login and applications
    scraping/             # Site-specific scrapers (e.g. RemoteOK, Lever)
    llm/                  # Prompt builders for local LLMs
    storage.py            # SQLite/CSV persistence for application status
    main.py               # Orchestrates scraping, prompt generation, and applying
    data/                 # Storage for resumes, cover letters and application DB
```

Refer to module docstrings and comments for details on extending the framework.

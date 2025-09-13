"""Entry point tying together scraping, prompt generation, and application automation."""
from __future__ import annotations

import logging
import os
from pathlib import Path

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from .automation.apply import JobApplicationAutomator
from .config import load_credentials
from .llm.prompt_builder import build_cover_letter_prompt
from .scraping import remoteok
from .storage import ApplicationStorage


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Prepare storage and paths
    storage = ApplicationStorage()
    data_dir = Path(__file__).resolve().parent / "data"
    cover_dir = data_dir / "cover_letters"
    cover_dir.mkdir(parents=True, exist_ok=True)
    resume_path = Path(os.getenv("RESUME_PATH", data_dir / "resumes" / "resume.txt"))

    # Scrape jobs
    jobs = remoteok.fetch_jobs("python")

    # Set up Selenium driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    automator = JobApplicationAutomator(driver)
    creds = load_credentials("LEVER")  # example prefix

    for job in jobs:
        # Build cover letter prompt
        description = requests.get(job["link"], timeout=30).text
        prompt = build_cover_letter_prompt(description, resume_path)
        cl_path = cover_dir / f"{job['company']}_{job['title']}.txt"
        cl_path.write_text(prompt, encoding="utf-8")

        # Example login and application; selectors must be customized per site
        try:
            automator.login(
                url="https://example.com/login",
                username=creds.username,
                password=creds.password,
                username_selector="#username",
                password_selector="#password",
                submit_selector="button[type='submit']",
                captcha_selector="#captcha",
            )
            automator.fill_application_form(
                url="https://example.com/application",
                fields={"input[name='name']": "Your Name"},
                resume_path=resume_path,
                cover_letter_path=cl_path,
                submit_selector="button[type='submit']",
                captcha_selector="#captcha",
            )
            status = "applied"
        except Exception as exc:
            logging.exception("Application failed: %s", exc)
            status = "failed"
        storage.add_application(job["title"], job["company"], job["link"], status)

    driver.quit()


if __name__ == "__main__":
    main()

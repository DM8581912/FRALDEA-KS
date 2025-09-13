"""Scraper for Lever job boards."""
from __future__ import annotations

import logging
from typing import Dict, List

import requests

logger = logging.getLogger(__name__)

API_URL = "https://api.lever.co/v0/postings/{company}?mode=json"


def fetch_jobs(company: str) -> List[Dict[str, str]]:
    """Fetch job listings from Lever for a given company."""
    url = API_URL.format(company=company)
    logger.info("Fetching Lever jobs from %s", url)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    jobs: List[Dict[str, str]] = []
    for posting in data:
        jobs.append(
            {
                "title": posting.get("text", ""),
                "company": company,
                "link": posting.get("hostedUrl", ""),
            }
        )
    logger.info("Found %d jobs", len(jobs))
    return jobs

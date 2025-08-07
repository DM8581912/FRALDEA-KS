"""Scraper for job listings on RemoteOK."""
from __future__ import annotations

import logging
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

REMOTEOK_URL = "https://remoteok.com/"


def fetch_jobs(keyword: str | None = None) -> List[Dict[str, str]]:
    """Fetch job listings from RemoteOK.

    Parameters
    ----------
    keyword: str, optional
        Keyword to filter job listings.

    Returns
    -------
    List[Dict[str, str]]
        List of jobs with title, company, and link.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    url = REMOTEOK_URL
    if keyword:
        url += f"remote-{keyword}"  # simple keyword search
    logger.info("Fetching jobs from %s", url)
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    jobs: List[Dict[str, str]] = []
    for row in soup.select("tr.job"):
        title_el = row.select_one("h2")
        company_el = row.select_one("h3")
        link_el = row.get("data-href")
        if not (title_el and company_el and link_el):
            continue
        job = {
            "title": title_el.get_text(strip=True),
            "company": company_el.get_text(strip=True),
            "link": f"https://remoteok.com{link_el}",
        }
        jobs.append(job)
    logger.info("Found %d jobs", len(jobs))
    return jobs

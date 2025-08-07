"""Automation helpers for logging in and submitting job applications."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class JobApplicationAutomator:
    """Automate login and job application form submission using Selenium."""

    def __init__(self, driver: WebDriver, timeout: int = 20) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _handle_captcha(self, captcha_selector: str) -> None:
        """Pause execution if a CAPTCHA is present and wait for user input."""
        if self.driver.find_elements(By.CSS_SELECTOR, captcha_selector):
            logger.warning("CAPTCHA detected. Please solve it manually in the browser.")
            input("Press Enter after solving the CAPTCHA...")

    def login(
        self,
        url: str,
        username: str,
        password: str,
        username_selector: str,
        password_selector: str,
        submit_selector: str,
        captcha_selector: Optional[str] = None,
    ) -> None:
        """Log in to a job site."""
        logger.info("Navigating to login page: %s", url)
        self.driver.get(url)

        if captcha_selector:
            self._handle_captcha(captcha_selector)

        logger.debug("Filling username and password")
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, username_selector))).send_keys(
            username
        )
        self.driver.find_element(By.CSS_SELECTOR, password_selector).send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, submit_selector).click()
        logger.info("Login submitted")

    def fill_application_form(
        self,
        url: str,
        fields: Dict[str, str],
        resume_path: Optional[Path] = None,
        cover_letter_path: Optional[Path] = None,
        submit_selector: Optional[str] = None,
        captcha_selector: Optional[str] = None,
    ) -> None:
        """Fill and optionally submit an application form.

        Parameters
        ----------
        url: str
            URL of the application form.
        fields: Dict[str, str]
            Mapping of CSS selectors to the values that should be entered.
        resume_path: Path, optional
            Path to the resume file to upload if required.
        cover_letter_path: Path, optional
            Path to the cover letter file to upload if required.
        submit_selector: str, optional
            CSS selector for the submit button. If provided, the form will be
            submitted automatically.
        """
        logger.info("Navigating to application form: %s", url)
        self.driver.get(url)

        if captcha_selector:
            self._handle_captcha(captcha_selector)

        for selector, value in fields.items():
            logger.debug("Setting field %s", selector)
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            element.clear()
            element.send_keys(value)

        if resume_path:
            logger.debug("Uploading resume from %s", resume_path)
            resume_element = self.driver.find_element(By.CSS_SELECTOR, '[type="file"][name*="resume"]')
            resume_element.send_keys(str(resume_path.resolve()))

        if cover_letter_path:
            logger.debug("Uploading cover letter from %s", cover_letter_path)
            cl_element = self.driver.find_element(By.CSS_SELECTOR, '[type="file"][name*="cover"]')
            cl_element.send_keys(str(cover_letter_path.resolve()))

        if submit_selector:
            logger.info("Submitting application form")
            self.driver.find_element(By.CSS_SELECTOR, submit_selector).click()

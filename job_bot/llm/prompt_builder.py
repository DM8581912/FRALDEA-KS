"""Utilities for building prompts for local LLMs."""
from __future__ import annotations

from pathlib import Path


def build_cover_letter_prompt(job_description: str, resume_path: Path) -> str:
    """Construct a prompt for a local LLM to generate a cover letter.

    Parameters
    ----------
    job_description: str
        Raw job description text.
    resume_path: Path
        Path to the user's resume in text format.

    Returns
    -------
    str
        Prompt string combining the resume and job description.
    """
    resume_text = resume_path.read_text(encoding="utf-8")
    prompt = (
        "Using the resume below, craft a personalized cover letter for the"
        " following job description.\n\n"\
        f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}\n"
    )
    return prompt

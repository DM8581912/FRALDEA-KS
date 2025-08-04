"""Utilities for persisting application status to SQLite and CSV."""
from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Tuple

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "applications.db"
CSV_PATH = DATA_DIR / "applications.csv"


@dataclass
class ApplicationRecord:
    title: str
    company: str
    link: str
    status: str
    applied_at: str


class ApplicationStorage:
    """Store application status in SQLite and mirror to CSV."""

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                link TEXT UNIQUE,
                status TEXT,
                applied_at TEXT
            )
            """
        )
        self.conn.commit()

    def add_application(self, title: str, company: str, link: str, status: str) -> None:
        """Insert a new application record and export to CSV."""
        now = datetime.utcnow().isoformat()
        self.conn.execute(
            "INSERT OR REPLACE INTO applications (title, company, link, status, applied_at) VALUES (?, ?, ?, ?, ?)",
            (title, company, link, status, now),
        )
        self.conn.commit()
        self._export_csv()

    def update_status(self, link: str, status: str) -> None:
        """Update status of an application by link."""
        self.conn.execute("UPDATE applications SET status=? WHERE link=?", (status, link))
        self.conn.commit()
        self._export_csv()

    def list_applications(self) -> Iterable[ApplicationRecord]:
        cur = self.conn.execute(
            "SELECT title, company, link, status, applied_at FROM applications ORDER BY applied_at DESC"
        )
        rows = cur.fetchall()
        for row in rows:
            yield ApplicationRecord(*row)

    def _export_csv(self) -> None:
        cur = self.conn.execute(
            "SELECT title, company, link, status, applied_at FROM applications ORDER BY applied_at DESC"
        )
        rows: Iterable[Tuple[str, str, str, str, str]] = cur.fetchall()
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["title", "company", "link", "status", "applied_at"])
            writer.writerows(rows)

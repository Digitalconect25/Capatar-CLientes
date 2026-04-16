import sqlite3
from datetime import datetime
from pathlib import Path

from app.models import LeadCreate, LeadRecord

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    postal_code TEXT NOT NULL,
    city TEXT NOT NULL,
    region TEXT NOT NULL,
    lead_type TEXT NOT NULL,
    budget_eur REAL NOT NULL,
    wants_portability INTEGER NOT NULL,
    preferred_channel TEXT NOT NULL,
    best_time_slot TEXT NOT NULL,
    has_confirmed_coverage INTEGER NOT NULL,
    gdpr_consent INTEGER NOT NULL,
    source TEXT NOT NULL,
    score INTEGER NOT NULL,
    priority TEXT NOT NULL,
    assigned_action TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class LeadStorage:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(SCHEMA)
            conn.commit()

    def insert_lead(self, lead: LeadCreate, score: int, priority: str, assigned_action: str) -> LeadRecord:
        created_at = datetime.utcnow().isoformat()
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO leads (
                    full_name, phone, email, postal_code, city, region,
                    lead_type, budget_eur, wants_portability, preferred_channel,
                    best_time_slot, has_confirmed_coverage, gdpr_consent, source,
                    score, priority, assigned_action, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    lead.full_name,
                    lead.phone,
                    lead.email,
                    lead.postal_code,
                    lead.city,
                    lead.region,
                    lead.lead_type,
                    lead.budget_eur,
                    int(lead.wants_portability),
                    lead.preferred_channel,
                    lead.best_time_slot,
                    int(lead.has_confirmed_coverage),
                    int(lead.gdpr_consent),
                    lead.source,
                    score,
                    priority,
                    assigned_action,
                    created_at,
                ),
            )
            conn.commit()
            lead_id = cursor.lastrowid

        return LeadRecord(
            id=lead_id,
            score=score,
            priority=priority,
            assigned_action=assigned_action,
            created_at=datetime.fromisoformat(created_at),
            **lead.model_dump(),
        )

    def list_leads(self, limit: int = 50) -> list[LeadRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, full_name, phone, email, postal_code, city, region, lead_type,
                       budget_eur, wants_portability, preferred_channel, best_time_slot,
                       has_confirmed_coverage, gdpr_consent, source,
                       score, priority, assigned_action, created_at
                FROM leads
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        records = []
        for row in rows:
            records.append(
                LeadRecord(
                    id=row[0],
                    full_name=row[1],
                    phone=row[2],
                    email=row[3],
                    postal_code=row[4],
                    city=row[5],
                    region=row[6],
                    lead_type=row[7],
                    budget_eur=row[8],
                    wants_portability=bool(row[9]),
                    preferred_channel=row[10],
                    best_time_slot=row[11],
                    has_confirmed_coverage=bool(row[12]),
                    gdpr_consent=bool(row[13]),
                    source=row[14],
                    score=row[15],
                    priority=row[16],
                    assigned_action=row[17],
                    created_at=datetime.fromisoformat(row[18]),
                )
            )
        return records

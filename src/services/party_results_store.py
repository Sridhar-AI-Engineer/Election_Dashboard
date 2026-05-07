import sqlite3
from csv import DictReader
from pathlib import Path

import pandas as pd


DB_PATH = Path("data") / "election_dashboard.db"
CONSTITUENCIES_CSV_PATH = Path("data") / "constituencies.csv"

PARTY_RESULTS = [
    {
        "party_code": "TVK",
        "party_name": "Tamilaga Vettri Kazhagam - TVK",
        "won": 108,
        "leading": 0,
        "total": 108,
    },
    {
        "party_code": "DMK",
        "party_name": "Dravida Munnetra Kazhagam - DMK",
        "won": 59,
        "leading": 0,
        "total": 59,
    },
    {
        "party_code": "ADMK",
        "party_name": "All India Anna Dravida Munnetra Kazhagam - ADMK",
        "won": 47,
        "leading": 0,
        "total": 47,
    },
    {
        "party_code": "INC",
        "party_name": "Indian National Congress - INC",
        "won": 5,
        "leading": 0,
        "total": 5,
    },
    {
        "party_code": "PMK",
        "party_name": "Pattali Makkal Katchi - PMK",
        "won": 4,
        "leading": 0,
        "total": 4,
    },
    {
        "party_code": "IUML",
        "party_name": "Indian Union Muslim League - IUML",
        "won": 2,
        "leading": 0,
        "total": 2,
    },
    {
        "party_code": "CPI",
        "party_name": "Communist Party of India - CPI",
        "won": 2,
        "leading": 0,
        "total": 2,
    },
    {
        "party_code": "VCK",
        "party_name": "Viduthalai Chiruthaigal Katchi - VCK",
        "won": 2,
        "leading": 0,
        "total": 2,
    },
    {
        "party_code": "CPI(M)",
        "party_name": "Communist Party of India (Marxist) - CPI(M)",
        "won": 2,
        "leading": 0,
        "total": 2,
    },
    {
        "party_code": "BJP",
        "party_name": "Bharatiya Janata Party - BJP",
        "won": 1,
        "leading": 0,
        "total": 1,
    },
    {
        "party_code": "DMDK",
        "party_name": "Desiya Murpokku Dravida Kazhagam - DMDK",
        "won": 1,
        "leading": 0,
        "total": 1,
    },
    {
        "party_code": "AMMKMNKZ",
        "party_name": "Amma Makkal Munnettra Kazagam - AMMKMNKZ",
        "won": 1,
        "leading": 0,
        "total": 1,
    },
]

TOP_CARD_CODES = ["TVK", "DMK", "ADMK", "INC", "PMK", "IUML", "CPI"]
PARTY_TABLE_CODES = [
    "TVK",
    "DMK",
    "ADMK",
    "INC",
    "PMK",
    "IUML",
    "CPI",
    "VCK",
    "CPI(M)",
    "BJP",
    "DMDK",
    "AMMKMNKZ",
]


def _get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_party_results() -> None:
    with _get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS party_results (
                party_code TEXT PRIMARY KEY,
                party_name TEXT NOT NULL,
                won INTEGER NOT NULL,
                leading INTEGER NOT NULL,
                total INTEGER NOT NULL
            )
            """
        )
        cursor.executemany(
            """
            INSERT INTO party_results (party_code, party_name, won, leading, total)
            VALUES (:party_code, :party_name, :won, :leading, :total)
            ON CONFLICT(party_code) DO UPDATE SET
                party_name = excluded.party_name,
                won = excluded.won,
                leading = excluded.leading,
                total = excluded.total
            """,
            PARTY_RESULTS,
        )
        connection.commit()


def init_constituencies() -> None:
    with _get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS constituencies (
                constituency_name TEXT PRIMARY KEY,
                leading_party TEXT NOT NULL,
                vote_share REAL NOT NULL,
                turnout_pct REAL NOT NULL,
                lat REAL,
                lon REAL,
                status TEXT
            )
            """
        )

        existing_row = cursor.execute("SELECT COUNT(1) FROM constituencies").fetchone()
        existing_count = int(existing_row[0]) if existing_row else 0

        if existing_count == 0 and CONSTITUENCIES_CSV_PATH.exists():
            with CONSTITUENCIES_CSV_PATH.open("r", encoding="utf-8", newline="") as file:
                rows = list(DictReader(file))

            payload = []
            for row in rows:
                vote_share = float(row.get("vote_share") or 0)
                turnout_pct = float(row.get("turnout_pct") or vote_share)
                lat = row.get("lat")
                lon = row.get("lon")
                payload.append(
                    {
                        "constituency_name": row.get("constituency_name", ""),
                        "leading_party": row.get("leading_party", ""),
                        "vote_share": vote_share,
                        "turnout_pct": turnout_pct,
                        "lat": float(lat) if lat not in (None, "") else None,
                        "lon": float(lon) if lon not in (None, "") else None,
                        "status": row.get("status", "leading"),
                    }
                )

            cursor.executemany(
                """
                INSERT INTO constituencies (
                    constituency_name,
                    leading_party,
                    vote_share,
                    turnout_pct,
                    lat,
                    lon,
                    status
                ) VALUES (
                    :constituency_name,
                    :leading_party,
                    :vote_share,
                    :turnout_pct,
                    :lat,
                    :lon,
                    :status
                )
                ON CONFLICT(constituency_name) DO UPDATE SET
                    leading_party = excluded.leading_party,
                    vote_share = excluded.vote_share,
                    turnout_pct = excluded.turnout_pct,
                    lat = excluded.lat,
                    lon = excluded.lon,
                    status = excluded.status
                """,
                payload,
            )

        connection.commit()


def fetch_party_table() -> list[dict]:
    with _get_connection() as connection:
        cursor = connection.cursor()
        rows = cursor.execute(
            """
            SELECT party_code, party_name, won, leading, total
            FROM party_results
            """
        ).fetchall()

    unordered = [
        {
            "party": row[0],
            "party_name": row[1],
            "won": row[2],
            "leading": row[3],
            "total": row[4],
        }
        for row in rows
    ]

    order_map = {party_code: index for index, party_code in enumerate(PARTY_TABLE_CODES)}
    return sorted(unordered, key=lambda item: order_map.get(item["party"], 9999))


def fetch_top_cards() -> list[dict]:
    with _get_connection() as connection:
        cursor = connection.cursor()
        rows = cursor.execute(
            """
            SELECT party_code, won
            FROM party_results
            WHERE party_code IN ({placeholders})
            """.format(placeholders=",".join(["?"] * len(TOP_CARD_CODES))),
            TOP_CARD_CODES,
        ).fetchall()

    seats_by_party = {party_code: won for party_code, won in rows}
    return [{"party": party_code, "won": int(seats_by_party.get(party_code, 0))} for party_code in TOP_CARD_CODES]


def fetch_total_ac() -> int:
    with _get_connection() as connection:
        cursor = connection.cursor()
        row = cursor.execute("SELECT COALESCE(SUM(total), 0) FROM party_results").fetchone()
    return int(row[0] or 0)


def fetch_constituencies(limit: int = 5000) -> list[dict]:
    with _get_connection() as connection:
        cursor = connection.cursor()
        rows = cursor.execute(
            """
            SELECT constituency_name, leading_party, vote_share, turnout_pct, lat, lon
            FROM constituencies
            ORDER BY constituency_name ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "constituency_name": row[0],
            "leading_party": row[1],
            "vote_share": float(row[2] or 0),
            "turnout_pct": float(row[3] or 0),
            "lat": row[4],
            "lon": row[5],
        }
        for row in rows
    ]


def fetch_constituencies_df(limit: int | None = None) -> pd.DataFrame:
    query = """
        SELECT constituency_name, leading_party, vote_share, turnout_pct, lat, lon, status
        FROM constituencies
        ORDER BY constituency_name ASC
    """

    params: tuple = ()
    if limit is not None:
        query += " LIMIT ?"
        params = (limit,)

    with _get_connection() as connection:
        frame = pd.read_sql_query(query, connection, params=params)
    return frame
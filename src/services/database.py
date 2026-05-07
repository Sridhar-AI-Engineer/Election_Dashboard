import sqlalchemy
from sqlalchemy import text

from src.config import CLOUD_SQL_INSTANCE, DB_NAME, DB_PASSWORD, DB_USER


_ENGINE: sqlalchemy.Engine | None = None

def get_cloudsql_engine() -> sqlalchemy.Engine:
    global _ENGINE
    if _ENGINE is not None:
        return _ENGINE

    if not all([CLOUD_SQL_INSTANCE, DB_USER, DB_PASSWORD, DB_NAME]):
        raise ValueError("Cloud SQL config missing. Set CLOUD_SQL_INSTANCE, DB_USER, DB_PASSWORD, DB_NAME.")

    try:
        from google.cloud.sql.connector import Connector
    except Exception as exc:
        raise RuntimeError("google-cloud-sql-connector is not installed") from exc

    connector = Connector()

    def getconn():
        return connector.connect(
            CLOUD_SQL_INSTANCE,
            driver="pg8000",
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
        )

    _ENGINE = sqlalchemy.create_engine("postgresql+pg8000://", creator=getconn, pool_pre_ping=True)
    return _ENGINE


def init_app_tables() -> None:
    engine = get_cloudsql_engine()
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS app_events (
                    id BIGSERIAL PRIMARY KEY,
                    event_type VARCHAR(120) NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS summary_snapshots (
                    id BIGSERIAL PRIMARY KEY,
                    total_ac INTEGER NOT NULL,
                    leading_party VARCHAR(120),
                    leading_seats INTEGER,
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        )


def write_app_event(event_type: str, payload: str) -> None:
    engine = get_cloudsql_engine()
    with engine.begin() as connection:
        connection.execute(
            text("INSERT INTO app_events (event_type, payload) VALUES (:event_type, :payload)"),
            {"event_type": event_type[:120], "payload": payload},
        )


def write_summary_snapshot(total_ac: int, leading_party: str | None, leading_seats: int | None) -> None:
    engine = get_cloudsql_engine()
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO summary_snapshots (total_ac, leading_party, leading_seats)
                VALUES (:total_ac, :leading_party, :leading_seats)
                """
            ),
            {
                "total_ac": int(total_ac),
                "leading_party": leading_party,
                "leading_seats": int(leading_seats) if leading_seats is not None else None,
            },
        )

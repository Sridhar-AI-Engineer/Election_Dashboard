import csv
from pathlib import Path

from src.services.kaggle_service import load_kaggle_results

DATA_DIR = Path("data")
CONSTITUENCY_FILE = DATA_DIR / "constituencies.csv"
ACTIVITY_FILE = DATA_DIR / "activity_logs.csv"


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def ensure_data_files() -> None:
    if CONSTITUENCY_FILE.exists() and ACTIVITY_FILE.exists():
        return

    print("🔥 Auto-fetching TN 2026 data from Kaggle...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    results_df = load_kaggle_results(file_path="")
    results = results_df.to_dict(orient="records")

    _write_csv(CONSTITUENCY_FILE, results)

    activity_rows = [
        {
            "timestamp": "2026-05-07T10:00:00Z",
            "message": f"Kaggle data bootstrap complete. Loaded {len(results)} constituencies.",
            "event": f"Kaggle data bootstrap complete. Loaded {len(results)} constituencies.",
        },
        {
            "timestamp": "2026-05-07T10:00:10Z",
            "message": "Live 2026 election dataset synced from KaggleHub",
            "event": "Live 2026 election dataset synced from KaggleHub",
        },
    ]
    _write_csv(ACTIVITY_FILE, activity_rows)


def main() -> None:
    ensure_data_files()
    print(f"✅ Data ready: {CONSTITUENCY_FILE}")


if __name__ == "__main__":
    main()

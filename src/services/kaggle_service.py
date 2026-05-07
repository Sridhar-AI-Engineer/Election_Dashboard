import hashlib
import os
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from src.config import KAGGLE_DATASET_LINK, KAGGLE_DATASET_REF, KAGGLE_FILE_PATH

DATASET_REF = KAGGLE_DATASET_REF
SUPPORTED_EXTENSIONS = {
    ".csv", ".tsv", ".json", ".jsonl", ".xml", ".parquet", ".feather",
    ".sqlite", ".sqlite3", ".db", ".db3", ".s3db", ".dl3",
    ".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt",
}


def _resolve_dataset_ref() -> str:
    env_link = KAGGLE_DATASET_LINK or os.getenv("KAGGLE_DATASET_LINK", "")
    env_ref = KAGGLE_DATASET_REF or os.getenv("KAGGLE_DATASET_REF", DATASET_REF)

    if env_link:
        parsed = urlparse(env_link)
        parts = [p for p in parsed.path.split("/") if p]
        if "datasets" in parts:
            idx = parts.index("datasets")
            if idx + 2 < len(parts):
                owner = parts[idx + 1]
                dataset = parts[idx + 2]
                return f"{owner}/{dataset}"
    return env_ref


def _pick_column(df: pd.DataFrame, candidates: list[str], default: str | None = None) -> str | None:
    lower_map = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]
    return default


def _coords_from_name(name: str) -> tuple[float, float]:
    digest = hashlib.md5(name.encode("utf-8")).hexdigest()
    a = int(digest[:8], 16) / 0xFFFFFFFF
    b = int(digest[8:16], 16) / 0xFFFFFFFF
    lat = 8.05 + (13.55 - 8.05) * a
    lon = 76.0 + (80.45 - 76.0) * b
    return round(lat, 4), round(lon, 4)


def normalize_results(df: pd.DataFrame) -> pd.DataFrame:
    constituency_col = _pick_column(df, ["constituency_name", "constituency", "ac_name", "seat", "assembly_constituency"])
    party_col = _pick_column(df, ["leading_party", "party", "winner_party", "winning_party"])
    vote_share_col = _pick_column(df, ["vote_share", "vote_share_pct", "vote_percent", "vote_percentage"])
    turnout_col = _pick_column(df, ["turnout_pct", "turnout", "turnout_percent"])
    lat_col = _pick_column(df, ["lat", "latitude"])
    lon_col = _pick_column(df, ["lon", "longitude"])

    if not constituency_col or not party_col:
        raise ValueError("Dataset is missing required columns for constituency/party.")

    out = pd.DataFrame()
    out["constituency_name"] = df[constituency_col].astype(str)
    out["leading_party"] = df[party_col].astype(str)

    if vote_share_col:
        out["vote_share"] = pd.to_numeric(df[vote_share_col], errors="coerce").fillna(0.0)
    else:
        party_counts = out["leading_party"].value_counts(normalize=True)
        out["vote_share"] = out["leading_party"].map(party_counts).fillna(0) * 100

    if turnout_col:
        out["turnout_pct"] = pd.to_numeric(df[turnout_col], errors="coerce").fillna(out["vote_share"])
    else:
        out["turnout_pct"] = out["vote_share"]

    if lat_col and lon_col:
        out["lat"] = pd.to_numeric(df[lat_col], errors="coerce")
        out["lon"] = pd.to_numeric(df[lon_col], errors="coerce")
    else:
        coords = out["constituency_name"].apply(_coords_from_name)
        out["lat"] = coords.apply(lambda x: x[0])
        out["lon"] = coords.apply(lambda x: x[1])

    out["status"] = "leading"
    return out.dropna(subset=["constituency_name", "leading_party"]).reset_index(drop=True)


def load_kaggle_results(file_path: str = "") -> pd.DataFrame:
    import kagglehub
    from kagglehub import KaggleDatasetAdapter

    dataset_ref = _resolve_dataset_ref()
    resolved_file = KAGGLE_FILE_PATH or os.getenv("KAGGLE_FILE_PATH", file_path)
    resolved_file = (resolved_file or "").strip()

    if resolved_file:
        ext = Path(resolved_file).suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            resolved_file = ""

    if not resolved_file:
        dataset_dir = Path(kagglehub.dataset_download(dataset_ref))
        candidates = sorted(
            [
                path for path in dataset_dir.rglob("*")
                if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
            ],
            key=lambda path: path.stat().st_size,
            reverse=True,
        )
        if not candidates:
            raise ValueError(
                "No supported files found in Kaggle dataset. "
                "Set KAGGLE_FILE_PATH in .env/.streamlit/secrets.toml"
            )
        resolved_file = str(candidates[0].relative_to(dataset_dir)).replace("\\", "/")

    raw = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        dataset_ref,
        resolved_file,
    )
    return normalize_results(raw)


def get_kaggle_party_summary(file_path: str = "") -> pd.DataFrame:
    df = load_kaggle_results(file_path=file_path)
    summary = (
        df.groupby("leading_party", as_index=False)
        .agg(seats_leading=("constituency_name", "count"), vote_share_pct=("vote_share", "mean"))
        .sort_values("seats_leading", ascending=False)
    )
    return summary.rename(columns={"leading_party": "party"})


def get_kaggle_activity(limit: int = 20, file_path: str = "") -> pd.DataFrame:
    df = load_kaggle_results(file_path=file_path)
    top = df.sort_values("vote_share", ascending=False).head(limit).copy()
    top["event"] = top.apply(
        lambda row: f"{row['constituency_name']}: {row['leading_party']} leading ({float(row['vote_share']):.1f}%)",
        axis=1,
    )
    return top[["event"]]

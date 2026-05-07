import pandas as pd


def _to_numeric(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series([None] * len(df))
    return pd.to_numeric(df[column], errors="coerce")


def _winner_margin_analysis(df: pd.DataFrame) -> list[dict]:
    if "Constituency" not in df.columns or "Total Votes" not in df.columns:
        return []

    work = df.copy()
    work["Total Votes"] = pd.to_numeric(work["Total Votes"], errors="coerce")
    work = work.dropna(subset=["Constituency", "Total Votes"])
    if work.empty:
        return []

    records = []
    for constituency, group in work.groupby("Constituency"):
        g = group.sort_values("Total Votes", ascending=False).head(2)
        if len(g) < 2:
            continue
        top = g.iloc[0]
        second = g.iloc[1]
        margin = int(top["Total Votes"] - second["Total Votes"])
        records.append(
            {
                "constituency": constituency,
                "winner": str(top.get("Candidate", "N/A")),
                "winner_party": str(top.get("Party", "N/A")),
                "runner": str(second.get("Candidate", "N/A")),
                "runner_party": str(second.get("Party", "N/A")),
                "margin_votes": margin,
            }
        )

    return sorted(records, key=lambda x: x["margin_votes"])[:10]


def _ml_benchmark(df: pd.DataFrame) -> dict:
    required = {"Party", "EVM Votes", "Postal Votes", "% Votes", "Constituency", "Total Votes"}
    if not required.issubset(set(df.columns)):
        return {"status": "skipped", "reason": "Required ML columns not available in dataset."}

    try:
        from sklearn.compose import ColumnTransformer
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
    except Exception as exc:
        return {"status": "skipped", "reason": f"Scikit-learn unavailable: {exc}"}

    work = df.copy()
    for col in ["EVM Votes", "Postal Votes", "Total Votes", "% Votes"]:
        work[col] = pd.to_numeric(work[col], errors="coerce")
    work = work.dropna(subset=["Party", "EVM Votes", "Postal Votes", "Total Votes", "% Votes", "Constituency"])
    if work.empty:
        return {"status": "skipped", "reason": "No clean rows for ML training."}

    work["Winner"] = work.groupby("Constituency")["Total Votes"].transform(lambda x: (x == x.max()).astype(int))

    X = work[["Party", "EVM Votes", "Postal Votes", "% Votes"]]
    y = work["Winner"]

    if y.nunique() < 2:
        return {"status": "skipped", "reason": "Target class has insufficient variety."}

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["Party"]),
            ("num", StandardScaler(), ["EVM Votes", "Postal Votes", "% Votes"]),
        ]
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    scores = []
    for name, model in models.items():
        pipe = Pipeline([("prep", preprocessor), ("model", model)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        scores.append({"model": name, "accuracy": round(float(accuracy_score(y_test, pred)), 4)})

    return {"status": "ok", "scores": scores}


def generate_analysis_report(df: pd.DataFrame) -> dict:
    report = {
        "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "missing": {k: int(v) for k, v in df.isnull().sum().to_dict().items()},
        "duplicates": int(df.duplicated().sum()),
        "columns": [str(c) for c in df.columns],
        "top_candidates": [],
        "top_parties": [],
        "high_turnout": [],
        "close_fights": [],
        "ml": {"status": "skipped", "reason": "Not attempted"},
    }

    if "Candidate" in df.columns and "Total Votes" in df.columns:
        temp = df.copy()
        temp["Total Votes"] = _to_numeric(temp, "Total Votes")
        tc = temp.sort_values("Total Votes", ascending=False).head(10)
        cols = [c for c in ["Candidate", "Party", "Constituency", "Total Votes"] if c in tc.columns]
        report["top_candidates"] = tc[cols].to_dict(orient="records")

    if "Party" in df.columns and "Total Votes" in df.columns:
        temp = df.copy()
        temp["Total Votes"] = _to_numeric(temp, "Total Votes")
        party_votes = (
            temp.groupby("Party", as_index=False)["Total Votes"]
            .sum()
            .sort_values("Total Votes", ascending=False)
            .head(15)
        )
        report["top_parties"] = party_votes.to_dict(orient="records")

    if "turnout_pct" in df.columns:
        temp = df.copy()
        temp["turnout_pct"] = _to_numeric(temp, "turnout_pct")
        cols = [c for c in ["constituency_name", "leading_party", "turnout_pct"] if c in temp.columns]
        report["high_turnout"] = temp.sort_values("turnout_pct", ascending=False).head(10)[cols].to_dict(orient="records")

    report["close_fights"] = _winner_margin_analysis(df)
    report["ml"] = _ml_benchmark(df)
    return report

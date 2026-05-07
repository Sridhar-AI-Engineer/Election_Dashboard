import pandas as pd
import streamlit as st

from src.config import GEMINI_API_KEY, GEMINI_MODEL

import google.generativeai as genai


genai.configure(api_key=GEMINI_API_KEY or st.secrets.get("VERTEX_API_KEY", "dummy"))


@st.cache_data
def generate_insights(df: pd.DataFrame) -> list[str]:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Analyze TN 2026 election: {df.head(10).to_json()}. Key insights (3 bullets):"
        response = model.generate_content(prompt)
        text = response.text or ""
        insights = [line.strip("-• ").strip() for line in text.split("\n") if line.strip()]
        return insights[:3]
    except Exception:
        return ["Gemini insight unavailable right now."]


def generate_election_insights(results_df: pd.DataFrame) -> str:
    if results_df.empty:
        return "No data available to generate insights."

    insights = generate_insights(results_df)
    if not insights:
        return "No insight generated."
    return "\n".join(f"- {item}" for item in insights)


@st.cache_data(ttl=30)
def explain_election_live(
    df_constituencies: pd.DataFrame,
    df_results: pd.DataFrame,
    df_activity: pd.DataFrame,
    explanation_mode: str = "News Anchor (Simple)",
) -> list[str]:
    if df_constituencies.empty or df_results.empty:
        return [
            "Live data is still loading.",
            "No close-fight signal yet.",
            "Trend will appear once seat data updates.",
        ]

    party_col = "party" if "party" in df_results.columns else "leading_party"
    turnout_col = "turnout_pct" if "turnout_pct" in df_constituencies.columns else None
    events_col = "event" if "event" in df_activity.columns else "message"

    party_counts = df_results[party_col].value_counts(dropna=True)
    top_party = party_counts.index[0] if len(party_counts) else "N/A"
    top_seats = int(party_counts.iloc[0]) if len(party_counts) else 0
    avg_turnout = (
        float(df_constituencies[turnout_col].mean()) if turnout_col else float(df_constituencies.get("vote_share", pd.Series([0])).mean())
    )

    recent_events = []
    if not df_activity.empty and events_col in df_activity.columns:
        recent_events = [str(x) for x in df_activity[events_col].tail(3).tolist()]

    summary = f"""
    TN 2026 Election Live Analysis:
    - Total seats: {len(df_constituencies)} / 234
    - Top party: {top_party} ({top_seats} seats)
    - Avg turnout: {avg_turnout:.1f}%
    - Recent activity: {len(df_activity)} events

    Recent changes: {recent_events}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Explain this TN election data in SIMPLE TERMS (like TV news):
        1. Who's winning and why?
        2. Any surprises or close fights?
        3. What's the big trend?

        Data: {summary}

        Output 3 bullet points only. News-style, no jargon.
        Explain like a {explanation_mode.lower()}.
        """
        response = model.generate_content(prompt)
        text = response.text or ""
        lines = [line.strip("-• ").strip() for line in text.split("\n") if line.strip()]
        if not lines:
            raise ValueError("Empty Gemini response")
        while len(lines) < 3:
            lines.append("Awaiting next counting trend update.")
        return lines[:3]
    except Exception:
        return [
            f"{top_party} is currently leading with {top_seats} seats from latest reported data.",
            "A few constituencies remain tight; watch the next activity updates for lead changes.",
            f"Turnout signal is around {avg_turnout:.1f}%, indicating momentum in active districts.",
        ]

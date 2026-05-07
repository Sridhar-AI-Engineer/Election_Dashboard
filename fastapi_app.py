from datetime import datetime
import re
import json
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from analysis import generate_analysis_report
from src.config import GEMINI_API_KEY, GEMINI_MODEL
from src.services.bigquery_service import (
    fetch_constituencies as fetch_constituencies_bq,
    fetch_constituencies_df as fetch_constituencies_df_bq,
    fetch_party_table as fetch_party_table_bq,
    fetch_top_cards as fetch_top_cards_bq,
    fetch_total_ac as fetch_total_ac_bq,
)
from src.services.database import init_app_tables, write_app_event, write_summary_snapshot
from src.services.firestore_service import fetch_activity_logs, publish_activity
from src.services.party_results_store import (
    fetch_constituencies as fetch_constituencies_local,
    fetch_constituencies_df as fetch_constituencies_df_local,
    fetch_party_table as fetch_party_table_local,
    fetch_top_cards as fetch_top_cards_local,
    fetch_total_ac as fetch_total_ac_local,
    init_constituencies,
    init_party_results,
)


app = FastAPI(title="TN Election 2026 - FastAPI")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

_BG_EXECUTOR = ThreadPoolExecutor(max_workers=4)
_GEMINI_CACHE_LOCK = Lock()
_GEMINI_CACHE: dict[str, list[str]] = {"key": "", "value": []}


@app.on_event("startup")
def startup_event():
    init_party_results()
    init_constituencies()
    try:
        init_app_tables()
        publish_activity("Startup complete with Cloud SQL table initialization.", "startup")
    except Exception:
        pass


def _safe_publish_activity(message: str, event: str | None = None) -> None:
    def _task():
        try:
            publish_activity(message, event)
        except Exception:
            pass

    _BG_EXECUTOR.submit(_task)


def _safe_write_event(event_type: str, payload: dict | str) -> None:
    def _task():
        try:
            text = payload if isinstance(payload, str) else json.dumps(payload, default=str)
            write_app_event(event_type=event_type, payload=text)
        except Exception:
            pass

    _BG_EXECUTOR.submit(_task)


def _get_cached_or_fallback_gemini_summary(party_table: list[dict], total_ac: int) -> list[str]:
    cache_key = f"{total_ac}|" + "|".join([f"{r.get('party')}:{r.get('won')}" for r in party_table])
    with _GEMINI_CACHE_LOCK:
        if _GEMINI_CACHE.get("key") == cache_key and _GEMINI_CACHE.get("value"):
            return list(_GEMINI_CACHE["value"])

    fallback = _fallback_gemini_summary(party_table, total_ac)

    def _refresh_cache():
        fresh = _generate_gemini_summary(party_table, total_ac)
        with _GEMINI_CACHE_LOCK:
            _GEMINI_CACHE["key"] = cache_key
            _GEMINI_CACHE["value"] = list(fresh)

    _BG_EXECUTOR.submit(_refresh_cache)
    return fallback


def _fetch_party_table() -> list[dict]:
    try:
        rows = fetch_party_table_bq()
        if rows:
            return rows
    except Exception:
        pass
    return fetch_party_table_local()


def _fetch_top_cards() -> list[dict]:
    try:
        rows = fetch_top_cards_bq()
        if rows:
            return rows
    except Exception:
        pass
    return fetch_top_cards_local()


def _fetch_total_ac() -> int:
    try:
        total = fetch_total_ac_bq()
        if total > 0:
            return total
    except Exception:
        pass
    return fetch_total_ac_local()


def _fetch_constituencies(limit: int = 5000) -> list[dict]:
    try:
        rows = fetch_constituencies_bq(limit=limit)
        if rows:
            return rows
    except Exception:
        pass
    return fetch_constituencies_local(limit)


def _fetch_activity_logs(limit: int = 10) -> list[dict]:
    try:
        return fetch_activity_logs(limit=limit)
    except Exception:
        return []


def _load_df():
    try:
        frame = fetch_constituencies_df_bq()
        if not frame.empty:
            return frame
    except Exception:
        pass
    return fetch_constituencies_df_local()


def _fallback_gemini_summary(party_table: list[dict], total_ac: int) -> list[str]:
    if not party_table:
        return ["Election summary is not available right now."]

    top_party = party_table[0]
    second_party = party_table[1] if len(party_table) > 1 else None
    margin_text = (
        f"{top_party['party']} leads {second_party['party']} by {top_party['won'] - second_party['won']} seats."
        if second_party
        else f"{top_party['party']} is currently leading."
    )
    return [
        f"{top_party['party_name']} is leading with {top_party['won']} seats out of {total_ac}.",
        margin_text,
        f"Majority mark is 118 and current leading bloc status can be tracked in the party table.",
    ]


def _generate_gemini_summary(party_table: list[dict], total_ac: int) -> list[str]:
    fallback = _fallback_gemini_summary(party_table, total_ac)
    if not GEMINI_API_KEY:
        return fallback

    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL or "gemini-1.5-flash")

        compact_rows = [
            {"party": row.get("party"), "name": row.get("party_name"), "won": row.get("won", 0)}
            for row in party_table
        ]
        prompt = (
            "You are an election analyst. Provide exactly 3 short bullet points for Tamil Nadu election trend summary. "
            "Keep each point within 20 words. Focus on leader, competition, and coalition/majority signal. "
            f"Total seats: {total_ac}. Party seats: {compact_rows}"
        )
        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        if not text:
            return fallback

        lines = [
            re.sub(r"^[-•\s]+", "", line).strip()
            for line in text.splitlines()
            if line.strip()
        ]
        lines = [line for line in lines if line]
        if not lines:
            return fallback
        return lines[:3]
    except Exception:
        return fallback


class ChatRequest(BaseModel):
    message: str


def _generate_gemini_chat_reply(user_message: str, party_table: list[dict], total_ac: int) -> str:
    clean_message = (user_message or "").strip()
    if not clean_message:
        return "Please ask a question about the current Tamil Nadu election trends."

    fallback_lines = _fallback_gemini_summary(party_table, total_ac)
    fallback_reply = " ".join(fallback_lines)
    if not GEMINI_API_KEY:
        return fallback_reply

    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL or "gemini-1.5-flash")

        compact_rows = [
            {
                "party": row.get("party"),
                "name": row.get("party_name"),
                "won": row.get("won", 0),
                "leading": row.get("leading", 0),
                "total": row.get("total", 0),
            }
            for row in party_table
        ]
        prompt = (
            "You are a Tamil Nadu election dashboard copilot. "
            "Answer only from the provided election data context. "
            "If the user asks unrelated questions, politely steer back to election insights. "
            "Keep reply concise (max 6 lines), factual, and easy to read.\n\n"
            f"Total Assembly seats: {total_ac}\n"
            f"Party table: {compact_rows}\n"
            f"User question: {clean_message}"
        )
        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        return text or fallback_reply
    except Exception:
        return fallback_reply


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "last_updated": datetime.now().strftime("%I:%M %p On %d/%m/%Y"),
        },
    )


@app.get("/api/summary")
def summary():
    party_table = _fetch_party_table()
    top_cards = _fetch_top_cards()
    total_ac = _fetch_total_ac()

    leading_party = party_table[0]["party"] if party_table else None
    leading_seats = party_table[0].get("won", 0) if party_table else 0

    response = {
        "total_ac": total_ac,
        "majority": 118,
        "top_cards": top_cards,
        "party_table": party_table,
        "updated": datetime.now().isoformat(),
    }
    try:
        write_summary_snapshot(total_ac=total_ac, leading_party=leading_party, leading_seats=leading_seats)
    except Exception:
        pass
    _safe_publish_activity(
        f"Summary refreshed. Leader: {leading_party or 'N/A'} ({leading_seats} seats)",
        "summary_refresh",
    )
    _safe_write_event("summary_refresh", response)
    return response


@app.get("/api/constituencies")
def constituencies(limit: int = 5000):
    rows = _fetch_constituencies(limit)
    _safe_write_event("constituencies_fetch", {"count": len(rows), "limit": limit})
    return rows


@app.get("/api/analytics")
def analytics():
    df = _load_df()
    report = generate_analysis_report(df)
    party_table = _fetch_party_table()
    total_ac = _fetch_total_ac()

    close_fights = report.get("close_fights", [])
    if not close_fights:
        close_fights = (
            df.sort_values("vote_share", ascending=True)
            .head(10)[["constituency_name", "leading_party", "vote_share"]]
            .to_dict(orient="records")
        )

    response = {
        "high_turnout": report.get("high_turnout", []),
        "close_fights": close_fights,
        "top_candidates": report.get("top_candidates", []),
        "top_parties_by_votes": report.get("top_parties", []),
        "gemini_summary": _get_cached_or_fallback_gemini_summary(party_table, total_ac),
        "ml": report.get("ml", {"status": "skipped"}),
        "data_quality": {
            "shape": report.get("shape", {}),
            "duplicates": report.get("duplicates", 0),
        },
        "activity_logs": _fetch_activity_logs(limit=10),
    }
    _safe_publish_activity(
        f"Analytics refreshed with {response['data_quality']['shape'].get('rows', 0)} rows.",
        "analytics_refresh",
    )
    _safe_write_event("analytics_refresh", {"rows": response["data_quality"]["shape"].get("rows", 0)})
    return response


@app.post("/api/chat")
def chat(payload: ChatRequest):
    party_table = _fetch_party_table()
    total_ac = _fetch_total_ac()
    reply = _generate_gemini_chat_reply(payload.message, party_table, total_ac)
    response = {
        "reply": reply,
        "updated": datetime.now().isoformat(),
    }
    _safe_publish_activity(f"Chat request processed: {payload.message[:80]}", "chat_request")
    _safe_write_event(
        "chat_request",
        {"question": payload.message, "answer_preview": reply[:300]},
    )
    return response

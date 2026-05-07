import json
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from src.services.kaggle_service import load_kaggle_results


st.set_page_config(
    page_title="TN 2026 Election Intelligence Platform",
    page_icon="🗳️",
    layout="wide",
)

st.markdown(
    """
<style>
    .stApp {
        background: radial-gradient(circle at 20% 20%, #1f2a44 0%, #0b1020 38%, #070b18 100%);
        color: #f4f6fb;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(23,37,73,0.92), rgba(13,20,40,0.92));
        border-right: 1px solid rgba(255,255,255,0.12);
    }
    .hero-wrap {
        position: sticky;
        top: 0;
        z-index: 20;
        background: linear-gradient(130deg, rgba(36,70,138,0.92), rgba(72,120,192,0.85));
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 0 0 22px 22px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
        backdrop-filter: blur(10px);
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
    .hero-title {
        margin: 0;
        text-align: center;
        color: #fff;
        letter-spacing: 0.3px;
        text-shadow: 0 2px 20px rgba(0,0,0,0.35);
    }
    .hero-subtitle {
        text-align: center;
        color: #d7deef;
        margin: 0.45rem 0 0;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.9rem;
        margin: 0.8rem 0 1.1rem;
    }
    .kpi-card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        backdrop-filter: blur(14px);
        box-shadow: 0 10px 24px rgba(0,0,0,0.22);
        transition: transform .25s ease, box-shadow .25s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(0,0,0,0.35);
    }
    .kpi-label { color: #c8d4f7; font-size: 0.78rem; letter-spacing: 0.45px; text-transform: uppercase; }
    .kpi-value { color: #fff; font-size: 1.5rem; font-weight: 700; margin-top: 0.2rem; }
    .ticker {
        overflow: hidden;
        white-space: nowrap;
        border: 1px solid rgba(255,255,255,0.14);
        background: rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 0.45rem 0;
        margin: 0.45rem 0 1rem;
        backdrop-filter: blur(8px);
    }
    .ticker-track {
        display: inline-block;
        padding-left: 100%;
        animation: tickerMove 30s linear infinite;
        color: #ecf2ff;
        font-size: 0.95rem;
    }
    .panel-title {
        color: #f2f6ff;
        letter-spacing: 0.25px;
        text-shadow: 0 2px 14px rgba(0,0,0,0.35);
    }
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 16px;
        overflow: hidden;
    }
    @keyframes tickerMove {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    @keyframes blink { 0%,50% { opacity:1; } 51%,100% { opacity:0.3; } }
    @media (max-width: 1000px) {
        .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
</style>
""",
    unsafe_allow_html=True,
)


def _render_ambient_effects() -> None:
    components.html(
        """
        <canvas id="bgfx" style="position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.25"></canvas>
        <script>
          const c = document.getElementById('bgfx');
          const x = c.getContext('2d');
          const dots = Array.from({length:45},()=>({
            x: Math.random()*window.innerWidth,
            y: Math.random()*window.innerHeight,
            r: Math.random()*2+0.5,
            vx:(Math.random()-.5)*0.2,
            vy:(Math.random()-.5)*0.2
          }));
          const resize=()=>{c.width=window.innerWidth;c.height=window.innerHeight};
          resize(); window.addEventListener('resize', resize);
          function draw(){
            x.clearRect(0,0,c.width,c.height);
            for(const p of dots){
              p.x+=p.vx; p.y+=p.vy;
              if(p.x<0||p.x>c.width) p.vx*=-1;
              if(p.y<0||p.y>c.height) p.vy*=-1;
              x.beginPath(); x.arc(p.x,p.y,p.r,0,Math.PI*2);
              x.fillStyle='rgba(160,205,255,.55)'; x.fill();
            }
            requestAnimationFrame(draw);
          }
          draw();
        </script>
        """,
        height=0,
    )


def _render_ticker(summary_df: pd.DataFrame, logs: list[dict]) -> None:
    seat_bits = []
    for _, row in summary_df.head(4).iterrows():
        seat_bits.append(f"{row['leading_party']}: {int(row['seats'])} seats")
    log_bits = [item.get("message", "") for item in logs[:4]]
    combined = "  •  ".join([*seat_bits, *log_bits])
    if not combined:
        combined = "Election analysis summary initializing..."
    st.markdown(
        f"""
        <div class="ticker">
            <div class="ticker-track">📊 ANALYSIS TAPE • {combined} • 📊 ANALYSIS TAPE • {combined}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpis(seats_loaded: int, lead_party: str, lead_seats: int, turnout: float) -> None:
    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card"><div class="kpi-label">Total Seats Tracked</div><div class="kpi-value">{seats_loaded}</div></div>
            <div class="kpi-card"><div class="kpi-label">Current Leader</div><div class="kpi-value">{lead_party}</div></div>
            <div class="kpi-card"><div class="kpi-label">Top Party Seats</div><div class="kpi-value">{lead_seats}</div></div>
            <div class="kpi-card"><div class="kpi-label">Avg Turnout</div><div class="kpi-value">{turnout:.1f}%</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _load_results() -> pd.DataFrame:
    try:
        df = load_kaggle_results(file_path="")
        if df.empty:
            raise ValueError("Kaggle dataset returned no rows.")
        if "turnout_pct" not in df.columns:
            df["turnout_pct"] = df["vote_share"]
        return df
    except Exception as exc:
        raise RuntimeError(f"Kaggle dataset load failed: {exc}") from exc


def _party_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("leading_party", as_index=False)
        .agg(
            seats=("constituency_name", "count"),
            avg_vote_share=("vote_share", "mean"),
        )
        .sort_values("seats", ascending=False)
    )


def _seat_leader(summary: pd.DataFrame) -> tuple[str, int]:
    if summary.empty:
        return "N/A", 0
    top = summary.iloc[0]
    return str(top["leading_party"]), int(top["seats"])


def _render_map(df: pd.DataFrame) -> None:
    map_df = df[["constituency_name", "leading_party", "vote_share", "lat", "lon"]].copy()
    map_df["lat"] = pd.to_numeric(map_df["lat"], errors="coerce")
    map_df["lon"] = pd.to_numeric(map_df["lon"], errors="coerce")
    map_df = map_df.dropna(subset=["lat", "lon"])
    if map_df.empty:
        st.warning("Map data is unavailable in the Kaggle dataset.")
        return

    center_lat = float(map_df["lat"].mean())
    center_lon = float(map_df["lon"].mean())
    points_json = json.dumps(map_df.to_dict(orient="records"))

    html = f"""
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
    <style>
        #eci-map {{ height: 520px; border-radius: 16px; border: 1px solid rgba(255,255,255,.2); box-shadow: 0 12px 28px rgba(0,0,0,.28); }}
        .leaflet-popup-content-wrapper {{ border-radius: 12px; }}
        .map-note {{ color: #dbe6ff; margin: 6px 0 10px; font-size: 13px; }}
    </style>
    <div class="map-note"><b>Constituency Wise Results</b> • Kaggle Dynamic Dataset</div>
    <div id="eci-map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    <script>
        const points = {points_json};
        const map = L.map('eci-map', {{ zoomControl:true }}).setView([{center_lat}, {center_lon}], 7);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap contributors'
        }}).addTo(map);

        const partyColors = {{
            'DMK': '#d64b4b', 'ADMK': '#3fb950', 'AIADMK': '#3fb950', 'BJP': '#f0a83c',
            'INC': '#4aa3ff', 'PMK': '#9b7df5', 'TVK': '#e35fca'
        }};

        points.forEach((p) => {{
            const color = partyColors[p.leading_party] || '#8fa6ff';
            const radius = Math.max(5, Math.min(18, Number(p.vote_share || 0) / 3));
            const marker = L.circleMarker([Number(p.lat), Number(p.lon)], {{
                radius, color, fillColor: color, fillOpacity: 0.62, weight: 1
            }}).addTo(map);
            marker.bindPopup(`<b>${{p.constituency_name}}</b><br/>Party: ${{p.leading_party}}<br/>Vote share: ${{Number(p.vote_share || 0).toFixed(1)}}%`);
        }});
    </script>
    """
    components.html(html, height=560)


def _analysis_cards(results_df: pd.DataFrame, summary_df: pd.DataFrame) -> None:
    top5 = summary_df.head(5).copy()
    top5["share"] = (top5["seats"] / max(int(results_df["constituency_name"].nunique()), 1) * 100).round(1)

    high_turnout = results_df.sort_values("turnout_pct", ascending=False).head(5)[
        ["constituency_name", "leading_party", "turnout_pct"]
    ]
    close_fights = results_df.sort_values("vote_share", ascending=False).tail(5)[
        ["constituency_name", "leading_party", "vote_share"]
    ]

    a, b, c = st.columns(3)
    with a:
        st.markdown("### <span class='panel-title'>Top Parties (Seat Share)</span>", unsafe_allow_html=True)
        st.dataframe(top5[["leading_party", "seats", "share"]], use_container_width=True, hide_index=True)
    with b:
        st.markdown("### <span class='panel-title'>Highest Turnout Constituencies</span>", unsafe_allow_html=True)
        st.dataframe(high_turnout, use_container_width=True, hide_index=True)
    with c:
        st.markdown("### <span class='panel-title'>Lower Vote Share Seats</span>", unsafe_allow_html=True)
        st.dataframe(close_fights, use_container_width=True, hide_index=True)


def main() -> None:
    _render_ambient_effects()
    try:
        results_df = _load_results()
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    seats_loaded = int(results_df["constituency_name"].nunique())

    header_html = f"""
    <div class="hero-wrap">
        <h1 class="hero-title">🇮🇳 TN Election 2026 Kaggle Analysis Dashboard</h1>
        <p class="hero-subtitle">{seats_loaded}/234 seats | Majority Mark: 118 | Updated: {pd.Timestamp.now().strftime('%H:%M:%S IST')}</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.14);padding:0.65rem 0.9rem;border-radius:12px;color:#dce8ff;font-size:0.9rem;">
            <b>Disclaimer:</b> Data shown is based on live system updates and intended for trend analysis. Final certified data is published in official forms.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Dynamic Source: Kaggle dataset `nuhmanpk/tamil-nadu-assembly-election-results-2026`")

    summary_df = _party_summary(results_df)
    lead_party, lead_seats = _seat_leader(summary_df)
    _render_ticker(summary_df, [])

    _render_kpis(
        seats_loaded=int(results_df["constituency_name"].nunique()),
        lead_party=lead_party,
        lead_seats=lead_seats,
        turnout=float(results_df.get("turnout_pct", results_df["vote_share"]).mean()),
    )

    st.progress(min(lead_seats / 118, 1.0), text=f"Majority race: {lead_party} at {lead_seats}/118")
    _analysis_cards(results_df, summary_df)

    left, right = st.columns([2, 1])

    with left:
        st.markdown("### <span class='panel-title'>Constituency Lead Heatmap</span>", unsafe_allow_html=True)
        _render_map(results_df)

        st.markdown("### <span class='panel-title'>Top Constituencies by Vote Share</span>", unsafe_allow_html=True)
        st.dataframe(
            results_df.sort_values("vote_share", ascending=False).head(20),
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.markdown("### <span class='panel-title'>Seat Distribution</span>", unsafe_allow_html=True)
        if not summary_df.empty:
            chart = px.pie(summary_df, values="seats", names="leading_party", hole=0.4)
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("No party summary available.")

        st.markdown("### <span class='panel-title'>Party-wise Seat Count</span>", unsafe_allow_html=True)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.caption(f"Last updated: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()

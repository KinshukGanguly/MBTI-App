"""
app.py — MBTI Personality Predictor
────────────────────────────────────
Run with:
    streamlit run app.py
"""

import os
import streamlit as st
import plotly.graph_objects as go
from dotenv import load_dotenv

from utils import (
    load_all_models,
    validate_input,
    predict_mbti,
    get_mbti_type,
    count_tokens,
    TRAIT_META,
    MIN_TOKENS,
)

load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "MBTI Personality Predictor")
APP_ICON  = os.getenv("APP_ICON",  "🧠")

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #ede9fe 0%, #fce7f3 50%, #e0f2fe 100%);
        min-height: 100vh;
    }
    .main .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 720px;
    }
    .app-header { text-align: center; margin-bottom: 0.3rem; }
    .app-title {
        font-size: 2rem;
        font-weight: 700;
        color: #4c1d95;
        letter-spacing: -0.5px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .app-title span {
        background: linear-gradient(90deg, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .app-subtitle {
        text-align: center;
        font-size: 0.85rem;
        color: #9333ea;
        letter-spacing: 0.5px;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 2rem;
        opacity: 0.75;
    }
    .card {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(139,92,246,0.15);
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 24px rgba(124,58,237,0.06);
    }
    .card-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #7c3aed;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .stTextArea textarea {
        background: rgba(255,255,255,0.95) !important;
        color: #1e1b4b !important;
        border: 1.5px solid rgba(139,92,246,0.25) !important;
        border-radius: 14px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        padding: 14px 16px !important;
        caret-color: #7c3aed !important;
        box-shadow: 0 2px 12px rgba(124,58,237,0.04) !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextArea textarea::placeholder { color: #c4b5fd !important; }
    .stTextArea textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
        outline: none !important;
    }
    .token-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        padding: 3px 10px;
        border-radius: 20px;
        margin-top: 6px;
        font-weight: 500;
    }
    .token-pill.ok   { background: #dcfce7; color: #15803d; }
    .token-pill.warn { background: #fef3c7; color: #92400e; }
    .token-pill.empty { background: #f3f4f6; color: #9ca3af; }
    .token-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 6px;
    }
    .token-hint { font-size: 0.72rem; color: #e11d48; font-family: 'JetBrains Mono', monospace; }
    div.stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.65rem 2rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        width: 100% !important;
        box-shadow: 0 4px 16px rgba(124,58,237,0.3) !important;
        transition: opacity 0.18s, transform 0.12s !important;
    }
    div.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
    .result-row {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 0 0.2rem;
    }
    .mbti-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: 6px;
        background: linear-gradient(135deg, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    .result-divider {
        height: 2px;
        background: linear-gradient(90deg, #ede9fe, #fce7f3, #ede9fe);
        border-radius: 2px;
        margin: 0.6rem 0 0.2rem;
    }
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.7) !important;
        border: 1px solid rgba(139,92,246,0.12) !important;
        border-radius: 14px !important;
        padding: 0.8rem 1rem !important;
    }
    [data-testid="metric-container"] label { color: #7c3aed !important; font-size: 0.78rem !important; font-weight: 600 !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #1e1b4b !important; font-family: 'JetBrains Mono', monospace !important; font-size: 1.3rem !important; }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] { color: #9333ea !important; font-size: 0.75rem !important; }
    .stAlert { border-radius: 12px !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading models…")
def get_artifacts():
    return load_all_models()


def build_trait_chart(scores: dict) -> go.Figure:
    axes_order = ["IE", "SN", "TF", "JP"]
    fig = go.Figure()

    for axis in axes_order:
        meta = TRAIT_META[axis]
        l_sym, l_name, l_emo = meta["left"]
        r_sym, r_name, r_emo = meta["right"]
        l_pct = scores[l_sym]
        r_pct = scores[r_sym]

        dominant_left = l_pct >= r_pct
        l_col = "#7c3aed" if dominant_left else "#c4b5fd"
        r_col = "#db2777" if not dominant_left else "#f9a8d4"

        y_label = f"{l_emo} {l_sym}  ·  {r_sym} {r_emo}"

        fig.add_trace(go.Bar(
            y=[y_label], x=[-l_pct], orientation="h",
            marker_color=l_col, marker_line_width=0,
            text=f"{l_sym} {l_pct:.1f}%",
            textposition="inside", insidetextanchor="end",
            textfont=dict(color="white", size=11, family="JetBrains Mono"),
            showlegend=False,
            hovertemplate=f"<b>{l_sym} — {l_name}</b><br>{l_pct:.1f}%<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            y=[y_label], x=[r_pct], orientation="h",
            marker_color=r_col, marker_line_width=0,
            text=f"{r_pct:.1f}% {r_sym}",
            textposition="inside", insidetextanchor="start",
            textfont=dict(color="white", size=11, family="JetBrains Mono"),
            showlegend=False,
            hovertemplate=f"<b>{r_sym} — {r_name}</b><br>{r_pct:.1f}%<extra></extra>",
        ))

    fig.update_layout(
        barmode="overlay",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="#4c1d95", size=12),
        height=260,
        margin=dict(l=8, r=8, t=8, b=8),
        xaxis=dict(
            range=[-105, 105],
            tickvals=[-100, -50, 0, 50, 100],
            ticktext=["100%", "50%", "0", "50%", "100%"],
            showgrid=True, gridcolor="rgba(139,92,246,0.1)", gridwidth=1,
            zeroline=True, zerolinecolor="rgba(139,92,246,0.3)", zerolinewidth=1.5,
            tickfont=dict(size=10, color="#9333ea"),
        ),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#4c1d95")),
        bargap=0.4,
    )
    return fig


def main():
    st.markdown(f"""
    <div class="app-header">
        <div class="app-title">{APP_ICON} <span>{APP_TITLE}</span></div>
    </div>
    <div class="app-subtitle">stacked ensemble based · not for clinical use · four dimensions</div>
    """, unsafe_allow_html=True)

    try:
        tfidf, models = get_artifacts()
    except (EnvironmentError, FileNotFoundError) as err:
        st.error(f"**Model loading failed.**\n\n{err}")
        st.stop()

    st.markdown('<div class="card"><div class="card-label">✍️ Your Text</div>', unsafe_allow_html=True)

    text_input = st.text_area(
        label="input",
        placeholder=f"Write freely — journal entry, opinions, how you think about things… (min {MIN_TOKENS} words)",
        height=160,
        label_visibility="collapsed",
    )

    n_tokens = count_tokens(text_input) if text_input else 0
    if n_tokens == 0:
        pill_cls, pill_icon, pill_txt = "empty", "○", f"0 / {MIN_TOKENS} words"
    elif n_tokens < MIN_TOKENS:
        pill_cls, pill_icon, pill_txt = "warn", "⚠", f"{n_tokens} / {MIN_TOKENS} words"
    else:
        pill_cls, pill_icon, pill_txt = "ok", "✓", f"{n_tokens} words · ready"

    need_txt = f"need {MIN_TOKENS - n_tokens} more" if 0 < n_tokens < MIN_TOKENS else ""

    st.markdown(f"""
    <div class="token-row">
        <span class="token-pill {pill_cls}">{pill_icon} {pill_txt}</span>
        <span class="token-hint">{need_txt}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    predict_clicked = st.button("⚡  Analyse Personality")

    if predict_clicked:
        is_valid, token_count, message = validate_input(text_input)

        if not is_valid:
            st.warning(message)
            st.stop()

        with st.spinner("Running inference…"):
            try:
                scores    = predict_mbti(text_input, tfidf, models)
                mbti_type = get_mbti_type(scores)
            except Exception as err:
                st.error(f"Prediction error: {err}")
                st.stop()

        st.markdown(f"""
        <div class="card">
            <div class="card-label">🎯 Your Personality Type</div>
            <div class="result-row">
                <div class="mbti-badge">{mbti_type}</div>
            </div>
            <div class="result-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-label">📊 Trait Breakdown</div>', unsafe_allow_html=True)
        st.plotly_chart(
            build_trait_chart(scores),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown('</div>', unsafe_allow_html=True)

        cols = st.columns(4)
        for col, axis in zip(cols, ["IE", "SN", "TF", "JP"]):
            meta = TRAIT_META[axis]
            l_sym, l_name, l_emo = meta["left"]
            r_sym, r_name, r_emo = meta["right"]
            l_pct = scores[l_sym]
            r_pct = scores[r_sym]
            winner_sym  = l_sym  if l_pct >= r_pct else r_sym
            winner_name = l_name if l_pct >= r_pct else r_name
            winner_emo  = l_emo  if l_pct >= r_pct else r_emo
            winner_pct  = max(l_pct, r_pct)
            with col:
                st.metric(
                    label=f"{winner_emo} {winner_sym}",
                    value=f"{winner_pct:.1f}%",
                    delta=winner_name,
                    delta_color="off",
                )

        st.caption(f"Analysed {token_count} tokens · stacked ensemble · TF-IDF")


if __name__ == "__main__":
    main()
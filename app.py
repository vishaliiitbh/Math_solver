import os
import sys
import json
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Math Mentor AI",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=Playfair+Display:wght@700;900&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #080b14;
    color: #f1f5f9;
}

.main .block-container {
    padding: 2rem 2.5rem 4rem;
    max-width: 1400px;
}

/* ── Animated Background Grid ── */
.main::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── Hero Header ── */
.hero-wrap {
    position: relative;
    padding: 2.5rem 0 1.5rem;
    margin-bottom: 0.5rem;
}

.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 24px;
    height: 1px;
    background: #6366f1;
}

.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 3.4rem;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: #f8fafc;
    margin: 0 0 0.4rem;
    position: relative;
}

.hero-title .accent {
    background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #fb7185 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    color: #94a3b8;
    font-size: 0.95rem;
    font-weight: 300;
    letter-spacing: 0.01em;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    flex-wrap: wrap;
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 99px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    color: #818cf8;
    font-family: 'Space Mono', monospace;
}

.hero-divider {
    height: 1px;
    background: linear-gradient(90deg, #6366f1 0%, rgba(99,102,241,0.3) 40%, transparent 70%);
    margin: 1.5rem 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0c0f1a !important;
    border-right: 1px solid #1e2235;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 0.15rem;
}

.sidebar-tagline {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #64748b;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.sidebar-section {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #64748b;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 1.2rem 0 0.5rem;
}

.history-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.4rem 0.5rem;
    border-radius: 6px;
    transition: background 0.15s;
    cursor: default;
}

.history-item:hover { background: #1a1f35; }

.history-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    margin-top: 0.3rem;
    flex-shrink: 0;
    background: #374151;
}

.history-dot.correct { background: #22c55e; }
.history-dot.incorrect { background: #ef4444; }

.history-text {
    font-size: 0.75rem;
    color: #94a3b8;
    line-height: 1.4;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
}

/* ── Input Section ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #64748b;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e2235;
}

/* Input mode radio */
div[data-testid="stRadio"] {
    background: #0e1220;
    border: 1px solid #1e2235;
    border-radius: 10px;
    padding: 0.3rem;
    display: inline-flex;
    margin-bottom: 1rem;
}

div[data-testid="stRadio"] > div {
    display: flex;
    gap: 0.2rem;
}

div[data-testid="stRadio"] label {
    color: #6b7280 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.35rem 0.9rem !important;
    border-radius: 7px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
}

/* Textarea */
.stTextArea textarea {
    background: #0e1220 !important;
    border: 1px solid #1e2235 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    line-height: 1.65 !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
    resize: none !important;
}

.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

.stTextArea textarea::placeholder { color: #374151 !important; }

/* Text input */
.stTextInput input {
    background: #0e1220 !important;
    border: 1px solid #1e2235 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-size: 0.85rem !important;
}

.stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #0e1220 !important;
    border: 1px dashed #1e2235 !important;
    border-radius: 10px !important;
}

/* ── Solve Button ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 60%, #9333ea 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1.8rem !important;
    height: auto !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.3) !important;
    transition: all 0.2s ease !important;
    position: relative;
    overflow: hidden;
}

.stButton > button::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
    opacity: 0;
    transition: opacity 0.2s;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.45) !important;
}

.stButton > button:hover::after { opacity: 1; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Agent Pipeline Trace ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.6rem;
    margin: 1rem 0;
}

.trace-node {
    background: #0c0f1a;
    border: 1px solid #1a1f35;
    border-radius: 10px;
    padding: 0.65rem 0.9rem;
    font-size: 0.78rem;
    color: #4b5563;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
    font-family: 'Space Mono', monospace;
}

.trace-node .node-icon { font-size: 0.85rem; }

.trace-node.pending {
    border-color: #1a1f35;
    color: #374151;
}

.trace-node.running {
    border-color: #f59e0b;
    color: #fde68a;
    background: rgba(245,158,11,0.05);
    box-shadow: 0 0 12px rgba(245,158,11,0.1);
}

.trace-node.done {
    border-color: rgba(34,197,94,0.3);
    color: #86efac;
    background: rgba(34,197,94,0.04);
}

/* ── Answer Hero ── */
.answer-hero {
    background: #0c0f1a;
    border: 1px solid #1e2235;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}

.answer-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
    pointer-events: none;
}

.answer-hero-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.2rem;
}

.answer-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #64748b;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.answer-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    line-height: 1.1;
}

.answer-value .answer-highlight {
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Confidence bar ── */
.conf-wrap {
    margin-top: 0.8rem;
}

.conf-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.35rem;
}

.conf-label-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #64748b;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.conf-pct {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
}

.conf-track {
    background: #1a1f35;
    border-radius: 99px;
    height: 5px;
    overflow: hidden;
}

.conf-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* ── Verification Badge ── */
.verdict-wrap {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.9rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 1.2rem;
    font-family: 'Space Mono', monospace;
}

.verdict-correct {
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.25);
    color: #86efac;
}

.verdict-incorrect {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
    color: #fca5a5;
}

/* ── Steps ── */
.steps-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #64748b;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
    margin-top: 1.2rem;
}

.step-card {
    display: flex;
    gap: 0.9rem;
    align-items: flex-start;
    margin-bottom: 0.5rem;
    padding: 0.8rem 1rem;
    background: #0c0f1a;
    border: 1px solid #1a1f35;
    border-radius: 10px;
    transition: border-color 0.2s;
}

.step-card:hover { border-color: rgba(99,102,241,0.3); }

.step-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #6366f1;
    font-weight: 700;
    min-width: 20px;
    padding-top: 0.05rem;
}

.step-text {
    font-size: 0.88rem;
    color: #e2e8f0;
    line-height: 1.55;
}

/* ── Formula card ── */
.formula-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.06), rgba(124,58,237,0.06));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
    display: flex;
    gap: 0.8rem;
    align-items: flex-start;
}

.formula-icon {
    font-size: 1rem;
    flex-shrink: 0;
    margin-top: 0.05rem;
}

.formula-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #6366f1;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

.formula-text {
    font-size: 0.9rem;
    color: #c7d2fe;
    font-style: italic;
}

/* ── Info Panel Cards ── */
.info-card {
    background: #0c0f1a;
    border: 1px solid #1a1f35;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
}

.info-card-head {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #64748b;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1a1f35;
}

.info-row {
    display: flex;
    gap: 0.4rem;
    align-items: baseline;
    margin-bottom: 0.35rem;
    font-size: 0.82rem;
}

.info-key {
    color: #64748b;
    font-size: 0.75rem;
    min-width: 70px;
    font-family: 'Space Mono', monospace;
}

.info-val { color: #f1f5f9; }

/* ── Source chips ── */
.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 5px;
    padding: 0.15rem 0.5rem;
    font-size: 0.68rem;
    color: #818cf8;
    font-family: 'Space Mono', monospace;
}

.rag-card {
    background: #0c0f1a;
    border: 1px solid #1a1f35;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.2s;
}

.rag-card:hover { border-color: rgba(99,102,241,0.25); }

.rag-score-bar {
    height: 2px;
    border-radius: 99px;
    margin-top: 0.5rem;
}

.rag-text {
    font-size: 0.78rem;
    color: #94a3b8;
    line-height: 1.5;
    margin-top: 0.4rem;
}

/* ── Insight / Tip / Pitfall ── */
.insight-block {
    background: rgba(34,197,94,0.04);
    border: 1px solid rgba(34,197,94,0.18);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}

.insight-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #22c55e;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

.insight-text { font-size: 0.87rem; color: #bbf7d0; line-height: 1.55; }

.tip-block {
    background: rgba(99,102,241,0.04);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}

.tip-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #818cf8;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

.tip-text { font-size: 0.85rem; color: #c7d2fe; line-height: 1.55; font-style: italic; }

.pitfall-block {
    background: rgba(239,68,68,0.03);
    border: 1px solid rgba(239,68,68,0.15);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}

.pitfall-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #ef4444;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.pitfall-item {
    font-size: 0.83rem;
    color: #fecaca;
    padding: 0.2rem 0;
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    line-height: 1.45;
}

.pitfall-item::before {
    content: '→';
    color: #ef4444;
    font-size: 0.75rem;
    margin-top: 0.05rem;
    flex-shrink: 0;
}

/* ── Badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace;
}

.badge-topic {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    color: #818cf8;
}

.badge-easy { background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.25); color: #86efac; }
.badge-medium { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.25); color: #fde68a; }
.badge-hard { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.25); color: #fca5a5; }

/* ── HITL Banner ── */
.hitl-banner {
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.2rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.hitl-icon { font-size: 1.3rem; flex-shrink: 0; }

.hitl-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #f59e0b;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

.hitl-reason { font-size: 0.85rem; color: #fde68a; line-height: 1.5; }

/* ── Feedback ── */
.feedback-wrap {
    background: #0c0f1a;
    border: 1px solid #1a1f35;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 0.5rem;
}

.feedback-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #64748b;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Empty State ── */
.empty-state {
    text-align: center;
    padding: 5rem 2rem;
}

.empty-glyph {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    opacity: 0.4;
}

.empty-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #64748b;
    margin-bottom: 0.5rem;
}

.empty-sub { font-size: 0.88rem; color: #374151; }

.empty-tags {
    margin-top: 1.2rem;
    display: flex;
    gap: 0.4rem;
    justify-content: center;
    flex-wrap: wrap;
}

.empty-tag {
    background: #0e1220;
    border: 1px solid #1a1f35;
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    color: #374151;
    font-family: 'Space Mono', monospace;
}

/* ── Section divider ── */
.section-divider {
    height: 1px;
    background: #1a1f35;
    margin: 1.8rem 0;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #0c0f1a !important;
    border: 1px solid #1a1f35 !important;
    border-radius: 8px !important;
    color: #64748b !important;
    font-size: 0.82rem !important;
}

/* ── OCR / transcript card ── */
.extracted-card {
    background: #0c0f1a;
    border: 1px solid #1a1f35;
    border-radius: 10px;
    padding: 1rem 1.2rem;
}

.extracted-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #4b5563;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0c0f1a; }
::-webkit-scrollbar-thumb { background: #1e2235; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #374151; }

/* ── Fix Streamlit white backgrounds ── */
div[data-testid="stDecoration"] { display: none; }
.stMarkdown { color: inherit; }
div[data-testid="stAppViewContainer"] { background: #080b14; }

/* Spinner */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* Alerts */
.stAlert { background: #0c0f1a !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def confidence_html(value: float, label: str = "Confidence") -> str:
    pct = int(value * 100)
    if pct >= 75:
        color = "#22c55e"
    elif pct >= 50:
        color = "#f59e0b"
    else:
        color = "#ef4444"
    return f"""
    <div class='conf-wrap'>
      <div class='conf-label'>
        <span class='conf-label-text'>{label}</span>
        <span class='conf-pct' style='color:{color}'>{pct}%</span>
      </div>
      <div class='conf-track'>
        <div class='conf-fill' style='width:{pct}%;background:{color}'></div>
      </div>
    </div>"""


def topic_badge(topic: str) -> str:
    return f"<span class='badge badge-topic'>{topic.replace('_', ' ')}</span>"


def diff_badge(diff: str) -> str:
    cls = f"badge-{diff.lower()}"
    return f"<span class='badge {cls}'>{diff}</span>"


# ── Init knowledge base ────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def init_kb():
    try:
        from rag.embedder import ingest_knowledge_base
        return ingest_knowledge_base()
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── Session state ──────────────────────────────────────────────────────────────
for k, v in [("result", None), ("hitl_override", None),
              ("feedback_given", False), ("memory_id", None)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sidebar-logo'>⟨ Math Mentor ⟩</div>
    <div class='sidebar-tagline'>JEE · AI · Multimodal</div>
    """, unsafe_allow_html=True)

    if st.button("📚 Ingest Knowledge Base", use_container_width=True):
        with st.spinner("Embedding docs into Pinecone..."):
            from rag.embedder import ingest_knowledge_base
            result = ingest_knowledge_base(force=True)
            if result.get("status") == "ingested":
                st.success(f"✅ {result['chunks']} chunks · {result['files']} files")
            else:
                st.info(f"ℹ️ {result.get('status', 'Done')}")

    st.divider()
    st.markdown("<div class='sidebar-section'>Recent Problems</div>", unsafe_allow_html=True)
    try:
        from memory.memory_store import get_recent_problems
        recent = get_recent_problems(5)
        if recent:
            for r in reversed(recent[-5:]):
                topic  = r.get("topic", "?")
                fb_val = r.get("user_feedback")
                dot_cls = "correct" if fb_val == "correct" else "incorrect" if fb_val == "incorrect" else ""
                text = r.get("problem_text", "")[:50]
                st.markdown(f"""
                <div class='history-item'>
                  <div class='history-dot {dot_cls}'></div>
                  <div class='history-text'>[{topic}] {text}…</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#374151;font-size:0.78rem;font-family:Space Mono,monospace'>// no history yet</span>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<span style='color:#374151;font-size:0.78rem;font-family:Space Mono,monospace'>// memory unavailable</span>", unsafe_allow_html=True)


# ── Hero Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-wrap'>
  <div class='hero-eyebrow'>Multimodal · RAG · Agents · HITL · Memory</div>
  <div class='hero-title'>Math Mentor <span class='accent'>AI</span></div>
  <div class='hero-sub'>
    <span class='hero-pill'>⚡ JEE-Style Solver</span>
    <span class='hero-pill'>🔍 Step-by-Step</span>
    <span class='hero-pill'>📚 Knowledge-Grounded</span>
  </div>
</div>
<div class='hero-divider'></div>
""", unsafe_allow_html=True)


# ── Input Section ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-label'>Input Problem</div>", unsafe_allow_html=True)

input_mode = st.radio("Input Mode", ["✍️ Text", "🖼️ Image", "🎙️ Audio"],
                      horizontal=True, label_visibility="collapsed")

raw_text = ""
ocr_confidence = 1.0
asr_confidence = 1.0
input_source = "text"
extracted_preview = None

col_input, col_preview = st.columns([3, 2], gap="large")

with col_input:
    if input_mode == "✍️ Text":
        input_source = "text"
        raw_text = st.text_area(
            "Problem",
            placeholder="e.g. Find the roots of 2x² − 5x + 3 = 0\nor: If P(A) = 0.4 and P(B) = 0.3 (independent), find P(A∪B)",
            height=150,
            label_visibility="collapsed",
        )

    elif input_mode == "🖼️ Image":
        input_source = "image"
        uploaded_img = st.file_uploader("Upload image", type=["jpg","jpeg","png"],
                                        label_visibility="collapsed")
        if uploaded_img:
            with st.spinner("Running OCR…"):
                try:
                    from tools.ocr_tool import extract_text_from_image
                    img_bytes = uploaded_img.read()
                    ocr_result = extract_text_from_image(img_bytes)
                    extracted_preview = ocr_result.get("text", "")
                    ocr_confidence    = ocr_result.get("confidence", 0.0)
                    st.image(img_bytes, caption="Uploaded", use_column_width=True)
                except Exception as e:
                    st.error(f"OCR error: {e}")

    elif input_mode == "🎙️ Audio":
        input_source = "audio"
        uploaded_audio = st.file_uploader("Upload audio", type=["wav","mp3","m4a"],
                                          label_visibility="collapsed")
        if uploaded_audio:
            with st.spinner("Transcribing…"):
                try:
                    from tools.audio_tool import process_audio
                    audio_bytes = uploaded_audio.read()
                    asr_result  = process_audio(audio_bytes, uploaded_audio.name)
                    extracted_preview = asr_result.get("text", "")
                    asr_confidence    = 0.85 if not asr_result.get("error") else 0.3
                    st.audio(audio_bytes)
                except Exception as e:
                    st.error(f"Transcription error: {e}")

with col_preview:
    if extracted_preview is not None:
        conf_val = ocr_confidence if input_source == "image" else asr_confidence
        conf_color = "#22c55e" if conf_val >= 0.75 else "#f59e0b"
        mode_label = "OCR Extraction" if input_source == "image" else "Transcript"
        warn_note  = "" if conf_val >= 0.75 else " · HITL will trigger"

        st.markdown(f"""
        <div class='extracted-card'>
          <div class='extracted-label'>{mode_label}</div>
          <div style='font-size:0.75rem;color:{conf_color};margin-bottom:0.6rem;font-family:Space Mono,monospace'>
            {conf_val:.0%} confidence{warn_note}
          </div>
        </div>
        """, unsafe_allow_html=True)
        raw_text = st.text_area("Review & edit extracted text", value=extracted_preview,
                                height=120, key="extracted_edit")


# ── Solve Button ───────────────────────────────────────────────────────────────
st.markdown("")
solve_col, _ = st.columns([1, 4])
with solve_col:
    solve_clicked = st.button("⟶  Solve Problem", use_container_width=True)

if solve_clicked:
    if not raw_text.strip():
        st.warning("Please enter a math problem first.")
    else:
        st.session_state.feedback_given = False
        st.session_state.hitl_override  = None
        st.session_state.memory_id      = None

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Agent Pipeline</div>", unsafe_allow_html=True)

        AGENT_LABELS = {
            "parser":    ("🔍", "Parser Agent",    "Structuring problem…"),
            "router":    ("🧭", "Router Agent",    "Classifying & routing…"),
            "retriever": ("📚", "RAG Retriever",   "Fetching formulas…"),
            "solver":    ("⚙️", "Solver Agent",    "Computing solution…"),
            "verifier":  ("✅", "Verifier Agent",  "Checking correctness…"),
            "explainer": ("💬", "Explainer Agent", "Generating explanation…"),
        }

        trace_placeholders = {}
        cols = st.columns(3)
        for i, (key, (icon, label, desc)) in enumerate(AGENT_LABELS.items()):
            with cols[i % 3]:
                trace_placeholders[key] = st.empty()
                trace_placeholders[key].markdown(
                    f"<div class='trace-node pending'>"
                    f"<span class='node-icon'>⏳</span>{label}</div>",
                    unsafe_allow_html=True)

        def on_step(name, _result):
            icon, label, _ = AGENT_LABELS.get(name, ("✅", name, ""))
            trace_placeholders[name].markdown(
                f"<div class='trace-node done'>"
                f"<span class='node-icon'>{icon}</span>{label}</div>",
                unsafe_allow_html=True)

        with st.spinner("Running pipeline…"):
            try:
                from pipeline import run_pipeline
                result = run_pipeline(
                    raw_text=raw_text,
                    input_source=input_source,
                    ocr_confidence=ocr_confidence,
                    asr_confidence=asr_confidence,
                    on_step=on_step,
                )
                st.session_state.result = result
            except Exception as e:
                st.error(f"Pipeline error: {e}")
                st.exception(e)


# ── Results ────────────────────────────────────────────────────────────────────
result = st.session_state.result
if result:
    parsed       = result["parsed_problem"]
    routing      = result["routing"]
    solution     = result["solution"]
    verification = result["verification"]
    explanation  = result["explanation"]
    retrieved    = result["retrieved_context"]

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ── HITL Banner ──
    if result.get("needs_hitl") and not st.session_state.hitl_override:
        st.markdown(f"""
        <div class='hitl-banner'>
          <div class='hitl-icon'>⚠️</div>
          <div>
            <div class='hitl-title'>Human Review Requested</div>
            <div class='hitl-reason'>{result.get('hitl_reason','')}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        h1, h2, h3 = st.columns(3)
        with h1:
            if st.button("✅ Approve"):
                st.session_state.hitl_override = "approved"; st.rerun()
        with h2:
            if st.button("✏️ Edit & Re-run"):
                st.session_state.hitl_override = "edit"
        with h3:
            if st.button("❌ Reject"):
                st.session_state.hitl_override = "rejected"; st.rerun()

        if st.session_state.hitl_override == "edit":
            corrected = st.text_area("Edit problem text:", value=parsed.get("problem_text",""), height=100)
            if st.button("Re-run with correction"):
                from pipeline import run_pipeline
                new_result = run_pipeline(corrected, input_source="text")
                st.session_state.result = new_result
                st.session_state.hitl_override = "approved"
                st.rerun()

    # ── Main Results ──
    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        topic      = parsed.get("topic", "")
        difficulty = explanation.get("difficulty_rating", "medium")
        answer_str = solution.get("answer", "—")
        is_correct = verification.get("is_correct", False)

        # Answer hero card
        verdict_cls  = "verdict-correct" if is_correct else "verdict-incorrect"
        verdict_icon = "✓" if is_correct else "✗"
        verdict_text = verification.get("verdict", "—")

        st.markdown(f"""
        <div class='answer-hero'>
          <div class='answer-hero-meta'>
            {topic_badge(topic)}
            {diff_badge(difficulty)}
          </div>
          <div class='answer-label'>Final Answer</div>
          <div class='answer-value'>
            <span class='answer-highlight'>{answer_str}</span>
          </div>
          {confidence_html(solution.get('confidence', 0))}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='verdict-wrap {verdict_cls}'>
          {verdict_icon} {verdict_text}
        </div>
        """, unsafe_allow_html=True)

        # Solution steps
        steps = solution.get("solution_steps", [])
        if steps:
            st.markdown("<div class='steps-header'>Solution Steps</div>", unsafe_allow_html=True)
            for i, step_text in enumerate(steps, 1):
                st.markdown(f"""
                <div class='step-card'>
                  <div class='step-num'>{i:02d}</div>
                  <div class='step-text'>{step_text}</div>
                </div>""", unsafe_allow_html=True)

        # Key formula
        if solution.get("key_formula_used"):
            st.markdown(f"""
            <div class='formula-card'>
              <div class='formula-icon'>∑</div>
              <div>
                <div class='formula-label'>Key Formula</div>
                <div class='formula-text'>{solution['key_formula_used']}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Detailed explanation
        if explanation.get("explanation"):
            with st.expander("💬 Detailed Explanation", expanded=True):
                st.markdown(
                    f"<div style='font-size:0.88rem;color:#e2e8f0;line-height:1.75'>"
                    f"{explanation['explanation']}</div>",
                    unsafe_allow_html=True)

        # Step-by-step walkthrough
        explainer_steps = explanation.get("step_by_step", [])
        if explainer_steps:
            with st.expander("🧩 Step-by-Step Walkthrough"):
                for s in explainer_steps:
                    st.markdown(f"""
                    <div class='step-card' style='flex-direction:column;gap:0.3rem'>
                      <div style='display:flex;align-items:center;gap:0.6rem'>
                        <span class='step-num'>{s.get('step','')}</span>
                        <span style='color:#a78bfa;font-size:0.85rem;font-weight:600'>{s.get('action','')}</span>
                      </div>
                      <div style='color:#94a3b8;font-size:0.78rem;padding-left:2rem'>{s.get('why','')}</div>
                      <div style='color:#86efac;font-size:0.82rem;font-family:Space Mono,monospace;padding-left:2rem'>{s.get('math','')}</div>
                    </div>""", unsafe_allow_html=True)

    with right_col:
        # Parsed problem card
        st.markdown(f"""
        <div class='info-card'>
          <div class='info-card-head'>Parsed Problem</div>
          <div style='font-size:0.88rem;color:#e2e8f0;margin-bottom:0.8rem;line-height:1.55'>
            {parsed.get('problem_text','')}
          </div>
          <div class='info-row'><span class='info-key'>Goal</span><span class='info-val'>{parsed.get('goal','—')}</span></div>
          <div class='info-row'><span class='info-key'>Variables</span><span class='info-val'>{', '.join(parsed.get('variables',[]) or ['—'])}</span></div>
          <div class='info-row'><span class='info-key'>Strategy</span><span class='info-val'>{routing.get('solution_strategy','—')}</span></div>
        </div>""", unsafe_allow_html=True)

        # Retrieved context
        if retrieved:
            st.markdown("<div class='info-card-head' style='margin-bottom:0.6rem'>Retrieved Context</div>", unsafe_allow_html=True)
            for chunk in retrieved:
                score     = chunk["score"]
                bar_color = "#22c55e" if score > 0.7 else "#f59e0b" if score > 0.5 else "#4b5563"
                st.markdown(f"""
                <div class='rag-card'>
                  <div style='display:flex;justify-content:space-between;align-items:center'>
                    <span class='source-chip'>📄 {chunk['source']}</span>
                    <span style='font-family:Space Mono,monospace;font-size:0.65rem;color:{bar_color}'>{score:.2f}</span>
                  </div>
                  <div class='rag-text'>{chunk['text'][:180]}…</div>
                  <div class='rag-score-bar' style='width:{int(score*100)}%;background:{bar_color};opacity:0.4'></div>
                </div>""", unsafe_allow_html=True)

        # Key insight
        if explanation.get("key_insight"):
            st.markdown(f"""
            <div class='insight-block'>
              <div class='insight-label'>💡 Key Insight</div>
              <div class='insight-text'>{explanation['key_insight']}</div>
            </div>""", unsafe_allow_html=True)

        # Memory tip
        if explanation.get("memory_tip"):
            st.markdown(f"""
            <div class='tip-block'>
              <div class='tip-label'>🧠 Memory Tip</div>
              <div class='tip-text'>{explanation['memory_tip']}</div>
            </div>""", unsafe_allow_html=True)

        # Common pitfalls
        pitfalls = explanation.get("common_pitfalls", [])
        if pitfalls:
            items_html = "".join(f"<div class='pitfall-item'>{p}</div>" for p in pitfalls)
            st.markdown(f"""
            <div class='pitfall-block'>
              <div class='pitfall-label'>⚠️ Common Pitfalls</div>
              {items_html}
            </div>""", unsafe_allow_html=True)

        # Verifier issues
        if verification.get("issues"):
            with st.expander("🔬 Verifier Issues"):
                for issue in verification["issues"]:
                    st.markdown(f"<div style='color:#fca5a5;font-size:0.83rem;padding:0.15rem 0'>→ {issue}</div>", unsafe_allow_html=True)
                if verification.get("corrections"):
                    st.markdown("<div style='color:#86efac;font-size:0.8rem;margin-top:0.5rem;font-weight:600'>Corrections</div>", unsafe_allow_html=True)
                    for c in verification["corrections"]:
                        st.markdown(f"<div style='color:#86efac;font-size:0.83rem;padding:0.15rem 0'>→ {c}</div>", unsafe_allow_html=True)

    # ── Feedback ──
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='feedback-wrap'>
      <div class='feedback-title'>Rate This Solution</div>
    """, unsafe_allow_html=True)

    if not st.session_state.feedback_given:
        fb1, fb2, fb3 = st.columns([1, 1, 3])
        with fb1:
            if st.button("✓  Correct", use_container_width=True):
                from pipeline import save_result_to_memory
                mid = save_result_to_memory(result, "correct")
                st.session_state.feedback_given = True
                st.session_state.memory_id = mid
                st.rerun()
        with fb2:
            if st.button("✗  Incorrect", use_container_width=True):
                from pipeline import save_result_to_memory
                mid = save_result_to_memory(result, "incorrect")
                st.session_state.feedback_given = True
                st.session_state.memory_id = mid
                st.rerun()
        with fb3:
            st.text_input("Add comment (optional)", placeholder="What was wrong?",
                          label_visibility="collapsed")
    else:
        st.success(f"Feedback saved · ID: `{st.session_state.memory_id}`")

    st.markdown("</div>", unsafe_allow_html=True)

    # Related topics
    related = explanation.get("related_topics", [])
    if related:
        chips = " ".join(f"<span class='empty-tag'>{t}</span>" for t in related)
        st.markdown(f"""
        <div style='margin-top:1rem'>
          <div class='section-label' style='margin-bottom:0.5rem'>Related Topics</div>
          <div style='display:flex;gap:0.4rem;flex-wrap:wrap'>{chips}</div>
        </div>""", unsafe_allow_html=True)


# ── Empty State ────────────────────────────────────────────────────────────────
if not result:
    st.markdown("""
    <div class='empty-state'>
      <div class='empty-glyph'>∫</div>
      <div class='empty-title'>Ready to Solve</div>
      <div class='empty-sub'>Enter a problem above and press <strong>Solve Problem</strong></div>
      <div class='empty-tags'>
        <span class='empty-tag'>Algebra</span>
        <span class='empty-tag'>Probability</span>
        <span class='empty-tag'>Calculus</span>
        <span class='empty-tag'>Linear Algebra</span>
        <span class='empty-tag'>Trigonometry</span>
        <span class='empty-tag'>Statistics</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
"""
Student Lab OS — Mission Cockpit
Single-screen guided research console for the Medical AI + Agentic Coding Lab.

Students operate in VS Code + Claude Code.
This dashboard is orientation, mission guidance, artifact preview, and progress.
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import re
import subprocess
import time
import streamlit as st

# ── Repo root ─────────────────────────────────────────────────────────────────

BASE       = Path(__file__).resolve().parents[1]
STATE_PATH = BASE / ".student_state" / "current_mission.json"

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title   = "Medical AI Lab",
    layout       = "wide",
    initial_sidebar_state = "expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────

def inject_css() -> None:
    st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════════════════════════
   BASE — light slate shell, white cards, dark ink
   ═══════════════════════════════════════════════════════════════════════════ */

html, body, .stApp {
    background-color: #EEF2F7 !important;
    color: #1E293B !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}
.stApp > header {
    background-color: #EEF2F7 !important;
    border-bottom: 1px solid #D6DFEA !important;
}
.main .block-container {
    background: transparent !important;
    padding: 1.4rem 2rem 2.5rem 2rem !important;
    max-width: none !important;
}

/* ── Sidebar — light cool grey, crisp borders ────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #F0F4F8 !important;
    border-right: 1px solid #D6DFEA !important;
}
section[data-testid="stSidebar"] > div:first-child {
    background: #F0F4F8 !important;
}
/* Sidebar text defaults */
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] label {
    color: #334155 !important;
}
/* Sidebar dividers */
section[data-testid="stSidebar"] hr {
    border-color: #D6DFEA !important;
}
/* Sidebar expander */
section[data-testid="stSidebar"] details[data-testid="stExpander"] > summary {
    background: #E8EEF4 !important;
    border-color: #D6DFEA !important;
    color: #334155 !important;
}
section[data-testid="stSidebar"] details[data-testid="stExpander"] > div {
    background: #F4F7FB !important;
    border-color: #D6DFEA !important;
}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    background: transparent !important;
    border-bottom: 2px solid #D6DFEA !important;
    gap: 0 !important;
    padding-bottom: 0 !important;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: #94A3B8 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    border-radius: 0 !important;
    padding: 10px 22px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    transition: color 0.15s !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: #475569 !important;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #1E40AF !important;
    border-bottom: 2px solid #2563EB !important;
    background: transparent !important;
}

/* ── Metrics ─────────────────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #FFFFFF !important;
    border: 1px solid #D6DFEA !important;
    border-radius: 10px !important;
    padding: 16px 18px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 0.80rem !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #0F172A !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] svg { display: none !important; }

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    background: #FFFFFF !important;
    color: #374151 !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 7px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
    padding: 8px 16px !important;
}
.stButton > button:hover {
    background: #F8FAFC !important;
    color: #1E293B !important;
    border-color: #94A3B8 !important;
}
.stButton > button[kind="primary"] {
    background: #1E40AF !important;
    color: #FFFFFF !important;
    border: 1px solid #1E40AF !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1D4ED8 !important;
    border-color: #1D4ED8 !important;
}

/* ── Code blocks ─────────────────────────────────────────────────────────── */
.stCodeBlock, .stCodeBlock pre {
    background: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
}
.stCodeBlock code {
    color: #1E293B !important;
    font-size: 0.90rem !important;
    line-height: 1.7 !important;
}
.stCodeBlock button {
    background: #F1F5F9 !important;
    border: 1px solid #CBD5E1 !important;
    color: #64748B !important;
}

/* ── Expanders ───────────────────────────────────────────────────────────── */
details[data-testid="stExpander"] > summary {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #475569 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
}
details[data-testid="stExpander"] > summary:hover {
    background: #F8FAFC !important;
    color: #1E293B !important;
}
details[data-testid="stExpander"] > div {
    background: #FAFBFC !important;
    border: 1px solid #E2E8F0 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 16px 18px !important;
}
details[data-testid="stExpander"][open] > summary {
    border-radius: 8px 8px 0 0 !important;
    color: #1E293B !important;
}

/* ── Progress bar ────────────────────────────────────────────────────────── */
.stProgress > div {
    background: #E2E8F0 !important;
    border-radius: 4px !important;
    height: 6px !important;
}
.stProgress > div > div {
    height: 6px !important;
    background: linear-gradient(90deg, #1E40AF, #3B82F6) !important;
    border-radius: 4px !important;
}

/* ── Selectbox ───────────────────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    color: #374151 !important;
    border-radius: 7px !important;
}

/* ── Alerts / notifications ──────────────────────────────────────────────── */
[data-testid="stNotification"],
.stAlert > div {
    border-radius: 8px !important;
    font-size: 0.88rem !important;
}
[data-testid="stInfo"]    > div {
    background: #EFF6FF !important;
    border-color: #BFDBFE !important;
    color: #1D4ED8 !important;
}
[data-testid="stSuccess"] > div {
    background: #F0FDF4 !important;
    border-color: #BBF7D0 !important;
    color: #15803D !important;
}
[data-testid="stWarning"] > div {
    background: #FFFBEB !important;
    border-color: #FDE68A !important;
    color: #92400E !important;
}

/* ── Divider ─────────────────────────────────────────────────────────────── */
hr { border-color: #E2E8F0 !important; margin: 14px 0 !important; }

/* ── Containers with border=True ─────────────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}

/* ── Markdown text ───────────────────────────────────────────────────────── */
.stMarkdown p {
    color: #334155 !important;
    font-size: 0.92rem !important;
    line-height: 1.70 !important;
}
.stMarkdown h1 { color: #0F172A !important; font-size: 1.4rem !important; font-weight: 700 !important; }
.stMarkdown h2 { color: #1E293B !important; font-size: 1.15rem !important; font-weight: 700 !important; }
.stMarkdown h3 { color: #334155 !important; font-size: 1.05rem !important; font-weight: 700 !important; }
.stMarkdown h4 { color: #475569 !important; font-size: 0.95rem !important; font-weight: 700 !important; }
.stMarkdown code {
    background: #EFF6FF !important;
    color: #1E40AF !important;
    border-radius: 4px !important;
    padding: 2px 7px !important;
    font-size: 0.85rem !important;
}
.stMarkdown blockquote {
    border-left: 3px solid #3B82F6 !important;
    padding-left: 14px !important;
    color: #475569 !important;
    background: #F8FAFC !important;
    border-radius: 0 6px 6px 0 !important;
    margin: 8px 0 !important;
}
.stMarkdown strong { color: #0F172A !important; font-weight: 700 !important; }
.stMarkdown li { color: #334155 !important; font-size: 0.92rem !important; }

/* ── Captions ────────────────────────────────────────────────────────────── */
.stCaption { color: #94A3B8 !important; font-size: 0.78rem !important; }
small.stCaption { color: #94A3B8 !important; }


/* ═══════════════════════════════════════════════════════════════════════════
   CUSTOM COMPONENTS
   ═══════════════════════════════════════════════════════════════════════════ */

/* ── Welcome / onboarding ────────────────────────────────────────────────── */
.welcome-wrap {
    max-width: 800px;
    margin: 56px auto 0 auto;
    text-align: center;
}
.welcome-eyebrow {
    font-size: 0.70rem;
    font-weight: 700;
    letter-spacing: 0.20em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 20px;
}
.welcome-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 18px;
}
.welcome-sub {
    font-size: 1.0rem;
    color: #475569;
    line-height: 1.70;
    margin-bottom: 40px;
}
.welcome-role-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 20px;
    text-align: left;
    height: 100%;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.welcome-role-eyebrow {
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 6px;
}
.welcome-role-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 8px;
}
.welcome-role-body {
    font-size: 0.85rem;
    color: #475569;
    line-height: 1.55;
}
.welcome-stats {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.10em;
    color: #94A3B8;
    margin: 32px 0 36px 0;
    text-transform: uppercase;
}
.welcome-stats span { color: #CBD5E1; margin: 0 10px; }

/* ── Mission header strip ────────────────────────────────────────────────── */
.cockpit-mission-header {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #2563EB;
    border-radius: 0 10px 10px 0;
    padding: 18px 22px;
    margin-bottom: 14px;
    box-shadow: 0 1px 5px rgba(0,0,0,0.05);
}
.cockpit-mission-eyebrow {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 6px;
}
.cockpit-mission-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 6px 0;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.cockpit-mission-goal {
    font-size: 0.90rem;
    color: #475569;
    margin: 0;
    line-height: 1.50;
}

/* ── Stage progress pills ────────────────────────────────────────────────── */
.stage-pills { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0 16px 0; }
.stage-pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 12px; border-radius: 16px;
    font-size: 0.75rem; font-family: monospace; font-weight: 600;
}
.stage-pill-done    { background: #F0FDF4; border: 1px solid #BBF7D0; color: #15803D; }
.stage-pill-pending { background: #F8FAFC; border: 1px solid #E2E8F0; color: #94A3B8; }
.stage-pill-active  { background: #EFF6FF; border: 1px solid #BFDBFE; color: #1D4ED8; }

/* ── Prompt copy section ─────────────────────────────────────────────────── */
.prompt-copy-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 6px;
}
.prompt-file-tag {
    font-size: 0.76rem;
    color: #94A3B8;
    font-family: monospace;
    margin-bottom: 10px;
}
.prompt-multistage-hint {
    font-size: 0.82rem;
    color: #64748B;
    margin-bottom: 10px;
    font-weight: 500;
}

/* ── After-running checklist ─────────────────────────────────────────────── */
.run-section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #64748B;
    margin: 18px 0 10px 0;
}
.run-step {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 8px 0; font-size: 0.88rem; color: #334155;
    line-height: 1.55;
}
.run-step-num {
    min-width: 22px; height: 22px; border-radius: 50%;
    background: #1E40AF; color: #FFFFFF;
    font-size: 0.68rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 2px;
}
.run-step code {
    background: #F1F5F9; color: #1E40AF;
    padding: 2px 7px; border-radius: 4px;
    font-size: 0.82rem; font-weight: 600;
}

/* ── Layer B locked / unlocked ───────────────────────────────────────────── */
.layer-b-lock {
    background: #F8FAFC;
    border: 1px dashed #CBD5E1;
    border-radius: 10px;
    padding: 24px 28px;
    text-align: center;
    margin: 4px 0;
}
.layer-b-lock-icon  { font-size: 1.2rem; margin-bottom: 6px; color: #CBD5E1; }
.layer-b-lock-title { font-size: 0.88rem; font-weight: 600; color: #94A3B8; margin-bottom: 4px; }
.layer-b-lock-hint  { font-size: 0.80rem; color: #CBD5E1; }
.layer-b-open-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: #15803D; margin-bottom: 10px;
}

/* ── Sidebar mission rail ─────────────────────────────────────────────────── */
.rail-item {
    display: flex; align-items: flex-start; gap: 9px;
    padding: 4px 0;
}
.rail-dot-col { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; }
.rail-dot {
    width: 26px; height: 26px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.70rem; font-weight: 700; flex-shrink: 0;
}
.rail-line { width: 2px; min-height: 14px; flex-grow: 1; }
.rail-label { font-size: 0.74rem; line-height: 1.3; padding-top: 5px; }

/* ── Artifact panel ──────────────────────────────────────────────────────── */
.artifact-panel-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: #64748B; margin-bottom: 12px;
}
.artifact-empty {
    background: #F8FAFC;
    border: 1px dashed #CBD5E1;
    border-radius: 10px;
    padding: 32px 24px;
    text-align: center;
}
.artifact-empty-icon  { font-size: 1.6rem; color: #CBD5E1; margin-bottom: 10px; }
.artifact-empty-title { font-size: 0.88rem; font-weight: 600; color: #94A3B8; margin-bottom: 5px; }
.artifact-empty-hint  { font-size: 0.80rem; color: #CBD5E1; line-height: 1.55; }

/* ── Completion / unlock card ─────────────────────────────────────────────── */
.unlock-card {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 14px;
}
.unlock-card-top    { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #15803D; margin-bottom: 4px; }
.unlock-card-title  { font-size: 0.95rem; font-weight: 600; color: #166534; margin-bottom: 5px; }
.unlock-card-next   { font-size: 0.84rem; color: #15803D; }
.unlock-card-next b { color: #14532D; font-weight: 700; }

/* ── Metric snippet card ─────────────────────────────────────────────────── */
.metric-snippet {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.metric-snippet-label { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #64748B; margin-bottom: 5px; }
.metric-snippet-value { font-size: 1.8rem; font-weight: 700; color: #0F172A; letter-spacing: -0.02em; }
.metric-snippet-sub   { font-size: 0.74rem; color: #94A3B8; margin-top: 3px; }

/* ── All-complete banner ─────────────────────────────────────────────────── */
.all-done-banner {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 12px;
    padding: 32px 28px;
    text-align: center;
    margin-bottom: 22px;
}
.all-done-icon    { font-size: 2.2rem; color: #15803D; margin-bottom: 10px; }
.all-done-title   { font-size: 1.2rem; font-weight: 700; color: #14532D; margin-bottom: 6px; }
.all-done-sub     { font-size: 0.92rem; color: #15803D; line-height: 1.55; }

/* ── Mission map card ────────────────────────────────────────────────────── */
.mmap-row {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 16px; border-radius: 10px; margin-bottom: 8px;
}
.mmap-row.complete { background: #F0FDF4; border: 1px solid #BBF7D0; border-left: 4px solid #22C55E; }
.mmap-row.current  { background: #FFFFFF; border: 1px solid #BFDBFE; border-left: 4px solid #2563EB;
                     box-shadow: 0 2px 8px rgba(37,99,235,0.08); }
.mmap-row.unlocked { background: #FFFFFF; border: 1px solid #E2E8F0; }
.mmap-row.locked   { background: #F8FAFC; border: 1px solid #F1F5F9; opacity: 0.50; }
.mmap-dot {
    width: 26px; height: 26px; border-radius: 50%;
    font-size: 0.70rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.mmap-dot.complete  { background: #DCFCE7; color: #15803D; border: 1px solid #BBF7D0; }
.mmap-dot.current   { background: #DBEAFE; color: #1D4ED8; border: 1px solid #BFDBFE; }
.mmap-dot.unlocked  { background: #F1F5F9; color: #64748B; border: 1px solid #E2E8F0; }
.mmap-dot.locked    { background: #F8FAFC; color: #CBD5E1; border: 1px solid #F1F5F9; }
.mmap-title { font-size: 0.92rem; font-weight: 600; }
.mmap-title.complete  { color: #166534; }
.mmap-title.current   { color: #1E40AF; }
.mmap-title.unlocked  { color: #1E293B; }
.mmap-title.locked    { color: #94A3B8; }
.mmap-goal { font-size: 0.82rem; color: #64748B; margin-top: 3px; }

.chip {
    display: inline-flex; align-items: center;
    padding: 3px 10px; border-radius: 14px;
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.07em; text-transform: uppercase;
    margin-left: auto; flex-shrink: 0;
}
.chip-complete { background: #DCFCE7; color: #15803D; border: 1px solid #BBF7D0; }
.chip-current  { background: #DBEAFE; color: #1D4ED8; border: 1px solid #BFDBFE; }
.chip-unlocked { background: #F1F5F9; color: #64748B; border: 1px solid #E2E8F0; }
.chip-locked   { background: #F8FAFC; color: #CBD5E1; border: 1px solid #F1F5F9; }

/* ── Notification strips ─────────────────────────────────────────────────── */
.notif {
    border-radius: 8px; padding: 12px 18px;
    font-size: 0.88rem; font-weight: 500;
    margin: 0 0 14px 0; line-height: 1.50;
}
.notif code {
    background: rgba(0,0,0,0.06);
    padding: 2px 6px; border-radius: 4px; font-size: 0.82rem;
}
.notif-warn    { background: #FFFBEB; border: 1px solid #FDE68A; color: #92400E; }
.notif-rebuilt { background: #EFF6FF; border: 1px solid #BFDBFE; color: #1D4ED8; }
.notif-reset   { background: #F8FAFC; border: 1px solid #E2E8F0; color: #64748B; }

/* Checkpoint panel */
.checkpoint-panel {
    background: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 12px;
    padding: 24px 28px; margin: 8px 0 16px 0; text-align: center;
}
.checkpoint-panel.fail {
    background: #FFF7ED; border-color: #FCD34D;
}
.checkpoint-title {
    font-size: 1.15rem; font-weight: 700; color: #166534; margin: 0 0 6px 0;
}
.checkpoint-panel.fail .checkpoint-title { color: #92400E; }
.checkpoint-detail { font-size: 0.83rem; color: #166534; margin: 0; line-height: 1.5; }
.checkpoint-panel.fail .checkpoint-detail { color: #92400E; }

/* Mission number badge */
.mission-num-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 34px; height: 34px; border-radius: 50%;
    background: #2563EB; color: #fff; font-size: 0.95rem; font-weight: 800;
    flex-shrink: 0; margin-right: 10px;
}

/* Prompt principle callout */
.prompt-principle-callout {
    background: #EFF6FF; border-left: 4px solid #2563EB; border-radius: 0 8px 8px 0;
    padding: 10px 14px; margin: 10px 0 4px 0;
}
.prompt-principle-label {
    font-size: 0.72rem; font-weight: 700; color: #2563EB; text-transform: uppercase;
    letter-spacing: 0.06em; margin: 0 0 3px 0;
}
.prompt-principle-name { font-size: 0.88rem; font-weight: 700; color: #1E40AF; margin: 0 0 4px 0; }
.prompt-principle-body { font-size: 0.80rem; color: #334155; margin: 0; line-height: 1.5; }

/* Session archive rows */
.archive-row {
    display: flex; align-items: center; justify-content: space-between;
    background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;
    padding: 8px 12px; margin: 4px 0; font-size: 0.80rem; color: #334155;
}
.archive-ts { font-family: monospace; color: #64748B; font-size: 0.76rem; }

/* Mission map clickable card highlight */
.mission-map-card-revisit {
    cursor: pointer; border: 2px solid #2563EB !important;
}

/* Bonus challenge callout */
.bonus-callout {
    background: #FFFBEB; border: 1px solid #FDE68A; border-left: 4px solid #F59E0B;
    border-radius: 0 8px 8px 0; padding: 10px 14px; margin: 10px 0 4px 0;
}
.bonus-label { font-size: 0.72rem; font-weight: 700; color: #92400E; text-transform: uppercase; letter-spacing: 0.06em; margin: 0 0 3px 0; }
.bonus-body  { font-size: 0.82rem; color: #78350F; margin: 0; line-height: 1.5; }


</style>
""", unsafe_allow_html=True)

# ── Data helpers ──────────────────────────────────────────────────────────────

def load_json(path: Path) -> dict | None:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def read_text(path: Path) -> str | None:
    if path.exists():
        try:
            return path.read_text(encoding="utf-8")
        except Exception:
            return None
    return None


def stage_ok(stage_name: str) -> bool:
    data = load_json(BASE / "outputs" / "status" / f"{stage_name}.json")
    return data is not None and data.get("status") == "ok"


def fig_exists(filename: str) -> bool:
    p = BASE / "outputs" / "figures" / filename
    return p.exists() and p.stat().st_size > 100


def metric_exists(filename: str) -> bool:
    return (BASE / "outputs" / "metrics" / filename).exists()


def report_text(filename: str) -> str | None:
    return read_text(BASE / "reports" / filename)


def prompt_text(filename: str) -> str | None:
    return read_text(BASE / "prompts" / filename)


def parse_prompt_layers(content: str) -> dict[str, str]:
    layers: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []
    for line in content.splitlines():
        m = re.match(r"^## Layer ([ABC])\b", line)
        if m:
            if current_key:
                layers[current_key] = "\n".join(current_lines).strip()
            current_key = m.group(1)
            current_lines = []
        elif line.startswith("## ") and current_key:
            layers[current_key] = "\n".join(current_lines).strip()
            current_key = None
            current_lines = []
        elif current_key is not None:
            current_lines.append(line)
    if current_key and current_lines:
        layers[current_key] = "\n".join(current_lines).strip()
    return layers


def extract_prompt_quote(layer_text: str) -> tuple[str, str]:
    """Split Layer A into (blockquote_to_copy, surrounding_context)."""
    lines         = layer_text.splitlines()
    quote_parts: list[str] = []
    other_parts: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(">"):
            clean = stripped.lstrip(">").strip()
            if clean.startswith('"') and clean.endswith('"'):
                clean = clean[1:-1]
            if clean:
                quote_parts.append(clean)
        else:
            other_parts.append(line)
    quote   = "\n".join(quote_parts).strip()
    context = "\n".join(other_parts).strip()
    if not quote and context:
        paras = [p.strip() for p in context.split("\n\n") if p.strip()]
        if paras:
            quote   = paras[0]
            context = "\n\n".join(paras[1:])
    return quote, context

# ── Student state ─────────────────────────────────────────────────────────────

DEFAULT_STATE: dict = {
    "current_mission":    0,
    "completed_missions": [],
    "unlocked_missions":  [0],
    "last_checked":       None,
    "mode":               "guided",
}


def load_student_state() -> dict:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if STATE_PATH.exists():
        try:
            data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            for k, v in DEFAULT_STATE.items():
                if k not in data:
                    data[k] = v
            return data
        except Exception:
            pass
    state = dict(DEFAULT_STATE)
    save_student_state(state)
    return state


def save_student_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def init_session_state() -> None:
    if "lab_state" not in st.session_state:
        st.session_state["lab_state"] = load_student_state()
    loaded_state = st.session_state["lab_state"]
    if "entered_lab" not in st.session_state:
        # Auto-skip welcome if student has already started
        st.session_state["entered_lab"] = (
            len(loaded_state["completed_missions"]) > 0 or
            loaded_state["current_mission"] > 0
        )
    if "last_refresh_result" not in st.session_state:
        st.session_state["last_refresh_result"] = None
    if "confirm_reset" not in st.session_state:
        st.session_state["confirm_reset"] = False
    if "reset_phase" not in st.session_state:
        st.session_state["reset_phase"] = 0   # 0=idle 1=confirm 2=done
    if "checkpoint" not in st.session_state:
        st.session_state["checkpoint"] = None  # None | {"phase": "checking"|"result", "mission_idx": int, "passed": bool, "details": list}
    if "viewing_mission_idx" not in st.session_state:
        st.session_state["viewing_mission_idx"] = None  # None = current; int = revisit mode
    if "tutorial_step" not in st.session_state:
        st.session_state["tutorial_step"] = None  # None=not started; int=current step; "done"=completed

# ── Mission definitions ───────────────────────────────────────────────────────

MISSIONS: list[dict] = [
    {
        "label": "Mission 0 — Wake the Lab",
        "goal":  "Environment setup and first prompt-driven success.",
        "purpose": (
            "Verify that the full tool chain — Python, Claude Code, VS Code, and the repo scaffold — "
            "is operational before any scientific work begins."
        ),
        "why_it_matters": (
            "A broken environment produces meaningless results. Confirming readiness is the first "
            "scientific step, not a formality. If the environment is wrong, every subsequent artifact "
            "may be wrong without any obvious error."
        ),
        "student_learns": (
            "How Claude Code reads and navigates a research repo; the difference between environment "
            "readiness and data readiness; what the status file format means."
        ),
        "stages":   ["stage_00_bootstrap"],
        "prompts":  ["stage_00_bootstrap.md"],
        "reports":  ["env_check.md"],
        "allowed_files":   ["scripts/bootstrap.py", "reports/env_check.md"],
        "protected_files": ["CLAUDE.md", "ASSIGNMENT.md", "tests/", "prompts/", "artifacts/schema.json"],
        "expected_outputs": ["outputs/status/stage_00_bootstrap.json", "reports/env_check.md"],
        "make_commands":    ["make bootstrap"],
        "prompt_principle": "Explicit task + expected output",
        "takeaway": "Naming exact output file paths in your prompt creates a verifiable contract. Without them, Claude may write outputs anywhere or skip them entirely.",
        "bonus_prompt": "Extend reports/env_check.md with hardware context: GPU availability, RAM, and disk space. Use psutil if available; note 'not checked' if not. A hardware summary is the first step toward realistic timeline estimation.",
    },
    {
        "label": "Mission 1 — Receive the Signal",
        "goal":  "Fetch the teaching pack and confirm the dataset is ready.",
        "purpose": (
            "Download the imaging teaching dataset and verify that it is structurally intact "
            "and ready for analysis."
        ),
        "why_it_matters": (
            "You cannot evaluate a model on data you have not inspected. Receiving and confirming "
            "data is a data integrity step — not just a download."
        ),
        "student_learns": (
            "What the teaching pack contains; how status files track pipeline progress; "
            "why input validation matters before modeling."
        ),
        "stages":   ["stage_01_fetch_sample"],
        "prompts":  ["stage_01_fetch_sample.md"],
        "reports":  [],
        "allowed_files":   ["scripts/fetch_data.py"],
        "protected_files": ["CLAUDE.md", "ASSIGNMENT.md", "tests/", "prompts/", "artifacts/schema.json"],
        "expected_outputs": ["outputs/status/stage_01_fetch_sample.json", "data/sample/  (imaging dataset)"],
        "make_commands":    ["make fetch-sample"],
        "prompt_principle": "File permission scope + state assertion",
        "takeaway": "Telling Claude which files it may touch prevents side effects. Asserting expected state ('confirm N slices were loaded') forces explicit validation rather than silent completion.",
        "bonus_prompt": "Load the first image and mask array. Report shape, dtype, value range, and mask foreground fraction. Write these statistics to reports/data_notes.md as a preliminary data characterization.",
    },
    {
        "label": "Mission 2 — Build the First Detector",
        "goal":  "Visualize the data, train the baseline, and record the first metric.",
        "purpose": (
            "Load the dataset, produce the first visual artifact, and run the smallest deterministic "
            "baseline model to establish a reproducible starting point."
        ),
        "why_it_matters": (
            "Every later comparison depends on this baseline being correct and reproducible. "
            "The goal is not a high Dice score — it is a score you can explain."
        ),
        "student_learns": (
            "What Dice score means in practice; what 'baseline' means in research; "
            "how to interpret a loss curve."
        ),
        "stages":   ["stage_02_load_visualize", "stage_03_train_baseline"],
        "prompts":  ["stage_02_load_visualize.md", "stage_03_train_baseline.md"],
        "reports":  ["data_notes.md", "train_notes.md"],
        "allowed_files":   ["scripts/visualize_sample.py", "scripts/run_train.py", "reports/data_notes.md", "reports/train_notes.md"],
        "protected_files": ["CLAUDE.md", "ASSIGNMENT.md", "tests/", "prompts/", "artifacts/schema.json"],
        "expected_outputs": ["outputs/figures/sample_overlay.png", "outputs/figures/loss_curve.png", "outputs/metrics/val_metrics.json", "outputs/status/stage_02_load_visualize.json", "outputs/status/stage_03_train_baseline.json"],
        "make_commands":    ["make visualize", "make smoke-train"],
        "prompt_principle": "Inspect before you act",
        "takeaway": "Asking Claude to describe what it sees in the data before creating outputs grounds its work in evidence. The interpretation is as important as the figure.",
        "bonus_prompt": "Create a multi-slice overview figure showing at least 3 slices with mask overlays. Save to outputs/figures/multi_slice_overview.png. Note whether mask coverage varies across slices — variation reveals dataset heterogeneity.",
    },
    {
        "label": "Mission 3 — Investigate Failure",
        "goal":  "Identify best and worst predictions and form a failure hypothesis.",
        "purpose": (
            "Analyse where and why the baseline fails — slice by slice — "
            "and produce a written hypothesis about the dominant failure mode."
        ),
        "why_it_matters": (
            "Blind improvement without error understanding is engineering guesswork, not science. "
            "The hypothesis you write here determines whether Mission 4 is a valid controlled experiment."
        ),
        "student_learns": (
            "How to read TP/FP/FN error maps; how to form a testable hypothesis from observational data."
        ),
        "stages":   ["stage_04_error_analysis"],
        "prompts":  ["stage_04_error_analysis.md"],
        "reports":  ["error_analysis.md"],
        "allowed_files":   ["scripts/error_analysis.py", "reports/error_analysis.md"],
        "protected_files": ["CLAUDE.md", "ASSIGNMENT.md", "tests/", "prompts/", "artifacts/schema.json"],
        "expected_outputs": ["outputs/figures/error_analysis_best.png", "outputs/figures/error_analysis_worst.png", "outputs/status/stage_04_error_analysis.json", "reports/error_analysis.md"],
        "make_commands":    ["make error-analysis"],
        "prompt_principle": "Observation → hypothesis",
        "takeaway": "Sequencing observe-first, explain-second forces evidence-grounded reasoning. A prompt that asks for a hypothesis before observation invites speculation, not science.",
        "bonus_prompt": "Compute the Dice score distribution across all validation slices and plot a histogram. Save to outputs/figures/dice_distribution.png. What is the 10th percentile Dice? How does it compare to the mean? Update reports/error_analysis.md with distributional findings.",
    },
    {
        "label": "Mission 4 — Improve With Intent",
        "goal":  "Make one controlled improvement, compare results, pack the Day 1 summary.",
        "purpose": (
            "Test one specific, well-motivated change to the baseline and measure the result "
            "with the same metric. Assemble all Day 1 findings into a summary deliverable."
        ),
        "why_it_matters": (
            "One controlled change with honest reporting is more scientifically valuable than multiple "
            "unjustified tweaks."
        ),
        "student_learns": (
            "What a controlled experiment means in ML; how to compare two pipelines fairly; "
            "that negative results are valid scientific results."
        ),
        "stages":   ["stage_05_model_swap", "stage_06_pack_report"],
        "prompts":  ["stage_05_model_swap.md", "stage_06_pack_report.md"],
        "reports":  ["model_swap.md", "day1_summary.md"],
        "allowed_files":   ["scripts/model_swap.py", "scripts/pack_report.py", "reports/model_swap.md", "reports/day1_summary.md"],
        "protected_files": ["CLAUDE.md", "ASSIGNMENT.md", "tests/", "prompts/", "artifacts/schema.json"],
        "expected_outputs": ["outputs/metrics/model_swap_comparison.json", "outputs/figures/model_swap_comparison.png", "outputs/status/stage_05_model_swap.json", "reports/model_swap.md", "reports/day1_summary.md", "outputs/status/stage_06_pack_report.json"],
        "make_commands":    ["make model-swap", "make pack-report"],
        "prompt_principle": "Control variable framing",
        "takeaway": "Naming the control variable in your prompt is experimental design, not micromanagement. Without it, Claude may change multiple things and produce an uninterpretable result.",
        "bonus_prompt": "Try one additional variation — a different improvement direction than the one tested. Save to outputs/metrics/model_swap_v2.json (same schema). In reports/model_swap.md, add a section comparing both variations. Which produced better results? Does combining both help or hurt?",
    },
    {
        "label": "Mission 5 — Design the Next Study",
        "goal":  "Write a Day 2 challenge plan, then implement and measure it.",
        "purpose": (
            "Before writing any code, produce a written plan for the Day 2 challenge. "
            "Then implement the adaptation and measure the outcome against Day 1."
        ),
        "why_it_matters": (
            "Research planning is a distinct skill from execution. A written plan forces clarity "
            "about what you believe before you commit to implementation."
        ),
        "student_learns": (
            "How to translate error observations into a testable strategy; "
            "how to report an outcome that differs from the plan."
        ),
        "stages":   ["stage_07_challenge_plan", "stage_08_adapt_pipeline"],
        "prompts":  ["stage_07_challenge_plan.md", "stage_08_adapt_pipeline.md"],
        "reports":  ["challenge_plan.md", "adapt_pipeline.md"],
        "allowed_files":   ["scripts/challenge_plan.py", "scripts/adapt_pipeline.py", "reports/challenge_plan.md", "reports/adapt_pipeline.md"],
        "protected_files": ["CLAUDE.md", "ASSIGNMENT.md", "tests/", "prompts/", "artifacts/schema.json"],
        "expected_outputs": ["outputs/status/stage_07_challenge_plan.json", "reports/challenge_plan.md", "outputs/metrics/challenge_comparison.json", "outputs/figures/challenge_comparison.png", "outputs/status/stage_08_adapt_pipeline.json", "reports/adapt_pipeline.md"],
        "make_commands":    ["make challenge-plan", "make adapt-pipeline"],
        "prompt_principle": "Plan before code",
        "takeaway": "A plan written before the experiment is the benchmark for judging the result. Code written without a plan is unverifiable. The plan also teaches role-switching: designer and critic are different perspectives.",
        "bonus_prompt": "Add a role-switching exercise to reports/challenge_plan.md. Ask Claude: (1) as the algorithm designer — what is the most technically promising change? (2) as a clinical safety reviewer — what change would you most want validated before clinical use? Do the two perspectives agree on priority?",
    },
    {
        "label": "Mission 6 — Translate Responsibly",
        "goal":  "Reflect on clinical implications and write the translation memo.",
        "purpose": (
            "Locate the prototype honestly on the path from a toy pipeline to a research contribution. "
            "Produce a written memo a clinical collaborator could read."
        ),
        "why_it_matters": (
            "Overstating prototype capabilities in clinical AI can cause direct patient harm. "
            "This is the most important writing exercise of the lab."
        ),
        "student_learns": (
            "The gap between in-sample performance and clinical validity; "
            "what regulatory pathways require before clinical deployment."
        ),
        "stages":   ["stage_09_translation_memo"],
        "prompts":  ["stage_09_translation_memo.md"],
        "reports":  ["translation_memo.md"],
        "allowed_files":   ["scripts/translation_memo.py", "reports/translation_memo.md"],
        "protected_files": ["CLAUDE.md", "ASSIGNMENT.md", "tests/", "prompts/", "artifacts/schema.json"],
        "expected_outputs": ["outputs/status/stage_09_translation_memo.json", "reports/translation_memo.md"],
        "make_commands":    ["make translation-memo"],
        "prompt_principle": "Honesty constraint + audience framing",
        "takeaway": "Without 'do not overstate capabilities' and an explicit audience, Claude defaults to technical optimism. Both constraints shape register and honesty simultaneously.",
        "bonus_prompt": "Write a second, more optimistic version of the memo at reports/translation_memo_optimistic.md. Then write reports/translation_comparison.md analyzing which version is appropriate for: a conference abstract, an FDA submission, a patient conversation. What specifically differs between the two versions?",
    },
]

# Artifact preview hints per mission index
MISSION_PREVIEW: dict[int, dict] = {
    0: {"figure": None,                        "metric": None,                                                            "status_stage": "stage_00_bootstrap"},
    1: {"figure": None,                        "metric": None,                                                            "status_stage": "stage_01_fetch_sample"},
    2: {"figure": "sample_overlay.png",        "metric": ("val_metrics.json",           "dice",     "Baseline Dice"),    "status_stage": None},
    3: {"figure": "error_analysis_best.png",   "metric": None,                                                            "status_stage": None},
    4: {"figure": "model_swap_comparison.png", "metric": ("model_swap_comparison.json", "new_dice", "Model Swap Dice"),  "status_stage": None},
    5: {"figure": "challenge_comparison.png",  "metric": ("challenge_comparison.json",  "new_dice", "Day 2 Dice"),       "status_stage": None},
    6: {"figure": None,                        "metric": None,                                                            "status_stage": "stage_09_translation_memo", "report": "translation_memo.md"},
}

# ── Mission progression helpers ───────────────────────────────────────────────

def mission_stages_complete(idx: int) -> bool:
    return all(stage_ok(s) for s in MISSIONS[idx]["stages"])


def get_mission_display_status(idx: int, state: dict) -> str:
    if idx in state["completed_missions"]:
        return "complete"
    if idx == state["current_mission"]:
        return "current"
    if idx in state["unlocked_missions"]:
        return "unlocked"
    return "locked"


def get_active_stage_idx(mission: dict) -> int:
    """Return index of first incomplete stage, or last if all complete."""
    for i, stage in enumerate(mission["stages"]):
        if not stage_ok(stage):
            return i
    return len(mission["stages"]) - 1


def rebuild_state_from_artifacts() -> dict:
    completed: list[int] = []
    unlocked:  list[int] = [0]
    current = 0
    all_done = True
    for i in range(len(MISSIONS)):
        if mission_stages_complete(i):
            if i not in completed:
                completed.append(i)
            nxt = i + 1
            if nxt < len(MISSIONS) and nxt not in unlocked:
                unlocked.append(nxt)
        else:
            current = i
            all_done = False
            break
    if all_done:
        current = len(MISSIONS) - 1
    return {
        "current_mission":    current,
        "completed_missions": completed,
        "unlocked_missions":  unlocked,
        "last_checked":       datetime.now(timezone.utc).isoformat(),
        "mode":               "guided",
    }


def do_refresh_current_mission(state: dict) -> tuple[dict, str]:
    idx     = min(state["current_mission"], len(MISSIONS) - 1)
    mission = MISSIONS[idx]
    state   = dict(state)
    state["last_checked"] = datetime.now(timezone.utc).isoformat()
    if mission_stages_complete(idx):
        if idx not in state["completed_missions"]:
            state["completed_missions"] = state["completed_missions"] + [idx]
        nxt = idx + 1
        if nxt < len(MISSIONS):
            if nxt not in state["unlocked_missions"]:
                state["unlocked_missions"] = state["unlocked_missions"] + [nxt]
            state["current_mission"] = nxt
            return state, f"complete:{mission['label']}|unlock:{MISSIONS[nxt]['label']}"
        else:
            return state, f"allcomplete:{mission['label']}"
    else:
        missing = [s for s in mission["stages"] if not stage_ok(s)]
        return state, "missing:" + ",".join(missing)

# ── Required artifacts (Evaluation tab) ──────────────────────────────────────

REQUIRED_STATUS = [
    ("stage_00_bootstrap.json",        "Mission 0"),
    ("stage_01_fetch_sample.json",     "Mission 1"),
    ("stage_02_load_visualize.json",   "Mission 2"),
    ("stage_03_train_baseline.json",   "Mission 2"),
    ("stage_04_error_analysis.json",   "Mission 3"),
    ("stage_05_model_swap.json",       "Mission 4"),
    ("stage_06_pack_report.json",      "Mission 4"),
    ("stage_07_challenge_plan.json",   "Mission 5"),
    ("stage_08_adapt_pipeline.json",   "Mission 5"),
    ("stage_09_translation_memo.json", "Mission 6"),
]
REQUIRED_FIGURES = [
    ("sample_overlay.png",        "Mission 2"),
    ("loss_curve.png",            "Mission 2"),
    ("error_analysis_best.png",   "Mission 3"),
    ("error_analysis_worst.png",  "Mission 3"),
    ("model_swap_comparison.png", "Mission 4"),
    ("challenge_comparison.png",  "Mission 5"),
]
REQUIRED_METRICS = [
    ("val_metrics.json",           "Mission 2"),
    ("model_swap_comparison.json", "Mission 4"),
    ("challenge_comparison.json",  "Mission 5"),
]
REQUIRED_REPORTS = [
    ("env_check.md",        "Mission 0"),
    ("data_notes.md",       "Mission 2"),
    ("train_notes.md",      "Mission 2"),
    ("error_analysis.md",   "Mission 3"),
    ("model_swap.md",       "Mission 4"),
    ("day1_summary.md",     "Mission 4"),
    ("challenge_plan.md",   "Mission 5"),
    ("adapt_pipeline.md",   "Mission 5"),
    ("translation_memo.md", "Mission 6"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# ARCHIVE / RESET HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

# Files in reports/ that are student-generated runtime artifacts (safe to clear)
_GENERATED_REPORTS = [
    "env_check.md", "data_notes.md", "train_notes.md", "error_analysis.md",
    "model_swap.md", "day1_summary.md", "challenge_plan.md",
    "adapt_pipeline.md", "translation_memo.md",
]

# Subdirectory names under outputs/ to clear on reset
_OUTPUT_SUBDIRS = ["status", "figures", "metrics"]


def archive_current_session(state: dict) -> Path:
    """
    Write a timestamped snapshot of the current session state to
    .session_archives/. Returns the archive file path.
    This is a read-only metadata snapshot — no files are moved or deleted.
    """
    archive_dir = BASE / ".session_archives"
    archive_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    archive_path = archive_dir / f"session_{ts}.json"

    n_complete = len(state.get("completed_missions", []))
    snapshot = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "missions_completed": n_complete,
        "current_mission": state.get("current_mission", 0),
        "completed_missions": state.get("completed_missions", []),
        "student_state_snapshot": state,
        "artifacts_present": {
            "status_files":  [p.name for p in sorted((BASE / "outputs" / "status").glob("*.json")) if p.exists()],
            "figures":       [p.name for p in sorted((BASE / "outputs" / "figures").glob("*.png")) if p.exists()],
            "metric_files":  [p.name for p in sorted((BASE / "outputs" / "metrics").glob("*.json")) if p.exists()],
            "reports":       [r for r in _GENERATED_REPORTS if (BASE / "reports" / r).exists()],
        },
    }
    archive_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return archive_path


def do_full_reset(state: dict) -> dict:
    """
    Safe reset: archive current session state, then clear all student-generated
    runtime outputs. Does NOT touch scaffold, scripts, tests, prompts, or docs.
    Returns the fresh DEFAULT_STATE dict.
    """
    # 1. Archive first
    archive_current_session(state)

    # 2. Clear output subdirectories (keep the directories themselves)
    for subdir in _OUTPUT_SUBDIRS:
        d = BASE / "outputs" / subdir
        if d.exists():
            for f in d.iterdir():
                if f.is_file():
                    f.unlink()

    # 3. Clear generated report files
    for fname in _GENERATED_REPORTS:
        p = BASE / "reports" / fname
        if p.exists():
            p.unlink()

    # 4. Clear fetched imaging data (student must re-run Mission 1)
    imaging_dir = BASE / "data" / "sample" / "imaging"
    if imaging_dir.exists():
        for f in imaging_dir.iterdir():
            if f.is_file():
                f.unlink()

    # 5. Clear lab history if present
    lab_history = BASE / ".lab_history"
    if lab_history.exists():
        import shutil
        shutil.rmtree(lab_history, ignore_errors=True)

    # 6. Write fresh state
    fresh = dict(DEFAULT_STATE)
    save_student_state(fresh)
    return fresh


# ── Tutorial debug flag ───────────────────────────────────────────────────────
TUTORIAL_DEBUG = False

_TUTORIAL_STEPS: list[dict] = [
    {
        "title": "Welcome to the Medical AI Lab",
        "body": (
            "You are a junior clinical AI investigator. Over 7 missions you will build, "
            "evaluate, and translate a medical image segmentation prototype — using "
            "natural-language prompts to direct Claude throughout. This tour takes 2 minutes."
        ),
        "target": None,
    },
    {
        "title": "Your current mission",
        "body": (
            "The mission header shows where you are in the sequence. "
            "The blue number badge is your mission index. Stage pills below the title "
            "show which stages are done (green) and which are next (blue)."
        ),
        "target": "mission-header",
    },
    {
        "title": "The prompt is your instrument",
        "body": (
            "Copy the prompt block into VS Code, open Claude Code (run <code>claude</code> "
            "in the terminal), and paste. Claude will read the repo, write scripts, and produce "
            "the required artifacts. Better prompts &#8594; better experimental control."
        ),
        "target": "prompt-block",
    },
    {
        "title": "Artifacts appear here after running",
        "body": (
            "Figures, metrics, and status files appear in the Artifacts panel "
            "after Claude runs. Click <strong>&#8635; Refresh</strong> to re-scan outputs. "
            "The Results tab shows all artifacts across all missions."
        ),
        "target": "artifacts",
    },
    {
        "title": "Stage status is your ground truth",
        "body": (
            "Each stage has a status file. A green &#10003; means the file exists and is valid. "
            "Stage status is the authoritative check &#8212; not what Claude said in chat. "
            "Click a completed stage to preview its JSON."
        ),
        "target": "stage-status",
    },
    {
        "title": "Check progress from the sidebar",
        "body": (
            "When Claude finishes in VS Code, return here and click "
            "<strong>&#10003; I finished &#8212; check my progress</strong> in the sidebar. "
            "This verifies all required artifacts and advances you if everything passes."
        ),
        "target": "sidebar-button",
    },
    {
        "title": "Reflection unlocks after completion",
        "body": (
            "After all stages pass, the Reflection Prompt (Layer B) unlocks below the base prompt. "
            "It asks you to interpret your results more deeply. "
            "Layer C is an optional exploration challenge."
        ),
        "target": "reflection",
    },
]


def _build_tutorial_focus_js(target: str) -> str:
    """Build the minimal iframe HTML that applies CSS focus classes + scrollIntoView.

    This component does EXACTLY three things:
    1. Inject one <style> block into parent <head> (once, idempotent)
    2. Add 'tut-mode' to parent body, 'tut-focus' to the active target element
    3. Call scrollIntoView on the target if it is below the viewport fold

    It does NOT inject a card. It does NOT wire any buttons. It does NOT proxy any clicks.
    Tutorial navigation is 100% handled by native Streamlit buttons in render_tutorial_nav().
    """
    show_debug = "true" if TUTORIAL_DEBUG else "false"
    target_safe = target.replace("'", "\\'")

    return f"""<!DOCTYPE html>
<html><head><style>body{{margin:0;padding:0;overflow:hidden}}</style></head>
<body><script>
(function() {{
  var WIN = window.parent;
  var PDOC;
  try {{ PDOC = WIN.document; }}
  catch(e) {{
    document.body.textContent = 'ERR: ' + e;
    return;
  }}

  var TARGET   = '{target_safe}';
  var SHOW_DBG = {show_debug};

  function dbg(msg) {{
    if (!SHOW_DBG) return;
    var d = PDOC.getElementById('tut-js-dbg');
    if (!d) {{
      d = PDOC.createElement('div');
      d.id = 'tut-js-dbg';
      d.style.cssText = 'position:fixed;bottom:8px;right:360px;z-index:10001;'
        + 'background:#0d1117;color:#39d353;font-family:monospace;font-size:10px;'
        + 'padding:6px 10px;border:1px solid #39d353;border-radius:4px;'
        + 'max-width:320px;pointer-events:none;white-space:pre-wrap;';
      PDOC.body.appendChild(d);
    }}
    d.textContent = 'JS: tgt=' + (TARGET||'none') + '\\n' + msg;
  }}

  // ── Inject focus CSS once ─────────────────────────────────────────────────
  if (!PDOC.getElementById('tut-focus-style')) {{
    var st = PDOC.createElement('style');
    st.id  = 'tut-focus-style';
    st.textContent =
      'body.tut-mode [id^="tut-target-"]{{' +
        'opacity:0.35;transition:opacity .2s,box-shadow .2s}}' +
      'body.tut-mode [id^="tut-target-"].tut-focus{{' +
        'opacity:1!important;' +
        'outline:4px solid #F97316!important;outline-offset:5px!important;' +
        'border-radius:8px!important;background:#FFFFFF!important;' +
        'box-shadow:0 0 0 8px rgba(249,115,22,.15),0 4px 24px rgba(0,0,0,.07)!important}}';
    PDOC.head.appendChild(st);
    dbg('CSS injected');
  }}

  // ── Remove previous focus class, set new one ──────────────────────────────
  PDOC.body.classList.add('tut-mode');
  PDOC.querySelectorAll('.tut-focus').forEach(function(e) {{
    e.classList.remove('tut-focus');
  }});

  if (TARGET) {{
    var el = PDOC.getElementById('tut-target-' + TARGET);
    if (el) {{
      el.classList.add('tut-focus');
      var r = el.getBoundingClientRect();
      dbg('found  top=' + Math.round(r.top) + ' h=' + Math.round(r.height));
      if (r.top < 0 || r.bottom > WIN.innerHeight) {{
        el.scrollIntoView({{behavior:'smooth', block:'center'}});
        dbg('scrolled');
      }}
    }} else {{
      var ids = [];
      PDOC.querySelectorAll('[id^="tut-target-"]').forEach(function(e){{ids.push(e.id);}});
      dbg('NOT FOUND\\nexisting: ' + ids.join(', '));
    }}
  }}
}})();
</script></body></html>"""


def _clear_tutorial_focus_js() -> str:
    """Build the minimal iframe HTML that strips tut-mode / tut-focus from the parent DOM.

    Called when tutorial ends (Skip / Finish). Removes body class, focus class,
    and the JS debug panel.
    """
    return """<!DOCTYPE html>
<html><head><style>body{margin:0;padding:0;overflow:hidden}</style></head>
<body><script>
(function() {
  var PDOC;
  try { PDOC = window.parent.document; } catch(e) { return; }
  PDOC.body.classList.remove('tut-mode');
  PDOC.querySelectorAll('.tut-focus').forEach(function(e){ e.classList.remove('tut-focus'); });
  var d = PDOC.getElementById('tut-js-dbg');
  if (d) d.remove();
})();
</script></body></html>"""


def render_tutorial_nav(step: int) -> None:
    """Render the tutorial guide card with native Streamlit navigation controls.

    Architecture:
    - The card header/content is HTML via st.markdown (styling only)
    - Back / Next / Skip / Start Mission 0 are st.button() widgets
    - st.button() clicks directly mutate st.session_state and call st.rerun()
    - No hidden buttons, no JS click proxies, no DOM lookup for button text

    A tiny components.html() handles ONLY CSS focus classes + scrollIntoView.
    """
    import streamlit.components.v1 as components

    total   = len(_TUTORIAL_STEPS)
    is_last = step >= total - 1
    s       = _TUTORIAL_STEPS[min(step, total - 1)]
    target  = s.get("target") or ""
    pct     = int((step + 1) / total * 100)

    if TUTORIAL_DEBUG:
        st.caption(
            f"Tutorial debug: active=True  step={step}/{total-1}"
            f"  target={target or 'none'}  title={s['title'][:32]}"
        )

    # ── Guide card visual (HTML styling only — no interactive elements) ───────
    st.markdown(
        f'<div style="background:#FFFFFF;border:1.5px solid #2563EB;border-radius:14px;'
        f'padding:20px 22px 14px 22px;margin-bottom:10px;'
        f'box-shadow:0 4px 20px rgba(37,99,235,0.12),0 2px 8px rgba(0,0,0,0.06)">'

        # Step badge + pct
        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">'
        f'<span style="background:#EFF6FF;color:#1D4ED8;border-radius:20px;padding:3px 12px;'
        f'font-size:0.62rem;font-weight:700;letter-spacing:0.10em;text-transform:uppercase">'
        f'STEP {step + 1} / {total}</span>'
        f'<span style="font-size:0.68rem;color:#94A3B8;font-weight:500">{pct}%</span>'
        f'</div>'

        # Progress bar
        f'<div style="background:#E2E8F0;border-radius:4px;height:3px;margin-bottom:14px;overflow:hidden">'
        f'<div style="background:linear-gradient(90deg,#2563EB,#60A5FA);height:100%;'
        f'width:{pct}%;border-radius:4px"></div></div>'

        # Title
        f'<p style="font-size:0.96rem;font-weight:700;color:#0F172A;margin:0 0 8px 0;line-height:1.3">'
        f'{s["title"]}</p>'

        # Body
        f'<p style="font-size:0.83rem;color:#475569;line-height:1.65;margin:0">'
        f'{s["body"]}</p>'

        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Native Streamlit navigation buttons ───────────────────────────────────
    # Layout: [Back] [Skip] [Next →]  or  [Back] [Start Mission 0 →]
    if is_last:
        b_cols = st.columns([1, 2])
        with b_cols[0]:
            if step > 0:
                if st.button("← Back", key="tut_back", use_container_width=True):
                    st.session_state["tutorial_step"] = step - 1
                    st.rerun()
        with b_cols[1]:
            if st.button("Start Mission 0 →", key="tut_finish",
                         type="primary", use_container_width=True):
                st.session_state["tutorial_step"] = "done"
                st.session_state["entered_lab"]   = True
                # Remove CSS focus state via a one-shot JS component
                components.html(_clear_tutorial_focus_js(), height=0, scrolling=False)
                st.rerun()
    else:
        b_cols = st.columns([1, 1, 2])
        with b_cols[0]:
            if step > 0:
                if st.button("← Back", key="tut_back", use_container_width=True):
                    st.session_state["tutorial_step"] = step - 1
                    st.rerun()
        with b_cols[1]:
            if st.button("Skip", key="tut_skip", use_container_width=True):
                st.session_state["tutorial_step"] = "done"
                st.session_state["entered_lab"]   = True
                components.html(_clear_tutorial_focus_js(), height=0, scrolling=False)
                st.rerun()
        with b_cols[2]:
            if st.button("Next →", key="tut_next",
                         type="primary", use_container_width=True):
                st.session_state["tutorial_step"] = step + 1
                st.rerun()

    # ── Tiny JS: CSS focus classes + scrollIntoView only, no button wiring ────
    components.html(
        _build_tutorial_focus_js(target),
        height=1,
        scrolling=False,
    )


def attempt_git_checkpoint(mission_label: str) -> tuple[bool, str]:
    """Try to create a git checkpoint commit. Returns (success, message)."""
    try:
        # Check if we're in a git repo
        r = subprocess.run(
            ["git", "-C", str(BASE), "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode != 0:
            return False, "Not a git repository — skipping checkpoint commit."
        # Stage all outputs and reports
        subprocess.run(
            ["git", "-C", str(BASE), "add", "outputs/", "reports/", ".lab_history/"],
            capture_output=True, timeout=10,
        )
        # Check if there's anything staged
        status = subprocess.run(
            ["git", "-C", str(BASE), "diff", "--cached", "--name-only"],
            capture_output=True, text=True, timeout=5,
        )
        if not status.stdout.strip():
            return True, "Nothing new to commit — artifacts already checkpointed."
        slug = mission_label.split("—")[0].strip().lower().replace(" ", "-")
        msg  = f"checkpoint: {mission_label} complete"
        cr = subprocess.run(
            ["git", "-C", str(BASE), "commit", "-m", msg],
            capture_output=True, text=True, timeout=15,
        )
        if cr.returncode == 0:
            return True, f"Checkpoint commit created: {msg}"
        return False, f"Commit failed: {cr.stderr.strip()[:120]}"
    except Exception as e:
        return False, f"Git checkpoint error: {e}"


def run_mission_checkpoint(mission_idx: int, state: dict) -> dict:
    """
    Run all completion checks for a mission and return a checkpoint result dict.
    Keys: passed (bool), details (list of (ok, label) tuples), summary (str)
    """
    mission  = MISSIONS[mission_idx]
    details  = []

    # Stage status checks
    for stage in mission["stages"]:
        ok = stage_ok(stage)
        details.append((ok, f"Stage {stage} complete"))

    # Expected output checks
    for out in mission["expected_outputs"]:
        path = BASE / out
        ok   = path.exists() if not out.endswith("/") else path.is_dir()
        details.append((ok, f"Output exists: {out.split('/')[-1]}"))

    passed  = all(ok for ok, _ in details)
    summary = "All checks passed." if passed else f"{sum(not ok for ok, _ in details)} check(s) failed."
    return {"passed": passed, "details": details, "summary": summary, "mission_idx": mission_idx}


def render_checkpoint_panel(cp: dict) -> None:
    """Render the mission completion checkpoint panel (animated checks → rich result)."""
    phase      = cp.get("phase", "result")
    mission_idx = cp.get("mission_idx", 0)
    mission     = MISSIONS[mission_idx]

    if phase == "checking":
        # ── Animated item-by-item check sequence ────────────────────────────
        st.markdown(
            f'<div style="background:#EFF6FF;border:1.5px solid #93C5FD;border-radius:12px;'
            f'padding:20px 26px;margin:8px 0 16px 0">'
            f'<p style="font-size:1.0rem;font-weight:700;color:#1E40AF;margin:0 0 4px 0">'
            f'Checking {mission["label"]}…</p>'
            f'<p style="font-size:0.82rem;color:#3B82F6;margin:0">Verifying stages and output artifacts</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        check_items = (
            [(True, f"Stage: {s}") for s in mission["stages"]]
            + [(True, f"Output: {out.split('/')[-1]}") for out in mission["expected_outputs"]]
        )
        placeholder = st.empty()
        rendered    = []
        for i, (_, label) in enumerate(check_items):
            time.sleep(0.22)
            rendered.append(label)
            rows = "".join(
                f'<div style="font-size:0.83rem;color:#1D4ED8;margin:3px 0">'
                f'<span style="display:inline-block;width:18px;text-align:center">…</span> {lbl}</div>'
                for lbl in rendered
            )
            placeholder.markdown(f'<div style="padding:4px 0">{rows}</div>', unsafe_allow_html=True)
        placeholder.empty()
        result = run_mission_checkpoint(mission_idx, st.session_state.get("lab_state", {}))
        st.session_state["checkpoint"] = {**cp, "phase": "result", **result}
        st.rerun()

    else:
        # ── Result card ──────────────────────────────────────────────────────
        passed  = cp.get("passed", False)
        details = cp.get("details", [])
        state   = st.session_state.get("lab_state", {})

        if passed:
            st.markdown(
                f'<div class="checkpoint-panel">'
                f'<p class="checkpoint-title">Mission checkpoint passed ✓</p>'
                f'<p class="checkpoint-detail">{mission["goal"]}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            n_fail = sum(1 for ok, _ in details if not ok)
            st.markdown(
                f'<div class="checkpoint-panel fail">'
                f'<p class="checkpoint-title">Checkpoint — {n_fail} item(s) not yet complete</p>'
                f'<p class="checkpoint-detail">Complete the remaining stages and run the prompt again.</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # Item checklist
        rows_html = "".join(
            f'<div style="display:flex;align-items:center;gap:8px;padding:3px 0;font-size:0.82rem;color:{"#166534" if ok else "#94A3B8"}">'
            f'<span style="width:16px;text-align:center;font-weight:700">{"✓" if ok else "○"}</span>'
            f'<span>{label}</span></div>'
            for ok, label in details
        )
        st.markdown(f'<div style="margin:10px 0 14px 0">{rows_html}</div>', unsafe_allow_html=True)

        if passed:
            # ── Prompt principle recap ───────────────────────────────────────
            pp = mission.get("prompt_principle")
            tk = mission.get("takeaway")
            if pp:
                st.markdown(
                    f'<div class="prompt-principle-callout" style="margin-bottom:14px">'
                    f'<p class="prompt-principle-label">Prompt principle for this mission</p>'
                    f'<p class="prompt-principle-name">{pp}</p>'
                    + (f'<p class="prompt-principle-body">{tk}</p>' if tk else "")
                    + '</div>',
                    unsafe_allow_html=True,
                )

            # ── What was accomplished ────────────────────────────────────────
            bonus_prompt = mission.get("bonus_prompt")
            if bonus_prompt:
                with st.expander("Bonus challenge — go deeper", expanded=False):
                    st.markdown(f'*{bonus_prompt}*')

            # ── Next mission teaser ──────────────────────────────────────────
            next_idx = mission_idx + 1
            if next_idx < len(MISSIONS):
                next_m = MISSIONS[next_idx]
                st.markdown(
                    f'<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;'
                    f'padding:14px 18px;margin-bottom:16px">'
                    f'<p style="font-size:0.70rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#64748B;margin:0 0 4px 0">Up next</p>'
                    f'<p style="font-size:0.92rem;font-weight:600;color:#1E40AF;margin:0 0 4px 0">{next_m["label"]}</p>'
                    f'<p style="font-size:0.82rem;color:#475569;margin:0">{next_m["goal"]}</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # ── CTAs ─────────────────────────────────────────────────────────
            cta_l, cta_r = st.columns(2)
            with cta_l:
                if st.button(
                    f"Go to Mission {next_idx}  →" if next_idx < len(MISSIONS) else "View all results  →",
                    key="btn_cp_next", type="primary", use_container_width=True,
                ):
                    st.session_state["checkpoint"]        = None
                    st.session_state["viewing_mission_idx"] = None
                    st.rerun()
            with cta_r:
                if st.button("View reflection prompt", key="btn_cp_reflect", use_container_width=True):
                    st.session_state["checkpoint"] = None
                    # Reflection is in cockpit center for this mission — just close and show cockpit
                    st.session_state["viewing_mission_idx"] = mission_idx
                    st.rerun()

            # ── Git checkpoint ────────────────────────────────────────────────
            with st.expander("Create checkpoint commit (optional)", expanded=False):
                st.caption("Saves your current artifacts to git history.")
                if st.button("Create git checkpoint commit", key="btn_git_cp"):
                    git_ok, git_msg = attempt_git_checkpoint(mission["label"])
                    if git_ok:
                        st.success(git_msg)
                    else:
                        st.warning(git_msg)
        else:
            if st.button("Close and keep working", key="btn_close_cp", use_container_width=True):
                st.session_state["checkpoint"] = None
                st.rerun()


def render_session_archive_section() -> None:
    """Show archived sessions from .session_archives/ as expandable rows."""
    archive_dir = BASE / ".session_archives"
    if not archive_dir.exists():
        st.markdown('<p style="font-size:0.82rem;color:#64748B">No session archives yet.</p>', unsafe_allow_html=True)
        return
    archives = sorted(archive_dir.glob("session_*.json"), reverse=True)
    if not archives:
        st.markdown('<p style="font-size:0.82rem;color:#64748B">No session archives yet.</p>', unsafe_allow_html=True)
        return
    for path in archives[:10]:
        ts = path.stem.replace("session_", "").replace("_", " ", 1)
        data = load_json(path)
        label = ts
        if data and "state" in data:
            cur = data["state"].get("current_mission", "?")
            comp = len(data["state"].get("completed_missions", []))
            label = f"{ts}  —  Mission {cur}, {comp} completed"
        with st.expander(label):
            if data:
                st.json(data.get("state", data), expanded=False)
            else:
                st.markdown("_Could not parse archive file._")


# ═══════════════════════════════════════════════════════════════════════════════
# UI RENDERING
# ═══════════════════════════════════════════════════════════════════════════════

def render_sidebar_rail(state: dict) -> None:
    """Vertical mission progress rail in the sidebar."""
    for i, m in enumerate(MISSIONS):
        disp    = get_mission_display_status(i, state)
        parts   = m["label"].split("—")
        short   = parts[1].strip()[:20] if len(parts) > 1 else f"M{i}"
        is_last = (i == len(MISSIONS) - 1)

        if disp == "complete":
            dot_bg, dot_bd, dot_fg = "#DCFCE7", "#86EFAC", "#15803D"
            line_col, text_col     = "#86EFAC", "#166534"
            icon = "&#10003;"
        elif disp == "current":
            dot_bg, dot_bd, dot_fg = "#DBEAFE", "#93C5FD", "#1D4ED8"
            line_col, text_col     = "#BFDBFE", "#1E40AF"
            icon = str(i)
        elif disp == "unlocked":
            dot_bg, dot_bd, dot_fg = "#F1F5F9", "#E2E8F0", "#64748B"
            line_col, text_col     = "#E2E8F0", "#475569"
            icon = str(i)
        else:
            dot_bg, dot_bd, dot_fg = "#F8FAFC", "#E2E8F0", "#CBD5E1"
            line_col, text_col     = "#E2E8F0", "#94A3B8"
            icon = str(i)

        fw = "font-weight:600;" if disp == "current" else ""
        # Build connector as inline element to avoid blank-line breaks in Markdown parser
        conn = (
            f'<div style="width:2px;height:12px;background:{line_col};margin:2px auto 0 auto;border-radius:1px"></div>'
            if not is_last else ""
        )
        # Single-line HTML — no internal newlines, avoids Streamlit markdown parser breaking on blank lines
        html = (
            f'<div style="display:flex;align-items:flex-start;gap:9px;padding:2px 0">'
            f'<div style="display:flex;flex-direction:column;align-items:center;flex-shrink:0">'
            f'<div style="width:26px;height:26px;border-radius:50%;background:{dot_bg};border:1px solid {dot_bd};display:flex;align-items:center;justify-content:center;color:{dot_fg};font-size:0.68rem;font-weight:700">{icon}</div>'
            f'{conn}'
            f'</div>'
            f'<div style="font-size:0.78rem;color:{text_col};line-height:1.3;padding-top:5px;{fw}">{short}</div>'
            f'</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


def render_welcome_screen() -> None:
    """Full-screen welcome / onboarding."""
    st.markdown(
        """<div class="welcome-wrap">
          <div class="welcome-eyebrow">Medical AI + Agentic Coding Lab — Summer Session</div>
          <div class="welcome-title">Begin your<br>research mission sequence.</div>
          <div class="welcome-sub">
            You are a junior clinical AI investigator.<br>
            Over seven missions you will build, evaluate, and translate a medical image
            segmentation prototype — using AI-assisted research methods throughout.
          </div>
        </div>""",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    roles = [
        ("You operate",     "VS Code + Claude Code",
         "You direct the research. You copy prompts, judge outputs, and advance missions. "
         "Claude executes under your direction."),
        ("Claude builds",   "Code · Artifacts · Reports",
         "Claude writes scripts, runs analyses, generates figures and metrics, and drafts "
         "written summaries. You review and guide."),
        ("Dashboard shows", "Progress · Prompts · Results",
         "This console shows your current mission, the prompts to run, your artifacts, "
         "and whether you are ready to submit."),
    ]
    for col, (eyebrow, title, body) in zip([c1, c2, c3], roles):
        with col:
            st.markdown(
                f"""<div class="welcome-role-card">
                  <div class="welcome-role-eyebrow">{eyebrow}</div>
                  <div class="welcome-role-title">{title}</div>
                  <div class="welcome-role-body">{body}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="welcome-stats">'
        '7 missions<span>·</span>2 research days<span>·</span>'
        'real FLAIR imaging data<span>·</span>real metrics'
        '</div>',
        unsafe_allow_html=True,
    )

    _, cta, _ = st.columns([0.32, 0.36, 0.32])
    with cta:
        if st.button("Enter Lab Studio  →", type="primary", use_container_width=True):
            st.session_state["entered_lab"] = True
            st.rerun()
    st.write("")


def render_cockpit_center(mission: dict, cur_idx: int, state: dict) -> None:
    """Center panel: mission header + one-step prompt + run checklist + Layer B."""

    # ── Mission header ─────────────────────────────────────────────────────
    # id="tut-target-mission-header" is measured by the tutorial JS
    parts   = mission["label"].split("—")
    m_num   = parts[0].strip()
    m_title = parts[1].strip() if len(parts) > 1 else mission["label"]
    m_digit = m_num.replace("Mission ", "").strip()

    st.markdown(
        f'<div id="tut-target-mission-header" class="cockpit-mission-header">'
        f'<div class="cockpit-mission-eyebrow">Current Mission</div>'
        f'<div style="display:flex;align-items:center;gap:10px;margin:2px 0 4px 0">'
        f'<div class="mission-num-badge">{m_digit}</div>'
        f'<div class="cockpit-mission-title" style="margin:0">{m_title}</div>'
        f'</div>'
        f'<div class="cockpit-mission-goal">{mission["goal"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Stage pills ─────────────────────────────────────────────────────────
    pills = ""
    active_si = get_active_stage_idx(mission)
    for si, s in enumerate(mission["stages"]):
        ok  = stage_ok(s)
        cls = "stage-pill-done" if ok else ("stage-pill-active" if si == active_si else "stage-pill-pending")
        mk  = "✓" if ok else ("→" if si == active_si else "○")
        pills += f'<span class="stage-pill {cls}">{mk}&nbsp;{s}</span>'
    st.markdown(f'<div class="stage-pills">{pills}</div>', unsafe_allow_html=True)

    # ── Active stage prompt ─────────────────────────────────────────────────
    pfile    = mission["prompts"][active_si]
    make_cmd = mission["make_commands"][active_si] if active_si < len(mission["make_commands"]) else None
    content  = prompt_text(pfile)

    n_stages = len(mission["stages"])
    if n_stages > 1:
        completed_stages = sum(1 for s in mission["stages"] if stage_ok(s))
        st.markdown(
            f'<div class="prompt-multistage-hint">'
            f'Stage {active_si + 1} of {n_stages} &nbsp;·&nbsp; {completed_stages} complete</div>',
            unsafe_allow_html=True,
        )

    # id on the label marks the top of the prompt block for the tutorial JS
    st.markdown(
        f'<div id="tut-target-prompt-block" class="prompt-copy-label">Copy this into Claude Code</div>'
        f'<div class="prompt-file-tag">{pfile}</div>',
        unsafe_allow_html=True,
    )

    if content:
        layers = parse_prompt_layers(content)
        layer_a = layers.get("A", content)
        quote, ctx = extract_prompt_quote(layer_a)
        if quote:
            st.code(quote, language=None)
            if ctx:
                with st.expander("Full prompt context", expanded=False):
                    st.markdown(ctx)
        else:
            st.code(layer_a[:600] + ("..." if len(layer_a) > 600 else ""), language=None)
    else:
        st.warning(f"`prompts/{pfile}` not found.")

    # ── Prompt principle callout ────────────────────────────────────────────
    pp = mission.get("prompt_principle")
    tk = mission.get("takeaway")
    if pp:
        st.markdown(
            f'<div class="prompt-principle-callout">'
            f'<p class="prompt-principle-label">Prompt principle</p>'
            f'<p class="prompt-principle-name">{pp}</p>'
            + (f'<p class="prompt-principle-body">{tk}</p>' if tk else "")
            + '</div>',
            unsafe_allow_html=True,
        )

    # ── After-running checklist ─────────────────────────────────────────────
    cmd_str = f"<code>{make_cmd}</code>" if make_cmd else "the verification command"
    run_steps = [
        "Open VS Code in this repo and start Claude Code: type <code>claude</code>.",
        "Paste the prompt above. Press Enter and let Claude run.",
        f"When done, verify: {cmd_str} — check for errors.",
        "Return here → click <b>Refresh</b> in the sidebar to confirm completion.",
    ]
    steps_html = "".join(
        f'<div class="run-step">'
        f'<div class="run-step-num">{n}</div>'
        f'<div>{s}</div></div>'
        for n, s in enumerate(run_steps, 1)
    )
    st.markdown(
        f'<div class="run-section-label">After running</div>{steps_html}',
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Layer B — Reflection ────────────────────────────────────────────────
    # Use mission_stages_complete for real-time check (doesn't require state refresh)
    mission_done = mission_stages_complete(cur_idx) or (cur_idx in state["completed_missions"])

    # id="tut-target-reflection" on the lock/unlock div — measured by tutorial JS
    if not mission_done:
        st.markdown(
            '<div id="tut-target-reflection" class="layer-b-lock">'
            '<div class="layer-b-lock-icon">🔒</div>'
            '<div class="layer-b-lock-title">Reflection prompt locked</div>'
            '<div class="layer-b-lock-hint">Complete all stages for this mission to unlock the reflection prompt.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div id="tut-target-reflection" class="layer-b-open-label">Layer B — Reflection prompt</div>', unsafe_allow_html=True)
        for pf in mission["prompts"]:
            c = prompt_text(pf)
            if c:
                layers = parse_prompt_layers(c)
                if "B" in layers:
                    with st.container(border=True):
                        st.markdown(layers["B"])

    # ── Deep context (collapsed) ────────────────────────────────────────────
    with st.expander("Scientific context — purpose, why it matters, learning objectives", expanded=False):
        st.markdown(f"**Purpose:** {mission['purpose']}")
        st.write("")
        st.markdown(f"**Why it matters:** {mission['why_it_matters']}")
        st.write("")
        st.markdown(f"**What you are learning:** {mission['student_learns']}")

    # ── Layer C (collapsed) ─────────────────────────────────────────────────
    all_c: list[str] = []
    for pf in mission["prompts"]:
        c = prompt_text(pf)
        if c:
            layers = parse_prompt_layers(c)
            if "C" in layers:
                all_c.append(layers["C"])
    if all_c:
        with st.expander("Layer C — Customization (optional extension)", expanded=False):
            for c_text in all_c:
                st.markdown(c_text)

    # ── Bonus challenge (collapsed) ─────────────────────────────────────────
    bonus = mission.get("bonus_prompt")
    if bonus:
        with st.expander("Bonus challenge — go deeper", expanded=False):
            st.markdown(
                f'<div class="bonus-callout">'
                f'<p class="bonus-label">Bonus</p>'
                f'<p class="bonus-body">{bonus}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )


def render_cockpit_right(cur_idx: int, state: dict, result_code: str | None) -> None:
    """Right panel: completion feedback + artifact preview + stage status."""
    mission  = MISSIONS[cur_idx]
    preview  = MISSION_PREVIEW.get(cur_idx, {})

    # ── Completion / unlock card ─────────────────────────────────────────────
    if result_code and result_code.startswith("complete:"):
        parts    = result_code[len("complete:"):].split("|unlock:")
        comp_lbl = parts[0]
        unl_lbl  = parts[1] if len(parts) > 1 else ""
        st.markdown(
            f"""<div class="unlock-card">
              <div class="unlock-card-top">Mission complete</div>
              <div class="unlock-card-title">{comp_lbl}</div>
              {"<div class='unlock-card-next'>Unlocked → <b>" + unl_lbl + "</b></div>" if unl_lbl else ""}
            </div>""",
            unsafe_allow_html=True,
        )
    elif result_code and result_code.startswith("allcomplete:"):
        st.markdown(
            """<div class="all-done-banner">
              <div class="all-done-icon">✓</div>
              <div class="all-done-title">Lab complete</div>
              <div class="all-done-sub">All missions finished.<br>Push to submit.</div>
            </div>""",
            unsafe_allow_html=True,
        )

    # ── Artifact preview ─────────────────────────────────────────────────────
    # id="tut-target-artifacts" marks the section label for the tutorial JS
    art_col, ref_col = st.columns([3, 1])
    with art_col:
        st.markdown('<div id="tut-target-artifacts" class="artifact-panel-label">Artifacts</div>', unsafe_allow_html=True)
    with ref_col:
        if st.button("⟳ Refresh", key="btn_artifact_refresh", help="Re-scan outputs for new artifacts"):
            st.rerun()

    fig_file    = preview.get("figure")
    metric_info = preview.get("metric")         # (filename, key, label)
    stat_stage  = preview.get("status_stage")
    report_file = preview.get("report")

    has_content = False

    # Figure
    if fig_file and fig_exists(fig_file):
        st.image(
            str(BASE / "outputs" / "figures" / fig_file),
            use_container_width=True,
        )
        has_content = True

    # Metric card
    if metric_info:
        mfile, mkey, mlabel = metric_info
        data = load_json(BASE / "outputs" / "metrics" / mfile)
        if data and mkey in data:
            val = data[mkey]
            val_str = f"{val:.3f}" if isinstance(val, float) else str(val)
            st.markdown(
                f"""<div class="metric-snippet">
                  <div class="metric-snippet-label">{mlabel}</div>
                  <div class="metric-snippet-value">{val_str}</div>
                  <div class="metric-snippet-sub">{mfile}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            has_content = True

    # Status JSON (missions 0, 1)
    if stat_stage and stage_ok(stat_stage):
        data = load_json(BASE / "outputs" / "status" / f"{stat_stage}.json")
        if data:
            has_content = True
            with st.expander("Status file", expanded=True):
                st.json({k: v for k, v in list(data.items())[:6]})

    # Report excerpt (mission 6)
    if report_file:
        content = report_text(report_file)
        if content and content.strip():
            has_content = True
            with st.expander("Report excerpt", expanded=True):
                st.markdown(content[:500] + ("…" if len(content) > 500 else ""))

    # Empty state
    if not has_content:
        st.markdown(
            """<div class="artifact-empty">
              <div class="artifact-empty-icon">○</div>
              <div class="artifact-empty-title">No artifacts yet</div>
              <div class="artifact-empty-hint">
                Run the prompt in VS Code + Claude Code,<br>
                then click Refresh to check for outputs.
              </div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Stage status ─────────────────────────────────────────────────────────
    # id="tut-target-stage-status" marks this section for the tutorial JS
    st.markdown('<div id="tut-target-stage-status" class="artifact-panel-label">Stage status</div>', unsafe_allow_html=True)
    for s in mission["stages"]:
        ok    = stage_ok(s)
        color = "#15803D" if ok else "#94A3B8"
        bg    = "#F0FDF4" if ok else "#F8FAFC"
        bd    = "#BBF7D0" if ok else "#E2E8F0"
        mark  = "✓" if ok else "○"
        status_data = load_json(BASE / "outputs" / "status" / f"{s}.json") if ok else None
        if ok and status_data:
            with st.expander(f"{mark} {s}", expanded=False):
                st.json({k: v for k, v in list(status_data.items())[:8]})
        else:
            st.markdown(
                f'<div style="font-size:0.80rem;font-family:monospace;color:{color};'
                f'background:{bg};border:1px solid {bd};border-radius:5px;'
                f'padding:4px 10px;margin-bottom:5px">{mark}&nbsp;{s}</div>',
                unsafe_allow_html=True,
            )

    # ── File constraints (collapsed) ─────────────────────────────────────────
    with st.expander("Allowed / protected files", expanded=False):
        st.markdown("**Allowed to edit**")
        for f in mission["allowed_files"]:
            st.markdown(
                f'<span style="font-size:0.80rem;font-family:monospace;'
                f'color:#15803D;background:#F0FDF4;border-radius:3px;'
                f'padding:1px 5px">• {f}</span>',
                unsafe_allow_html=True,
            )
        st.write("")
        st.markdown("**Protected**")
        for f in mission["protected_files"]:
            st.markdown(
                f'<span style="font-size:0.80rem;font-family:monospace;'
                f'color:#B91C1C;background:#FEF2F2;border-radius:3px;'
                f'padding:1px 5px">• {f}</span>',
                unsafe_allow_html=True,
            )

# ═══════════════════════════════════════════════════════════════════════════════
# BOOTSTRAP
# ═══════════════════════════════════════════════════════════════════════════════

init_session_state()
inject_css()
state: dict = st.session_state["lab_state"]

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    n_complete = len(state["completed_missions"])
    n_total    = len(MISSIONS)

    # ── Lab header + progress bar ─────────────────────────────────────────────
    pct = int(n_complete / n_total * 100)
    st.markdown(
        f'<div style="padding:8px 0 14px 0">'
        f'<div style="font-size:0.62rem;font-weight:700;letter-spacing:0.20em;text-transform:uppercase;color:#64748B;margin-bottom:4px">Medical AI Lab</div>'
        f'<div style="font-size:0.95rem;font-weight:700;color:#1E40AF;margin-bottom:16px;letter-spacing:-0.01em">Mission Console</div>'
        f'<div style="background:#D6DFEA;border-radius:4px;height:5px;margin-bottom:8px;overflow:hidden">'
        f'<div style="background:linear-gradient(90deg,#1E40AF,#3B82F6);height:100%;width:{pct}%;border-radius:4px;transition:width 0.5s ease"></div>'
        f'</div>'
        f'<div style="font-size:0.74rem;color:#475569;font-weight:500">{n_complete} of {n_total} missions complete</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if state["last_checked"]:
        try:
            ts = datetime.fromisoformat(state["last_checked"])
            st.markdown(
                f'<div style="font-size:0.68rem;color:#64748B;margin-bottom:10px">Last checked {ts.strftime("%Y-%m-%d %H:%M")} UTC</div>',
                unsafe_allow_html=True,
            )
        except Exception:
            pass

    st.divider()

    # ── PRIMARY ACTION — used after every mission ─────────────────────────────
    # id="tut-target-sidebar-button" is measured by the tutorial JS for spotlight
    st.markdown(
        '<div id="tut-target-sidebar-button">'
        '<div style="font-size:0.68rem;color:#475569;margin-bottom:6px;line-height:1.45">'
        'After finishing a mission in VS Code + Claude Code, click here to record your progress.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    if st.button("✓  I finished — check my progress", use_container_width=True, type="primary"):
        cur_mission_idx = min(state["current_mission"], len(MISSIONS) - 1)
        st.session_state["checkpoint"] = {"phase": "checking", "mission_idx": cur_mission_idx}
        st.session_state["reset_phase"] = 0
        st.rerun()

    st.divider()

    # ── ADVANCED TOOLS (collapsed by default) ────────────────────────────────
    with st.expander("Advanced tools", expanded=False):
        st.markdown(
            '<div style="font-size:0.74rem;color:#475569;margin-bottom:10px;line-height:1.5">'
            'These tools are for recovery only. You do not need them for normal lab work.</div>',
            unsafe_allow_html=True,
        )

        # Rebuild
        st.markdown(
            '<div style="font-size:0.72rem;color:#374151;font-weight:600;margin-bottom:3px">Rebuild progress from files on disk</div>'
            '<div style="font-size:0.70rem;color:#475569;margin-bottom:6px;line-height:1.4">'
            'Use if the dashboard lost track of which missions you completed.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Rebuild from saved artifacts", use_container_width=True):
            new_state = rebuild_state_from_artifacts()
            save_student_state(new_state)
            st.session_state["lab_state"]           = new_state
            n_det = len(new_state["completed_missions"])
            st.session_state["last_refresh_result"] = f"rebuilt:{n_det}"
            st.session_state["reset_phase"]         = 0
            st.rerun()

        st.write("")

        # Archive + full reset — 3-phase confirmation
        st.markdown(
            '<div style="font-size:0.72rem;color:#7A3A2A;font-weight:600;margin-bottom:3px">Archive and reset to Mission 0</div>'
            '<div style="font-size:0.70rem;color:#6A3020;margin-bottom:6px;line-height:1.4">'
            'Clears all generated outputs and restarts from the beginning. '
            'Your current work is archived in <code>.session_archives/</code> before anything is deleted.</div>',
            unsafe_allow_html=True,
        )

        phase = st.session_state.get("reset_phase", 0)
        if phase == 0:
            if st.button("Archive & reset to Mission 0", use_container_width=True):
                st.session_state["reset_phase"] = 1
                st.rerun()
        elif phase == 1:
            st.markdown(
                '<div style="font-size:0.74rem;color:#7A3A2A;background:#FEF2F2;border:1px solid #FECACA;'
                'border-radius:6px;padding:8px 10px;margin-bottom:8px;line-height:1.5">'
                'This will delete all generated outputs, reports, and fetched data from this session. '
                'A backup snapshot will be saved first. This cannot be undone through the dashboard.</div>',
                unsafe_allow_html=True,
            )
            r1, r2 = st.columns(2)
            if r1.button("Confirm reset", use_container_width=True):
                fresh = do_full_reset(st.session_state["lab_state"])
                st.session_state["lab_state"]           = fresh
                st.session_state["entered_lab"]         = False
                st.session_state["last_refresh_result"] = "reset:"
                st.session_state["reset_phase"]         = 0
                st.rerun()
            if r2.button("Cancel", use_container_width=True):
                st.session_state["reset_phase"] = 0
                st.rerun()

    st.divider()

    # ── Mission rail ──────────────────────────────────────────────────────────
    st.markdown(
        '<div style="font-size:0.62rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#64748B;margin-bottom:10px">Missions</div>',
        unsafe_allow_html=True,
    )
    render_sidebar_rail(st.session_state["lab_state"])

# ── Page header ────────────────────────────────────────────────────────────────

state = st.session_state["lab_state"]
result_code = st.session_state.get("last_refresh_result")

st.markdown(
    '<div style="display:flex;align-items:baseline;gap:14px;padding:4px 0 8px 0">'
    '<span style="font-size:1.25rem;font-weight:700;color:#0F172A;letter-spacing:-0.02em">Medical AI Lab</span>'
    '<span style="font-size:0.74rem;color:#94A3B8;font-weight:600;letter-spacing:0.06em;text-transform:uppercase">Mission Cockpit</span>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Notification strips ───────────────────────────────────────────────────────

if result_code:
    if result_code.startswith("missing:"):
        missing_list = result_code[len("missing:"):]
        pills_html = " ".join(
            f'<code style="background:rgba(0,0,0,0.06);color:#92400E;'
            f'padding:2px 6px;border-radius:4px;font-size:0.80rem">{s}.json</code>'
            for s in missing_list.split(",") if s
        )
        st.markdown(
            f'<div class="notif notif-warn">Artifacts not yet detected — still waiting for {pills_html}</div>',
            unsafe_allow_html=True,
        )
    elif result_code.startswith("rebuilt:"):
        n_det = result_code[len("rebuilt:"):]
        st.markdown(
            f'<div class="notif notif-rebuilt">Progress rebuilt from disk. '
            f'{n_det} mission(s) detected as complete.</div>',
            unsafe_allow_html=True,
        )
    elif result_code.startswith("reset:"):
        st.markdown(
            '<div class="notif notif-reset">Session archived and reset to Mission 0. Your previous work is saved in <code>.session_archives/</code>.</div>',
            unsafe_allow_html=True,
        )
    # completion notifications are rendered inside the cockpit right panel

st.divider()

# ── Tabs ───────────────────────────────────────────────────────────────────────

tab_cockpit, tab_map, tab_results, tab_reports, tab_eval, tab_prompts = st.tabs([
    "▶  Lab Cockpit",
    "Mission Map",
    "Results",
    "Reports",
    "Evaluation",
    "Prompt Archive",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — LAB COCKPIT
# ═══════════════════════════════════════════════════════════════════════════════

with tab_cockpit:
    state    = st.session_state["lab_state"]
    cur_idx  = min(state["current_mission"], len(MISSIONS) - 1)
    all_done = (len(state["completed_missions"]) == len(MISSIONS))

    # ── Checkpoint mode — replaces cockpit with animated checkpoint panel ────
    checkpoint    = st.session_state.get("checkpoint")
    in_checkpoint = checkpoint is not None

    if in_checkpoint:
        view_idx = checkpoint.get("mission_idx", cur_idx)
        st.markdown(
            f'<div style="font-size:0.90rem;font-weight:600;color:#1E40AF;margin-bottom:12px">'
            f'Checking: {MISSIONS[view_idx]["label"]}</div>',
            unsafe_allow_html=True,
        )
        render_checkpoint_panel(checkpoint)
        # After checkpoint passes, also propagate state advancement
        if checkpoint.get("phase") == "result" and checkpoint.get("passed"):
            new_state, code = do_refresh_current_mission(state)
            if new_state != state:
                save_student_state(new_state)
                st.session_state["lab_state"]           = new_state
                st.session_state["last_refresh_result"] = code

    if not in_checkpoint:
        # ── Revisit mode — show a completed mission instead of current ───────
        view_idx_override = st.session_state.get("viewing_mission_idx")
        if view_idx_override is not None:
            view_state = get_mission_display_status(view_idx_override, state)
            if view_state not in ("complete", "current", "unlocked"):
                st.session_state["viewing_mission_idx"] = None
                view_idx_override = None
            else:
                st.markdown(
                    f'<div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;'
                    f'padding:8px 14px;margin-bottom:12px">'
                    f'<span style="font-size:0.83rem;color:#1E40AF;font-weight:600">'
                    f'Revisiting: {MISSIONS[view_idx_override]["label"]}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                back_col, _ = st.columns([0.22, 0.78])
                with back_col:
                    if st.button("← Back to current", key="btn_back_current"):
                        st.session_state["viewing_mission_idx"] = None
                        st.rerun()

        display_idx = view_idx_override if view_idx_override is not None else cur_idx
        mission = MISSIONS[display_idx]

        show_welcome = (
            not st.session_state.get("entered_lab", False) and
            len(state["completed_missions"]) == 0 and
            cur_idx == 0
        )

        # ── Welcome / onboarding ──────────────────────────────────────────────
        if show_welcome:
            render_welcome_screen()

        # ── Tutorial — auto-starts when entering lab for the first time ───────
        elif (
            st.session_state.get("entered_lab", False)
            and st.session_state.get("tutorial_step") is None
            and cur_idx == 0
            and len(state["completed_missions"]) == 0
            and view_idx_override is None
        ):
            # Auto-start tutorial on first lab entry
            st.session_state["tutorial_step"] = 0
            st.rerun()

        # ── All-done banner ───────────────────────────────────────────────────
        elif all_done and mission_stages_complete(cur_idx) and view_idx_override is None:
            st.markdown(
                '<div class="all-done-banner">'
                '<div class="all-done-icon">✓</div>'
                '<div class="all-done-title">Lab complete — all missions finished</div>'
                '<div class="all-done-sub">Review your artifacts in the Results and Reports tabs, then push to submit.</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        tutorial_step_val = st.session_state.get("tutorial_step")

        # ── Cockpit (2-column) ────────────────────────────────────────────────
        if not show_welcome:
            # ── Tutorial card — rendered at TOP so always visible ─────────────
            # Native st.button() controls mutate session state directly.
            # JS component below only handles CSS focus classes + scrollIntoView.
            if isinstance(tutorial_step_val, int) and not in_checkpoint:
                render_tutorial_nav(tutorial_step_val)

            col_center, col_right = st.columns([0.63, 0.37])

            with col_center:
                render_cockpit_center(mission, display_idx, state)

            with col_right:
                render_cockpit_right(display_idx, state, result_code if view_idx_override is None else None)

            # Clear result after rendering
            if result_code and not result_code.startswith("missing:"):
                st.session_state["last_refresh_result"] = None

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MISSION MAP
# ═══════════════════════════════════════════════════════════════════════════════

with tab_map:
    state = st.session_state["lab_state"]

    hdr_col, restart_col = st.columns([0.75, 0.25])
    with hdr_col:
        st.markdown(
            '<div style="font-size:1.05rem;font-weight:700;color:#0F172A;margin-bottom:4px">'
            'Mission Map</div>'
            '<div style="font-size:0.88rem;color:#64748B;margin-bottom:18px">'
            'Complete missions in order — each unlocks the next.</div>',
            unsafe_allow_html=True,
        )
    with restart_col:
        st.write("")
        if st.button("↺ Restart tutorial", key="btn_restart_tutorial", help="Restart the Mission 0 guided tutorial"):
            st.session_state["tutorial_step"] = 0
            st.rerun()

    for i, m in enumerate(MISSIONS):
        disp      = get_mission_display_status(i, state)
        chip_text = {"complete":"Complete","current":"Current","unlocked":"Unlocked","locked":"Locked"}[disp]

        st.markdown(
            f"""<div class="mmap-row {disp}">
              <div class="mmap-dot {disp}">{("✓" if disp=="complete" else str(i))}</div>
              <div style="flex:1;min-width:0">
                <div class="mmap-title {disp}">{m['label']}</div>
                <div class="mmap-goal">{m['goal']}</div>
              </div>
              <span class="chip chip-{disp}">{chip_text}</span>
            </div>""",
            unsafe_allow_html=True,
        )

        if disp != "locked":
            exp_col, btn_col = st.columns([0.78, 0.22])
            with exp_col:
                with st.expander("Context + stage detail", expanded=False):
                    st.markdown(f"**Purpose:** {m['purpose']}")
                    st.markdown(f"**Why it matters:** {m['why_it_matters']}")
                    st.markdown(f"**Learning:** {m['student_learns']}")
                    st.write("")
                    for s in m["stages"]:
                        ok    = stage_ok(s)
                        color = "#15803D" if ok else "#64748B"
                        bg    = "#F0FDF4" if ok else "#F8FAFC"
                        mark  = "✓" if ok else "○"
                        st.markdown(
                            f'<span style="font-family:monospace;font-size:0.82rem;'
                            f'color:{color};background:{bg};border-radius:4px;'
                            f'padding:2px 7px">{mark}&nbsp;{s}.json</span>',
                            unsafe_allow_html=True,
                        )
            with btn_col:
                if disp == "complete":
                    if st.button("Revisit", key=f"revisit_{i}", help=f"View {m['label']} in Lab Cockpit"):
                        st.session_state["viewing_mission_idx"] = i
                        st.rerun()
        st.write("")

    st.divider()
    st.metric("Missions complete", f"{len(state['completed_missions'])} / {len(MISSIONS)}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

with tab_results:
    st.markdown(
        '<div style="font-size:1.05rem;font-weight:700;color:#0F172A;margin-bottom:14px">'
        'Results</div>',
        unsafe_allow_html=True,
    )

    val_m  = load_json(BASE / "outputs" / "metrics" / "val_metrics.json")
    swap_m = load_json(BASE / "outputs" / "metrics" / "model_swap_comparison.json")
    chal_m = load_json(BASE / "outputs" / "metrics" / "challenge_comparison.json")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Baseline Dice (M2)",    f"{val_m['dice']:.3f}"      if val_m  and "dice"    in val_m  else "—")
    with c2:
        dlt = swap_m.get("delta") if swap_m else None
        st.metric("After model swap (M4)", f"{swap_m['new_dice']:.3f}" if swap_m and "new_dice" in swap_m else "—",
                  delta=f"{dlt:+.3f}" if isinstance(dlt, float) else None)
    with c3:
        dlt = chal_m.get("delta") if chal_m else None
        st.metric("Day 2 adaptation (M5)", f"{chal_m['new_dice']:.3f}" if chal_m and "new_dice" in chal_m else "—",
                  delta=f"{dlt:+.3f}" if isinstance(dlt, float) else None)

    st.divider()
    st.markdown(
        '<div style="font-size:0.80rem;font-weight:700;color:#475569;'
        'letter-spacing:0.10em;text-transform:uppercase;margin-bottom:12px">Figures</div>',
        unsafe_allow_html=True,
    )
    fig_paths = sorted((BASE / "outputs" / "figures").glob("*.png"))
    if not fig_paths:
        st.markdown(
            '<div style="font-size:0.88rem;color:#94A3B8;padding:8px 0">'
            'No figures yet. Run Mission 2 to produce the first visualization.</div>',
            unsafe_allow_html=True,
        )
    else:
        for i in range(0, len(fig_paths), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(fig_paths):
                    p = fig_paths[i + j]
                    with col:
                        st.image(str(p), caption=p.stem.replace("_", " "), use_container_width=True)

    st.divider()
    with st.expander("Raw stage status (JSON)", expanded=False):
        for p in sorted((BASE / "outputs" / "status").glob("*.json")):
            d = load_json(p)
            if d:
                st.markdown(f"**{p.name}**")
                st.json(d)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — REPORTS
# ═══════════════════════════════════════════════════════════════════════════════

with tab_reports:
    st.markdown(
        '<div style="font-size:1.05rem;font-weight:700;color:#0F172A;margin-bottom:4px">'
        'Reports</div>'
        '<div style="font-size:0.88rem;color:#64748B;margin-bottom:16px">'
        'Written summaries produced by you and Claude during each mission.</div>',
        unsafe_allow_html=True,
    )
    report_files = [
        ("Day 1 Summary",       "day1_summary.md"),
        ("Translation Memo",    "translation_memo.md"),
        ("Error Analysis",      "error_analysis.md"),
        ("Model Swap",          "model_swap.md"),
        ("Challenge Plan",      "challenge_plan.md"),
        ("Pipeline Adaptation", "adapt_pipeline.md"),
        ("Training Notes",      "train_notes.md"),
        ("Data Notes",          "data_notes.md"),
        ("Environment Check",   "env_check.md"),
    ]
    any_report = False
    for name, fname in report_files:
        content = report_text(fname)
        if content and content.strip():
            any_report = True
            with st.expander(name, expanded=False):
                st.markdown(content)
    if not any_report:
        st.markdown(
            '<div style="font-size:0.88rem;color:#94A3B8;padding:8px 0">'
            'No reports yet. Reports appear here as you complete missions.</div>',
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════

with tab_eval:
    st.markdown(
        '<div style="font-size:1.05rem;font-weight:700;color:#0F172A;margin-bottom:4px">'
        'Evaluation</div>'
        '<div style="font-size:0.88rem;color:#64748B;margin-bottom:16px">'
        'Mirrors the autograding CI tests. Run <code>make test</code> locally for the same result.</div>',
        unsafe_allow_html=True,
    )

    def artifact_row(label: str, present: bool, tag: str) -> None:
        ic = "✅" if present else "⬜"
        c1, c2, c3 = st.columns([0.05, 0.65, 0.22])
        c1.write(ic)
        c2.write(label)
        c3.caption(tag)

    st.markdown(
        '<div style="font-size:0.80rem;font-weight:700;color:#475569;'
        'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px">Stage status files</div>',
        unsafe_allow_html=True,
    )
    for fname, tag in REQUIRED_STATUS:
        artifact_row(f"`outputs/status/{fname}`", stage_ok(fname.replace(".json", "")), tag)

    st.write("")
    st.markdown(
        '<div style="font-size:0.80rem;font-weight:700;color:#475569;'
        'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px">Figures</div>',
        unsafe_allow_html=True,
    )
    for fname, tag in REQUIRED_FIGURES:
        artifact_row(f"`outputs/figures/{fname}`", fig_exists(fname), tag)

    st.write("")
    st.markdown(
        '<div style="font-size:0.80rem;font-weight:700;color:#475569;'
        'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px">Metrics</div>',
        unsafe_allow_html=True,
    )
    for fname, tag in REQUIRED_METRICS:
        artifact_row(f"`outputs/metrics/{fname}`", metric_exists(fname), tag)

    st.write("")
    st.markdown(
        '<div style="font-size:0.80rem;font-weight:700;color:#475569;'
        'letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px">Reports</div>',
        unsafe_allow_html=True,
    )
    for fname, tag in REQUIRED_REPORTS:
        c = report_text(fname)
        artifact_row(f"`reports/{fname}`", bool(c and len(c.strip()) > 50), tag)

    st.divider()
    all_checks = (
        [stage_ok(f.replace(".json","")) for f,_ in REQUIRED_STATUS]
        + [fig_exists(f)    for f,_ in REQUIRED_FIGURES]
        + [metric_exists(f) for f,_ in REQUIRED_METRICS]
        + [bool(report_text(f) and len((report_text(f) or "").strip()) > 50) for f,_ in REQUIRED_REPORTS]
    )
    n_pass = sum(all_checks)
    n_tot  = len(all_checks)
    if n_pass == n_tot:
        st.success(f"All {n_tot} artifacts present — ready to push.")
    else:
        st.warning(f"{n_pass} / {n_tot} artifacts present. Complete remaining missions before your final push.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — PROMPT ARCHIVE
# ═══════════════════════════════════════════════════════════════════════════════

with tab_prompts:
    st.markdown(
        '<div style="font-size:1.05rem;font-weight:700;color:#0F172A;margin-bottom:4px">'
        'Prompt Archive</div>'
        '<div style="font-size:0.88rem;color:#64748B;margin-bottom:16px">'
        'Read-only reference. Prompts are run in VS Code + Claude Code, not here. '
        'The Lab Cockpit tab shows the active prompt in context.</div>',
        unsafe_allow_html=True,
    )

    for mi, m in enumerate(MISSIONS):
        disp = get_mission_display_status(mi, state)
        parts   = m["label"].split("—")
        m_digit = parts[0].strip().replace("Mission ", "").strip()
        m_title = parts[1].strip() if len(parts) > 1 else m["label"]
        status_badge = {"complete": "✓ Complete", "current": "→ Current", "unlocked": "Unlocked", "locked": "Locked"}[disp]
        badge_color  = {"complete": "#166534", "current": "#1E40AF", "unlocked": "#475569", "locked": "#94A3B8"}[disp]
        header_html = (
            f'<div style="display:flex;align-items:center;gap:10px">'
            f'<div class="mission-num-badge" style="width:26px;height:26px;font-size:0.80rem">{m_digit}</div>'
            f'<span style="font-weight:600;color:#0F172A">{m_title}</span>'
            f'<span style="font-size:0.75rem;font-weight:600;color:{badge_color};margin-left:4px">{status_badge}</span>'
            f'</div>'
        )

        with st.expander(m["label"], expanded=(disp == "current")):
            st.markdown(header_html, unsafe_allow_html=True)
            pp = m.get("prompt_principle")
            tk = m.get("takeaway")
            if pp:
                st.markdown(
                    f'<div class="prompt-principle-callout">'
                    f'<p class="prompt-principle-label">Prompt principle</p>'
                    f'<p class="prompt-principle-name">{pp}</p>'
                    + (f'<p class="prompt-principle-body">{tk}</p>' if tk else "")
                    + '</div>',
                    unsafe_allow_html=True,
                )
            st.write("")
            for pf in m["prompts"]:
                content = prompt_text(pf)
                if not content:
                    st.caption(f"`prompts/{pf}` — not found")
                    continue
                layers = parse_prompt_layers(content)
                st.markdown(f'<span style="font-size:0.75rem;font-family:monospace;color:#64748B">{pf}</span>', unsafe_allow_html=True)
                if layers:
                    if "A" in layers:
                        st.markdown("**Layer A — Base prompt**")
                        st.caption("Run in VS Code + Claude Code to start the mission.")
                        quote, ctx = extract_prompt_quote(layers["A"])
                        if quote:
                            st.code(quote, language=None)
                            if ctx:
                                with st.expander("Full context", expanded=False):
                                    st.markdown(ctx)
                        else:
                            st.code(layers["A"][:500] + ("..." if len(layers["A"]) > 500 else ""), language=None)
                    if "B" in layers:
                        st.write("")
                        st.markdown("**Layer B — Reflection prompt**")
                        st.caption("Run after completing Layer A and reviewing the artifacts.")
                        with st.container(border=True):
                            st.markdown(layers["B"])
                    if "C" in layers:
                        st.write("")
                        with st.expander("Layer C — Customization (optional)", expanded=False):
                            st.markdown(layers["C"])
                else:
                    st.code(content[:500] + ("..." if len(content) > 500 else ""), language=None)
                st.write("")

    st.divider()
    st.markdown(
        '<div style="font-size:0.90rem;font-weight:700;color:#0F172A;margin-bottom:10px">Session Archives</div>'
        '<div style="font-size:0.82rem;color:#64748B;margin-bottom:10px">Snapshots saved when you ran Archive & Reset.</div>',
        unsafe_allow_html=True,
    )
    render_session_archive_section()

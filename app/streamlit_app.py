from pathlib import Path
import json
import streamlit as st
BASE = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="Medical AI Lab", layout="wide")
st.title("Medical AI + Agentic Coding Lab")
st.header("Stage status")
status_dir = BASE / "outputs" / "status"
status_files = sorted(status_dir.glob("*.json"))
if not status_files:
    st.info("No stage status files found yet. Run the lab steps first.")
else:
    for p in status_files:
        st.json(json.loads(p.read_text()))
st.header("Figures")
fig_dir = BASE / "outputs" / "figures"
figs = list(fig_dir.glob("*.png"))
if figs:
    for f in figs:
        st.image(str(f), caption=f.name)
else:
    st.info("No figures yet.")
st.header("Metrics")
metric_file = BASE / "outputs" / "metrics" / "val_metrics.json"
if metric_file.exists():
    st.json(json.loads(metric_file.read_text()))
else:
    st.info("No metrics yet.")

"""
Student Lab OS — Mission Dashboard
Navigation and feedback console for the Medical AI + Agentic Coding lab.

This dashboard is for orientation, artifact inspection, and submission readiness.
Claude interaction happens in VS Code + Claude Code, not here.
"""

from pathlib import Path
import json
import re
import streamlit as st

# ── Repo root ─────────────────────────────────────────────────────────────────

BASE = Path(__file__).resolve().parents[1]

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Medical AI Lab — Mission Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
    """Extract Layer A, B, C sections from a structured prompt file."""
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
            # Hit the next top-level section — close current layer
            layers[current_key] = "\n".join(current_lines).strip()
            current_key = None
            current_lines = []
        elif current_key is not None:
            current_lines.append(line)

    if current_key and current_lines:
        layers[current_key] = "\n".join(current_lines).strip()

    return layers

# ── Mission definitions ───────────────────────────────────────────────────────

MISSIONS = [
    {
        "label": "Mission 0 — Wake the Lab",
        "goal": "Environment setup and first prompt-driven success.",
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
        "stages": ["stage_00_bootstrap"],
        "prompts": ["stage_00_bootstrap.md"],
        "reports": ["env_check.md"],
    },
    {
        "label": "Mission 1 — Receive the Signal",
        "goal": "Fetch the teaching pack and confirm the dataset is ready.",
        "purpose": (
            "Download the imaging teaching dataset and verify that it is structurally intact "
            "and ready for analysis."
        ),
        "why_it_matters": (
            "You cannot evaluate a model on data you have not inspected. Receiving and confirming "
            "data is a data integrity step — not just a download. Silent data corruption is one of "
            "the most common sources of irreproducible results in medical AI."
        ),
        "student_learns": (
            "What the teaching pack contains; how status files track pipeline progress; "
            "why input validation matters before modeling."
        ),
        "stages": ["stage_01_fetch_sample"],
        "prompts": ["stage_01_fetch_sample.md"],
        "reports": [],
    },
    {
        "label": "Mission 2 — Build the First Detector",
        "goal": "Visualize the data, train the baseline, and record the first metric.",
        "purpose": (
            "Load the dataset, produce the first visual artifact, and run the smallest deterministic "
            "baseline model to establish a reproducible starting point."
        ),
        "why_it_matters": (
            "Every later comparison depends on this baseline being correct and reproducible. "
            "A poorly understood baseline makes all subsequent improvements uninterpretable. "
            "The goal is not a high Dice score — it is a score you can explain."
        ),
        "student_learns": (
            "What Dice score means in practice; what 'baseline' means in research (a reference, not a target); "
            "how to interpret a loss curve; how visualization can reveal data quality issues before training."
        ),
        "stages": ["stage_02_load_visualize", "stage_03_train_baseline"],
        "prompts": ["stage_02_load_visualize.md", "stage_03_train_baseline.md"],
        "reports": ["data_notes.md", "train_notes.md"],
    },
    {
        "label": "Mission 3 — Investigate Failure",
        "goal": "Identify best and worst predictions and form a failure hypothesis.",
        "purpose": (
            "Analyse where and why the baseline fails — slice by slice, error type by error type — "
            "and produce a written hypothesis about the dominant failure mode."
        ),
        "why_it_matters": (
            "Blind improvement without error understanding is engineering guesswork, not science. "
            "The hypothesis you write here determines whether Mission 4 is a valid controlled experiment "
            "or an arbitrary change."
        ),
        "student_learns": (
            "How to read TP/FP/FN error maps; the difference between best-case and worst-case Dice; "
            "how to form a testable hypothesis from observational data; why a failure pattern matters "
            "more than the average metric."
        ),
        "stages": ["stage_04_error_analysis"],
        "prompts": ["stage_04_error_analysis.md"],
        "reports": ["error_analysis.md"],
    },
    {
        "label": "Mission 4 — Improve With Intent",
        "goal": "Make one controlled improvement, compare results, and pack the Day 1 summary.",
        "purpose": (
            "Test one specific, well-motivated change to the baseline and measure the result "
            "with the same metric. Then assemble all Day 1 findings into a summary deliverable."
        ),
        "why_it_matters": (
            "One controlled change with honest reporting is more scientifically valuable than multiple "
            "unjustified tweaks. You learn whether your Mission 3 hypothesis was correct — and that "
            "finding, positive or negative, is the scientific contribution of Day 1."
        ),
        "student_learns": (
            "What a controlled experiment means in a machine learning context; how to compare two "
            "pipelines fairly; that negative results are valid scientific results; how to assemble "
            "a research summary that honestly represents its findings."
        ),
        "stages": ["stage_05_model_swap", "stage_06_pack_report"],
        "prompts": ["stage_05_model_swap.md", "stage_06_pack_report.md"],
        "reports": ["model_swap.md", "day1_summary.md"],
    },
    {
        "label": "Mission 5 — Design the Next Study",
        "goal": "Write a Day 2 challenge plan, then implement and measure it.",
        "purpose": (
            "Before writing any code, produce a concrete written plan for the Day 2 challenge. "
            "Then implement the planned adaptation and measure the outcome against Day 1."
        ),
        "why_it_matters": (
            "Research planning is a distinct skill from execution. A written plan forces clarity "
            "about what you believe and why before you commit to any implementation. "
            "It also makes it possible to report honestly when the outcome differs from the prediction."
        ),
        "student_learns": (
            "How to translate error observations into a testable strategy; how Otsu's method differs "
            "from fixed thresholding; how to design a fair before/after comparison; "
            "how to report an outcome that differs from the plan."
        ),
        "stages": ["stage_07_challenge_plan", "stage_08_adapt_pipeline"],
        "prompts": ["stage_07_challenge_plan.md", "stage_08_adapt_pipeline.md"],
        "reports": ["challenge_plan.md", "adapt_pipeline.md"],
    },
    {
        "label": "Mission 6 — Translate Responsibly",
        "goal": "Reflect on clinical implications and write the translation memo.",
        "purpose": (
            "Locate the prototype honestly on the path from a toy pipeline to a research contribution "
            "to a clinical tool. Produce a written memo that a non-technical clinical collaborator "
            "could read and act on."
        ),
        "why_it_matters": (
            "Overstating prototype capabilities in clinical AI can cause direct patient harm. "
            "This is the most important writing exercise of the lab. The memo is grounded in actual "
            "results — including disappointing ones — not in best-case interpretation."
        ),
        "student_learns": (
            "The gap between in-sample performance and clinical validity; what regulatory pathways "
            "(MDR, FDA 510(k)) require before a tool can be used clinically; what 'key limitation' "
            "means to a clinical collaborator versus to a benchmark paper."
        ),
        "stages": ["stage_09_translation_memo"],
        "prompts": ["stage_09_translation_memo.md"],
        "reports": ["translation_memo.md"],
    },
]


def mission_status(mission: dict) -> str:
    stages = mission["stages"]
    n_ok = sum(1 for s in stages if stage_ok(s))
    if n_ok == 0:
        return "not started"
    if n_ok == len(stages):
        return "complete"
    return "in progress"


STATUS_ICON = {
    "complete":    "🟢",
    "in progress": "🟡",
    "not started": "⚪",
}

STATUS_LABEL = {
    "complete":    "Complete",
    "in progress": "In progress",
    "not started": "Not started",
}

# ── Required artifacts for Evaluation tab ────────────────────────────────────

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
    ("env_check.md",       "Mission 0"),
    ("data_notes.md",      "Mission 2"),
    ("train_notes.md",     "Mission 2"),
    ("error_analysis.md",  "Mission 3"),
    ("model_swap.md",      "Mission 4"),
    ("day1_summary.md",    "Mission 4"),
    ("challenge_plan.md",  "Mission 5"),
    ("adapt_pipeline.md",  "Mission 5"),
    ("translation_memo.md","Mission 6"),
]

# ── Header ────────────────────────────────────────────────────────────────────

st.title("Medical AI + Agentic Coding Lab")
st.caption(
    "**Mission dashboard** — navigation, artifact inspection, and submission readiness.  "
    "Claude interaction happens in **VS Code + Claude Code**, not here."
)
st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────

tab_map, tab_results, tab_reports, tab_eval, tab_prompts = st.tabs([
    "🗺️  Mission Map",
    "📊  Results",
    "📄  Reports",
    "✅  Evaluation",
    "💬  Prompt Studio",
])

# ── Tab 1: Mission Map ────────────────────────────────────────────────────────

with tab_map:
    st.subheader("Mission Map")
    st.write(
        "Your research journey through the lab. Complete missions in order. "
        "Each mission produces artifacts you can inspect in the other tabs."
    )
    st.write("")

    completed_count = 0
    for mission in MISSIONS:
        status = mission_status(mission)
        if status == "complete":
            completed_count += 1
        icon = STATUS_ICON[status]
        status_label = STATUS_LABEL[status]

        # Mission card header row
        col_icon, col_header, col_badge = st.columns([0.04, 0.72, 0.20])
        with col_icon:
            st.write(icon)
        with col_header:
            st.markdown(f"**{mission['label']}**")
            st.caption(mission["goal"])
        with col_badge:
            st.write(status_label)

        # Mission framing and stage detail in expander
        with st.expander("Mission context + stage detail", expanded=False):
            st.markdown(f"**Scientific purpose:** {mission['purpose']}")
            st.markdown(f"**Why it matters:** {mission['why_it_matters']}")
            st.markdown(f"**What you are learning:** {mission['student_learns']}")
            st.write("")
            st.markdown("**Stage completion:**")
            for stage in mission["stages"]:
                ok = stage_ok(stage)
                tick = "✓" if ok else "○"
                st.write(f"{tick}  `{stage}.json`")

        st.write("")

    st.divider()
    st.metric("Missions complete", f"{completed_count} / {len(MISSIONS)}")

# ── Tab 2: Results ────────────────────────────────────────────────────────────

with tab_results:
    st.subheader("Results")

    # Metrics summary
    st.markdown("#### Key metrics")

    val_metrics      = load_json(BASE / "outputs" / "metrics" / "val_metrics.json")
    swap_metrics     = load_json(BASE / "outputs" / "metrics" / "model_swap_comparison.json")
    challenge_metrics = load_json(BASE / "outputs" / "metrics" / "challenge_comparison.json")

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        if val_metrics and "dice" in val_metrics:
            st.metric("Baseline Dice (Mission 2)", f"{val_metrics['dice']:.3f}")
        else:
            st.metric("Baseline Dice (Mission 2)", "—")
    with m_col2:
        if swap_metrics and "new_dice" in swap_metrics:
            delta = swap_metrics.get("delta")
            delta_str = f"{delta:+.3f}" if isinstance(delta, (int, float)) else None
            st.metric("After model swap (Mission 4)", f"{swap_metrics['new_dice']:.3f}", delta=delta_str)
        else:
            st.metric("After model swap (Mission 4)", "—")
    with m_col3:
        if challenge_metrics and "new_dice" in challenge_metrics:
            delta = challenge_metrics.get("delta")
            delta_str = f"{delta:+.3f}" if isinstance(delta, (int, float)) else None
            st.metric("Day 2 adaptation (Mission 5)", f"{challenge_metrics['new_dice']:.3f}", delta=delta_str)
        else:
            st.metric("Day 2 adaptation (Mission 5)", "—")

    st.divider()

    # Figures
    st.markdown("#### Figures")

    fig_paths = sorted((BASE / "outputs" / "figures").glob("*.png"))
    if not fig_paths:
        st.info("No figures yet. Run Mission 2 to produce the first visualization.")
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
        status_files = sorted((BASE / "outputs" / "status").glob("*.json"))
        if not status_files:
            st.info("No stage status files found yet.")
        else:
            for p in status_files:
                data = load_json(p)
                if data:
                    st.markdown(f"**{p.name}**")
                    st.json(data)

# ── Tab 3: Reports ────────────────────────────────────────────────────────────

with tab_reports:
    st.subheader("Reports")
    st.write("Written summaries produced by you and Claude during each mission.")
    st.write("")

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
    for display_name, filename in report_files:
        content = report_text(filename)
        if content and content.strip():
            any_report = True
            with st.expander(display_name, expanded=False):
                st.markdown(content)

    if not any_report:
        st.info(
            "No reports yet. Reports appear here as you complete missions. "
            "Each report is written by you and Claude together during the mission."
        )

# ── Tab 4: Evaluation ─────────────────────────────────────────────────────────

with tab_eval:
    st.subheader("Evaluation — Submission Readiness")
    st.write(
        "This checklist mirrors the autograding tests CI runs on every push. "
        "Run `make test` locally to see the same results. "
        "All items must be present before your final push."
    )
    st.write("")

    def artifact_row(label: str, present: bool, mission: str) -> None:
        icon = "✅" if present else "❌"
        col_icon, col_label, col_mission = st.columns([0.05, 0.65, 0.20])
        with col_icon:
            st.write(icon)
        with col_label:
            st.write(label)
        with col_mission:
            st.caption(mission)

    st.markdown("**Stage status files**")
    for filename, mission in REQUIRED_STATUS:
        stage_name = filename.replace(".json", "")
        artifact_row(f"`outputs/status/{filename}`", stage_ok(stage_name), mission)

    st.write("")
    st.markdown("**Figures**")
    for filename, mission in REQUIRED_FIGURES:
        artifact_row(f"`outputs/figures/{filename}`", fig_exists(filename), mission)

    st.write("")
    st.markdown("**Metric files**")
    for filename, mission in REQUIRED_METRICS:
        artifact_row(f"`outputs/metrics/{filename}`", metric_exists(filename), mission)

    st.write("")
    st.markdown("**Reports**")
    for filename, mission in REQUIRED_REPORTS:
        content = report_text(filename)
        present = bool(content and len(content.strip()) > 50)
        artifact_row(f"`reports/{filename}`", present, mission)

    st.divider()

    all_checks = (
        [stage_ok(f.replace(".json", "")) for f, _ in REQUIRED_STATUS]
        + [fig_exists(f) for f, _ in REQUIRED_FIGURES]
        + [metric_exists(f) for f, _ in REQUIRED_METRICS]
        + [bool(report_text(f) and len((report_text(f) or "").strip()) > 50) for f, _ in REQUIRED_REPORTS]
    )
    n_pass  = sum(all_checks)
    n_total = len(all_checks)

    if n_pass == n_total:
        st.success(f"All {n_total} artifacts present — ready to push.")
    else:
        st.warning(
            f"{n_pass} / {n_total} artifacts present. "
            "Complete remaining missions before your final push."
        )

# ── Tab 5: Prompt Studio ─────────────────────────────────────────────────────

with tab_prompts:
    st.subheader("Prompt Studio")
    st.info(
        "These prompts are **read-only** here. "
        "To run a prompt, copy the relevant layer into your **VS Code + Claude Code** session. "
        "The dashboard is for orientation — Claude interaction happens in VS Code + Claude Code."
    )
    st.write("")

    # Build selector: one entry per prompt file, grouped by mission label
    prompt_options: list[tuple[str, str]] = []
    for mission in MISSIONS:
        for pfile in mission["prompts"]:
            display = f"{mission['label']}  ·  {pfile}"
            prompt_options.append((display, pfile))

    option_labels = [label for label, _ in prompt_options]
    option_files  = [pfile for _, pfile in prompt_options]

    selected_idx = st.selectbox(
        "Select a mission prompt",
        range(len(option_labels)),
        format_func=lambda i: option_labels[i],
    )

    selected_file = option_files[selected_idx]
    content = prompt_text(selected_file)

    st.write("")

    if not content:
        st.warning(f"`prompts/{selected_file}` not found. Check that the prompts directory is intact.")
    else:
        layers = parse_prompt_layers(content)

        if layers:
            # Structured display: Layer A / B / C
            st.markdown(f"**File:** `prompts/{selected_file}`")
            st.divider()

            if "A" in layers:
                st.markdown("#### Layer A — Base prompt")
                st.caption("Run this prompt in VS Code + Claude Code to start the mission.")
                st.markdown(layers["A"])

            if "B" in layers:
                st.write("")
                st.markdown("#### Layer B — Reflection prompt")
                st.caption("Run after completing Layer A and reviewing the artifacts.")
                st.markdown(layers["B"])

            if "C" in layers:
                st.write("")
                st.markdown("#### Layer C — What you can customize")
                st.caption("Optional extension — experiment with your own prompt variation.")
                st.markdown(layers["C"])

            # Full file available in expander
            with st.expander("Full prompt file", expanded=False):
                st.markdown(content)

        else:
            # Prompt doesn't have Layer A/B/C sections — show full content
            st.markdown(f"**File:** `prompts/{selected_file}`")
            st.divider()
            st.markdown(content)
